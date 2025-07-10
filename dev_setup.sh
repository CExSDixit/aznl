#!/usr/bin/env bash
# Dev environment and build setup script for aznl
set -e

# 1. Create virtual environment if not present
if [ ! -d "venv" ]; then
  echo "Creating Python virtual environment..."
  python3 -m venv venv
fi

# 2. Activate virtual environment (cross-platform)
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
  ACTIVATE_CMD="venv\\Scripts\\activate"
  echo "To activate the virtual environment on Windows, run:"
  echo "  venv\\Scripts\\activate"
else
  ACTIVATE_CMD="source venv/bin/activate"
  echo "Activating the virtual environment (macOS/Linux)..."
  source venv/bin/activate
fi

echo "Virtual environment ready."

# 3. Install dependencies
if [ -f requirements.txt ]; then
  echo "Installing dependencies..."
  pip install -r requirements.txt
else
  echo "requirements.txt not found!"
  exit 1
fi

# 4. Copy .env.example to .env if needed
if [ ! -f .env ]; then
  if [ -f .env.example ]; then
    echo "Copying .env.example to .env..."
    cp .env.example .env
    echo "\n[INFO] Please edit .env and add your API keys."
  else
    echo ".env.example not found! Please create your .env manually."
  fi
else
  echo ".env already exists."
fi

# 5. (Optional) Install CLI in editable mode
read -p "Install CLI globally for development (pip install --editable .)? [y/N]: " yn
case $yn in
    [Yy]*)
        pip install --editable .
        ;;
    *)
        echo "Skipping global CLI install."
        ;;
esac

echo "\n[SETUP COMPLETE]"
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
  echo "To activate your virtual environment on Windows:"
  echo "  venv\\Scripts\\activate"
else
  echo "To activate your virtual environment on macOS/Linux:"
  echo "  source venv/bin/activate"
fi
echo "Then you can run:"
echo "  aznl 'List AKS clusters'" 