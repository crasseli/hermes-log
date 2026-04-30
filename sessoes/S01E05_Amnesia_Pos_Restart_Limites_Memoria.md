# Amnésia Pós-Restart: Diagnóstico e Correção dos Limites de Memória Persistente

**Sessão:** S01E05
**Autores:** Christian Rasseli, Cohen (agente no M70q), Hermes (agente no notebook DELL)
**Data:** 2026-04-30
**Tipo:** Diagnóstico / Correção de incidente

---

## Resumo do Incidente

Após um restart do gateway, o agente Cohen perdeu completamente o contexto da tarefa ativa e retornou falando de um assunto não relacionado — comportamento que denominamos "amnésia pós-restart". A investigação revelou saturação nos limites de caracteres da memória persistente: `memory_char_limit` em 3.200 com 99% de ocupação, e `user_char_limit` em 2.000 com 92%. Sem espaço para registrar o contexto corrente, novas entradas forçavam a substituição de informações essenciais — que se perderam quando o gateway reiniciou a conversa.

A correção — limites aumentados para 10.000 / 5.000, alinhados com a proposta do GitHub Issue #5320 (2% do contexto do modelo) — reduziu a ocupação média de 90% para 32%, restabelecendo a capacidade de preservar contexto entre sessões.

---

## O Problema

Durante uma sessão ativa no Telegram, o agente Cohen foi submetido a um restart do gateway (comando `/new`). Ao retornar, não apenas perdeu o fio da meada — começou a falar de um assunto completamente diferente (Ollama) como se fosse uma sessão nova, ignorando toda a tarefa em andamento.

### Sintoma observado

```
Operador:  "Continua aquela tarefa de configuração?"
Agente:    "Olá! Posso ajudar com instalação do Ollama hoje?"
           ↑ Comportamento de amnésia total
```

A memória persistente — injetada automaticamente a cada turno no prompt do sistema — deveria ter fornecido contexto suficiente para retomar a tarefa. Mas não forneceu. O agente "acordou" sem saber do que estava falando.

---

## Causa Raiz

### Limites hardcoded por padrão

O projeto Hermes Agent define defaults conservadores para a memória persistente, conforme a [documentação oficial](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/memory.md):

| Arquivo | Função | Default (chars) | Aprox. tokens |
|---------|--------|----------------|---------------|
| `MEMORY.md` | Notas do agente | **2.200** | ~800 |
| `USER.md` | Perfil do usuário | **1.375** | ~500 |

Esses valores foram projetados para modelos com janela de contexto de 8k tokens. Para modelos modernos com 128k+ tokens, são excessivamente restritivos — consomem menos de 1% do contexto disponível.

### Ocupação crítica antes da correção

| Instância | memory_char_limit | Ocupação | user_char_limit | Ocupação |
|-----------|-------------------|----------|-----------------|----------|
| Cohen | 2.200 → 3.200 (config) | **3.144/3.200 (99%)** | 1.375 → 2.000 (config) | 1.700/2.000 (85%) |
| Hermes | 2.200 → 3.200 (config) | 2.716/3.200 (84%) | 1.375 → 2.000 (config) | **1.858/2.000 (92%)** |

### Mecanismo da falha

O problema não é o restart em si, mas a **incapacidade de registrar contexto suficiente antes que o limite force a compactação**:

1. Tarefa ativa gera entradas na memória
2. Memória atinge 99% de capacidade (3.144/3.200 chars)
3. Novas entradas forçam substituição — contexto da tarefa é removido para liberar espaço
4. Restart do gateway limpa a conversa ativa
5. Memória persistente é injetada no novo turno, mas **sem o contexto compactado no passo 3**
6. Agente "acorda" sem saber do que estava falando — amnésia

Quando a memória atinge o limite, `MemoryStore.add()` rejeita novas escritas com a mensagem: *"Memory at 2094/2200 chars. Adding this entry would exceed the limit. Replace or remove existing entries first."* (Issue #5320). Isso converte silenciosamente `memory add` em `memory add failed` pelo resto da sessão.

---

## Base Oficial: GitHub Issues do Projeto

A alteração via `config.yaml` é **oficialmente suportada**. Três issues documentam o problema, a solução e um bug relacionado.

### Issue #5320 — Auto-escala dos Limites (Proposta)

| Campo | Valor |
|-------|-------|
| **Título** | feat(memory): raise/auto-scale memory_char_limit defaults and surface usage pressure |
| **Autor** | @trevorgordon981 |
| **Repositório** | NousResearch/hermes-agent |
| **Status** | Aberto |
| **Link** | [github.com/NousResearch/hermes-agent/issues/5320](https://github.com/NousResearch/hermes-agent/issues/5320) |

**Proposta principal:**

1. **Aumentar os defaults** para ~4x o atual (8.800 / 5.500 chars, ~3.200 / 2.000 tokens)
2. **Auto-escala baseada em contexto**: derivar limites como fração configurável (default 2%) do `context_length` do modelo
3. **Aviso proativo de pressão**: exibir hint quando o store ultrapassar 80% da capacidade
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
| **Link** | [github.com/NousResearch/hermes-agent/issues/16831](https://github.com/NousResearch/hermes-agent/issues/16831) |

Este issue formalizou a necessidade de override via `config.yaml`. A funcionalidade foi implementada, permitindo que usuários configurem `memory.memory_char_limit` e `memory.user_char_limit` diretamente.

> *"The short-term memory is uniquely valuable because it is automatically injected into every turn without requiring explicit search calls. Hitting the 2,200 cap forces users to constantly prune facts that are still relevant."*
> — @Kikk79, Issue #16831

### Issue #11665 — Bug: CLI/MCP Ignora Config (Aberto)

| Campo | Valor |
|-------|-------|
| **Título** | Memory char limits ignored by CLI/MCP tool dispatch path |
| **Autor** | @iamvinay5555 |
| **Repositório** | NousResearch/hermes-agent |
| **Status** | Aberto (bug confirmado) |
| **Link** | [github.com/NousResearch/hermes-agent/issues/11665](https://github.com/NousResearch/hermes-agent/issues/11665) |

O `memory_char_limit` e `user_char_limit` do `config.yaml` só são lidos pelo caminho do gateway. Sessões CLI e chamadas via dispatch do registry usam os defaults hardcoded.

| Via | Lê config.yaml? | Limite efetivo |
|-----|-----------------|---------------|
| Gateway (Telegram, Discord, WhatsApp) | Sim | 10.000 / 5.000 |
| CLI (terminal local) | **Não** (bug) | 2.200 / 1.375 (hardcoded) |
| MCP | **Não** (bug) | 2.200 / 1.375 (hardcoded) |

**Impacto:** O agente remoto opera via gateway — não é afetado. O agente local opera via CLI — ainda sujeito aos limites hardcoded até correção upstream.

---

## Cálculo de 2% do Contexto

A proposta do Issue #5320 é derivar os limites como 2% do `context_length` do modelo. Aplicando ao modelo em uso (128k tokens):

| Campo | 2% do Contexto (tokens) | Equivalente chars | Config Aplicado | Margem |
|-------|------------------------|-------------------|-----------------|--------|
| `memory_char_limit` | ~3.200 tokens | ~8.800 chars | **10.000** | **+13,6%** |
| `user_char_limit` | ~2.000 tokens | ~5.500 chars | **5.000** | -9,1% (*) |

(*) O `user_char_limit` de 5.000 chars fica ~9% abaixo do cálculo ideal de 5.500. Na prática, o perfil de usuário é mais estável e cresce lentamente — 5.000 é adequado. Se atingir 80% (4.000 chars), considerar ajuste para 6.000.

**Conclusão:** O config de 10.000/5.000 está alinhado com a proposta de 2% do contexto (#5320), com folga adicional em memory e margem justificada em user.

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
2. Alteração via Python (`yaml.safe_load`/`dump`) — sem risco de corromper o YAML
3. Validação de integridade: campos críticos preservados (provider, enabled, model, _config_version)
4. Aplicado em ambas as instâncias com restart do gateway

### Resultado Após a Correção

| Instância | Ocupação Antes | Ocupação Depois | Redução | Folga Disponível |
|-----------|---------------|-----------------|---------|------------------|
| Cohen — memory | **99%** (3.144/3.200) | 31% (3.144/10.000) | -68 pp | 6.856 chars |
| Cohen — user | 85% (1.700/2.000) | 34% (1.700/5.000) | -51 pp | 3.300 chars |
| Hermes — memory | 84% (2.716/3.200) | 27% (2.716/10.000) | -57 pp | 7.284 chars |
| Hermes — user | **92%** (1.858/2.000) | 37% (1.858/5.000) | -55 pp | 3.142 chars |

A ocupação média caiu de **90% para 32%** — folga de 58 pontos percentuais. O contexto de tarefas ativas agora pode ser registrado sem forçar substituição de entradas existentes.

---

## Visualizações Comparativas

<div align="center">

### 1. Ocupação de Memória — Antes vs Depois
![Ocupação Antes vs Depois](https://github.com/crasseli/hermes-log/blob/main/assets/s01e05_ocupacao_antes_depois.svg)

### 2. Limites: Default vs Recomendado vs Aplicado
![Limites Default vs Recomendado](https://github.com/crasseli/hermes-log/blob/main/assets/s01e05_limites_default_vs_recomendado.svg)

### 3. Timeline do Incidente
![Timeline do Incidente](https://github.com/crasseli/hermes-log/blob/main/assets/s01e05_timeline_incidente.svg)

</div>

---

## Lições para Mantenedores

1. **Defaults de memória são conservadores demais para modelos modernos** 
 Projetados para janelas de 8k tokens, consomem menos de 1% do contexto em modelos de 128k+. Ajuste proativo é essencial.

2. **Saturação de memória é silenciosa e degradante** 
 Quando `memory add` falha por limite, não há notificação visível ao operador. O agente simplesmente para de registrar fatos novos sem aviso.

3. **O bug #11665 cria comportamento inconsistente entre vias de acesso** 
 Sessões gateway respeitam o config; sessões CLI não. Um mesmo agente pode ter limites diferentes dependendo de como é invocado.

4. **Verifique a ocupação antes de reiniciar o gateway** 
 Se a memória estiver acima de 80%, um restart pode causar amnésia. Não há espaço para registrar checkpoint de contexto.

5. **Correções de configuração devem ser sincronizadas entre instâncias** 
 Quando um agente aplica uma mudança, o outro precisa aplicar o mesmo ajuste. Senão uma instância fica vulnerável.

6. **2% do contexto é um guia, não uma regra rígida** 
 Para `memory_char_limit`, 2% + folga (+13,6%) funcionou bem. Para `user_char_limit`, 2% − margem (−9,1%) é adequado, pois o perfil de usuário cresce mais lentamente.

---

## Recomendações

1. **Monitorar ocupação semanalmente** 
 Se `memory_char_limit` atingir 80% de 10.000 (8.000 chars), avaliar compactação ou aumento adicional.

2. **Protocolo de checkpoint antes de restart** 
 Registrar contexto da tarefa ativa no armazenamento persistente antes de reiniciar o gateway.

3. **Acompanhar Issue #11665** 
 Quando o bug de leitura do config pelo CLI for corrigido, verificar se os limites passam a ser respeitados em sessões de terminal.

4. **Avaliar `user_char_limit` para 6.000** 
 Se atingir 80% de 5.000 (4.000 chars), considerar aumento.

5. **Auto-escala futura (Issue #5320)** 
 Se implementado, os limites serão calculados automaticamente. Até lá, config manual é o caminho oficial (#16831).

---

## Fontes e Referências

### GitHub Issues (Fontes Primárias)

| Issue | Título | Autor | Status | Link |
|-------|--------|-------|--------|------|
| **#5320** | feat(memory): raise/auto-scale memory_char_limit defaults and surface usage pressure | @trevorgordon981 | Aberto | [github.com/.../issues/5320](https://github.com/NousResearch/hermes-agent/issues/5320) |
| **#16831** | [Feature Request] Configurable memory character limit (currently hardcoded at 2,200) | @Kikk79 | Fechado | [github.com/.../issues/16831](https://github.com/NousResearch/hermes-agent/issues/16831) |
| **#11665** | Memory char limits ignored by CLI/MCP tool dispatch path | @iamvinay5555 | Aberto (bug) | [github.com/.../issues/11665](https://github.com/NousResearch/hermes-agent/issues/11665) |

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

Documentado por: Christian Rasseli, Cohen (agente no M70q), Hermes (agente no notebook DELL) — 30 de abril de 2026
