# S01E05 — Amnésia Pós-Restart: Diagnóstico e Correção dos Limites de Memória

> **Data:** 30/04/2026 | **Autores:** Christian Rasseli, Cohen (agente remoto), Hermes (agente local)
> **Palavras-chave:** memória persistente, config.yaml, memory_char_limit, amnésia, restart

---

## Resumo

Após um restart do gateway, o agente perdeu completamente o contexto da tarefa ativa e retornou falando de assuntos não relacionados — um comportamento que chamamos de "amnésia pós-restart". A investigação revelou que a causa raiz era a saturação dos limites de caracteres da memória persistente (`memory_char_limit: 2.200` e `user_char_limit: 1.375`, defaults do projeto). Com 99% de ocupação, não havia espaço para registrar o contexto da tarefa corrente, que era substituído a cada nova entrada. A correção — aumentar os limites para 10.000 / 5.000 — está alinhada com a proposta do GitHub Issue #5320 e reduz a ocupação de 99% para 31%.

---

## O Problema

### O que aconteceu

Durante uma sessão ativa no Telegram, o agente Cohen foi submetido a um restart do gateway (comando `/new`). Ao retornar, ele não apenas perdeu o fio da meada — começou a falar de um assunto completamente diferente (Ollama) como se fosse uma nova sessão, ignorando toda a tarefa em andamento.

### Sintoma

```
Usuário: "Continua aquela tarefa de configuração?"
Agente:   "Olá! Posso ajudar com instalação do Ollama hoje?"
          ↑ Comportamento de amnésia total
```

A memória persistente (injetada automaticamente a cada turno) deveria ter fornecido contexto suficiente para o agente retomar. Mas não forneceu.

---

## Causa Raiz

### Limites hardcoded por padrão

O projeto Hermes Agent define defaults conservadores para os limites de memória ([documentação oficial](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/memory.md)):

| Arquivo | Função | Default (chars) | Aprox. tokens |
|---------|--------|----------------|---------------|
| `MEMORY.md` | Notas do agente | **2.200** | ~800 |
| `USER.md` | Perfil do usuário | **1.375** | ~500 |

Esses valores foram projetados para modelos com contexto de 8k tokens. Para modelos modernos (128k+), são excessivamente restritivos.

### Ocupação crítica antes da correção

| Instância | memory_char_limit | Ocupação | user_char_limit | Ocupação |
|-----------|-------------------|----------|-----------------|----------|
| Cohen | 2.200 → 3.200 (config) | **3.144/3.200 (99%)** | 1.375 → 2.000 (config) | 1.700/2.000 (85%) |
| Hermes | 2.200 → 3.200 (config) | 2.716/3.200 (84%) | 1.375 → 2.000 (config) | **1.858/2.000 (92%)** |

![Ocupação de Memória: Antes vs Depois](assets/s01e05_memoria_antes_depois.png)

### Mecanismo da falha

![Mecanismo da Falha](assets/s01e05_mecanismo_falha.png)

```
1. Tarefa ativa gera entradas na memória
2. Memória atinge 99% de capacidade (3.144/3.200 chars)
3. Novas entradas forçam substituição — contexto da tarefa é removido
4. Restart do gateway limpa a conversa ativa
5. Memória persistente é injetada, mas SEM o contexto perdido no passo 3
6. Agente "acorda" sem saber do que estava falando — amnésia
```

O problema não é o restart em si, mas a **inabilidade de registrar contexto suficiente** antes que o limite force a compactação.

---

## Base Oficial: GitHub Issues do Projeto

A alteração via `config.yaml` é **oficialmente suportada** pelo projeto. Três issues documentam o problema, a solução e um bug relacionado:

### Issue #5320 — Auto-escala dos Limites (Proposta)

| Campo | Valor |
|-------|-------|
| **Título** | feat(memory): raise/auto-scale memory_char_limit defaults and surface usage pressure |
| **Autor** | @trevorgordon981 |
| **Repositório** | NousResearch/hermes-agent |
| **Status** | Aberto |
| **Link** | https://github.com/NousResearch/hermes-agent/issues/5320 |

**Proposta principal:**

1. **Aumentar os defaults** para ~4x o atual (8.800 / 5.500 chars, ~3.200 / 2.000 tokens)
2. **Auto-escala baseada em contexto**: quando `model.context_length` está configurado, derivar os limites como fração configurável (default 2%) do contexto
3. **Aviso proativo de pressão**: quando o store acima de 80%, exibir hint como `[memory 1821/2200 chars (83%) — consider consolidating older entries]`
4. **Comando CLI** `hermes memory stats` para consultar utilização

> *"Multi-day / multi-session users accumulate curated memory steadily. Hitting the 2200 cap silently converts `memory add` into `memory add failed` for the rest of the session, degrading the agent's usefulness at exactly the point where more history would help."*
> — @trevorgordon981, Issue #5320

### Issue #16831 — Override Configurável (Implementado)

| Campo | Valor |
|-------|-------|
| **Título** | [Feature Request] Configurable memory character limit (currently hardcoded at 2,200) |
| **Autor** | @Kikk79 |
| **Repositório** | NousResearch/hermes-agent |
| **Status** | Fechado (implementado) |
| **Link** | https://github.com/NousResearch/hermes-agent/issues/16831 |

**Contexto:** Este issue formalizou a necessidade de override via config.yaml. A funcionalidade foi implementada, permitindo que usuários configurem `memory.memory_char_limit` e `memory.user_char_limit` diretamente no `config.yaml`.

> *"The short-term memory is uniquely valuable because it is automatically injected into every turn without requiring explicit search calls. Hitting the 2,200 cap forces users to constantly prune facts that are still relevant."*
> — @Kikk79, Issue #16831

### Issue #11665 — Bug: CLI/MCP Ignora Config (Aberto)

| Campo | Valor |
|-------|-------|
| **Título** | Memory char limits ignored by CLI/MCP tool dispatch path |
| **Autor** | @iamvinay5555 |
| **Repositório** | NousResearch/hermes-agent |
| **Status** | Aberto (bug confirmado) |
| **Link** | https://github.com/NousResearch/hermes-agent/issues/11665 |

**Bug:** O `memory_char_limit` e `user_char_limit` do `config.yaml` só são lidos pelo caminho do gateway (`run_agent.py` → `AIAgent.__init__`). Sessões CLI e chamadas via `handle_function_call` usam os defaults hardcoded em `MemoryStore.__init__`.

| Via | Lê config.yaml? | Limite efetivo |
|-----|-----------------|---------------|
| Gateway (Telegram, Discord, WhatsApp) | Sim | 10.000 / 5.000 |
| CLI (terminal local) | **Não** (bug) | 2.200 / 1.375 (hardcoded) |
| MCP | **Não** (bug) | 2.200 / 1.375 (hardcoded) |

**Impacto para nós:** O agente remoto opera via gateway (Telegram) — não é afetado. O agente local opera primariamente via CLI — ainda está sujeito aos limites hardcoded até correção upstream.

---

## Cálculo de 2% do Contexto

A proposta do Issue #5320 é derivar os limites como 2% do `context_length` do modelo. Aplicando ao modelo em uso (`z-ai/glm-5.1`, contexto de 128k tokens):

![Cálculo de 2% do Contexto](assets/s01e05_calculo_2porcento_contexto.png)

| Campo | 2% do Contexto (tokens) | Equivalente chars | Config Aplicado | Margem |
|-------|------------------------|-------------------|-----------------|--------|
| `memory_char_limit` | ~3.200 tokens | ~8.800 chars | **10.000** | **+13,6%** |
| `user_char_limit` | ~2.000 tokens | ~5.500 chars | **5.000** | -9,1% (*) |

(*) O `user_char_limit` de 5.000 chars fica ~9% abaixo do cálculo ideal de 5.500. Na prática, o user_profile é mais estável e cresce mais lentamente — 5.000 é adequado. Se ultrapassar 80% (4.000 chars), pode ser ajustado para 6.000.

**Conclusão:** Nosso config de 10.000/5.000 está alinhado com a proposta de 2% do contexto, com folga adicional em memory e margem justificada em user.

---

## Solução Aplicada

### Alteração no config.yaml

```yaml
memory:
  memory_char_limit: 10000  # era 3200 (override anterior), default original 2200
  user_char_limit: 5000     # era 2000 (override anterior), default original 1375
```

### Procedimento

1. Backup de segurança: `cp config.yaml config.yaml.bak`
2. Alteração via Python (yaml.safe_load/dump) — sem risco de corromper o YAML
3. Validação de integridade: campos críticos preservados
4. Aplicado em ambas as instâncias com restart do gateway

### Resultado

| Instância | Ocupação Antes | Ocupação Depois | Redução |
|-----------|---------------|-----------------|---------|
| Cohen — memory | **99%** (3.144/3.200) | 31% (3.144/10.000) | -68 pp |
| Cohen — user | 85% (1.700/2.000) | 34% (1.700/5.000) | -51 pp |
| Hermes — memory | 84% (2.716/3.200) | 27% (2.716/10.000) | -57 pp |
| Hermes — user | **92%** (1.858/2.000) | 37% (1.858/5.000) | -55 pp |

---

## Análise de Impacto

### Benefícios

1. **Folga de memória:** 3x mais espaço em memory e 2,5x em user_profile reduz drasticamente a chance de saturação
2. **Continuidade de tarefas:** Contexto de tarefas ativas agora tem espaço para ser registrado sem forçar substituição
3. **Menos compactação automática:** O compressor de contexto atua com menos frequência, preservando mais detalhes
4. **Redução da amnésia:** O padrão de "perder o fio da meada" após restart deve se tornar raro

### Riscos e Mitigações

| Risco | Mitigação |
|-------|-----------|
| Maior uso de tokens por turno (memória maior = mais contexto injetado) | O compressor atua com threshold de 0,66 — compacta automaticamente se necessário |
| Custo marginalmente maior por requisição | Impacto mínimo vs benefício de continuidade de tarefas |
| Bug #11665 — CLI não lê config | Operar via gateway para sessões críticas até correção upstream |

---

## Recomendações

1. **Monitorar ocupação semanalmente:** Se `memory_char_limit` atingir 80% de 10.000 (8.000 chars), avaliar compactação ou aumento adicional
2. **Protocolo de checkpoint antes de restart:** Registrar contexto da tarefa ativa no armazenamento persistente antes de reiniciar o gateway
3. **Acompanhar Issue #11665:** Quando o bug de leitura do config pelo CLI for corrigido, verificar se os limites passam a ser respeitados em sessões de terminal
4. **Avaliar user_char_limit para 6.000:** Se atingir 80% de 5.000 (4.000 chars), considerar aumento
5. **Auto-escala futura (Issue #5320):** Se implementado, os limites serão calculados automaticamente. Até lá, config manual é o caminho oficial (#16831)
6. **Sincronizar correções entre instâncias:** Quando um agente aplica uma correção de config, comunicar ao outro para aplicar o mesmo change

---

## Fontes e Referências

### GitHub Issues (Fontes Primárias)

| Issue | Título | Autor | Status | Link |
|-------|--------|-------|--------|------|
| **#5320** | feat(memory): raise/auto-scale memory_char_limit defaults and surface usage pressure | @trevorgordon981 | Aberto | [github.com/NousResearch/hermes-agent/issues/5320](https://github.com/NousResearch/hermes-agent/issues/5320) |
| **#16831** | [Feature Request] Configurable memory character limit (currently hardcoded at 2,200) | @Kikk79 | Fechado | [github.com/NousResearch/hermes-agent/issues/16831](https://github.com/NousResearch/hermes-agent/issues/16831) |
| **#11665** | Memory char limits ignored by CLI/MCP tool dispatch path | @iamvinay5555 | Aberto (bug) | [github.com/NousResearch/hermes-agent/issues/11665](https://github.com/NousResearch/hermes-agent/issues/11665) |

### Documentação Oficial

| Fonte | Descrição | Link |
|-------|-----------|------|
| Memory Feature Docs | Documentação oficial de memória persistente | [hermes-agent/.../memory.md](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/memory.md) |
| Configuration Reference | Referência completa de configuração | [hermes-agent/.../configuration.md](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/configuration.md) |

### Issue Relacionado

| Issue | Descrição | Link |
|-------|-----------|------|
| **#5563** | [Critical UX] Memory persistence, token waste from session replay | [github.com/.../issues/5563](https://github.com/NousResearch/hermes-agent/issues/5563) |

---

*Christian Rasseli, Cohen (agente remoto), Hermes (agente local)*
