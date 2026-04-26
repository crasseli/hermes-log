#!/bin/bash
# docling-wrapper.sh - Wrapper para executar Docling no ambiente virtual
# Uso: source scripts/docling-wrapper.sh && docling arquivo.pdf

VENV_PATH="$HOME/.hermes/skills/docling/.venv"

if [[ ! -d "$VENV_PATH" ]]; then
    echo "ERRO: Ambiente virtual nao encontrado. Execute: bash scripts/setup.sh"
    return 1
fi

source "$VENV_PATH/bin/activate"

# Se executado diretamente, passa argumentos para docling
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    docling "$@"
fi
