---
title: Hermes Update v0.10.0 → v0.11.0
date: 2026-04-24 12:53:23
updated: 2026-04-24 12:53:23
tags:
  - hermes
  - update
  - backup
  - v0.11.0
source: 
related: []
---

# Atualização Hermes Agent

**Data:** 24/04/2026
**Versão anterior:** v0.10.0
**Nova versão:** v0.11.0 (v2026.4.23)

## Resumo
Atualização bem-sucedida preservando customizações locais.

## Processo Executado
1. Detectou 13 linhas customizadas em `run_agent.py`
2. Criado backup em: `/home/christian/.hermes/backups/hermes-agent-20260424-pre-update`
3. Stash das modificações: `pre-update-customizations-20260424`
4. Checkout da tag: `v2026.4.23`
5. Patch reaplicado com sucesso
6. Sintaxe validada via `py_compile`

## Customizações Preservadas
- Bloco de injeção semântica no `run_agent.py`
- Scripts Python em `~/.hermes/skills/*/scripts/`

## Validação
```
✓ Python syntax: OK
✓ hermes doctor: Passou (config v18 → v22 disponível)
✓ Patch aplicado: Sem conflitos
```

## Próximos Passos
- Config pode ser atualizada para v22 quando conveniente
- Stash mantido para referência: `git stash list`

## Backup
/home/christian/.hermes/backups/hermes-agent-20260424-pre-update/run_agent_custom.patch
