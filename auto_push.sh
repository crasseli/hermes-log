#!/bin/bash
# Auto-push para hermes-log
# Le token do .env do Hermes
REPO_DIR="/home/christian/.hermes/repos/hermes-log"
TOKEN=$(grep '^GITHUB_TOKEN=' /home/christian/.hermes/.env 2>/dev/null | head -1 | cut -d'=' -f2 | tr -d '"' | tr -d "'")

cd "$REPO_DIR" || exit 1

# Configurar remote com token se necessario
if ! git remote get-url origin | grep -q '@github.com'; then
  git remote set-url origin "https://crasseli:${TOKEN}@github.com/crasseli/hermes-log.git"
fi

# Add, commit, push
git add -A
if git diff --cached --quiet; then
  echo "Nada a commitar"
  exit 0
fi

TIMESTAMP=$(date '+%Y-%m-%d %H:%M')
git commit -m "Atualizacao automatica - $TIMESTAMP" --allow-empty-message
git push origin main 2>&1

# Limpar token do remote URL apos push
git remote set-url origin https://github.com/crasseli/hermes-log.git

echo "Push realizado com sucesso - $TIMESTAMP"
