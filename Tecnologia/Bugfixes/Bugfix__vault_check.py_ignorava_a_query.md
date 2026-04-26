---
title: Bugfix: vault_check.py ignorava a query
date: 2026-04-22 16:29:22
updated: 2026-04-22 16:29:22
tags:
  - bugfix
  - vault
  - obsidian
  - hermes
source: 
related: []
---

## Problema
O script vault_check.py (linha 74) chamava  em vez de , fazendo com que a query fosse ignorada e o threshold (numero 2) fosse usado como termo de busca.

## Impacto
O sistema vault-first do web_search_tool sempre retornava has_results: False para queries que nao coincidiam com o numero 2, forçando fallback desnecessario para web.

## Correcao
Linha 74 alterada de:

Para:


## Validacao
- Query 'nv-embedcode-7b-v1' → has_results: true, count: 2
- Query 'receita de bolo' → has_results: false, count: 0 (comportamento esperado)

## Arquivo modificado
~/.hermes/skills/obsidian/scripts/vault_check.py