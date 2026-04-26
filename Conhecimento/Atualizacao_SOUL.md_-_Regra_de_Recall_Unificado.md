---
title: Atualizacao SOUL.md - Regra de Recall Unificado
date: 2026-04-20 22:54:18
updated: 2026-04-20 22:54:18
tags:
  - soul
  - recall
  - memoria
  - regra
source: 
related: []
---

## Alteracao

Adicionada nova secao ao SOUL.md:

### REGRA: Recall Unificado

Quando precisar lembrar de projetos, implementacoes, decisoes tecnicas ou contexto de conversas anteriores, SEMPRE seguir esta ordem:

1. python3 ~/.hermes/skills/obsidian/scripts/search_vault.py "termo" --combined
2. session_search como fallback se search_vault nao retornar resultados relevantes

O search_vault busca tanto em notas do vault quanto em sessoes vinculadas, com ranking BM25 por relevancia. Preferir sempre resultados do vault sobre sessoes brutas, pois o vault contem informacao ja consolidada.

### Motivacao

Padronizar o processo de recall de memoria do Hermes, priorizando:
- Vault (informacao consolidada) sobre sessoes brutas
- Busca combinada (metadata + conteudo full-text)
- Ranking por relevancia BM25

Data: 2026-04-20
Sessao: 20260420_223828_68927c