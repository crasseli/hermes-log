---
title: Skill: Hermes Safe Update Workflow
date: 2026-04-24 02:37:22
updated: 2026-04-24 02:37:22
tags:
  - hermes
  - skill
  - update
  - backup
  - git
  - devops
  - workflow
source: 
related:
  - Projetos/Docling/SKILL
---

# [[Projetos/Docling/SKILL|Skill]]: Hermes Safe Update Workflow

## Contexto
Durante o update do Hermes Agent v0.10.0 para v0.11.0, precisei preservar uma customização local (injeção semântica em run_agent.py). A tentativa inicial de aplicar o patch manualmente falhou com IndentationError na linha 8995.

## Solução Desenvolvida
Criada skill `hermes-safe-update` com workflow testado:

1. **Detectar**: `git status --short` + `git diff run_agent.py`
2. **Backup**: `git diff > patch` + `git stash`
3. **Update**: `git checkout v2026.4.23` (por tag)
4. **Reaplicar**: `git apply patch`
5. **Validar**: `python3 -m py_compile run_agent.py`

## Lições Chave
- Sempre usar `git stash` + `git apply` (evita erros de indentação)
- Checkout por tag garante versão específica estável
- Validar sintaxe antes de testar funcionalmente

## Localização
- Skill: `~/.hermes/skills/devops/hermes-safe-update/`
- Categoria: devops
- Tags: hermes, update, backup, git, patch

## Uso Futuro
Carregar skill antes de qualquer update do Hermes Agent:
```
skill_view("hermes-safe-update")
```


## Referências

Esta nota menciona:
- [[Projetos/Docling/SKILL]]
