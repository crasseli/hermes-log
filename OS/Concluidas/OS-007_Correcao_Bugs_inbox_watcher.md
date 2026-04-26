---
title: "OS-007 — Correção de Bugs: inbox_watcher.py"
date: 2026-04-26
tipo: ordem-de-servico
prioridade: alta
status: pendente-execução
agente: Hermes
solicitante: Christian
vault_destino: Hermes/OS/Ativas/
tags:
  - os-007
  - bug
  - inbox-watcher
  - race-condition
  - notify-alert
  - powershell
referencias:
  - Relatório de Diagnóstico GLM-5.1 de 25/04/2026
  - inbox_watcher.py
  - notify_alert.sh
---

# OS-007 — Correção de Bugs: inbox_watcher.py

> **LEIA ANTES DE EXECUTAR**: Esta OS corrige dois bugs confirmados pelo
> diagnóstico de 25/04/2026. As causas raiz estão documentadas — não
> investigue novamente, corrija diretamente. Cada fase tem trava obrigatória.
> Nenhuma alteração sem backup confirmado.

---

## Contexto

Diagnóstico concluído em 25/04/2026 identificou dois bugs no sistema
de automação de inbox:

**Bug 1 — Race Condition em `update_daily_summary()`**
- Arquivo: `~/.hermes/scripts/inbox_watcher.py` linhas 62-68
- Padrão TOCTOU: read-then-write sem lock
- Evidência: teste com 5 processos simultâneos → contador final = 1 (perdeu 4)
- Impacto: contadores do `inbox_daily_summary.json` subestimados silenciosamente

**Bug 2 — Falha Silenciosa de Notificações por Aspas Simples**
- Arquivo: `~/.hermes/scripts/notify_alert.sh` linha 14
- Causa: aspas simples no PowerShell quebram quando `filename` contém `'`
- Evidência: `TerminatorExpectedAtEndOfString` no PS, engolido por `2>/dev/null &`
- Impacto: toasts não aparecem para arquivos com apóstrofo no nome

---

## FASE 1 — Backup

### 1.1 — Fazer backup dos arquivos antes de qualquer alteração

```bash
BACKUP_DIR=~/.hermes/backups/os007_$(date +%Y-%m-%d)
mkdir -p "$BACKUP_DIR"
cp ~/.hermes/scripts/inbox_watcher.py "$BACKUP_DIR/inbox_watcher.py.bak"
cp ~/.hermes/scripts/notify_alert.sh "$BACKUP_DIR/notify_alert.sh.bak"
echo "Backups criados em: $BACKUP_DIR"
ls -lh "$BACKUP_DIR"
```

### ✅ TRAVA FASE 1

```bash
ls -lh ~/.hermes/backups/os007_*/
```

Só avançar se os dois arquivos `.bak` existirem com tamanho > 0.

---

## FASE 2 — Correção do Bug 1: Race Condition

**Objetivo**: proteger `update_daily_summary()` com `filelock` para eliminar
o padrão TOCTOU. Leitura e escrita do JSON devem ser atômicas.

### 2.1 — Verificar se `filelock` está disponível

```bash
python3 -c "import filelock; print('filelock OK:', filelock.__version__)" 2>/dev/null \
  || pip3 install filelock --break-system-packages --quiet && echo "filelock instalado"
```

### 2.2 — Localizar as linhas exatas da função

```bash
grep -n "def update_daily_summary\|def check_daily_summary\|DAILY_SUMMARY_DB" \
  ~/.hermes/scripts/inbox_watcher.py | head -20
```

### 2.3 — Aplicar a correção

Adicionar import do `filelock` no topo do arquivo (após os imports existentes):

```python
from filelock import FileLock
```

Substituir a função `update_daily_summary()` atual pela versão com lock:

```python
def update_daily_summary(status: str):
    """Atualiza o resumo diário com lock para evitar race condition."""
    today = datetime.now().strftime('%Y-%m-%d')
    lock_path = str(DAILY_SUMMARY_DB) + ".lock"
    try:
        with FileLock(lock_path, timeout=5):
            db = {}
            if DAILY_SUMMARY_DB.exists():
                try:
                    db = json.loads(DAILY_SUMMARY_DB.read_text())
                except json.JSONDecodeError:
                    log("WARN", "inbox_daily_summary.json corrompido — reiniciando")
                    db = {}
            if today not in db:
                db[today] = {'processed': 0, 'errors': 0,
                             'unrecognized': 0, 'notified': False}
            if status in db[today]:
                db[today][status] += 1
            DAILY_SUMMARY_DB.parent.mkdir(parents=True, exist_ok=True)
            DAILY_SUMMARY_DB.write_text(json.dumps(db, indent=2))
    except Exception as e:
        log("WARN", f"Erro ao atualizar summary: {e}")
```

### 2.4 — Validar sintaxe após edição

```bash
python3 -m py_compile ~/.hermes/scripts/inbox_watcher.py \
  && echo "SINTAXE OK" || echo "ERRO DE SINTAXE"
```

### 2.5 — Reproduzir o teste de concorrência para confirmar correção

```bash
cat > /tmp/test_fix_race.py << 'EOF'
import multiprocessing, json, sys
from pathlib import Path
from datetime import datetime
sys.path.insert(0, str(Path.home() / '.hermes/scripts'))

from filelock import FileLock

DAILY_SUMMARY_DB = Path.home() / '.hermes/logs/inbox_daily_summary.json'

def update_summary_fixed(status):
    today = datetime.now().strftime('%Y-%m-%d')
    lock_path = str(DAILY_SUMMARY_DB) + ".lock"
    try:
        with FileLock(lock_path, timeout=5):
            db = {}
            if DAILY_SUMMARY_DB.exists():
                db = json.loads(DAILY_SUMMARY_DB.read_text())
            if today not in db:
                db[today] = {'processed': 0, 'errors': 0,
                             'unrecognized': 0, 'notified': False}
            if status in db[today]:
                db[today][status] += 1
            DAILY_SUMMARY_DB.write_text(json.dumps(db, indent=2))
        return "OK"
    except Exception as e:
        return f"ERRO: {e}"

# Reset
DAILY_SUMMARY_DB.write_text(json.dumps(
    {"2026-04-26": {"processed": 0, "errors": 0,
                    "unrecognized": 0, "notified": False}}, indent=2))

with multiprocessing.Pool(5) as pool:
    results = pool.map(update_summary_fixed, ['processed'] * 5)

db = json.loads(DAILY_SUMMARY_DB.read_text())
count = db['2026-04-26']['processed']
print(f"Resultados: {results}")
print(f"Contador final: {count} | Esperado: 5 | Perda: {5 - count}")
print("BUG 1 CORRIGIDO" if count == 5 else "BUG 1 AINDA PRESENTE")
EOF
python3 /tmp/test_fix_race.py
```

### ✅ TRAVA FASE 2

Só avançar se o teste retornar `Contador final: 5` e `BUG 1 CORRIGIDO`.

---

## FASE 3 — Correção do Bug 2: Aspas Simples nas Notificações

**Objetivo**: sanitizar `$TITLE` e `$MESSAGE` em `notify_alert.sh` para
escapar aspas simples antes de passar ao PowerShell.

### 3.1 — Ler o script atual completo

```bash
cat -n ~/.hermes/scripts/notify_alert.sh
```

### 3.2 — Aplicar a correção

Substituir a linha 14 do `notify_alert.sh` que monta o comando PowerShell.

**Antes (linha 14 — problemática):**
```bash
powershell.exe -Command "New-BurntToastNotification -Text '$TITLE', '$MESSAGE' -Sound '$SOUND'" 2>/dev/null &
```

**Depois — com sanitização e tratamento de erro:**
```bash
# Escapar aspas simples: ' → '' (convenção PowerShell)
SAFE_TITLE="${TITLE//\'/\'\'}"
SAFE_MESSAGE="${MESSAGE//\'/\'\'}"

# Rodar em foreground para capturar erro real, redirecionar para log
PS_RESULT=$(powershell.exe -Command \
  "New-BurntToastNotification -Text '$SAFE_TITLE', '$SAFE_MESSAGE' -Sound '$SOUND'" \
  2>&1)
PS_EXIT=$?

if [ $PS_EXIT -ne 0 ]; then
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] [WARN] Toast falhou (exit $PS_EXIT): $PS_RESULT" \
    >> ~/.hermes/logs/notify_alert.log
fi
```

### 3.3 — Validar sintaxe do shell script

```bash
bash -n ~/.hermes/scripts/notify_alert.sh && echo "SINTAXE OK" || echo "ERRO DE SINTAXE"
```

### 3.4 — Testar os casos que anteriormente falhavam

```bash
echo "=== Teste 1: apóstrofo no filename ==="
bash ~/.hermes/scripts/notify_alert.sh \
  "Hermes Inbox" "Christian's documento.pdf → Tecnologia/" "normal"
echo "EXIT=$?"

echo ""
echo "=== Teste 2: múltiplos apóstrofos ==="
bash ~/.hermes/scripts/notify_alert.sh \
  "Hermes" "D'água da it's company.pdf → Erros/" "critical"
echo "EXIT=$?"

echo ""
echo "=== Teste 3: mensagem limpa (sem apóstrofo) ==="
bash ~/.hermes/scripts/notify_alert.sh \
  "Hermes Inbox" "relatorio_2026.pdf → Tecnologia/" "normal"
echo "EXIT=$?"

echo ""
echo "=== Verificar log de erros ==="
cat ~/.hermes/logs/notify_alert.log 2>/dev/null || echo "Nenhum erro registrado"
```

### 3.5 — Verificar se `notify_alert.sh` tem a chamada correta no `inbox_watcher.py`

```bash
grep -n "send_notification\|notify_alert\|subprocess" \
  ~/.hermes/scripts/inbox_watcher.py | head -20
```

Confirmar que `capture_output=True` ainda funciona corretamente com a nova versão
do script (que agora não roda em background com `&`).

Se necessário, ajustar o timeout do `subprocess.run` em `inbox_watcher.py`
de 5s para 10s para acomodar o tempo de resposta do PowerShell:

```python
subprocess.run(
    ["bash", str(NOTIFY_SCRIPT), title, message, urgency],
    capture_output=True,
    timeout=10  # era 5
)
```

### ✅ TRAVA FASE 3

Os três testes devem retornar `EXIT=0` e os toasts devem aparecer no Windows.
Se qualquer teste falhar, verificar `~/.hermes/logs/notify_alert.log`.

---

## FASE 4 — Teste de Integração Real

**Objetivo**: confirmar que o watcher inteiro funciona com os dois bugs corrigidos.

### 4.1 — Verificar se o watcher está rodando

```bash
ps aux | grep inbox_watcher | grep -v grep
```

### 4.2 — Criar um arquivo de teste na pasta Inbox

```bash
INBOX_PATH=$(grep -i "inbox\|watch_path\|WATCH" ~/.hermes/scripts/inbox_watcher.py \
  | grep "Path\|=.*/" | head -3)
echo "Paths configurados: $INBOX_PATH"

# Identificar o caminho real do Inbox
grep -n "INBOX\|inbox_path\|watch_dir\|WATCH_DIR" \
  ~/.hermes/scripts/inbox_watcher.py | head -10
```

### 4.3 — Copiar arquivo de teste com apóstrofo no nome

```bash
# Substituir <INBOX_PATH> pelo caminho real encontrado no passo anterior
INBOX=$(grep -oP "(?<=INBOX_PATH = Path\()['\"].*?['\"]" \
  ~/.hermes/scripts/inbox_watcher.py | tr -d "'\"" | head -1)
echo "Inbox: $INBOX"

# Criar PDF de teste
echo "Teste de integracao OS-007" > "/tmp/Christian's_teste_os007.txt"
cp "/tmp/Christian's_teste_os007.txt" "$INBOX/" 2>/dev/null \
  && echo "Arquivo copiado para inbox" \
  || echo "Copiar manualmente para: $INBOX"
```

### 4.4 — Monitorar logs por 30 segundos

```bash
timeout 30 tail -f ~/.hermes/logs/inbox_watcher.log 2>/dev/null \
  || tail -20 ~/.hermes/logs/inbox_watcher.log
```

### 4.5 — Verificar o summary após processamento

```bash
python3 -c "
import json
from pathlib import Path
db = Path.home() / '.hermes/logs/inbox_daily_summary.json'
if db.exists():
    print(json.dumps(json.loads(db.read_text()), indent=2))
else:
    print('Arquivo não existe ainda')
"
```

### ✅ TRAVA FASE 4

Confirmar:
- [ ] Watcher processou o arquivo de teste
- [ ] Toast apareceu no Windows (mesmo com apóstrofo no nome)
- [ ] Summary foi atualizado com contador correto
- [ ] Nenhum erro nos logs

---

## FASE 5 — Documentação e Encerramento

### 5.1 — Salvar relatório no vault

```bash
VAULT="/mnt/e/Obsidian/Cofre/Hermes"
cat > "$VAULT/OS/Concluidas/Relatorio_OS-007_$(date +%Y-%m-%d).md" << 'EOF'
---
title: "Relatório OS-007 — Correção Bugs inbox_watcher"
date: 2026-04-26
tags: os-007, bug, inbox-watcher, race-condition, notify-alert
---

# Relatório OS-007

## Bug 1 — Race Condition
- Arquivo: inbox_watcher.py linhas 62-68
- Correção: FileLock em update_daily_summary()
- Teste: 5/5 incrementos preservados
- Status: [CORRIGIDO/FALHOU]

## Bug 2 — Aspas Simples nas Notificações
- Arquivo: notify_alert.sh linha 14
- Correção: sanitização TITLE/MESSAGE + log de erros
- Teste: EXIT=0 com apóstrofo no filename
- Status: [CORRIGIDO/FALHOU]

## Teste de Integração
- Arquivo com apóstrofo processado: SIM/NÃO
- Toast apareceu: SIM/NÃO
- Summary atualizado: SIM/NÃO

## Status Final
Ambos os bugs corrigidos: SIM/NÃO
Backups em: ~/.hermes/backups/os007_YYYY-MM-DD/
Solicitante: Christian | Executor: Hermes
EOF
```

### 5.2 — Commit no git do vault

```bash
cd /mnt/e/Obsidian/Cofre/Hermes
git add OS/Concluidas/Relatorio_OS-007_*.md
git commit -m "OS-007: correção bugs inbox_watcher — race condition e aspas simples"
```

### 5.3 — Registrar no Holographic

```
fact_store(action="add"):
  "OS-007 concluída em [data]. Bug 1 corrigido: race condition em
  update_daily_summary() resolvida com FileLock (filelock lib).
  Bug 2 corrigido: aspas simples em notify_alert.sh sanitizadas
  com substituição POSIX antes de passar ao PowerShell."
```

### 5.4 — Mover OS para Concluídas

```bash
VAULT="/mnt/e/Obsidian/Cofre/Hermes"
mv "$VAULT/OS/Ativas/OS-007_Correcao_Bugs_inbox_watcher.md" \
   "$VAULT/OS/Concluidas/" 2>/dev/null && echo "OS-007 arquivada"
```

---

## Checklist Final

- [ ] Fase 1 — Backup dos dois arquivos confirmado
- [ ] Fase 2 — Race condition corrigida com FileLock, teste 5/5
- [ ] Fase 3 — Aspas simples sanitizadas, 3 testes passaram
- [ ] Fase 4 — Teste de integração com arquivo real passou
- [ ] Fase 5 — Relatório salvo, git commit, fact_store atualizado
- [ ] Christian informado do resultado

---

## Resumo das Correções

| Bug | Arquivo | Linha | Correção |
|-----|---------|-------|----------|
| Race condition | inbox_watcher.py | 62-68 | `FileLock` em `update_daily_summary()` |
| Aspas simples | notify_alert.sh | 14 | Sanitização `${VAR//\'/\'\'}` antes do PS |
| Erro silencioso | notify_alert.sh | 15 | Log de erros em `notify_alert.log` |
| Timeout curto | inbox_watcher.py | ~49 | `timeout=10` no subprocess |

---

*OS emitida em 2026-04-26 | Solicitante: Christian | Agente executor: Hermes*
*Prerequisito: Diagnóstico OS-007 de 25/04/2026 concluído*
*Versão: 1.0*
