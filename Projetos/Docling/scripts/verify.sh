#!/bin/bash
# verify.sh - Verifica se o Docling esta corretamente instalado
# Uso: bash scripts/verify.sh

echo "=== Verificacao da Instalacao Docling ==="
echo

# Verificar ambiente virtual
VENV_PATH="$HOME/.hermes/skills/docling/.venv"
if [[ ! -d "$VENV_PATH" ]]; then
    echo "❌ Ambiente virtual nao encontrado em $VENV_PATH"
    echo "   Execute: bash scripts/setup.sh"
    exit 1
fi
echo "✓ Ambiente virtual encontrado"

# Ativar ambiente
source "$VENV_PATH/bin/activate"

# Verificar Python
PYTHON=$(which python3)
echo "✓ Python: $PYTHON"
echo "  Versao: $(python3 --version)"

# Verificar Docling CLI
if command -v docling &> /dev/null; then
    echo "✓ Docling CLI instalado: $(docling --version)"
else
    echo "❌ Docling CLI nao encontrado"
    exit 1
fi

# Verificar modulos Python
echo
echo "Verificando modulos Python..."
python3 -c "from docling.document_converter import DocumentConverter; print('✓ DocumentConverter OK')" 2>/dev/null || echo "❌ DocumentConverter nao disponivel"
python3 -c "from docling.chunking import HybridChunker; print('✓ HybridChunker OK')" 2>/dev/null || echo "❌ HybridChunker nao disponivel"

# Verificar scripts
echo
echo "Verificando scripts..."
for script in convert_document.py batch_convert.py extract_tables.py chunk_for_rag.py; do
    if [[ -f "scripts/$script" ]]; then
        echo "✓ scripts/$script"
    else
        echo "❌ scripts/$script nao encontrado"
    fi
done

echo
echo "=== Verificacao concluida ==="
