# S01E19 — Update Hermes 0.21.3 e o traceback do dashboard_procs

**Data:** 20/09/2026
**Autor:** Christian Rasseli (Homelab)
**Agente:** Hermes (DELL Latitude 3400 / Windows 11 Pro 25H2)
**Modelo:** qwen3.8-flash

---

## Resumo

`hermes update --force` levou o agente de 0.21.2 → 0.21.3 (~5000 commits puxados) e colou todas as etapas — deps, node, build do web UI, sync de skills, migracao de config v42→v45 — mas derrubou no ultimo passo de manutencao com `TypeError: _find_stale_dashboard_pids() got an unexpected keyword argument 'scope_home'`. A sessao diagnosticou o traceback como conflito bytecode-fonte no filho pos-swap, confirmou o dano real (gateway servindo codigo velho em memoria), executou o restart manual, validou o fleet inteiro e descobriu — pela auditoria dos receipts de update — que o backup pre-update esta desativado.

---

## 1. Contexto

Update manual no Windows com gateway rodando via Scheduled Task (`Hermes_Gateway`). O updater para o gateway, faz o swap de codigo, re-executa as etapas finais num interprete filho limpo (`update_handoff`) e termina com restart/verify da frota + limpeza de processos dashboard obsoletos. O comando colou ate o fim e imprimiu `✓ Update complete! (v0.21.2 → v0.21.3) [main @ d39caf45a0]` — e logo depois o traceback.

## 2. Diagnostico do traceback

```
File "...hermes_cli/dashboard_procs.py", line 584, in _kill_stale_dashboard_processes
    pids = _dash._find_stale_dashboard_pids(exclude_pids=..., scope_home=...)
TypeError: _find_stale_dashboard_pids() got an unexpected keyword argument 'scope_home'
```

Tres linhas de evidencia:

1. **A fonte nova aceita `scope_home`.** `main_dashboard.py:21-22` (arvore em disco, pos-pull) define a funcao com o parametro keyword `scope_home: str | None = None` documentado no docstring.
2. **As linhas do traceback estao desalinhadas com a fonte.** Frames apontando para `sys.stderr = _saved_stderr` e `pass` como se fossem `cmd_update`/`_apply_pulled_update` — assinatura clasica de `.pyc` obsoleto sendo executado contra fonte nova (o traceback resolve as linhas pelo fonte em disco, mas executa o bytecode em memoria).
3. **Local do crash:** etapa de restart/verify da frota (`update_cmd_fleet._verify_fleet_after_update` → `_finish_dashboard_update_cleanup`). Por ele ter estourado ali, o restart automatico do gateway nao aconteceu — o PID antigo (7352, 06:59) seguiu servindo Telegram com 0.21.2 em `sys.modules`.

Conclusao: bug de corrida do updater Windows (limpeza de `__pycache__` nao alcanca o interpretador filho que herdou a arvore trocada). Intermitente — os dois updates seguintes rodaram limpos.

## 3. A pegadinha dos stamps de versao

`gateway_state.json` do PID 7352 carimbava `code_version: 0.21.3` / `code_sha: d39caf45` — **falso**: os stamps sao lidos do checkout em disco, nao do codigo importado no processo. Regra pratica: para saber a versao real de um processo, compare StartTime do PID com o horario do update, ou confira o carimbo no log de boot do gateway.

## 4. Correcao aplicada

```
hermes gateway restart
# ✓ Gateway stopped (drained cleanly)
# ✓ Gateway started via direct spawn (PID 14076)
```

Verificacao: PID novo com StartTime pos-restart, `gateway_state.json` consistente, Telegram `connected`, sem novos frames de erro em `errors.log`.

## 5. Health check do fleet pos-update

| Componente | Estado |
|---|---|
| Gateway + Telegram (PID 1124) | ✅ 0.21.3 / `3dae1f73`, polling saudavel, 60 slash cmds registrados |
| Honcho API :8000 | ✅ `{"status":"ok"}` (PID 10092) |
| Deriver worker | ✅ PID 9628, watchdog `OK` a cada 2 min |
| PostgreSQL :5432 | ✅ TCP aceitando |
| Memurai :6379 | ✅ servico Running (deriver usa fallback in-memory por IPv6 — PIT conhecido) |
| Desktop app | ✅ 5 processos Hermes.exe + 2 backends `serve` |

## 6. Auditoria dos receipts — 3 updates, nao 1

Reflog + `logs/update_receipts/` mostraram que, alem do update colado pelo operador, rodaram mais dois: 07:11 (`1ec61e4d`) e 07:21 (`3dae1f73`, argv `--yes --gateway --force` — **auto-update do desktop app**), este com `outcome: success` e gateway reiniciado corretamente (PID 1124). Isso explicou o "salto de PID" observado entre as verificações.

Achado lateral do ultimo receipt:

```
"skips": [{ "name": "pre_update_backup", "reason": "disabled by updates.pre_update_backup (mode: off)" }]
```

O script `pre-update-backup.ps1` (Robocopy de config.yaml, .env, auth.json, SOUL.md, honcho.json, gateway_state, channel_directory, memories/) **nao rodou**. Suspeita: desligado durante a migracao de schema v42→v45. Pendencia registrada.

## Resultado Final

| Item | Valor |
|---|---|
| Versao final | 0.21.3 @ `3dae1f73` (alinhado disco/memoria) |
| Gates de atualizacao | 3 updates no dia, todos colados |
| Dano do traceback | nenhum permanente (restart manual resolveu) |
| Bugs identificados | `.pyc` stale no limpo dashboard_procs (upstream); pre_update_backup off — confirmado como decisao intencional |

---

## Proximos Passos

- [ ] Decidir `gateway.multiplex_profiles`: `hermes gateway migrate --multiplex` ou `config set gateway.multiplex_profiles false`
- [x] `updates.pre_update_backup`: **decidido — manter off de proposito** (backup dos sensiveis fica sob demanda com o script manual `pre-update-backup.ps1`)
- [ ] Reportar upstream o crash do `_kill_stale_dashboard_processes` (keyword `scope_home`)

---

## Metricas da Sessao

- Tool calls estimados: ~15
- Artefatos criados: diario, sessao tecnica, metricas 2026-09, nota vault
- Duracao: ~1 hora
