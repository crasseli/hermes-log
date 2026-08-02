# S01E18 — Upgrade Honcho Server 3.0.11 → 3.0.12

**Data:** 02/08/2026
**Autor:** Christian Rasseli (Homelab)
**Agente:** Hermes (DELL/Windows 11 Pro 25H2)
**Modelo:** DeepSeek V4 Flash (opencode-zen)

---

## Resumo

Upgrade completo e validado do Honcho Server de 3.0.11 para 3.0.12 em `D:\honcho-server`, preservando os 7 patches Windows locais e revalidando o stack end-to-end. Nao e um patch de manutencao simples: 23 commits substantivos (telemetria Langfuse/CloudEvents, Redis cluster, novo `llm/capture.py` +403 linhas, document dedup). Christian decidiu **manter `deepseek-chat`** como modelo LLM de todos os pipelines; embedding permanece `nvidia/nv-embedqa-e5-v5` via NIM. Teste funcional real confirmou a derivacao de conclusao funcionando no v3.0.12.

---

## 1. Contexto

- Christian queria atualizar o Honcho de 3.0.11 para 3.0.12 de forma segura, sem quebrar nada, validar pos-upgrade, e so entao montar material para o hermes-log.
- Gatilho extra: nada de novo para registrar em 02/08 — o upgrade era a unica atualizacao concreta que valia virar conteudo do repositorio.
- O repo local `honcho` tinha **7 arquivos modificados + 4 untracked** (patches Windows de runtime) que NAO podiam ser perdidos no `git checkout v3.0.12`.

---

## 2. Diagnostico Pre-Upgrade

| Item | Resultado |
|------|-----------|
| v3.0.12 | 23 commits substantivos, NAO patch simples |
| Upstream corrige issues Windows? | NAO — gpt-5.4-mini em 5 lugares (era 2), uvloop/embedding intactos |
| Alembic | Nenhuma migracao nova — schema nao muda |
| 7 arquivos patchados | 4 mudaram upstream (config.py, queue_manager.py, embedding_client.py, openai.py) |
| DB head | `e4eba9cfaa6f` (inalterado) |

---

## 3. Execucao

### 3.1 Backup
Backup completo em `D:\honcho-server\upgrade-backup\`: config.toml ×2, .env, honcho.json, 7 .patch, run_api.py, run_api_boot.py, src/rate_limiter.py.

### 3.2 Passos
1. `git stash push -u` (patches preservados)
2. `git checkout v3.0.12` (detached HEAD, commit `5ad22840`)
3. `git apply` dos 7 patches — **todos aplicaram limpos** (interfaces patcheadas sobreviveram no upstream)
4. Remap dos 5 spots de `gpt-5.4-mini` (3 novos + 2 antigos) → `meta/llama-3.3-70b-instruct` (seguranca; config.toml rege os modelos)
5. Restaurar untracked: run_api.py, run_api_boot.py, src/rate_limiter.py
6. `uv sync` → cashews 7.4.4→7.5.0, **honcho-ai 2.1.2→2.2.0**
7. Alembic confirmou DB no head (sem migracao)
8. restart via `start-honcho.ps1`

### 3.3 Pitfalls Windows
- `git apply` exige path Windows `D:/...` — path MSYS `/d/...` falha com o git nativo
- Testes validados via HTTP `/v3` (contrato real) em vez da ABI sync do SDK, que mudou

---

## 4. Validacao Pos-Upgrade (REAL)

- **API health:** `{"status":"ok"}` HTTP 200
- **SDK rodando:** `honcho-ai 2.2.0`
- **Teste funcional end-to-end:** workspace `test_upgrade_v3_0_12` + peer + sessao + mensagem → **conclusao derivada gerada pelo deriver (deepseek-chat)**:
  - *"test_peer prefers using winget to update packages in bulk on Windows 11."*
- **Fila:** 1/1 work units concluidas, 0 pendentes
- **Embedding NIM:** OK (conclusao persistida)
- **DB head:** mantido, sem erros criticos
- Workspace de teste deletado (HTTP 202)

---

## 5. Resultado Final

| Item | Resultado |
|------|-----------|
| Versao | Honcho **v3.0.12** |
| SDK | honcho-ai 2.2.0 |
| Modelos | LLM deepseek-chat, Embedding nv-embedqa-e5-v5 (NIM) |
| DB | PostgreSQL 16 + pgvector, head `e4eba9cfaa6f` |
| Backup | `D:\honcho-server\upgrade-backup\` |
| Downtime | ~1-2min (API PID 7360, Deriver PID 5040) |

---

## 6. Aprendizados

1. `git apply` no Windows precisa de path `D:/...`, nao MSYS `/d/...`
2. SDK 2.2.0 mudou API (`peer.session()` → `peer.sessions()`/`peer.message()`); validar via HTTP /v3
3. API /v3 mensagem exige `messages:[{content, peer_id}]` (4 refinamentos 422)
4. Workspace de teste nao deleta com sessao ativa — apagar sessao antes
5. API local nao tem `/v3/keys` (Feature disabled) — usa placeholder
6. gpt-5.4-mini cresceu de 2 para 5 lugares no upstream — sempre re-grep apos checkout
7. `VECTOR_STORE_DIMENSIONS` deprecated — autoritativo agora `EMBEDDING_VECTOR_DIMENSIONS`

---

## Metricas da Sessao

- Tool calls: ~45
- Artefatos criados: 1 nota MP (Obsidian), diario 02/08, sessao S01E18, metricas 08/08
- Duracao: ~2h

---

*Registrado por Hermes Agent em 02/08/2026.*