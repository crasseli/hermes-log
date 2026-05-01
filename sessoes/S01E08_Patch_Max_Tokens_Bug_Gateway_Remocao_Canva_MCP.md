# S01E08 — Patch Max Tokens: Bug do Gateway e Remoção do Canva MCP

**Data:** 2026-05-01
**Duração:** ~4 horas
**Autor:** Christian Rasseli, Hermes (DELL), Cohen (M70q)
**Severidade:** Alto — truncamento silencioso de respostas

---

## Resumo

O `gateway/run.py` do Hermes Agent **não passa** o parâmetro `max_tokens` para o `AIAgent()` nas suas 4 instanciações. A função `_resolve_runtime_agent_kwargs()` retorna apenas credenciais (api_key, base_url, provider, api_mode, command, args, credential_pool) — sem `max_tokens`. Isso fazia com que o fallback hardcoded `or 4096` na linha 8246 do `run_agent.py` limitasse **todas as respostas do gateway a 4096 tokens** (~16KB). O problema era invisível nos logs — o truncamento é silencioso.

A sessão também cobriu: diagnóstico de uso MCP do Cohen, remoção do Canva MCP (desconectado), e a correção do mesmo bug em ambas as instâncias (DELL + M70q).

---

## Diagnóstico

### Estatísticas do Cohen (M70q) — 30/04 a 01/05

| Métrica | Valor |
|---|---|
| Sessões respondidas | 38 |
| Total API calls | 88 |
| Média API calls/sessão | 2.3 |
| Pico API calls/sessão | 7 |
| Média chars/resposta | 1.018 |
| Pico chars/resposta | 4.250 (~1.062 tokens) |
| Média tempo/sessão | 3 min |
| Pico tempo/sessão | 19 min (1.148s) |

### MCP Composio no Cohen

- 11 ferramentas registradas via HTTP (streamablehttp_client)
- YouTube tool acessada via `COMPOSIO_MULTI_EXECUTE_TOOL`
- mcp-stderr.log: 27.216 linhas, 7.946 (29%) de "Long poll timeout" — ruído de OAuth pendente
- Chave API Composio com 401 intermitente (Christian verificando no dashboard)

### Canva MCP

- Desconectado pelo Christian, removido do config
- Causava erros de TaskGroup (conexão remota `mcp-remote@latest`)
- Processos zombie (PID 811, 965, 966) limpos com kill manual
- Redução de overhead: 78 → 54 ferramentas MCP (~3.192 tokens economizados por request)

### Bug Raiz: max_tokens ignorado pelo gateway

```
gateway/run.py: _resolve_runtime_agent_kwargs() 
  → retorna: {api_key, base_url, provider, api_mode, command, args, credential_pool}
  → NÃO inclui: max_tokens

run_agent.py:8246
  → max_tokens=self.max_tokens or 4096  (self.max_tokens é None → usa 4096)
```

O `hermes config set model.max_tokens 32768` grava a chave no `config.yaml`, mas o gateway **ignora completamente**.

---

## Patches Aplicados

### Patch 1 — Injeção de max_tokens no `__init__` (run_agent.py, ~linha 1657-1660)

```python
_agent_cfg = _load_agent_config()
# Patch 2026-05-01: inject max_tokens from config.yaml when not passed explicitly
if self.max_tokens is None:
    self.max_tokens = _agent_cfg.get("model", {}).get("max_tokens")
```

O `_load_agent_config()` já era chamado no `__init__` para ler configs de memory/skills/compression. Aproveitamos o mesmo dict para injetar `max_tokens` quando o parâmetro não foi passado explicitamente.

### Patch 2 — Fallback hardcoded (run_agent.py, ~linha 8246)

```python
# Antes:
max_tokens=self.max_tokens or 4096,
# Depois:
max_tokens=self.max_tokens or 32768,
```

Redundante com o Patch 1, mas garante que mesmo se o `_load_agent_config` falhar silenciosamente, o fallback será 32768 em vez de 4096.

### Instâncias corrigidas

| Instância | Host | Patch 1 | Patch 2 | Status |
|---|---|---|---|---|
| Hermes DELL | notebook | OK | OK | gateway ativo |
| Cohen M70q | homelab | OK | OK | gateway ativo |

---

## Lições Aprendidas

1. **`yaml.dump()` corrompe `config.yaml`** — converte `max_tokens` para `max_token`, reordena chaves, quebra indentação. **Usar `sed -i` ou Python com `str.replace()`.**
2. **`patch` tool e `mcp_filesystem_edit_file` destroem indentação em `.py`** — stripam tabs/espaços. O **único método seguro**: Python inline lendo `repr()` das linhas reais e fazendo `str.replace()`.
3. **Se falhar, `git checkout HEAD -- arquivo.py`** antes de retry.
4. **O gateway lê `config.yaml` via `_load_gateway_config()`** que retorna o YAML inteiro como dict, mas **NÃO repassa `model.max_tokens`** para o AIAgent.

---

## Bug Report Upstream

**Projeto:** NousResearch/hermes-agent
**Problema:** O `gateway/run.py` deveria ler `model.max_tokens` do config e passar para o AIAgent. A função `_resolve_runtime_agent_kwargs()` deveria incluir `max_tokens` no dict retornado, ou o `AIAgent.__init__` deveria ler o config internamente (como faz para memory/skills/compression).

---

## Config Final

```yaml
model:
  max_tokens: 32768  # Agora é lido pelo patch no __init__
```

---

*Próximo episódio: S01E09*
