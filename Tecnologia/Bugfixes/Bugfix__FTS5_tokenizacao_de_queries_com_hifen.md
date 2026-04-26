---
title: Bugfix: FTS5 tokenização de queries com hífen
date: 2026-04-22 17:25:04
updated: 2026-04-22 17:25:04
tags:
  - bugfix
  - fts5
  - sqlite
  - vault
  - search
source: 
related:
  - Tarefas/Skills/Skill__Systematic_Config_Debugging
  - Projetos/Docling/SKILL
  - Tecnologia/Integracao_Embeddings_NVIDIA_sqlite_vec
  - Conhecimento/Manuais/Docling
---

## Problema

A busca vault-first falhava para queries como 'nv-embedcode-7b-v1 NVIDIA model embedding' porque:

1. A função  envolvia a query inteira em aspas quando detectava 
2. FTS5 interpreta  como operador NOT (exclusão), não como caractere literal
3. A frase exata não existia no banco → 0 resultados

## Solução

Modificar  para:
- Tokenizar a query em palavras individuais
- Escapar cada token com aspas apenas se contiver caracteres especiais
- Juntar com OR em vez de AND implícito

### Exemplo

Antes:  → 0 resultados
Depois:  → 10 resultados

## Arquivo modificado

-  (função )

## Validação

{
  "has_results": true,
  "count": 10,
  "results": "[content] [[Tecnologia/Integracao_Embeddings_NVIDIA_sqlite_vec|Integracao_Embeddings_NVIDIA_sqlite_vec]]\n  /mnt/e/Obsidian/Cofre/Hermes/Tecnologia/Integracao_Embeddings_NVIDIA_sqlite_vec.md\n  ## Resumo  Integracao bem-sucedida do sistema de embeddings NVIDIA nv-embedcode-7b-v1 ao fluxo de salvamento de notas do Obsidian via sqlite-vec.  ## Alteracoes Aplicadas  ### 1. Configuracao NVIDIA (linhas 16-17, 30+) - Carregamento de dotenv de  - Configuracao: ,  - Funcao  com  e   ### 2. Estrutu\n\n[content] Hermes — Projeto de Evolução: Recall Semântico e Classificação Inteligente\n  /mnt/e/Obsidian/Cofre/Hermes/Tecnologia/Hermes_—_Projeto_de_Evolução__Recall_Semântico_e_Classificação_Inteligente.md\n  # Hermes — Projeto de Evolução: Recall Semântico e Classificação Inteligente  ## Contexto  Este documento descreve as próximas 4 features que elevarão o Hermes de 8.5 para 10/10. Gerado pelo copiloto Claude (Anthropic) em 21/04/2026 após implementação completa do Pipeline Hierárquico de Recall e do \n\n[content] Checkpoint Final — Índice 100% Sincronizado\n  /mnt/e/Obsidian/Cofre/Hermes/System/Checkpoints/Checkpoint_Final_—_Índice_100%_Sincronizado.md\n  ## Resumo da Limpeza Final  **Data:** 22/04/2026   **Operação:** Remoção de entradas órfãs do índice SQLite  ### Resultados - **Entradas removidas:** 7 arquivos órfãos - **Entradas válidas restantes:** 153 - **Status:** Índice 100% sincronizado com filesystem físico  ### Arquivos Removidos 1. [[Inbo\n\n[content] [[Projetos/[[Conhecimento/Manuais/Docling|Docling]]/SKILL|Skill]]: Systematic Config Debugging\n  /mnt/e/Obsidian/Cofre/Hermes/Tarefas/Skills/[[Tarefas/Skills/Skill__Systematic_Config_Debugging|Skill__Systematic_Config_Debugging]].md\n  Criada skill systematic-config-debugging para debugging sistemático de configurações.  Padrão documentado: 1. Verificação byte-level com xxd/cat -A (backtick = 0x60) 2. Cross-referencing de múltiplas fontes (SOUL.md, prompt_builder.py, skills) 3. Identificação de inconsistências entre instruções 4. \n\n[content] Bugfix: vault_check.py ignorava a query\n  /mnt/e/Obsidian/Cofre/Hermes/Tecnologia/Bugfixes/Bugfix__vault_check.py_ignorava_a_query.md\n  ## Problema O script vault_check.py (linha 74) chamava  em vez de , fazendo com que a query fosse ignorada e o threshold (numero 2) fosse usado como termo de busca.  ## Impacto O sistema vault-first do web_search_tool sempre retornava has_results: False para queries que nao coincidiam com o numero 2\n\n[content] Documentação — Sistema de Memória Persistente Hermes\n  /mnt/e/Obsidian/Cofre/Hermes/Projetos/Documentação_—_Sistema_de_Memória_Persistente_Hermes.md\n  # Sistema de Memória Persistente Hermes  **Status:** Concluído ✅   **Data de conclusão:** 22/04/2026   **Versão:** 1.0  ---  ## 1. Visão Geral  ### 1.1 O Que Foi Construído  Sistema híbrido de memória persistente que combina: - **Obsidian** como interface de visualização e navegação - **SQLite** com\n\n[content] Sessoes_2026-04-16\n  /mnt/e/Obsidian/Cofre/Hermes/Conversas/2026/Sessoes_2026-04-16.md\n  --- title: Sessoes_2026-04-16 date: 2026-04-20 00:32:08 updated: 2026-04-20 00:32:08 tags:   - hermes   - sessoes   - historico source:  related: [] ---  # Resumo de Sessoes - 2026-04-16\\n\\nTotal de sessoes: 124\\n\\n## Sessao 1 - 2026-04-16 11:25\\n- Comandos: 1\\n- Preview: +Oi Hermes! Christian aqui.\n\n[content] Servidores MCP #8\n  /mnt/e/Obsidian/Cofre/Hermes/Conversas/2026/Sessao_2026-04-19_Servidores_MCP_8.md\n  --- title: Servidores MCP #8 date: 2026-04-19 16:29 updated: 2026-04-21 14:49:30 session_id: 20260419_162957_e4ceb8 tags:   - sessao   - cli   - pesquise   - diga   - podemos   - fazer   - forma source: hermes_state_db related: [] ---  # Servidores MCP #8  ## Metadados  - **Sessão ID:** `20260419_16\n\n[content] SYSTEM_The_user_has_invoked_the_tts-edge-ffmpeg_skill\n  /mnt/e/Obsidian/Cofre/Hermes/Conversas/2026/Sessao_2026-04-19_SYSTEM_The_user_has_invoked_the_tts-edge-ffmpeg_skill.md\n  --- title: SYSTEM_The_user_has_invoked_the_tts-edge-ffmpeg_skill date: 2026-04-19 12:46 updated: 2026-04-21 14:49:30 session_id: 20260419_124631_fa9666 tags:   - sessao   - cli   - system   - user   - invoked   - edge   - ffmpeg source: hermes_state_db related: [] ---  # SYSTEM_The_user_has_invoked_\n\n[content] SKILL\n  /mnt/e/Obsidian/Cofre/Hermes/Projetos/Docling/SKILL.md\n  --- name: docling description: Convert and extract structured data from documents (PDF, DOCX, PPTX, XLSX, HTML, images, audio, and more) using Docling. Supports OCR, table extraction, formula detection, reading order, and export to Markdown, JSON, or HTML for AI/RAG pipelines. version: 1.0.0 author:"
}

## Referências

Esta nota menciona:
- [[Tarefas/Skills/Skill__Systematic_Config_Debugging]]
- [[Projetos/Docling/SKILL]]
- [[Tecnologia/Integracao_Embeddings_NVIDIA_sqlite_vec]]
- [[Conhecimento/Manuais/Docling]]
