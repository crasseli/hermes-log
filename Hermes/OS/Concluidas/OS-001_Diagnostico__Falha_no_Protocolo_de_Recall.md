---
title: OS-001 — Diagnóstico: Falha no Protocolo de Recall
date: 2026-04-25 12:36:01
updated: 2026-04-25 12:36:01
tags:
  - inbox-auto
  - md
source: 
related: []
---

---
title: "OS-003 — Diagnóstico: Falha no Protocolo de Recall"
date: 2026-04-25
tipo: ordem-de-servico
prioridade: crítica
status: pendente-execução
agente: Hermes
solicitante: Christian Rasseli
vault_destino: Hermes/OS/Ativas/Diagnosticos/
tags:
  - diagnóstico
  - protocolo
  - recall
  - soul
  - orquestrador
  - kimi-k2.5
  - ordem-de-servico
---

# OS-001 — Diagnóstico: Falha no Protocolo de Recall

> **LEIA ANTES DE EXECUTAR**: Esta OS é um documento de execução sequencial com travas. Cada fase possui um critério de conclusão obrigatório (✅ TRAVA) que deve ser satisfeito antes de avançar para a próxima fase. Nenhuma fase pode ser pulada. Nenhuma suposição substitui evidência coletada. O relatório final deve ser baseado exclusivamente nos achados documentados aqui.

---

## Contexto do Problema

O protocolo definido no `SOUL.md` exige que a primeira tool call de qualquer sessão de recall siga a sequência:

```
1º → search_vault.py (ou vault_check.py)
2º → session_search (somente se vault vazio)
3º → web_search (somente se ambos vazios)
```

Comportamento observado em 25/04/2026: a primeira tool call foi `session_search`, violando o protocolo. O `SOUL.md` foi atualizado e commitado. O `git pull` do Hermes não interfere no `SOUL.md`. A violação persiste.

**Hipóteses abertas:**
- A: Orquestrador tem lógica hardcoded que sobrepõe o SOUL.md
- B: O modelo Kimi K2.5 (NVIDIA NIM) não segue restrições de ordem de tool use
- C: O SOUL.md não está sendo carregado corretamente no contexto da sessão

---

## FASE 1 — Verificação do SOUL.md

**Objetivo**: confirmar que o SOUL.md contém as instruções corretas e está sendo injetado no contexto.

### 1.1 — Ler o SOUL.md atual

```bash
cat ~/.hermes/SOUL.md
```

**Registrar no relatório:**
- [ ] Confirmar que a seção `RECALL: PROTOCOLO OBRIGATORIO` existe
- [ ] Copiar o trecho exato da seção de recall para o relatório
- [ ] Registrar o número da linha onde a seção começa

### 1.2 — Verificar posição do SOUL.md no system prompt

Localizar no código do Hermes onde o SOUL.md é injetado no contexto:

```bash
grep -rn "SOUL" ~/.hermes/ --include="*.py" | grep -v "__pycache__"
grep -rn "soul" ~/.hermes/ --include="*.py" | grep -v "__pycache__"
grep -rn "system_prompt" ~/.hermes/ --include="*.py" | grep -v "__pycache__"
```

**Registrar no relatório:**
- [ ] Arquivo(s) onde o SOUL.md é lido/injetado
- [ ] Linha exata da injeção
- [ ] Posição no system prompt: INÍCIO, MEIO ou FIM (crítico — LLMs priorizam o início)

### 1.3 — Imprimir o system prompt completo de uma sessão real

Se o orquestrador permitir:

```bash
# Adicionar print temporário ou verificar se existe modo debug
grep -rn "debug\|verbose\|print.*prompt\|log.*system" ~/.hermes/ --include="*.py" | grep -v "__pycache__"
```

**Registrar no relatório:**
- [ ] O system prompt completo, ou pelo menos os primeiros e últimos 500 caracteres
- [ ] Tamanho total estimado em tokens/caracteres

### ✅ TRAVA FASE 1

Só avançar para Fase 2 após confirmar:
1. SOUL.md existe e contém a seção de protocolo de recall
2. Localizado o ponto de injeção no código
3. Posição do SOUL.md no system prompt documentada

---

## FASE 2 — Auditoria do Orquestrador

**Objetivo**: determinar se o orquestrador tem lógica própria de seleção de tools que opera independente do SOUL.md.

### 2.1 — Mapear o ponto de decisão de tool calls

```bash
# Localizar onde tools são selecionadas ou priorizadas
grep -rn "tool\|session_search\|search_vault\|recall" ~/.hermes/ --include="*.py" \
  | grep -v "__pycache__" \
  | grep -v "\.pyc"
```

### 2.2 — Verificar se há lista fixa ou prioridade hardcoded

```bash
# Procurar por arrays/listas de tools, priority, default_tool
grep -rn "tools\s*=\s*\[" ~/.hermes/ --include="*.py" | grep -v "__pycache__"
grep -rn "priority\|default_tool\|first_tool\|fallback" ~/.hermes/ --include="*.py" | grep -v "__pycache__"
grep -rn "session_search" ~/.hermes/ --include="*.py" | grep -v "__pycache__"
```

### 2.3 — Ler os arquivos críticos encontrados nos passos anteriores

Para cada arquivo identificado, ler as funções relevantes completas:

```bash
# Substituir <arquivo> pelo caminho encontrado
cat <arquivo> | head -200
```

**Registrar no relatório:**
- [ ] Existe lógica de seleção de tool no código? SIM / NÃO
- [ ] Se SIM: copiar o trecho exato para o relatório
- [ ] O orquestrador monta a lista de tools antes ou depois de ler o SOUL.md?
- [ ] Existe algum `if "recall" in query` ou similar que força `session_search`?

### 2.4 — Verificar o fluxo de inicialização do agente

```bash
# Encontrar o arquivo principal de inicialização
find ~/.hermes/ -name "agent.py" -o -name "main.py" -o -name "hermes.py" -o -name "run.py" 2>/dev/null
```

Ler o arquivo principal e documentar a sequência de inicialização:

```bash
cat <arquivo_principal>
```

**Registrar no relatório:**
- [ ] Sequência de carregamento: o que é inicializado antes do que
- [ ] Em que ponto as tools são registradas vs. em que ponto o SOUL.md é lido

### ✅ TRAVA FASE 2

Só avançar para Fase 3 após:
1. Ter lido o código do orquestrador nas seções relevantes
2. Ter uma resposta definitiva (com evidência de código) para: "existe lógica hardcoded de seleção de tools?"
3. Documentado o fluxo de inicialização

---

## FASE 3 — Teste de Isolamento do Modelo

**Objetivo**: determinar se o Kimi K2.5 via NVIDIA NIM obedece restrições de ordem de tool use quando recebe o system prompt correto, sem o orquestrador como intermediário.

### 3.1 — Extrair o system prompt atual do Hermes

A partir dos achados da Fase 1, obter o system prompt completo que seria enviado ao modelo.

### 3.2 — Construir chamada de teste direto à API

```python
# Salvar como /tmp/test_recall_order.py
import json
import os

# Usar a mesma configuração de endpoint do Hermes
# Localizar as credenciais/endpoint no config do Hermes
```

```bash
grep -rn "NVIDIA\|NIM\|api_key\|endpoint\|base_url\|integrate.api" ~/.hermes/ \
  --include="*.py" --include="*.env" --include="*.yaml" --include="*.toml" \
  | grep -v "__pycache__" | grep -v "secret"
```

### 3.3 — Executar o teste de isolamento

Criar um script que:
1. Use o mesmo system prompt do Hermes (sem modificação)
2. Envie uma query simples de recall: `"O que foi feito na integração SQLite-Obsidian?"`
3. Liste as tools disponíveis: `search_vault`, `session_search`, `web_search`
4. Capture qual tool o modelo escolhe como primeira ação

```bash
python3 /tmp/test_recall_order.py 2>&1 | tee /tmp/test_resultado.txt
cat /tmp/test_resultado.txt
```

### 3.4 — Repetir o teste 3 vezes

O comportamento de LLMs tem variância. Executar 3 vezes e registrar cada resultado.

**Registrar no relatório:**
- [ ] Teste 1: primeira tool call = ___________
- [ ] Teste 2: primeira tool call = ___________
- [ ] Teste 3: primeira tool call = ___________
- [ ] O modelo obedeceu o protocolo em quantas das 3 tentativas? ___/3

### ✅ TRAVA FASE 3

Só avançar para Fase 4 após:
1. Ter executado os 3 testes com resultados registrados
2. Ter uma resposta definitiva: "o modelo isolado obedece ou não a ordem?"

---

## FASE 4 — Teste de Posicionamento do SOUL.md

**Objetivo**: verificar se a posição do SOUL.md no system prompt afeta o comportamento.

> Esta fase só é necessária se a Fase 3 mostrou que o modelo isolado TAMBÉM falha. Se a Fase 2 já identificou lógica hardcoded no orquestrador, esta fase é informativa mas não bloqueante.

### 4.1 — Testar com SOUL.md no início do system prompt

Modificar o teste da Fase 3 para colocar o SOUL.md como **primeira coisa** no system prompt, antes de qualquer outro conteúdo.

Executar 3 vezes. Registrar resultados.

**Registrar:**
- [ ] Teste com SOUL no início: obedeceu em ___/3

### 4.2 — Testar com instrução de recall isolada e reforçada

Testar com uma versão ultra-simplificada e explícita do protocolo:

```
REGRA ABSOLUTA E INVIOLÁVEL — PRIMEIRA AÇÃO OBRIGATÓRIA:
Quando o usuário pedir qualquer informação sobre o passado, memórias ou projetos,
sua PRIMEIRA e ÚNICA primeira tool call DEVE ser: terminal com search_vault.py
É PROIBIDO chamar session_search antes de search_vault.py.
Esta regra não tem exceções.
```

Executar 3 vezes. Registrar resultados.

**Registrar:**
- [ ] Teste com instrução reforçada: obedeceu em ___/3

### ✅ TRAVA FASE 4

Documentar:
1. Resultado comparativo entre posição normal vs. início do system prompt
2. Resultado com instrução reforçada vs. instrução atual
3. Conclusão: o problema é de posicionamento? de fraseamento? ou o modelo ignora completamente?

---

## FASE 5 — Síntese e Parecer Final

**Objetivo**: consolidar todos os achados em diagnóstico definitivo com direção de ação.

### 5.1 — Preencher a matriz de diagnóstico

| Hipótese | Evidência Encontrada | Confirmada? |
|----------|---------------------|-------------|
| A: Orquestrador hardcoded | (preencher com trecho de código ou "nenhuma") | SIM / NÃO / PARCIAL |
| B: Modelo ignora ordem | (preencher com resultados dos testes) | SIM / NÃO / PARCIAL |
| C: SOUL.md mal posicionado | (preencher com posição encontrada) | SIM / NÃO / PARCIAL |

### 5.2 — Identificar a causa raiz

Com base na matriz acima, responder:

**A violação do protocolo é causada por:**

- [ ] Código do orquestrador sobrepõe o SOUL.md → solução: modificar o código
- [ ] Modelo não segue restrições de ordem → solução: reforçar fraseamento / mudar posição
- [ ] SOUL.md injetado muito tarde no contexto → solução: reposicionar no system prompt
- [ ] Combinação de múltiplos fatores → especificar quais

### 5.3 — Redigir o parecer final

O parecer deve ter:
1. **Diagnóstico em 1 frase**: a causa raiz identificada
2. **Evidências**: os 3 achados mais relevantes com referência ao código/teste
3. **Recomendação**: a ação corretiva específica (com exemplo de implementação se aplicável)
4. **Riscos**: o que pode dar errado na correção proposta
5. **Próximo passo imediato**: a primeira coisa a fazer após ler este relatório

---

## FASE 6 — Documentação no Vault Obsidian

**Objetivo**: salvar o relatório completo no vault de forma classificada e indexada.

### 6.1 — Salvar o relatório

```bash
python3 ~/.hermes/skills/obsidian/scripts/save_note.py \
  --title "Relatório OS-001 — Diagnóstico Protocolo Recall $(date +%Y-%m-%d)" \
  --folder "Hermes/Diagnósticos" \
  --tags "diagnóstico,protocolo,recall,soul,os-001,kimi-k2.5,orquestrador" \
  --content "$(cat /tmp/relatorio_os001.md)"
```

### 6.2 — Verificar indexação

```bash
python3 ~/.hermes/skills/obsidian/scripts/vault_check.py \
  --query "OS-001 diagnóstico protocolo recall" \
  --threshold 2
```

**Confirmar:**
- [ ] Nota criada com sucesso no vault
- [ ] Nota indexada no SQLite (`has_results=true`)
- [ ] Auto-links gerados para notas relacionadas

### 6.3 — Criar nota de referência cruzada

Se já existir uma nota sobre o SOUL.md ou sobre o sistema de recall, adicionar um link bidirecional:

```bash
# Verificar nota existente do SOUL.md
python3 ~/.hermes/skills/obsidian/scripts/search_vault.py "SOUL protocolo" --combined
```

### ✅ TRAVA FASE 6

Só encerrar esta OS após:
1. Relatório salvo no vault em `Hermes/Diagnósticos/`
2. Indexação confirmada
3. Confirmação do caminho completo da nota criada impressa no terminal

---

## Template do Relatório Final

> Preencher à medida que as fases são concluídas. Salvar como `/tmp/relatorio_os001.md` durante a execução.

```markdown
---
title: "Relatório OS-001 — Diagnóstico Protocolo Recall"
data_execucao: YYYY-MM-DD
executor: Hermes
os_referencia: OS-001
status: concluído
---

# Relatório de Diagnóstico — Protocolo de Recall

## 1. Resumo Executivo
<!-- Uma frase. Causa raiz identificada. -->

## 2. Achados por Fase

### Fase 1 — SOUL.md
- Seção de recall encontrada: SIM/NÃO
- Posição no system prompt: INÍCIO/MEIO/FIM
- Trecho exato da instrução:
  ```
  [colar aqui]
  ```

### Fase 2 — Orquestrador
- Lógica hardcoded encontrada: SIM/NÃO
- Arquivo: 
- Linha:
- Trecho:
  ```python
  [colar aqui]
  ```

### Fase 3 — Teste do Modelo Isolado
- Teste 1: primeira tool call = 
- Teste 2: primeira tool call = 
- Teste 3: primeira tool call = 
- Taxa de conformidade: /3

### Fase 4 — Posicionamento (se aplicável)
- SOUL no início: /3
- Instrução reforçada: /3

## 3. Matriz de Diagnóstico
| Hipótese | Evidência | Confirmada? |
|----------|-----------|-------------|
| A: Orquestrador hardcoded | | |
| B: Modelo ignora ordem | | |
| C: SOUL.md mal posicionado | | |

## 4. Causa Raiz
<!-- Descrição detalhada -->

## 5. Recomendação
<!-- Ação corretiva com exemplo de implementação -->

## 6. Riscos da Correção
<!-- O que pode dar errado -->

## 7. Próximo Passo Imediato
<!-- A primeira coisa a fazer -->
```

---

## Checklist de Encerramento da OS

Antes de marcar esta OS como concluída, confirmar todos os itens:

- [ ] Fase 1 completa — SOUL.md verificado e posição documentada
- [ ] Fase 2 completa — Orquestrador auditado com evidência de código
- [ ] Fase 3 completa — 3 testes de isolamento executados e registrados
- [ ] Fase 4 completa — (ou justificativa para pular documentada)
- [ ] Fase 5 completa — Parecer final redigido com causa raiz e recomendação
- [ ] Fase 6 completa — Relatório salvo no vault em `Hermes/Diagnósticos/`
- [ ] Indexação confirmada no SQLite
- [ ] Caminho da nota no vault informado ao Christian

---

*OS emitida em 2026-04-25 | Solicitante: Christian | Agente executor: Hermes*
*Versão: 1.0 | Próxima revisão: após execução e análise dos resultados*
