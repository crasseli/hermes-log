---
title: O_autosave_nao_esta_funcionando_Verifique_duas_coisas
date: 2026-04-20 00:23
updated: 2026-04-21 14:49:27
session_id: 20260420_002320_51b0d2
tags:
  - sessao
  - cli
  - autosave
  - funcionando
  - verifique
  - duas
  - coisas
source: hermes_state_db
related: []
---

# O_autosave_nao_esta_funcionando_Verifique_duas_coisas

## Metadados

- **Sessão ID:** `20260420_002320_51b0d2`
- **Data:** 2026-04-20 00:23
- **Fonte:** cli
- **Modelo:** moonshotai/kimi-k2.5
- **Mensagens:** 29
- **Tool Calls:** 15

## Resumo

### Perguntas do Usuário

1. O autosave não está funcionando. Verifique duas coisas:
1. Mostre o conteúdo atual da memória relacionada ao autosave Obsidian
2. Verifique se existe um arquivo de perfil ou system prompt do Hermes onde essa regra deve ser adicionada permanentemente — algo como ~/.hermes/profiles/ ou ~/.hermes/confi...
2. You just executed tool calls but returned an empty response. Please process the tool results above and continue with the task.
3. Prossiga Hermes

### Respostas Principais

1.  Vou verificar a memória atual e procurar pelos arquivos de perfil/configuração do
2.  Encontrei o problema. A regra de autosave está apenas na **memória dinâmica** (99% cheia) e **não existe** nos arquivos permanentes. 

**Arquivos relevantes encontrados:**
- `~/.hermes/SOUL.md` - Sys...
3. (empty)

## Keywords

autosave, funcionando, verifique, duas, coisas, mostre, atual, relacionada, obsidian, existe

---

*Nota gerada automaticamente do state.db em 2026-04-21 14:49:27*