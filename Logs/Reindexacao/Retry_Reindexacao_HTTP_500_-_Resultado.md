---
title: Retry Reindexacao HTTP 500 - Resultado
date: 2026-04-22 19:53:20
updated: 2026-04-22 19:53:20
tags:
  - hermes
  - autosave
  - reindexacao
  - http500
  - nvidia-api
source: 
related:
  - Conhecimento/Manuais/Docling
  - Pesquisas/Test_Paper
  - Projetos/hermes_plano_memoria_obsidian
  - Inbox/Processados/Hermes_Evolucao_Fases
  - Pesquisas/Example_Paper
  - Pesquisas/Christian_Rasseli_Wantil_Souza
---

## Resumo do Retry de Reindexacao

**Data:** 22/04/2026
**Tarefa:** Retry de reindexacao de 11 notas que falharam com HTTP 500

### Resultado Final

| Metrica | Valor |
|---------|-------|
| Total de notas | 11 |
| Sucessos | 11 (100%) |
| Falhas | 0 |

### Problema Identificado

A API NVIDIA NIM (nv-embedcode-7b-v1) tem limite de ~3500-3600 caracteres por requisicao, nao 8000 como inicialmente configurado.

### Solucao Aplicada

1. Reduzido MAX_CHARS de 8000 para 3500 (margem de seguranca)
2. Corrigido nome da tabela: vault_embeddings -> vec_obsidian
3. Corrigido nome da coluna: path -> file_path

### Notas Processadas

**Sucesso (11):**
- [[Conhecimento/Manuais/Docling|Docling]].md
- [[Inbox/Processados/Hermes_Evolucao_Fases|Hermes_Evolucao_Fases]].md
- [[Pesquisas/Christian_Rasseli_Wantil_Souza|Christian_Rasseli_Wantil_Souza]].md
- [[Pesquisas/Test_Paper|Test_Paper]].md
- [[Pesquisas/Example_Paper|Example_Paper]].md
- [[Projetos/hermes_plano_memoria_obsidian|hermes_plano_memoria_obsidian]].md
- Documentacao_Sistema_de_Memoria_Persistente_Hermes.md
- Bugfix_FTS5_tokenizacao_de_queries_com_hifen.md
- Hermes_Projeto_de_Evolucao_Recall_Semantico (3 versoes)

**Falhas (0):** Nenhuma

### Proximos Passos

Atualizar script reindex_vault.py com limite de 3500 caracteres para evitar futuros HTTP 500.

## Referências

Esta nota menciona:
- [[Conhecimento/Manuais/Docling]]
- [[Pesquisas/Test_Paper]]
- [[Projetos/hermes_plano_memoria_obsidian]]
- [[Inbox/Processados/Hermes_Evolucao_Fases]]
- [[Pesquisas/Example_Paper]]
- [[Pesquisas/Christian_Rasseli_Wantil_Souza]]
