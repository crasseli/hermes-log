---
title: "OS-006 — Restauração e Profissionalização da Integração Hermes-Obsidian"
date: 2026-04-25
tipo: ordem-de-servico
prioridade: crítica
status: pendente-execução
agente: Hermes
solicitante: Christian
vault_destino: Hermes/OS/Ativas/
tags:
  - os-006
  - obsidian
  - restauração
  - recall
  - soul
  - scripts
  - git
  - nomenclatura
referencias:
  - OS-003 (diagnóstico original)
  - OS-004 (limpeza arquitetural)
  - OS-005 (governança do vault)
  - Parecer GLM-5.1 de 25/04/2026
---

# OS-006 — Restauração e Profissionalização da Integração Hermes-Obsidian

> **LEIA ANTES DE EXECUTAR**: Esta OS resolve os 7 problemas críticos
> identificados no parecer de 25/04/2026. As fases são sequenciais e
> obrigatórias. Cada fase tem uma trava explícita — não avance sem satisfazê-la.
> Ao final, produza um relatório completo e atualize suas memórias.
> Esta OS é autocontida: tudo que você precisa está aqui.

---

## Contexto e Problema

O parecer técnico de 25/04/2026 identificou 7 problemas críticos:

1. **Scripts destruídos** — 10 de 12 scripts da skill Obsidian ausentes/desativados
2. **SOUL.md sem regra de autosave** — dependência de memória volátil (92% cheia)
3. **Vault sem git** — sem controle de versão, sem rollback
4. **Nomenclatura violada** — 19 arquivos e 4 pastas com acentos
5. **Spam residual** — 22 notas Sessao_Cron/Autosave ainda presentes
6. **Fragmentação de pastas** — 33 pastas raiz, duplicatas, órfãs
7. **Protocolo de recall quebrado** — pipeline depende de scripts inexistentes

**Causa raiz:** A OS-004 arquivou os scripts customizados sem substituição
funcional. O SOUL.md perdeu a regra de autosave em edição posterior.

---

## FASE 1 — Controle de Versão (Git)

**Objetivo:** proteger o vault antes de qualquer alteração destrutiva.
Se algo der errado nas fases seguintes, git permite rollback total.

### 1.1 — Inicializar repositório git no vault

```bash
cd /mnt/e/Obsidian/Cofre/Hermes
git init
git add .
git commit -m "OS-006: snapshot inicial antes da restauração"
echo "Git inicializado com $(git log --oneline | wc -l) commit(s)"
```

### 1.2 — Verificar .gitignore

```bash
cat > /mnt/e/Obsidian/Cofre/Hermes/.gitignore << 'EOF'
.obsidian/workspace
.obsidian/workspace.json
.trash/
*.tmp
EOF
git add .gitignore
git commit -m "OS-006: adicionar .gitignore"
```

### ✅ TRAVA FASE 1

```bash
git -C /mnt/e/Obsidian/Cofre/Hermes log --oneline | head -3
```

Só avançar se retornar pelo menos 1 commit confirmado.

---

## FASE 2 — Limpeza de Spam Residual

**Objetivo:** remover as 22 notas de spam que sobreviveram à OS-003.

### 2.1 — Identificar e listar o spam residual

```bash
cd /mnt/e/Obsidian/Cofre/Hermes
find . -name "Sessao_Cron_*" -o -name "Autosave_Sessao_*" \
       -o -name "sessao_cron_*" -o -name "autosave_sessao_*" | sort
```

Registrar a lista completa antes de deletar.

### 2.2 — Deletar o spam residual

```bash
cd /mnt/e/Obsidian/Cofre/Hermes
find . \( -name "Sessao_Cron_*" -o -name "Autosave_Sessao_*" \
          -o -name "sessao_cron_*" -o -name "autosave_sessao_*" \) \
     -delete -print
```

### 2.3 — Commit da limpeza

```bash
cd /mnt/e/Obsidian/Cofre/Hermes
git add -A
git commit -m "OS-006: remover $(git status --short | grep D | wc -l) notas de spam residual"
```

### ✅ TRAVA FASE 2

```bash
find /mnt/e/Obsidian/Cofre/Hermes \
  -name "Sessao_Cron_*" -o -name "Autosave_Sessao_*" | wc -l
```

Só avançar se retornar 0.

---

## FASE 3 — Normalização de Nomenclatura

**Objetivo:** renomear os 19 arquivos e 4 pastas com acentos, seguindo
a convenção sem acentos definida na OS-005.

### 3.1 — Listar todos os arquivos e pastas com acentos

```bash
find /mnt/e/Obsidian/Cofre/Hermes -name "*[áàãâäéèêëíìîïóòõôöúùûüçÁÀÃÂÄÉÈÊËÍÌÎÏÓÒÕÔÖÚÙÛÜÇ]*" | sort
```

### 3.2 — Renomear usando iconv/sed

Para cada arquivo encontrado, renomear substituindo os caracteres acentuados:

```bash
# Função de normalização
normalize() {
  echo "$1" | sed 'y/áàãâäéèêëíìîïóòõôöúùûüçÁÀÃÂÄÉÈÊËÍÌÎÏÓÒÕÔÖÚÙÛÜÇ/aaaaaaeeeeiiiiooooouuuucAAAAAAAAEEEEIIIIOOOOOUUUUC/'
}

# Renomear arquivos (processar do mais profundo para o mais raso)
find /mnt/e/Obsidian/Cofre/Hermes -depth \
  -name "*[áàãâäéèêëíìîïóòõôöúùûüçÁÀÃÂÄÉÈÊËÍÌÎÏÓÒÕÔÖÚÙÛÜÇ]*" | \
while IFS= read -r path; do
  dir=$(dirname "$path")
  base=$(basename "$path")
  new_base=$(normalize "$base")
  if [ "$base" != "$new_base" ]; then
    mv -v "$path" "$dir/$new_base"
  fi
done
```

### 3.3 — Commit da normalização

```bash
cd /mnt/e/Obsidian/Cofre/Hermes
git add -A
git commit -m "OS-006: normalizar nomenclatura — remover acentos de arquivos e pastas"
```

### ✅ TRAVA FASE 3

```bash
find /mnt/e/Obsidian/Cofre/Hermes \
  -name "*[áàãâäéèêëíìîïóòõôöúùûüç]*" | wc -l
```

Só avançar se retornar 0 ou próximo de 0 (links do Obsidian podem ter alguns).

---

## FASE 4 — Consolidação de Pastas Duplicadas

**Objetivo:** resolver a fragmentação de 33 pastas raiz eliminando duplicatas
e órfãs identificadas no parecer.

### 4.1 — Listar estrutura atual de primeiro nível

```bash
ls -d /mnt/e/Obsidian/Cofre/Hermes/*/
```

### 4.2 — Consolidar pastas duplicadas identificadas

Executar as consolidações na seguinte ordem, uma por vez, verificando
conteúdo antes de mover:

**a) blacklist/ → Referencias/Tecnologias/**
```bash
ls /mnt/e/Obsidian/Cofre/Hermes/blacklist/ 2>/dev/null && \
mv /mnt/e/Obsidian/Cofre/Hermes/blacklist/* \
   /mnt/e/Obsidian/Cofre/Hermes/Referencias/Tecnologias/ 2>/dev/null && \
rmdir /mnt/e/Obsidian/Cofre/Hermes/blacklist/
```

**b) infraestrutura/ → DevOps/**
```bash
ls /mnt/e/Obsidian/Cofre/Hermes/infraestrutura/ 2>/dev/null && \
mv /mnt/e/Obsidian/Cofre/Hermes/infraestrutura/* \
   /mnt/e/Obsidian/Cofre/Hermes/DevOps/ 2>/dev/null && \
rmdir /mnt/e/Obsidian/Cofre/Hermes/infraestrutura/
```

**c) projects/ → Projetos/**
```bash
ls /mnt/e/Obsidian/Cofre/Hermes/projects/ 2>/dev/null && \
mv /mnt/e/Obsidian/Cofre/Hermes/projects/* \
   /mnt/e/Obsidian/Cofre/Hermes/Projetos/ 2>/dev/null && \
rmdir /mnt/e/Obsidian/Cofre/Hermes/projects/
```

**d) sistema/ + System/ + Sistemas/ → Tecnologia/Sistema/**
```bash
mkdir -p /mnt/e/Obsidian/Cofre/Hermes/Tecnologia/Sistema
for dir in sistema System Sistemas; do
  if [ -d "/mnt/e/Obsidian/Cofre/Hermes/$dir" ]; then
    mv /mnt/e/Obsidian/Cofre/Hermes/$dir/* \
       /mnt/e/Obsidian/Cofre/Hermes/Tecnologia/Sistema/ 2>/dev/null
    rmdir /mnt/e/Obsidian/Cofre/Hermes/$dir/ 2>/dev/null
  fi
done
```

**e) troubleshooting/ → Tecnologia/Bugfixes/**
```bash
ls /mnt/e/Obsidian/Cofre/Hermes/troubleshooting/ 2>/dev/null && \
mv /mnt/e/Obsidian/Cofre/Hermes/troubleshooting/* \
   /mnt/e/Obsidian/Cofre/Hermes/Tecnologia/Bugfixes/ 2>/dev/null && \
rmdir /mnt/e/Obsidian/Cofre/Hermes/troubleshooting/
```

**f) Faculdade/ → FAMEESP/** (verificar qual tem mais conteúdo primeiro)
```bash
echo "Faculdade:" && ls /mnt/e/Obsidian/Cofre/Hermes/Faculdade/ 2>/dev/null | wc -l
echo "FAMEESP:" && ls /mnt/e/Obsidian/Cofre/Hermes/FAMEESP/ 2>/dev/null | wc -l
```
Mover o menor para o maior após verificação.

**g) Hermes/OS/ vs OS/** (verificar e consolidar)
```bash
echo "OS/ na raiz:" && ls /mnt/e/Obsidian/Cofre/Hermes/OS/ 2>/dev/null
echo "Hermes/OS/:" && ls /mnt/e/Obsidian/Cofre/Hermes/Hermes/OS/ 2>/dev/null
```

### 4.3 — Commit da consolidação

```bash
cd /mnt/e/Obsidian/Cofre/Hermes
git add -A
git commit -m "OS-006: consolidar pastas duplicadas e orfas — $(ls -d */ | wc -l) pastas raiz restantes"
```

### ✅ TRAVA FASE 4

```bash
ls -d /mnt/e/Obsidian/Cofre/Hermes/*/ | wc -l
```

Registrar o número de pastas raiz antes e depois. Objetivo: reduzir de 33
para menos de 20.

---

## FASE 5 — Restauração dos Scripts da Skill Obsidian

**Objetivo:** restaurar os 10 scripts ausentes usando o backup da OS-004,
ou recriar os essenciais para o protocolo de recall funcionar.

### 5.1 — Verificar o backup da OS-004

```bash
ls ~/.hermes/skills/obsidian/scripts_archived_*/
```

Se o backup existir, restaurar diretamente:

```bash
BACKUP=$(ls -d ~/.hermes/skills/obsidian/scripts_archived_*/ | tail -1)
echo "Backup encontrado: $BACKUP"
ls "$BACKUP"
```

### 5.2 — Restaurar scripts do backup (se disponível)

```bash
BACKUP=$(ls -d ~/.hermes/skills/obsidian/scripts_archived_*/ | tail -1)
mkdir -p ~/.hermes/skills/obsidian/scripts

# Copiar apenas os scripts funcionais (excluindo os 3 com syntax error conhecidos)
for script in search_vault.py vault_check.py search_semantic.py \
              append_note.py list_notes.py reindex_vault.py; do
  if [ -f "$BACKUP/$script" ]; then
    cp "$BACKUP/$script" ~/.hermes/skills/obsidian/scripts/
    python3 -m py_compile ~/.hermes/skills/obsidian/scripts/$script 2>&1 \
      && echo "OK: $script" || echo "ERRO SINTAXE: $script"
  else
    echo "AUSENTE no backup: $script"
  fi
done
```

### 5.3 — Verificar e corrigir syntax errors conhecidos

Para cada script com erro de sintaxe (link_notes.py, populate_vault_from_sessions.py,
show_backlinks.py), ler o erro e corrigir:

```bash
for script in link_notes.py populate_vault_from_sessions.py show_backlinks.py; do
  if [ -f "$BACKUP/$script" ]; then
    echo "=== $script ==="
    python3 -m py_compile "$BACKUP/$script" 2>&1
    echo "Linhas próximas ao erro:"
    # Ler a linha do erro e contexto
  fi
done
```

Corrigir o syntax error de cada um (try/except mal formado, indentation)
e instalar a versão corrigida.

### 5.4 — Testar os scripts restaurados

```bash
# Teste do script mais crítico para o protocolo de recall
python3 ~/.hermes/skills/obsidian/scripts/search_vault.py \
  "protocolo recall" --combined 2>&1 | head -20

# Teste do vault_check
python3 ~/.hermes/skills/obsidian/scripts/vault_check.py \
  --query "OS-006" --threshold 2 2>&1
```

### 5.5 — Atualizar o SKILL.md para referenciar os scripts restaurados

```bash
cat ~/.hermes/skills/obsidian/SKILL.md | grep -n "scripts"
```

Verificar se o SKILL.md está referenciando os scripts corretamente e
atualizar se necessário.

### ✅ TRAVA FASE 5

```bash
for script in search_vault.py vault_check.py append_note.py list_notes.py; do
  python3 -m py_compile ~/.hermes/skills/obsidian/scripts/$script 2>/dev/null \
    && echo "OK: $script" || echo "FALHOU: $script"
done
```

Só avançar se todos os 4 scripts essenciais retornarem OK.

---

## FASE 6 — Restauração do SOUL.md

**Objetivo:** restaurar a regra de autosave e verificar integridade do
protocolo de recall no SOUL.md.

### 6.1 — Auditar o SOUL.md atual

```bash
cat ~/.hermes/SOUL.md
```

Verificar:
- [ ] Existe seção de autosave? Se não, recriar
- [ ] O protocolo de recall referencia search_vault.py corretamente?
- [ ] A seção OBSIDIAN da OS-005 está íntegra?

### 6.2 — Restaurar regra de autosave (se ausente)

Se a regra não existir, adicionar ao SOUL.md após a seção RECALL:

```markdown
## AUTOSAVE: REGRA OBRIGATÓRIA

Após qualquer sessão com 5 ou mais tool calls que produziu:
- Decisão técnica relevante
- Descoberta ou diagnóstico documentado
- Configuração de sistema alterada
- OS executada ou atualizada

OBRIGATÓRIO executar ao final da sessão:
1. fact_store(action="add") — registrar os fatos principais no Holographic
2. Criar nota no vault se o conteúdo superar o critério mínimo da seção OBSIDIAN
3. Atualizar daily note com resumo do que foi feito

NUNCA encerrar uma sessão produtiva sem salvar no fact_store.
```

### 6.3 — Corrigir protocolo de recall se necessário

Verificar se a seção RECALL referencia `search_vault.py` como terminal call
ou como tool inexistente no gateway. Se referenciado incorretamente:

```markdown
## RECALL: PROTOCOLO OBRIGATÓRIO

Sequência para qualquer query sobre projetos, memórias ou histórico:

PASSO 1 — fact_store(action="search", query="<termo>")
  Se retornar resultados relevantes → usar. Avançar para passo 2 apenas se vazio.

PASSO 2 — terminal: python3 ~/.hermes/skills/obsidian/scripts/search_vault.py "<termo>" --combined
  Se retornar resultados → usar. Avançar para passo 3 apenas se vazio.

PASSO 3 — session_search(query="<termo>")
  Se retornar resultados → usar. Avançar para passo 4 apenas se vazio.

PASSO 4 — web_search (somente para informações externas)

REGRA INVIOLÁVEL: NUNCA pular do fact_store direto para session_search
sem tentar o vault. O vault é a segunda fonte obrigatória.
```

### 6.4 — Verificar e commitar

```bash
# Verificar integridade
grep -c "AUTOSAVE\|RECALL\|OBSIDIAN" ~/.hermes/SOUL.md

# Backup antes de qualquer edição
cp ~/.hermes/SOUL.md ~/.hermes/SOUL_pre_os006_$(date +%Y-%m-%d).md
```

### ✅ TRAVA FASE 6

```bash
grep -c "AUTOSAVE: REGRA OBRIGATÓRIA\|RECALL: PROTOCOLO\|OBSIDIAN: PROTOCOLO" ~/.hermes/SOUL.md
```

Só avançar se retornar 3 (todas as três seções presentes).

---

## FASE 7 — Teste de Integração do Protocolo de Recall

**Objetivo:** confirmar que o pipeline completo funciona de ponta a ponta.

### 7.1 — Teste do fact_store

```bash
# Buscar um fato que deve existir
hermes -c "fact_store search: integração SQLite Obsidian" 2>/dev/null | head -20
```

### 7.2 — Teste do search_vault via terminal

```bash
python3 ~/.hermes/skills/obsidian/scripts/search_vault.py \
  "OS-003 diagnóstico protocolo recall" --combined 2>&1 | head -30
```

### 7.3 — Teste do protocolo completo em sessão real

Iniciar uma nova sessão do Hermes e perguntar:
```
"O que foi feito na OS-003?"
```

Verificar a sequência de tool calls:
- [ ] Primeira call: `fact_store`
- [ ] Segunda call (se necessário): `terminal > search_vault.py`
- [ ] Terceira call (se necessário): `session_search`
- [ ] `web_search` NÃO foi chamado para essa query

### ✅ TRAVA FASE 7

O protocolo de recall está funcionando se:
1. `search_vault.py` executa sem erro
2. A sessão de teste usou fact_store como primeira call
3. O vault foi consultado antes de session_search

---

## FASE 8 — Commit Final e Relatório

**Objetivo:** documentar tudo, atualizar memórias, encerrar a OS.

### 8.1 — Commit final do vault

```bash
cd /mnt/e/Obsidian/Cofre/Hermes
git add -A
git status
git commit -m "OS-006: restauração completa — vault profissionalizado"
git log --oneline | head -10
```

### 8.2 — Redigir relatório final

Salvar em `Hermes/OS/Concluidas/Relatorio_OS-006_$(date +%Y-%m-%d).md`:

```markdown
---
title: "Relatório OS-006 — Restauração Hermes-Obsidian"
date: YYYY-MM-DD
tags: os-006, obsidian, restauração, recall, soul, scripts
---

# Relatório OS-006

## Resumo Executivo
[1 parágrafo descrevendo o estado antes e depois]

## Resultados por Fase

| Fase | Descrição | Status | Detalhes |
|------|-----------|--------|----------|
| 1 | Git inicializado | ✅/❌ | [commits criados] |
| 2 | Spam removido | ✅/❌ | [N notas deletadas] |
| 3 | Nomenclatura normalizada | ✅/❌ | [N arquivos renomeados] |
| 4 | Pastas consolidadas | ✅/❌ | [33 → N pastas raiz] |
| 5 | Scripts restaurados | ✅/❌ | [N/10 scripts funcionais] |
| 6 | SOUL.md restaurado | ✅/❌ | [seções presentes] |
| 7 | Protocolo de recall | ✅/❌ | [sequência testada] |

## Problemas Não Resolvidos
[Se alguma fase falhou, documentar aqui com causa]

## Estado Final do Vault
- Total de notas: [N]
- Pastas raiz: [N]
- Scripts funcionais: [N/12]
- Git commits: [N]

## Memórias Atualizadas
- fact_store: SIM/NÃO
- Daily note: SIM/NÃO

## Próximas Recomendações
[O que ainda pode ser melhorado]

---
*Executor: Hermes | Solicitante: Christian | OS-006*
```

### 8.3 — Atualizar memórias no Holographic

```
fact_store(action="add"):
  "OS-006 concluída em [data]. Vault Obsidian profissionalizado: git inicializado,
  spam removido, nomenclatura normalizada, pastas consolidadas, scripts restaurados,
  SOUL.md com autosave e recall corretos. Protocolo de recall testado e funcional.
  Estado: [N] notas, [N] pastas raiz, [N/12] scripts funcionais."
```

### 8.4 — Atualizar daily note

```bash
python3 ~/.hermes/skills/obsidian/scripts/daily_note.py \
  --append "OS-006 concluída: vault Obsidian profissionalizado em 8 fases."
```

### 8.5 — Mover OS para Concluídas

```bash
VAULT="/mnt/e/Obsidian/Cofre/Hermes"
mv "$VAULT/OS/Ativas/OS-006_Restauracao_Hermes_Obsidian.md" \
   "$VAULT/OS/Concluidas/" 2>/dev/null && echo "OS-006 arquivada em Concluidas"
```

### ✅ TRAVA FASE 8 — ENCERRAMENTO

Confirmar ao Christian:
1. Caminho do relatório final no vault
2. Número de commits git criados
3. Estado final: N notas, N pastas raiz, N scripts funcionais
4. Protocolo de recall: FUNCIONAL ou PARCIAL (com detalhes)

---

## Checklist Final

- [ ] Fase 1 — Git inicializado com snapshot inicial
- [ ] Fase 2 — Spam residual zerado
- [ ] Fase 3 — Nenhum arquivo/pasta com acento
- [ ] Fase 4 — Pastas duplicadas consolidadas (meta: < 20 raiz)
- [ ] Fase 5 — Scripts essenciais restaurados e funcionais
- [ ] Fase 6 — SOUL.md com autosave + recall + obsidian (3 seções)
- [ ] Fase 7 — Protocolo de recall testado end-to-end
- [ ] Fase 8 — Relatório salvo, fact_store atualizado, OS arquivada
- [ ] Christian informado do resultado completo

---

## Estado Esperado Após Esta OS

| Item | Antes | Depois |
|------|-------|--------|
| Controle de versão | Nenhum | Git com histórico completo |
| Spam no vault | 22 notas | 0 notas |
| Arquivos com acentos | 19+ | 0 |
| Pastas raiz | 33 | < 20 |
| Scripts funcionais | 2/12 | 10+/12 |
| Protocolo de recall | Quebrado | Funcional |
| Autosave no SOUL.md | Ausente | Presente e ativo |

---

*OS emitida em 2026-04-25 | Solicitante: Christian | Agente executor: Hermes*
*Prerequisitos: OS-003, OS-004, OS-005 concluídas*
*Versão: 1.0*
