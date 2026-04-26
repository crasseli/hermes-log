---
title: Skill_Obsidian_Memoria_Persistente_Documentacao
date: 2026-04-25 11:38:37
updated: 2026-04-25 11:38:37
tags:
  - sessao
  - autosave
  - hermes
  - cron
source: hermes_cron
related: []
---

## Visao Geral

Sessao cron do Hermes focada na documentacao e utilizacao da skill Obsidian - sistema de memoria persistente baseado em Obsidian.

### Contexto da Execucao

- **Session ID:** cron_fa8ceb2aa589_20260425_113025
- **Inicio:** 2026-04-25 11:10:25
- **Origem:** cron job
- **Tipo:** Auto-documentacao

### Conteudo Abordado

Esta sessao carregou a skill obsidian completa, que inclui:

1. **Scripts Disponiveis:**
   - save_note.py - Criar notas com auto-links
   - show_backlinks.py - Ver mencoes
   - search_notes.py - Busca full-text
   - search_semantic.py - Busca por embeddings NVIDIA
   - append_note.py - Atualizar notas
   - list_notes.py - Listar notas
   - daily_note.py - Nota diaria
   - open_in_obsidian.py - Abrir no app
   - link_notes.py - Criar links
   - populate_vault_from_sessions.py - Migrar sessoes

2. **Convencoes do Vault:**
   - Sem acentos nos nomes de arquivos
   - Sem espacos (underscore como separador)
   - Frontmatter YAML padrao
   - Tags em caixa baixa
   - Estrutura hierarquica organizada

3. **Regra de Autosave:**
   - Salvar automaticamente apos 5+ tool calls
   - Atualizar daily_note.py
   - Pasta automatica baseada em contexto
   - Sem confirmacao do usuario

4. **Localizacao:**
   - Vault: /mnt/e/Obsidian/Cofre/Hermes/
   - Scripts: ~/.hermes/skills/obsidian/scripts/

### Acao Executada

Auto-persistencia realizada via save_note.py em execucao cron.