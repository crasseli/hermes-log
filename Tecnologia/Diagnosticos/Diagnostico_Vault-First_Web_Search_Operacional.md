---
title: Diagnóstico: Vault-First Web Search Operacional
date: 2026-04-22 18:11:20
updated: 2026-04-22 18:11:20
tags:
  - diagnostico
  - vault-first
  - web-search
  - operacional
source: 
related: []
---

## Status: OPERACIONAL

Testes realizados confirmam que o sistema vault-first está funcionando corretamente.

### Testes Executados

**1. _run_vault_check isolado**
- Query: nv-embedcode-7b-v1
- Resultado: has_results=true, count=4
- Script encontrado: ~/.hermes/skills/obsidian/scripts/vault_check.py

**2. web_search_tool completo**
- Retornou: source=obsidian_vault
- web_search_skipped: true
- Web NÃO foi consultada

### Código Verificado

Local: ~/.hermes/hermes-agent/tools/web_tools.py
- Linha 1037: def _run_vault_check
- Linha 1107-1115: vault-first check dentro de web_search_tool
- Linha 2117: handler correto no registry.register

### Bytecode

Arquivo .pyc deletado antes dos testes para garantir código atualizado.

### Conclusão

O sistema vault-first está operacional. Eventuais comportamentos anteriores foram causados por:
- Cache de bytecode desatualizado
- Queries sem matches suficientes (threshold=2)
- Notas ainda não indexadas (requer reindex_vault.py)