---
title: OS-004 — Limpeza Arquitetural e Restauração de Serviços Nativos
date: 2026-04-25 13:54:16
updated: 2026-04-25 13:54:16
tags:
  - inbox-auto
  - md
source: 
related: []
---

---
title: "OS-004 — Limpeza Arquitetural e Restauração de Serviços Nativos"
date: 2026-04-25
tipo: ordem-de-servico
prioridade: crítica
status: pendente-execução
agente: Hermes
solicitante: Christian
vault_destino: Hermes/OS/Ativas/Diagnosticos/
tags:
  - os-004
  - limpeza
  - arquitetura
  - holographic
  - memory-providers
  - soul
  - restauração
referencias:
  - https://hermes-agent.nousresearch.com/docs/user-guide/features/memory
  - https://hermes-agent.nousresearch.com/docs/user-guide/features/memory-providers
  - https://hermes-agent.nousresearch.com/docs/user-guide/features/personality
  - https://hermes-agent.nousresearch.com/docs/user-guide/features/tools
---

# OS-004 — Limpeza Arquitetural e Restauração de Serviços Nativos

> **LEIA ANTES DE EXECUTAR**: Esta OS é sequencial com travas obrigatórias.
> Nenhuma fase pode ser pulada. Nenhum arquivo pode ser deletado permanentemente
> antes de ser arquivado. O objetivo é fotografar, arquivar, limpar e restaurar
> — nessa ordem. Toda evidência deve ser registrada antes de qualquer alteração.

---

## Contexto e Motivação

A OS-003 revelou que o sistema de memória do Hermes acumulou duas arquiteturas
paralelas ao longo de sessões anteriores:

**Arquitetura A — Nativa (oficial):**
- `session_search` com FTS5 em `~/.hermes/state.db`
- `memory` tool com `MEMORY.md` e `USER.md`
- Provider **Holographic** (possivelmente ativo) com `memory_store.db`
- Documentação: https://hermes-agent.nousresearch.com/docs/user-guide/features/memory

**Arquitetura B — Customizada (construída por fora):**
- Scripts Python em `~/.hermes/skills/obsidian/scripts/`
- `memory_store.db` potencialmente compartilhado ou sobreposto
- Protocolo no SOUL.md referenciando ferramentas fora do tool gateway
- `nv-embedcode-7b-v1` para embeddings (modelo voltado para código)
- 3 scripts com erros de sintaxe confirmados

**Problema:** As duas arquiteturas operam sobre o mesmo banco `memory_store.db`,
causando estado inconsistente, contagens divergentes e comportamento imprevisível.

**Solução:** Arquivar a Arquitetura B, ativar corretamente a Arquitetura A,
reescrever o SOUL.md usando exclusivamente o vocabulário oficial do tool gateway.

---

## FASE 1 — Inventário Completo do Estado Atual

**Objetivo:** fotografar tudo antes de tocar em qualquer coisa.

### 1.1 — Verificar status do Memory Provider ativo

```bash
# Verificar qual provider está configurado
grep -A5 "memory:" ~/.hermes/config.yaml 2>/dev/null || echo "Seção memory não encontrada"

# Verificar via CLI oficial
hermes memory status 2>/dev/null || echo "Comando não disponível"
```

Registrar no relatório:
- [ ] Provider ativo: _______________
- [ ] Holographic está ou não configurado

### 1.2 — Verificar estado do Holographic

```bash
# Schema do banco — Holographic usa tabelas específicas
python3 -c "
import sqlite3, os
db = os.path.expanduser('~/.hermes/memory_store.db')
conn = sqlite3.connect(db)
c = conn.cursor()
tables = c.execute(\"SELECT name FROM sqlite_master WHERE type='table' ORDER BY name\").fetchall()
print('TABELAS:')
for t in tables:
    name = t[0]
    count = c.execute(f'SELECT COUNT(*) FROM \"{name}\"').fetchone()[0]
    print(f'  {name}: {count} registros')
conn.close()
"
```

```bash
# Verificar se o plugin Holographic está instalado
ls ~/.hermes/plugins/memory/ 2>/dev/null || echo "Diretório de plugins não encontrado"
grep -r "holographic" ~/.hermes/config.yaml ~/.hermes/.env 2>/dev/null || echo "Holographic não encontrado nas configs"
```

Registrar no relatório:
- [ ] Tabelas encontradas no memory_store.db: _______________
- [ ] As tabelas correspondem ao schema do Holographic (`facts`, `fact_feedback`)?
- [ ] Ou são tabelas customizadas (`obsidian_index`, `obsidian_content`, `vec_obsidian`)?
- [ ] Ou ambas coexistem?

### 1.3 — Inventário dos scripts customizados

```bash
# Listar todos os scripts com status
for script in ~/.hermes/skills/obsidian/scripts/*.py; do
    echo "--- $(basename $script) ---"
    wc -l "$script"
    python3 -m py_compile "$script" 2>&1 && echo "STATUS: OK" || echo "STATUS: QUEBRADO"
done
```

```bash
# Verificar se algum script está referenciado fora da pasta obsidian
grep -rn "search_vault\|vault_check\|save_note\|search_semantic\|populate_vault" \
  ~/.hermes/ --include="*.py" --include="*.yaml" --include="*.md" \
  | grep -v "skills/obsidian/scripts" \
  | grep -v "__pycache__"
```

Registrar no relatório:
- [ ] Lista completa de scripts com status (OK/QUEBRADO)
- [ ] Scripts referenciados fora da pasta obsidian

### 1.4 — Verificar MEMORY.md e USER.md atuais

```bash
echo "=== MEMORY.md ===" && cat ~/.hermes/memories/MEMORY.md 2>/dev/null || echo "Não encontrado"
echo "=== USER.md ===" && cat ~/.hermes/memories/USER.md 2>/dev/null || echo "Não encontrado"
```

```bash
# Verificar uso de capacidade
python3 -c "
import os
for f in ['MEMORY.md', 'USER.md']:
    path = os.path.expanduser(f'~/.hermes/memories/{f}')
    if os.path.exists(path):
        size = len(open(path).read())
        print(f'{f}: {size} chars')
    else:
        print(f'{f}: não encontrado')
"
```

Registrar no relatório:
- [ ] Conteúdo atual de MEMORY.md
- [ ] Conteúdo atual de USER.md
- [ ] Uso de capacidade de cada um

### 1.5 — Ler o SOUL.md atual completo

```bash
cat ~/.hermes/SOUL.md
```

Registrar no relatório:
- [ ] Seções presentes no SOUL.md
- [ ] Quais tools são referenciadas que NÃO existem no gateway oficial

### ✅ TRAVA FASE 1

Só avançar após:
1. Status do memory provider documentado com evidência
2. Schema completo do memory_store.db registrado
3. Inventário de scripts com status OK/QUEBRADO
4. Conteúdo de MEMORY.md e USER.md registrado
5. SOUL.md lido na íntegra

---

## FASE 2 — Arquivamento da Infraestrutura Customizada

**Objetivo:** preservar tudo antes de remover. Nada é deletado, tudo é arquivado.

### 2.1 — Criar diretório de arquivo

```bash
ARCHIVE_DATE=$(date +%Y-%m-%d)
ARCHIVE_DIR=~/.hermes/archive/custom_infra_$ARCHIVE_DATE
mkdir -p "$ARCHIVE_DIR"
echo "Diretório de arquivo criado: $ARCHIVE_DIR"
```

### 2.2 — Arquivar scripts customizados

```bash
# Copiar (não mover ainda) todos os scripts para o arquivo
cp -r ~/.hermes/skills/obsidian/scripts/ "$ARCHIVE_DIR/obsidian_scripts_backup/"
echo "Scripts copiados para: $ARCHIVE_DIR/obsidian_scripts_backup/"
ls "$ARCHIVE_DIR/obsidian_scripts_backup/"
```

### 2.3 — Arquivar o banco de dados atual

```bash
# Fazer backup completo do memory_store.db antes de qualquer alteração
cp ~/.hermes/memory_store.db "$ARCHIVE_DIR/memory_store_backup_$ARCHIVE_DATE.db"
echo "Banco arquivado em: $ARCHIVE_DIR/memory_store_backup_$ARCHIVE_DATE.db"
ls -lh "$ARCHIVE_DIR/memory_store_backup_$ARCHIVE_DATE.db"
```

### 2.4 — Arquivar o SOUL.md atual

```bash
cp ~/.hermes/SOUL.md "$ARCHIVE_DIR/SOUL_backup_$ARCHIVE_DATE.md"
echo "SOUL.md arquivado em: $ARCHIVE_DIR/SOUL_backup_$ARCHIVE_DATE.md"
```

### 2.5 — Confirmar integridade do arquivo

```bash
echo "=== CONTEÚDO DO ARQUIVO ==="
find "$ARCHIVE_DIR" -type f | sort
echo ""
echo "=== TAMANHOS ==="
du -sh "$ARCHIVE_DIR"/*
```

### ✅ TRAVA FASE 2

Só avançar após:
1. Confirmação visual de que todos os arquivos foram copiados
2. `memory_store_backup` existe e tem tamanho esperado (~18MB)
3. `SOUL_backup` existe e tem conteúdo

---

## FASE 3 — Verificação e Ativação do Sistema Nativo

**Objetivo:** verificar se o Holographic está ativo e configurado corretamente.
Se não estiver, ativá-lo via CLI oficial.

### 3.1 — Verificar instalação do Holographic

Conforme documentação oficial, o Holographic não requer dependências externas —
SQLite já está disponível nativamente.

Fonte: https://hermes-agent.nousresearch.com/docs/user-guide/features/memory-providers

```bash
# Verificar se o plugin existe
find ~/.hermes/ -path "*/memory/holographic*" -o -path "*/plugins/holographic*" 2>/dev/null | head -20

# Verificar config atual
cat ~/.hermes/config.yaml | grep -A10 "memory:"
```

### 3.2 — Verificar se Holographic já está ativo

```bash
hermes memory status 2>&1
```

**Se retornar que Holographic está ativo:** registrar e pular para 3.4.

**Se retornar que nenhum provider está ativo ou outro provider está ativo:**
executar o passo 3.3.

### 3.3 — Ativar Holographic via CLI oficial

```bash
# Ativar via comando oficial
hermes memory setup
# Selecionar "holographic" no menu interativo
```

**OU via config manual:**

```bash
hermes config set memory.provider holographic
```

Verificar ativação:

```bash
hermes memory status
```

### 3.4 — Verificar schema do Holographic no banco

O Holographic usa as tabelas `facts` e `fact_feedback` no `memory_store.db`.
Fonte: https://hermes-agent.nousresearch.com/docs/user-guide/features/memory-providers

```bash
python3 -c "
import sqlite3, os
db = os.path.expanduser('~/.hermes/memory_store.db')
conn = sqlite3.connect(db)
c = conn.cursor()

# Verificar se tabelas do Holographic existem
for table in ['facts', 'fact_feedback']:
    try:
        count = c.execute(f'SELECT COUNT(*) FROM {table}').fetchone()[0]
        print(f'{table}: {count} registros — OK')
    except Exception as e:
        print(f'{table}: NÃO ENCONTRADA — {e}')

# Verificar se tabelas customizadas ainda existem
for table in ['obsidian_index', 'obsidian_content', 'vec_obsidian']:
    try:
        count = c.execute(f'SELECT COUNT(*) FROM {table}').fetchone()[0]
        print(f'{table}: {count} registros — AINDA PRESENTE (customizada)')
    except:
        print(f'{table}: não encontrada (OK)')
conn.close()
"
```

Registrar no relatório:
- [ ] Tabelas nativas do Holographic existem e têm dados?
- [ ] Tabelas customizadas ainda coexistem?

### 3.5 — Verificar session_search nativo

```bash
# Verificar state.db — banco oficial do session_search
ls -lh ~/.hermes/state.db 2>/dev/null || echo "state.db não encontrado"

python3 -c "
import sqlite3, os
db = os.path.expanduser('~/.hermes/state.db')
if not os.path.exists(db):
    print('state.db NÃO ENCONTRADO')
else:
    conn = sqlite3.connect(db)
    c = conn.cursor()
    tables = c.execute(\"SELECT name FROM sqlite_master WHERE type='table'\").fetchall()
    print('Tabelas em state.db:')
    for t in tables:
        count = c.execute(f'SELECT COUNT(*) FROM \"{t[0]}\"').fetchone()[0]
        print(f'  {t[0]}: {count} registros')
    conn.close()
"
```

Registrar no relatório:
- [ ] state.db existe e tem sessões armazenadas?
- [ ] FTS5 está funcional no state.db?

### ✅ TRAVA FASE 3

Só avançar após:
1. Holographic ativo e confirmado via `hermes memory status`
2. Tabelas nativas do Holographic verificadas
3. state.db confirmado com sessões armazenadas

---

## FASE 4 — Limpeza das Tabelas Customizadas

**Objetivo:** remover as tabelas da Arquitetura B do `memory_store.db` para
eliminar a sobreposição. O backup já foi feito na Fase 2.

> **ATENÇÃO:** Só executar esta fase após confirmar na Fase 2 que o backup
> do banco existe e está íntegro.

### 4.1 — Remover tabelas customizadas do banco

```bash
python3 -c "
import sqlite3, os
db = os.path.expanduser('~/.hermes/memory_store.db')
conn = sqlite3.connect(db)
c = conn.cursor()

custom_tables = ['obsidian_index', 'obsidian_content', 'vec_obsidian']
for table in custom_tables:
    try:
        c.execute(f'DROP TABLE IF EXISTS \"{table}\"')
        print(f'Tabela {table}: REMOVIDA')
    except Exception as e:
        print(f'Tabela {table}: ERRO — {e}')

conn.commit()
conn.close()
print('Limpeza concluída.')
"
```

### 4.2 — Verificar banco após limpeza

```bash
python3 -c "
import sqlite3, os
db = os.path.expanduser('~/.hermes/memory_store.db')
conn = sqlite3.connect(db)
c = conn.cursor()
tables = c.execute(\"SELECT name FROM sqlite_master WHERE type='table' ORDER BY name\").fetchall()
print('Tabelas restantes:')
for t in tables:
    count = c.execute(f'SELECT COUNT(*) FROM \"{t[0]}\"').fetchone()[0]
    print(f'  {t[0]}: {count} registros')
conn.close()
"
```

### 4.3 — Arquivar (não deletar) os scripts customizados

O diretório de scripts já foi copiado na Fase 2. Agora renomear para indicar
que está desativado:

```bash
mv ~/.hermes/skills/obsidian/scripts/ ~/.hermes/skills/obsidian/scripts_archived_$(date +%Y-%m-%d)/
echo "Scripts movidos para arquivo."
ls ~/.hermes/skills/obsidian/
```

### ✅ TRAVA FASE 4

Só avançar após:
1. Tabelas customizadas removidas do banco
2. Apenas tabelas nativas do Holographic permanecem
3. Scripts movidos para diretório arquivado (não deletados)

---

## FASE 5 — Reescrita do SOUL.md

**Objetivo:** reescrever o protocolo de recall usando exclusivamente ferramentas
que existem no tool gateway oficial do Hermes.

### Ferramentas oficiais de memória disponíveis no gateway:

Conforme documentação oficial:
- `memory` — add/replace/remove entradas em MEMORY.md e USER.md
- `session_search` — busca FTS5 em sessões passadas (`state.db`)
- `fact_store` — 9 ações do Holographic: add, search, probe, related, reason,
  contradict, update, remove, list
- `fact_feedback` — rating helpful/unhelpful para treinar trust scores

### 5.1 — Ler o SOUL.md atual para referência

```bash
cat ~/.hermes/SOUL.md
```

### 5.2 — Reescrever a seção de protocolo de recall

Substituir a seção `RECALL: PROTOCOLO OBRIGATORIO` atual pelo seguinte conteúdo:

```markdown
## RECALL: PROTOCOLO OBRIGATORIO

Sequência obrigatória para qualquer query sobre projetos, memórias ou
informações de sessões anteriores:

### PASSO 1 — Verificar memória ativa (instantâneo)
Antes de qualquer busca, as entradas de MEMORY.md já estão no contexto.
Verificar se a resposta já está disponível sem tool call.

### PASSO 2 — Buscar fatos no Holographic (se necessário)
Primeira tool call obrigatória quando MEMORY.md não contém a resposta:

  fact_store(action="search", query="<termo relevante>")

Se retornar resultados relevantes: usar os fatos encontrados.
Só avançar para o Passo 3 se fact_store retornar vazio ou irrelevante.

### PASSO 3 — Buscar em sessões passadas (se necessário)
Segunda opção, somente se fact_store não respondeu:

  session_search(query="<termo relevante>")

### PASSO 4 — Web search (somente para informações externas)
Apenas para informações que não são do histórico pessoal/projetos:

  web_search(query="...")

### REGRA INVIOLÁVEL
- PROIBIDO usar session_search antes de fact_store
- PROIBIDO usar web_search para buscar informações de projetos ou histórico
- PROIBIDO referenciar search_vault.py, vault_check.py ou qualquer script
  Python customizado — essas ferramentas não estão no tool gateway

### EXCEÇÕES (podem ir direto para web_search)
- Clima e notícias em tempo real
- Informações técnicas externas (documentação, releases)
```

### 5.3 — Aplicar a reescrita

```bash
# Fazer backup do SOUL.md atual antes de editar
cp ~/.hermes/SOUL.md ~/.hermes/SOUL_pre_os004_$(date +%Y-%m-%d).md

# Abrir para edição
nano ~/.hermes/SOUL.md
# OU
code ~/.hermes/SOUL.md
```

### 5.4 — Verificar SOUL.md após edição

```bash
cat ~/.hermes/SOUL.md | grep -A30 "RECALL"
```

Confirmar:
- [ ] Nenhuma referência a `search_vault.py`
- [ ] Nenhuma referência a `vault_check.py`
- [ ] `fact_store` está como primeira tool call
- [ ] `session_search` está como segunda opção

### ✅ TRAVA FASE 5

Só avançar após:
1. SOUL.md reescrito sem referências a scripts customizados
2. Protocolo usa apenas ferramentas do tool gateway oficial
3. Backup do SOUL.md anterior confirmado

---

## FASE 6 — Teste de Validação

**Objetivo:** confirmar que o protocolo agora funciona corretamente com as
ferramentas nativas.

### 6.1 — Teste do fact_store

```bash
# Verificar se fact_store está disponível
hermes tools list 2>/dev/null | grep -i "fact\|holographic\|memory"
```

### 6.2 — Teste de sessão real

Iniciar uma nova sessão do Hermes e fazer uma pergunta de recall:

```
"O que foi feito na integração SQLite-Obsidian?"
```

Verificar:
- [ ] Primeira tool call foi `fact_store` ou verificação de MEMORY.md?
- [ ] `session_search` foi chamado apenas se `fact_store` retornou vazio?
- [ ] `search_vault.py` NÃO foi chamado?

### 6.3 — Registrar resultado do teste

Copiar o output da sessão de teste para o relatório final.

### ✅ TRAVA FASE 6

Só encerrar a OS após:
1. Teste de sessão executado
2. Sequência de tool calls registrada
3. Protocolo obedecido confirmado (ou nova falha documentada para próxima OS)

---

## FASE 7 — Documentação e Encerramento

### 7.1 — Salvar o relatório final no vault

```bash
VAULT="${OBSIDIAN_VAULT_PATH:-$HOME/Documents/Obsidian Vault}"
mkdir -p "$VAULT/Hermes/OS/Ativas/Diagnosticos"
cat > "$VAULT/Hermes/OS/Ativas/Diagnosticos/Relatorio_OS-004_$(date +%Y-%m-%d).md" << 'EOF'
---
title: Relatório OS-004 — Limpeza Arquitetural e Restauração
date: 2026-04-25
tags: os-004, limpeza, holographic, soul, restauração
---

# Relatório OS-004

## Resumo
[preencher]

## Fase 1 — Estado inicial documentado
[preencher]

## Fase 2 — Arquivamento
- Diretório de arquivo: [preencher]
- Backup do banco: [preencher]

## Fase 3 — Sistema nativo
- Holographic ativo: SIM/NÃO
- state.db com sessões: SIM/NÃO

## Fase 4 — Limpeza
- Tabelas removidas: [listar]
- Scripts arquivados em: [preencher]

## Fase 5 — SOUL.md
- Reescrito: SIM/NÃO
- Backup anterior em: [preencher]

## Fase 6 — Teste de validação
- Primeira tool call: [preencher]
- Protocolo obedecido: SIM/NÃO/PARCIAL

## Status Final
Limpeza: CONCLUÍDA/PARCIAL
Alterações realizadas: [listar]
Pendências: [listar]
Solicitante: Christian
Executor: Hermes
EOF
```

### 7.2 — Confirmar caminho do relatório

```bash
ls -lh "$VAULT/Hermes/OS/Ativas/Diagnosticos/Relatorio_OS-004_$(date +%Y-%m-%d).md"
```

---

## Checklist Final de Encerramento

- [ ] Fase 1 — Inventário completo documentado
- [ ] Fase 2 — Backup de tudo confirmado antes de qualquer alteração
- [ ] Fase 3 — Holographic ativo e state.db confirmado
- [ ] Fase 4 — Tabelas customizadas removidas, scripts arquivados
- [ ] Fase 5 — SOUL.md reescrito com ferramentas nativas
- [ ] Fase 6 — Teste de validação executado e registrado
- [ ] Fase 7 — Relatório salvo no vault no caminho correto
- [ ] Nenhum arquivo foi deletado permanentemente
- [ ] Christian foi informado do resultado

---

## Referências Oficiais Utilizadas

| Tópico | URL |
|--------|-----|
| Sistema de memória nativo | https://hermes-agent.nousresearch.com/docs/user-guide/features/memory |
| Memory providers (Holographic) | https://hermes-agent.nousresearch.com/docs/user-guide/features/memory-providers |
| SOUL.md e personalidade | https://hermes-agent.nousresearch.com/docs/user-guide/features/personality |
| Tools e tool gateway | https://hermes-agent.nousresearch.com/docs/user-guide/features/tools |
| Skill Obsidian oficial | https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/note-taking/note-taking-obsidian |

---

*OS emitida em 2026-04-25 | Solicitante: Christian | Agente executor: Hermes*
*Baseada exclusivamente na documentação oficial do Hermes Agent (Nous Research)*
*Versão: 1.0*
