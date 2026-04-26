---
title: Pendências - Pipeline Recall e Desenvolvimento
date: 2026-04-25 11:24:02
updated: 2026-04-25 11:24:02
tags:
  - hermes
  - pendencias
  - pipeline-recall
  - os
source: 
related: []
---

# Pendências - Pipeline Recall e Desenvolvimento

**Atualizado:** 2026-04-26
**Status:** Aguardando aprovação para próxima OS

---

## Classificação por Prioridade

### PRIORIDADE 1: Teste Real do Pipeline
**Status:** PENDENTE | **Urgência:** ALTA
- **Problema:** Ainda não validamos se o SOUL.md é obedecido em sessão real do usuário
- **Objetivo:** Abrir sessão nova e verificar se search_vault.py é executado primeiro
- **Critério de Sucesso:** Quando usuário pergunta "o que foi feito sobre X?", Hermes executa search_vault antes de session_search
- **Bloqueante:** Sim - sem este teste não sabemos se o pipeline funciona de verdade
- **Tempo Estimado:** 5 minutos (teste rápido)

### PRIORIDADE 2: Auto-patch Script
**Status:** PENDENTE | **Urgência:** MÉDIA
- **Problema:** git pull apaga modificações no hermes-agent/
- **Objetivo:** Criar script que re-aplica patches automaticamente após update
- **Solução Proposta:** Hook post-merge ou script de re-aplicação
- **Valor:** Resolve problema estrutural de manutenção de customizações
- **Tempo Estimado:** 30-45 minutos

---

## Backlog - Outras Pendências

| Item | Status | Prioridade | Descrição |
|------|--------|------------|-----------|
| Populate Vault Histórico | PENDENTE | BAIXA | Migrar sessões anteriores a 16/04 |
| Search Semântico | PENDENTE | BAIXA | Validar embeddings end-to-end |
| Skills Audit | PENDENTE | BAIXA | Revisar todas as skills criadas |

---

## Documentos Relacionados

- ÍNDICE - Pipeline de Recall e Organização do Vault
- Pipeline Recall - SOUL.md Atualizado 2026-04-25
- Pipeline Hierárquico de Recall - Implementação

---

**Próxima Ação Recomendada:** Aprovar OS "Teste Real do Pipeline"