---
title: Integracao SQLite-Obsidian Completa
date: 2026-04-20 22:46:55
updated: 2026-04-20 22:46:55
tags:
  - integracao
  - sqlite
  - obsidian
  - fts5
source: 
related:
  - Projetos/hermes_plano_memoria_obsidian
---

## Resumo

Implementacao de 3 etapas para integrar sistema de sessoes SQLite (state.db) com vault Obsidian (memory_store.db):

### ETAPA 1: Session ID no save_note.py
- Adicionada funcao get_current_session_id()
- Modificada funcao save_note() para aceitar session_id
- Registro automatico no obsidian_index

### ETAPA 2: Tabela FTS5 obsidian_content
- Criada tabela virtual FTS5 com tokenize='unicode61'
- Suporte a busca full-text em portugues com acentos
- DELETE+INSERT para evitar duplicatas

### ETAPA 3: search_vault.py
- Busca em metadata (obsidian_index)
- Busca full-text (obsidian_content) com ranking BM25
- Busca combinada
- Verificacao de notas nao indexadas

### Comandos
Encontrados 28 arquivos .md

Reindex concluído: 0 atualizados, 0 removidos, 28 sem alteração

=== BUSCA FULL-TEXT: 'termo' ===

  [[Projetos/hermes_plano_memoria_obsidian|hermes_plano_memoria_obsidian]] (Projetos)
  Arquivo: hermes_plano_memoria_obsidian.md
  Score: -1.6000

=== BUSCA COMBINADA: 'termo' ===

[CONTENT] hermes_plano_memoria_obsidian
  Pasta: Projetos
  Arquivo: hermes_plano_memoria_obsidian.md

✓ Todas as notas estao indexadas em obsidian_content.

### Status
- obsidian_index: 28 registros
- obsidian_content: 28 registros
- Sincronizacao: 100%

Data: 2026-04-20

## Referências

Esta nota menciona:
- [[Projetos/hermes_plano_memoria_obsidian]]
