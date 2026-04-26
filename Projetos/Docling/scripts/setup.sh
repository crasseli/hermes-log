#!/bin/bash
# setup.sh - Instalacao automatica do Docling para Hermes Agent
# Uso: bash scripts/setup.sh

set -e

echo "=== Docling Setup para Hermes Agent ==="
echo

# Verificar Python
PYTHON_VERSION=$(python3 --version 2>/dev/null | grep -oP '\d+\.\d+' || echo "")
if [[ -z "$PYTHON_VERSION" ]]; then
    echo "ERRO: Python 3 nao encontrado. Instale Python 3.9+ primeiro."
    exit 1
fi

MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

if [[ "$MAJOR" -lt 3 ]] || [[ "$MAJOR" -eq 3 && "$MINOR" -lt 9 ]]; then
    echo "ERRO: Python $PYTHON_VERSION encontrado, mas Docling requer Python 3.9+"
    exit 1
fi

echo "Python $PYTHON_VERSION OK"

# Verificar/instalar dependencias do sistema (Ubuntu/Debian)
if command -v apt-get &> /dev/null; then
    echo "Verificando dependencias do sistema..."
    sudo apt-get update -qq
    sudo apt-get install -y -qq tesseract-ocr libtesseract-dev poppler-utils 2>/dev/null || true
fi

# Criar ambiente virtual se nao existir
VENV_PATH="$HOME/.hermes/skills/docling/.venv"
if [[ ! -d "$VENV_PATH" ]]; then
    echo "Criando ambiente virtual em $VENV_PATH..."
    python3 -m venv "$VENV_PATH"
fi

# Ativar ambiente virtual
source "$VENV_PATH/bin/activate"

# Instalar Docling
echo "Instalando Docling..."
pip install -q --upgrade pip
pip install -q docling

# Verificar instalacao
if command -v docling &> /dev/null; then
    echo
    echo "=== Instalacao concluida com sucesso! ==="
    echo "Versao: $(docling --version)"
    echo
    echo "Para usar:"
    echo "  docling arquivo.pdf                    # Converter para Markdown"
    echo "  docling arquivo.pdf --to json          # Converter para JSON"
    echo "  python scripts/convert_document.py --help"
    echo
else
    echo "ERRO: Falha na instalacao do Docling."
    exit 1
fi
