---
title: Ponto_Injecao_Contexto_run_agent_py
date: 2026-04-22 15:10:21
updated: 2026-04-22 15:10:21
tags:
  - hermes
  - arquitetura
  - injection-points
  - run_agent
source: 
related: []
---

## Ponto de Injecao de Contexto no run_agent.py

### Descoberta Principal

O run_agent.py tem arquitetura de dois niveis para contexto:

1. **_cached_system_prompt** - Construido uma vez por sessao, cacheado (linha ~3993)
2. **Injecao na mensagem do usuario** - Efemera, nao persiste (linhas ~9618-9632)

### Onde NAO Injetar

❌ **_build_system_prompt()** - Quebra prefix cache da Anthropic, sem acesso a query atual.

### Onde SIM Injetar

✅ **Bloco de injecoes (linhas ~9618-9632):**



### Query do Usuario

- **original_user_message** (linha ~9318): Versao limpa, usar para busca
- **user_message**: Pode conter injecoes de skills, nao usar para busca

### Pre-busca de Contexto

**Local:** Linhas ~9540-9548 (antes do loop)



### Estrategia de Integracao

**Opcao A (Recomendada):** Estender  do MemoryManager para incluir busca semantica do vault.

**Opcao B:** Adicionar variavel  paralela a .

### Validacao

Antes de modificar run_agent.py:


### Skill Criada


