# Natural Language Azure CLI Query Tool

This utility lets you use natural language to query Azure CLI (`az cli`) commands by referencing the official Azure documentation. It uses LLMs (OpenRouter or local Ollama) to interpret your queries and return the most relevant command, explanation, and documentation link.


---

## Features
- Query Azure CLI with natural language
- Uses OpenRouter (cloud) or Ollama (local) as LLM providers
- Returns command, explanation, and doc link
- Configurable provider/model preferences and API keys
- **Quiet mode**: Output only the az cli command for piping (`-q` or `--just-command`)

---

## Quick Dev Environment & Build Setup (Scripted)

For a one-step setup, use the provided script to prepare your development environment and build everything needed:

```bash
bash dev_setup.sh
```

This will:
- Create a Python virtual environment (if not present)
- Install all dependencies
- Copy `.env.example` to `.env` if needed
- Remind you to add your API keys to `.env`
- (Optional) Build/install the CLI for development

---

## Manual Setup

### 1. Clone the Repository
```bash
git clone git@github.com:CExSDixit/aznl.git
cd aznl
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

---

## Build/Install CLI for Development

To install the CLI globally (for development):
```bash
pip install --editable .
```
Or, for a one-time install:
```bash
pip install .
```

---

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

## Global CLI Usage (Recommended: pip install with setup.py)

You can install this tool globally as a CLI command using pip and the provided `setup.py`:

1. **Install in Editable Mode (for development):**
   ```bash
   pip install --editable .
   ```
   Or, for a one-time install:
   ```bash
   pip install .
   ```

2. **Run from Anywhere:**
   ```bash
   aznl "List AKS clusters"
   ```

**Note:** You must still activate your virtual environment or ensure all dependencies are installed globally for the script to work.

---

## Usage

### Basic Query
```bash
aznl "How do I list all resource groups in Azure?"
```

### Specify Provider or Model
```bash
aznl "List AKS clusters" --provider openrouter --model openai/gpt-4o
```

### Quiet Mode (Output Only the Command)
Use `-q` or `--just-command` to output only the az cli command (no explanation or docs), suitable for piping:
```bash
aznl "List AKS clusters" -q
# or
aznl "List AKS clusters" --just-command
```

#### Example (Piping to Shell)
```bash
aznl "List AKS clusters" -q | bash
```

### Example Output (Default)
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
