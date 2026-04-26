---
title: Pipeline Recall - SOUL.md Atualizado 2026-04-25
date: 2026-04-25 10:51:25
updated: 2026-04-25 10:51:25
tags:
  - pipeline
  - recall
  - soul
  - protocolo
source: 
related: []
---

## Resumo

Pipeline de Recall atualizado com sucesso em 25/04/2026.

### Alterações no SOUL.md

1. **Nova seção RECALL: PROTOCOLO OBRIGATORIO**
   - Sequência obrigatória: search_vault → session_search → web_search
   - PROIBIDO usar session_search ou web_search como primeira ação
   - Exceção: clima, notícias de hoje, informações em tempo real

2. **Nova seção FERRAMENTA: vault_check antes de web_search**
   - Executar vault_check.py --threshold 2 antes de web_search
   - Se has_results=true: usar vault, não chamar web_search
   - Se has_results=false: prosseguir com web_search
   - Regra INVIOLÁVEL

3. **Removido**: Seção "REGRA: Recall Unificado" (obsoleta após git revert do código do web_search)

### Arquivos Modificados
- `/home/christian/.hermes/SOUL.md` (versão commitada no git)

### Scripts Verificados
- `vault_check.py` já suporta --threshold (não necessitou modificação)
- `search_vault.py` operacional via CLI

### Status
✅ Protocolo de recall documentado e ativo
✅ Sem dependência de código Python wrapper
✅ Resistente a git revert

---
*Nota criada automaticamente pelo Hermes*