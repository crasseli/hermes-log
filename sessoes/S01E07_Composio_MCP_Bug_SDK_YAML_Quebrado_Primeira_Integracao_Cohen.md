# S01E07 — Composio MCP: Bug do SDK, YAML Quebrado e a Primeira Integração do Cohen

**Data:** 2026-04-30  
**Autoria:** Christian Rasseli, Hermes (agente no notebook DELL)  
**Status:** RESOLVIDO  

---

## Resumo

O Cohen (Hermes Agent v0.12.0 no M70q) não conseguia conectar ao MCP server do Composio (`https://connect.composio.dev/mcp`). A sessão de diagnóstico revelou três problemas encadeados: um bug estrutural no código do Hermes, um YAML malformatado no config do Cohen, e cache de bytecode stale. Após corrigir os três, o Composio subiu com 11 ferramentas registradas.

---

## Contexto

O Composio é uma plataforma de integração que conecta agentes de IA a mais de 1.000 aplicações via protocolo MCP. O Christian configurou o MCP server do Composio no `config.yaml` do Cohen, mas a conexão falhava sistematicamente desde a primeira tentativa.

---

## Diagnóstico — Sequência de Erros

### Erro 1: `name 'StdioServerParameters' is not defined`

**Horário:** ~16:46  
**Sintoma:** O Hermes tentava conectar o Composio como servidor stdio via `npx`, mas o Composio é HTTP-only.  
**Causa:** Config inicial do Cohen usava `command: npx` em vez de `url:`, tratando um servidor HTTP como stdio.

### Erro 2: `streamable_http is not available`

**Horário:** ~19:05  
**Sintoma:** Após corrigir a config para usar `url:`, o gateway informava que o módulo `mcp.client.streamable_http` não estava disponível.  
**Causa:** `__pycache__` stale com `_MCP_HTTP_AVAILABLE = False` cacheado de versão anterior do SDK. O flag era lido do bytecode compilado em vez de reavaliar o import.  
**Resolução:** Limpeza de `__pycache__` em `~/.hermes/hermes-agent/tools/`. Após limpar, o import funcionou e `_MCP_HTTP_AVAILABLE` passou a `True`.

### Erro 3: `unhandled errors in a TaskGroup (1 sub-exception)` → `401 Unauthorized`

**Horário:** ~19:01 em diante (persistiu por toda a sessão)  
**Sintoma:** A conexão HTTP era estabelecida, mas o Composio retornava 401 Unauthorized. O erro era empacotado como `ExceptionGroup` (TaskGroup), mascarando a causa real.  
**Causa raiz (dupla):**

1. **Bug estrutural no `mcp_tool.py`:** O branch `_MCP_NEW_HTTP` usava `streamable_http_client(url, http_client=http_client)` — a API deprecated do SDK MCP. Na versão 1.27.0 do SDK, essa função internamente chama `httpx_client_factory(headers=..., timeout=..., auth=...)`, mas a factory que o Hermes criava era `def _custom_client_factory() -> httpx.AsyncClient` **sem parâmetros**, causando `TypeError: got an unexpected keyword argument 'headers'`. Esse TypeError era capturado como sub-exception de um TaskGroup, ocultando a mensagem real.

2. **YAML malformatado no config:** `x-consumer-api-key` estava no mesmo nível de indentação que `headers:`, resultando em `headers: None` e a chave API como chave irmã de `headers`. O Hermes não encontrava a chave de autenticação no lugar esperado, gerando 401.

---

## Patch Aplicado

**Arquivo:** `~/.hermes/hermes-agent/tools/mcp_tool.py` (Cohen/M70q)  
**Backup:** `mcp_tool.py.bak` no mesmo diretório

### Bloco substituído (linhas ~1208-1228)

O bloco original construía um `httpx.AsyncClient` custom e o passava como `http_client=` para `streamable_http_client()`:

```python
# ANTES (quebrado)
# Caller owns the client lifecycle — the SDK skips cleanup when
# http_client is provided, so we wrap in async-with.
async with httpx.AsyncClient(**client_kwargs) as http_client:
    async with streamable_http_client(url, http_client=http_client) as (
        read_stream, write_stream, _get_session_id,
    ):
```

### Bloco novo (linhas ~1208-1256)

O bloco novo usa `streamablehttp_client` (API nova do SDK) com `httpx_client_factory` custom que aceita os parâmetros que o SDK passa internamente:

```python
# DEPOIS (corrigido)
_base_client_kwargs = {
    k: v for k, v in client_kwargs.items()
    if k not in ("headers", "timeout", "auth")  # SDK provides these via factory args
}

def _custom_client_factory(
    headers: dict | None = None,
    timeout: "httpx.Timeout" = None,
    auth: "httpx.Auth" = None,
) -> httpx.AsyncClient:
    merged = dict(_base_client_kwargs)
    if headers:
        merged["headers"] = headers
    if timeout is not None:
        merged["timeout"] = timeout
    if auth is not None:
        merged["auth"] = auth
    return httpx.AsyncClient(**merged)

_http_kwargs_new: dict = {
    "headers": headers,
    "timeout": float(connect_timeout),
    "sse_read_timeout": 300.0,
    "httpx_client_factory": _custom_client_factory,
}
if _oauth_auth is not None:
    _http_kwargs_new["auth"] = _oauth_auth
async with streamablehttp_client(url, **_http_kwargs_new) as (
    read_stream, write_stream, _get_session_id,
):
```

**Por que funciona:** A função `streamablehttp_client` (deprecated wrapper no SDK 1.27.0) internamente chama `httpx_client_factory(headers=headers, timeout=..., auth=...)`. Nossa factory custom aceita esses parâmetros e faz merge com as configs customizadas do Hermes (follow_redirects, ssl_verify, event_hooks de cross-origin auth stripping).

### Correção do YAML

```yaml
# ANTES (quebrado — chave no nível errado)
composio:
  url: "https://connect.composio.dev/mcp"
  headers:
  x-consumer-api-key: "ck_..."

# DEPOIS (corrigido — chave dentro de headers)
composio:
  url: "https://connect.composio.dev/mcp"
  headers:
    x-consumer-api-key: "ck_..."
```

A indentação de `x-consumer-api-key` precisava ter 2 espaços a mais que `headers:` para ser interpretada como valor dentro dele, não como chave irmã.

---

## Resultado

Após aplicar o patch e corrigir o YAML:

```
MCP server 'composio' (HTTP): registered 11 tool(s):
  mcp_composio_COMPOSIO_MANAGE_CONNECTIONS
  mcp_composio_COMPOSIO_MULTI_EXECUTE_TOOL
  mcp_composio_COMPOSIO_REMOTE_BASH_TOOL
  mcp_composio_COMPOSIO_REMOTE_WORKBENCH
  mcp_composio_COMPOSIO_SEARCH_TOOLS
  mcp_composio_COMPOSIO_WAIT_FOR_CONNECTIONS
  mcp_composio_COMPOSIO_GET_TOOL_SCHEMAS
  mcp_composio_list_resources
  mcp_composio_read_resource
  mcp_composio_list_prompts
  mcp_composio_get_prompt
```

**Total: 32 ferramentas de 4 servidores MCP** (composio + sequential-thinking + sqlite + time). Canva e filesystem falharam por problemas separados (não relacionados ao Composio).

---

## Lições Aprendidas

1. **SDK MCP 1.27.0 — Mudança de API:** A função `streamable_http_client` (deprecated) internamente chama `httpx_client_factory(headers=..., timeout=..., auth=...)`. Qualquer factory custom DEVE aceitar esses parâmetros. O código do Hermes assumia que a factory era chamada sem argumentos — isso era verdade em versões antigas do SDK, mas quebrou na 1.27.0.

2. **TaskGroup mascara erros:** `ExceptionGroup` no Python 3.11 empacota sub-exceptions de tarefas concorrentes. O TypeError real (`got an unexpected keyword argument 'headers'`) ficava escondido dentro do TaskGroup, dificultando o diagnóstico. Sempre extrair as sub-exceptions com `hasattr(e, 'exceptions')`.

3. **YAML indentation:** Headers HTTP com chaves customizadas (como `x-consumer-api-key`) devem estar indentados sob a chave `headers:`, não no mesmo nível. O YAML interpreta chaves no mesmo nível como irmãs, não como filhas.

4. **`__pycache__` stale:** Após atualizar o Hermes (`hermes update`), sempre limpar cache de bytecode para evitar flags como `_MCP_HTTP_AVAILABLE = False` persistindo de versões anteriores do código.

5. **Segurança — Nunca expor credenciais:** NUNCA trazer output de `grep`/`cat`/`read_file` em configs remotos sem pipe `sed` para mascarar chaves API. Esta sessão teve três violações dessa regra — todas corrigidas, mas o padrão precisa ser automático.

---

## Pendências

- [ ] Avaliar se o mesmo patch precisa ser aplicado no Hermes DELL (notebook)
- [ ] Investigar falha do MCP filesystem no Cohen (`unhandled errors in a TaskGroup`)
- [ ] Investigar falha do MCP canva no Cohen (`CancelledError`)
- [ ] Reportar o bug do `_MCP_NEW_HTTP` no repositório NousResearch/hermes-agent
