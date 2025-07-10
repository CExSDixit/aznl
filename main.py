import argparse
import json
import os
from dotenv import load_dotenv
import requests
from openai import OpenAI

# Load environment variables from .env
load_dotenv()

CONFIG_FILE = 'config.json'

# Load config
with open(CONFIG_FILE, 'r') as f:
    config = json.load(f)

def get_api_key(provider):
    if provider == 'openrouter':
        key = os.getenv('OPENROUTER_API_KEY')
        if not key:
            key = input('Enter your OpenRouter API key: ')
        return key
    elif provider == 'ollama':
        # Ollama local, no API key needed
        return None
    return None

def call_openrouter(nl_query, model, api_key, extra_headers=None):
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
    system_prompt = (
        "You are an assistant that helps users translate natural language queries into Azure CLI (az cli) commands. "
        "For each query, respond ONLY with a JSON object containing: 'command', 'explanation', and 'doc_link' (a link to the relevant Azure documentation). "
        "Do not include any other text."
    )
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": nl_query}
    ]
    kwargs = {
        "model": model,
        "messages": messages
    }
    if extra_headers:
        kwargs["extra_headers"] = extra_headers
    completion = client.chat.completions.create(**kwargs)
    content = completion.choices[0].message.content.strip()
    # Remove code block markers and leading 'json' if present
    if content.startswith('```json'):
        content = content[len('```json'):].strip()
    if content.startswith('```'):
        content = content[len('```'):].strip()
    if content.lower().startswith('json'):
        content = content[4:].strip()
    if content.endswith('```'):
        content = content[:-3].strip()
    try:
        result = json.loads(content)
        return result
    except Exception as e:
        raise RuntimeError(f"Failed to parse OpenRouter response: {e}\nRaw content: {content}")

def call_ollama(nl_query, model):
    url = "http://localhost:11434/api/generate"
    system_prompt = (
        "You are an assistant that helps users translate natural language queries into Azure CLI (az cli) commands. "
        "For each query, respond ONLY with a JSON object containing: 'command', 'explanation', and 'doc_link' (a link to the relevant Azure documentation). "
        "Do not include any other text."
    )
    data = {
        "model": model,
        "prompt": f"{system_prompt}\nUser: {nl_query}",
        "stream": False
    }
    response = requests.post(url, json=data)
    response.raise_for_status()
    try:
        # Ollama returns {'response': '...'}
        content = response.json()["response"]
        if content.strip().startswith("```"):
            content = content.strip().strip("` ")
        result = json.loads(content)
        return result
    except Exception as e:
        raise RuntimeError(f"Failed to parse Ollama response: {e}\nRaw content: {response.text}")

def query_llm(nl_query, provider_order, openrouter_model, ollama_model, provider_override=None, model_override=None):
    tried = []
    if provider_override:
        provider_order = [provider_override]
    # Load extra_headers from config if present
    extra_headers = None
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
            extra_headers = config.get('openrouter_extra_headers')
    for idx, provider in enumerate(provider_order):
        tried.append(provider)
        if provider == 'openrouter':
            model = model_override if model_override else openrouter_model
            print(f"Invoking OpenRouter with model: {model}")
            api_key = get_api_key('openrouter')
            try:
                result = call_openrouter(nl_query, model, api_key, extra_headers=extra_headers)
                if result:
                    return result
            except Exception as e:
                print(f"OpenRouter failed: {e}")
                # If next provider is ollama, print fallback message
                if idx + 1 < len(provider_order) and provider_order[idx + 1] == 'ollama':
                    next_model = model_override if model_override else ollama_model
                    print(f"Falling back to Ollama (local LLM) with model: {next_model} ...")
        elif provider == 'ollama':
            model = model_override if model_override else ollama_model
            print(f"Invoking Ollama (local LLM) with model: {model}")
            try:
                result = call_ollama(nl_query, model)
                if result:
                    return result
            except Exception as e:
                print(f"Ollama failed: {e}")
    print(f"All providers failed: {tried}")
    return None

def main():
    parser = argparse.ArgumentParser(description='Query az cli commands using natural language.')
    parser.add_argument('query', type=str, nargs='+', help='Your natural language query')
    parser.add_argument('--provider', type=str, choices=['openrouter', 'ollama'], help='Provider to use (overrides config)')
    parser.add_argument('--model', type=str, help='Model to use (overrides config)')
    args = parser.parse_args()
    nl_query = ' '.join(args.query)
    provider_order = config.get('provider_order', ['openrouter', 'ollama'])
    openrouter_model = config.get('openrouter_model', 'gpt-3.5-turbo')
    ollama_model = config.get('ollama_model', 'llama2')
    result = query_llm(
        nl_query,
        provider_order,
        openrouter_model,
        ollama_model,
        provider_override=args.provider,
        model_override=args.model
    )
    if result:
        print(f"\nCommand: {result['command']}")
        print(f"Explanation: {result['explanation']}")
        print(f"Docs: {result['doc_link']}")
    else:
        print("No result found.")

if __name__ == '__main__':
    main() 