---
title: Instalacao_Skill_Chroma_MLOps
date: 2026-04-25 00:20:53
updated: 2026-04-25 00:20:53
tags:
  - hermes
  - mlops
  - chroma
  - vector-db
  - skill
  - instalacao
source: hermes_skill_install
related:
  - Projetos/Docling/SKILL
---

# Instalacao da [[Projetos/Docling/SKILL|Skill]] Chroma (MLOps)

Data: 25/04/2026
Skill: official/mlops/chroma
Status: Instalada com sucesso

## Resumo

Instalacao da skill oficial do Hermes para integracao com ChromaDB - banco de dados open-source de embeddings para aplicacoes de IA.

## O que e Chroma

Banco de dados de embeddings (vetores) open-source para:
- Aplicacoes RAG (Retrieval-Augmented Generation)
- Busca semantica sobre documentos
- Armazenamento de embeddings com metadados
- Escalabilidade desde notebooks ate clusters de producao

## Estatisticas do Projeto

- **GitHub Stars:** 24.300+
- **Forks:** 1.900+
- **Versao:** 1.3.3 (stable)
- **Licenca:** Apache 2.0

## Local da Instalacao

```
~/.hermes/skills/mlops/chroma/
├── SKILL.md              # Documentacao principal
└── references/
    └── integration.md    # Guia de integracao
```

## API Principal (4 Funcoes)

| Funcao | Descricao |
|--------|-----------|
| `create_collection()` | Cria colecao de documentos |
| `add()` | Adiciona documentos com metadados |
| `query()` | Busca por similaridade semantica |
| `get()` | Recupera documentos por ID ou filtro |

## Modos de Persistencia

- **Client()** - Memoria volatil (dados perdidos ao reiniciar)
- **PersistentClient(path)** - Persistencia em disco

## Casos de Uso Recomendados

- Construcao de aplicacoes RAG
- Banco de dados vetorial local/self-hosted
- Prototipagem em notebooks
- Busca semantica sobre corpus de documentos
- Armazenamento de embeddings com metadados filtraveis

## Alternativas Consideradas

| Ferramenta | Quando Usar |
|------------|-------------|
| **Pinecone** | Nuvem gerenciada, auto-scaling |
| **FAISS** | Apenas busca de similaridade pura (sem metadados) |
| **Weaviate** | Banco ML-native para producao |
| **Qdrant** | Alto desempenho, base Rust |

## Dependencias

- `chromadb`
- `sentence-transformers`

## Proximos Passos

- [ ] Testar criacao de colecao de exemplo
- [ ] Integrar com pipeline de embeddings existente
- [ ] Avaliar performance vs alternativas (Pinecone, FAISS)

## Referencias

- GitHub: https://github.com/chroma-core/chroma
- Documentacao: https://docs.trychroma.com
- Discord: https://discord.gg/MMeYNTmh3x

## Referências

Esta nota menciona:
- [[Projetos/Docling/SKILL]]
