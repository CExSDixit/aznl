import argparse

# Stub for LLM integration
def query_llm(nl_query):
    # TODO: Replace with actual OpenAI API call
    # For now, return a dummy command, explanation, and doc link
    return {
        'command': 'az group create --name MyResourceGroup --location eastus',
        'explanation': 'Creates a new resource group named MyResourceGroup in the East US region.',
        'doc_link': 'https://learn.microsoft.com/en-us/cli/azure/group#az-group-create'
    }

def main():
    parser = argparse.ArgumentParser(description='Query az cli commands using natural language.')
    parser.add_argument('query', type=str, nargs='+', help='Your natural language query')
    args = parser.parse_args()
    nl_query = ' '.join(args.query)
    result = query_llm(nl_query)
    print(f"\nCommand: {result['command']}")
    print(f"Explanation: {result['explanation']}")
    print(f"Docs: {result['doc_link']}")

if __name__ == '__main__':
    main() 