---
title: Skill: Systematic Config Debugging
date: 2026-04-22 17:03:00
updated: 2026-04-22 17:03:00
tags:
  - hermes
  - autosave
  - skill
  - debugging
source: 
related: []
---

Criada skill systematic-config-debugging para debugging sistemático de configurações.

Padrão documentado:
1. Verificação byte-level com xxd/cat -A (backtick = 0x60)
2. Cross-referencing de múltiplas fontes (SOUL.md, prompt_builder.py, skills)
3. Identificação de inconsistências entre instruções
4. Documentação antes de corrigir

Exemplo aplicado: identificação de instrução incorreta em OPENAI_MODEL_EXECUTION_GUIDANCE sobre vault 'automático' vs instrução correta em SESSION_SEARCH_GUIDANCE.

Skill path: ~/.hermes/skills/devops/systematic-config-debugging/