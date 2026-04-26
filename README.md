---
title: Hermes Vault - Índice Central
date: 2026-04-20
updated: 2026-04-20
tags:
  - index
  - vault
  - hermes
---

# Hermes Vault - Cérebro Externo

Sistema de memória persistente do agente Hermes.

## Estrutura de Pastas

```
Hermes/
├── Conhecimento/          # Aprendizados, skills, documentação técnica
│   ├── Skills/             # Documentação de skills do Hermes
│   └── Seguranca/          # Conteúdo de segurança da informação
├── Conversas/              # Registros de sessões e conversas
│   └── 2026/               # Ano atual
│       ├── Diario_*.md     # Diários diários
│       ├── Sessoes_*.md    # Resumos de sessões
│       └── Sessao_*        # Retrospectivas e análises
├── Inbox/                  # Entrada temporária
│   └── Processados/        # Arquivos processados
├── NotebookLM/             # Documentação da integração NotebookLM
│   └── Documentacao/
├── Pesquisas/              # Papers, artigos, resultados de pesquisa
│   └── Arxiv/
├── Pessoas/                # Contatos, perfis, informações de pessoas
├── Projetos/               # Projetos em andamento
├── Tarefas/                # Listas de tarefas e TODOs
└── Tecnologia/             # Conteúdo técnico e referências
    └── Seguranca/          # Segurança de APIs, autenticação
```

## Convenções de Nomenclatura

- **Sem acentos** em nomes de arquivos (Sessao, nao Sessão)
- **Data no formato**: AAAA-MM-DD
- **Separador**: underscore (_)
- **Extensoes**: .md para notas, .base para views

## Tags Principais

- `hermes` - Relacionado ao agente
- `skill` - Documentação de skill
- `diario` - Entrada diária
- `sessoes` - Resumo de sessões
- `retrospectiva` - Análise retrospectiva
- `obsidian` - Sistema Obsidian
- `notebooklm` - Integração NotebookLM

## Scripts de Manutenção

Localizados em: `~/.hermes/skills/obsidian/scripts/`

1. **save_note.py** - Criar notas com frontmatter
2. **search_notes.py** - Busca full-text
3. **append_note.py** - Adicionar conteúdo
4. **list_notes.py** - Listar por pasta/tag
5. **daily_note.py** - Gerenciar diário
6. **link_notes.py** - Criar links entre notas
7. **reindex_vault.py** - Sincronizar vault com SQLite (Holographic)

## Sistema de Memória

- **Provider**: Holographic (SQLite local)
- **Banco**: `~/.hermes/memory_store.db`
- **Regra**: Obsidian SEMPRE vence em conflitos
- **Reindex**: Executar após reorganizações de pastas
