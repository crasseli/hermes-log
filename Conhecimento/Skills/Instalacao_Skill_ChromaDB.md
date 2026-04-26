---
title: Instalacao_Skill_ChromaDB
date: 2026-04-25 00:54:00
updated: 2026-04-25 00:54:00
tags:
  - chroma
  - mlops
  - skill
  - instalacao
  - embeddings
  - vetor
source: hermes
related: []
---

## Instalacao da Skill ChromaDB

**Data:** 25/04/2026
**Status:** Instalado com sucesso

### O que e ChromaDB

Chroma e um banco de dados open-source de embeddings (vetoriais) para aplicacoes de IA, especialmente:
- RAG (Retrieval-Augmented Generation)
- Busca semantica
- Sistemas de recomendacao

### Comando de Instalacao

```bash
# Primeira tentativa - cancelada por falta de --yes
hermes skills install official/mlops/chroma
# Resultado: Cancelado (exigiu confirmacao interativa)

# Segunda tentativa - sucesso com flag --yes
hermes skills install official/mlops/chroma --yes
```

### Alertas de Seguranca

Veredicto do scan: **CAUTION** (Cuidado)
- 2 alertas MEDIUM na categoria supply_chain:
  - Linha 46: `pip install chromadb`
  - Linha 49: `npm install chromadb @chroma-core/default-embed`

**Decisao:** ALLOWED - permitido porque fonte e builtin (oficial)

### Localizacao dos Arquivos

- Pasta da skill: `~/.hermes/skills/mlops/chroma/`
- Arquivos instalados:
  - `SKILL.md` (documentacao principal)
  - `references/integration.md` (guia de integracao)

### Funcoes Principais da API

1. **create_collection** - Criar colecao de embeddings
2. **add** - Adicionar documentos com embeddings
3. **query** - Buscar por similaridade semantica
4. **get** - Recuperar documentos por ID

### Recursos Adicionais

- Suporte a embedding automatico (sem precisar gerar manualmente)
- Colecoes multimodais (texto, imagem)
- Persistencia em SQLite

## Referencias
- [[Conhecimento/Skills/Indice_de_Skills]]
