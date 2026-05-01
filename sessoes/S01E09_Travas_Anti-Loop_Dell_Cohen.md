# S01E09 — Travas Anti-Loop: DELL + Cohen (M70q)

**Data:** 2026-05-01
**Autoria:** Christian Rasseli, Hermes (agente no notebook DELL)
**Modelo:** z-ai/glm-5.1 via NVIDIA NIM

---

## Contexto

O Hermes (ambas as instancias) entrava em loops de investigacao durante tarefas de diagnostico, consumindo turns sem progredir. O padrao tipico era: grep sem resultado, outro grep, mais um grep, sem acao corretiva. Nenhuma trava formal impedia o agente de ciclar indefinidamente, gastando tokens e tempo.

## Problema Identificado

1. **max_turns alto demais** (120 no DELL, 90 no Cohen) permitia loops longos
2. **delegation.max_iterations: 50** muito permissivo para subagentes
3. **terminal.timeout** de 180/120 segundos permitia tool calls penduradas
4. **Ausencia de Direct Action Mode** — o agente investigava em vez de agir
5. **tool_output limits** permissivos (50KB / 2000 linhas) alimentavam contextos enormes

## Acoes Realizadas

### Travas de Iteracao

| Parametro | DELL (antes) | DELL (depois) | Cohen (antes) | Cohen (depois) |
|-----------|------|-------|------|-------|
| agent.max_turns | 120 | **60** | 90 | **60** |
| delegation.max_iterations | 50 | **15** | 50 | **15** |
| terminal.timeout | 180 | **90** | 120 | **90** |
| delegation.child_timeout_seconds | 600 | **300** | 600 | **300** |
| tool_output.max_bytes | 50000 | **30000** | 50000 | **30000** |
| tool_output.max_lines | 2000 | **1000** | 2000 | **1000** |

No DELL: aplicado via `hermes config set` (5 comandos diretos).

No Cohen: aplicado via sed para max_turns/child_timeout/max_iterations, e Python inline via yaml.dump para terminal.timeout.

### Direct Action Mode (System Prompt)

Adicionado ao `agent.system_prompt` de ambas as instancias:

> DIRECT ACTION MODE: After 3 failed diagnostic attempts (grep/read/search with no result), STOP investigating and ACT with best available information. Never loop more than 2 consecutive diagnostic commands without making progress. If a fix is clear, apply it immediately. Maximum 2 diagnostic commands before acting on any issue.

### Incidente: YAML Corrompido no Cohen

O `sed -i` que injetou o system_prompt com `DIRECT ACTION MODE: After...` sem aspas causou ScannerError na linha 14 do config.yaml do Cohen. O parser YAML interpretou o `:` como separador de mapping key.

**Correcao:** Script Python que reescreveu a secao com bloco `>` (folded scalar) do YAML, removeu a linha residual `information.` do prompt antigo, e validou com `yaml.safe_load()`.

### Incidente: sed Atingiu Timeouts Errados no Cohen

O `sed -i 's/: 120/: 90/'` converteu TODOS os `timeout: 120` do config, incluindo auxiliary timeouts. Corrigido manualmente identificando que os auxiliary (compression: 360, vision: 180, web_extract: 360) ficaram intactos — o sed so pegou valores 120.

## Licoes Aprendidas

1. **NUNCA usar sed para injetar texto com `:` em YAML sem aspas.** Usar bloco folded scalar (`>`) ou aspas simples para strings longas com dois-pontos.
2. **sed com padrao generico atinge multiplos alvos.** Usar contexto de linha (endereco + padrao) ou `python3 -c "import yaml"` para edicao cirurgica.
3. **yaml.dump() reordena chaves e remove comentarios.** Preferir sed com contexto ou ruamel.yaml para preservar estrutura.
4. **Sempre validar YAML com `yaml.safe_load()` apos qualquer edicao.** Um YAML quebrado causa "No inference provider configured" no startup.
5. **Config changes exigem restart.** No DELL: `/reset` ou novo session. No Cohen: restart manual do gateway.

## Estado Final

- **DELL:** Todas as travas ativas. Funcional a partir do proximo `/reset`.
- **Cohen:** Todas as travas preparadas nos arquivos. YAML validado e pronto. **Nao houve restart** — Christian fara manualmente quando o trabalho atual terminar.

## Pendencias

- Confirmar que o Cohen sobe limpo apos restart manual
- Monitorar se max_turns=60 e suficiente para tarefas longas (pode precisar ajuste para 75)
- Avaliar se Direct Action Mode esta sendo respeitado pelo modelo em proximas sessoes
