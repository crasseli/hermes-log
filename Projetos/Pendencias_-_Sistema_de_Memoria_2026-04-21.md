---
title: Pendencias - Sistema de Memoria 2026-04-21
date: 2026-04-21 13:54:19
updated: 2026-04-21 13:54:19
tags:
  - pendencias
  - memoria
  - sqlite
  - obsidian
  - wrapper
source: 
related: []
---

## Pendências do Sistema de Memória

### ORDEM DE EXECUÇÃO (fazer nesta sequência)

#### 1. Corrigir regex no wrapper session_search_tool.py
- Arquivo: ~/.hermes/hermes-agent/tools/session_search_tool.py
- Linha ~362
- ERRADO: re.sub(r'[\s\S]*?', '', last_user_msg)
- CORRETO: re.sub(r'```[\s\S]*?```', '', last_user_msg)
- Validar com py_compile após corrigir

#### 2. Verificar db.get_messages() no wrapper
- Confirmar que o método existe no objeto db passado para session_search
- Se não existir, adaptar para o método correto
- Testar chamada real com session_id válido

#### 3. Script populate_vault_from_sessions.py
- Ler as 145 sessões do state.db
- Filtrar sessões com mais de 10 mensagens (sessões relevantes)
- Gerar nota no vault para cada sessão importante
- Vincular session_id nas notas geradas

#### 4. Validar recall com conteúdo real
- Após populate, testar: "Hermes o que foi feito hoje?"
- Confirmar que search_vault retorna antes do session_search
- Verificar ranking BM25 está priorizando conteúdo relevante

### REGRA
Executar nesta ordem. Não pular etapas. Confirmar cada etapa antes de avançar.