---
title: ÍNDICE - Pipeline de Recall e Organização do Vault
date: 2026-04-25 11:22:17
updated: 2026-04-25 11:22:17
tags:
  - hermes
  - indice
  - recall-pipeline
  - organizacao
source: 
related: []
---

# ÍNDICE - Pipeline de Recall e Organização do Vault

**Data:** 2026-04-26
**Sessão:** Organização e mapeamento de entregas do Hermes

---

## Pipeline de Recall - Estrutura Implementada

### 1. Hierarquia de Recall (Prioridade)
1. **vault_check.py** → Busca rápida (threshold 2) no vault
2. **search_vault.py** → Busca combinada (título + conteúdo)
3. **session_search** → Busca em histórico de sessões
4. **web_search** → Internet como ÚLTIMO RECURSO

### 2. Scripts do Pipeline
| Script | Localização | Função |
|--------|-------------|--------|
| vault_check.py | ~/.hermes/skills/obsidian/scripts/ | Validação rápida antes de web_search |
| search_vault.py | ~/.hermes/skills/obsidian/scripts/ | Busca combinada (título + conteúdo) |
| save_note.py | ~/.hermes/skills/obsidian/scripts/ | Salvar notas automaticamente |
| populate_vault_from_sessions.py | ~/.hermes/skills/obsidian/scripts/ | Migrar sessões históricas |
| daily_notes.py | ~/.hermes/skills/obsidian/scripts/ | Notas diárias |

### 3. Arquivos de Configuração
| Arquivo | Localização | Função |
|---------|-------------|--------|
| SOUL.md | ~/.hermes/SOUL.md | Instruções injetadas em cada sessão |
| datura_checkpointer.py | ~/.hermes/shell/ | Wrapper de checkpoint para segurança |

---

## Pendências Atuais (por prioridade)

### Prioridade 1 - Teste Real do Pipeline
- **Status:** PENDENTE
- **Objetivo:** Validar que o SOUL.md força search_vault antes de session_search/web_search em sessão nova
- **Critério de Sucesso:** Hermes executa search_vault.py primeiro quando o usuário pergunta sobre histórico
- **Referência:** OS/Concluidas/Pipeline_Recall_*.md

### Prioridade 2 - Auto-patch Script
- **Status:** PENDENTE
- **Objetivo:** Criar mecanismo que re-aplica customizações após git pull
- **Problema:** Modificações no código são perdidas em updates
- **Solução Proposta:** Script que aplica patches automaticamente

### Backlog - Outras Pendências
- **Populate Vault Histórico:** Migrar sessões de antes de 16/04
- **Search Semântico:** Validar embeddings end-to-end
- **Auto-save Obsidian:** 93% das sessões sem registro (corrigido 2026-04-20)

---

## Links Rápidos no Vault

- Pipeline Hierárquico de Recall - Implementação
- Pipeline de Recall - Internet como último recurso
- Pipeline Recall - SOUL.md Atualizado 2026-04-25
- OS - Confirmar que session_search wrapper está ativo

---

**Próxima Ação:** Aguardar aprovação para criar OS de "Teste Real do Pipeline"