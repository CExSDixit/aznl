# Natural Language Azure CLI Query Tool

This utility lets you use natural language to query Azure CLI (`az cli`) commands by referencing the official Azure documentation. It uses LLMs (OpenRouter or local Ollama) to interpret your queries and return the most relevant command, explanation, and documentation link.

---

## Features
- Query Azure CLI with natural language
- Uses OpenRouter (cloud) or Ollama (local) as LLM providers
- Returns command, explanation, and doc link
- Configurable provider/model preferences and API keys

---

## Setup

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd azure-docs-cursor
```

### 2. Create and Activate a Virtual Environment
**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```
**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure API Keys
- Copy `.env.example` to `.env`:
  ```bash
  cp .env.example .env
  ```
- Add your OpenRouter API key to `.env`:
  ```env
  OPENROUTER_API_KEY=sk-...
  OLLAMA_API_KEY=   # (leave blank for local Ollama)
  ```

### 5. Configure Provider and Model (Optional)
Edit `config.json` to set your preferred provider order and model names:
```json
{
  "provider_order": ["openrouter", "ollama"],
  "openrouter_model": "openai/gpt-4o",
  "ollama_model": "llama2"
}
```
You can also add `openrouter_extra_headers` for custom headers (see OpenRouter docs).

---

## Usage

### Basic Query
```bash
python main.py "How do I list all resource groups in Azure?"
```

### Specify Provider or Model
```bash
python main.py "List AKS clusters" --provider openrouter --model openai/gpt-4o
```

### Example Output
```
Command: az aks list
Explanation: Lists all AKS (Azure Kubernetes Service) clusters in the current subscription.
Docs: https://docs.microsoft.com/en-us/cli/azure/aks?view=azure-cli-latest#az-aks-list
```

---

## Notes
- If OpenRouter fails, the tool will automatically try Ollama (if running locally).
- Make sure the Ollama model you specify is available locally (`ollama list`).
- For OpenRouter, ensure your API key is valid and you have access to the selected model.

---

## Deactivate the Virtual Environment
```bash
deactivate
```

---

## License
MIT 