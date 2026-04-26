---
title: Update Hermes Agent v0.10.0 → v0.11.0
date: 2026-04-24 02:32:51
updated: 2026-04-24 02:32:51
tags:
  - hermes
  - update
  - v0.11.0
  - backup
  - customizacoes
source: 
related: []
---

## Resumo

Update do Hermes Agent da versão 0.10.0 para 0.11.0 realizado com sucesso em 24/04/2026 02:32.

## Versões

- Versão anterior: v0.10.0 (release 16/04/2026)
- Nova versão: v0.11.0 (release 23/04/2026)
- Tag: v2026.4.23
- Commit: bf196a3fc0fd1f79353369e8732051db275c6276

## Principais Novidades da v0.11.0

### Interface (TUI)
- Nova interface interativa baseada em React/Ink
- Comando: `hermes --tui`
- Backend Python JSON-RPC (`tui_gateway`)
- Suporte a streaming com OSC-52 clipboard
- Barra de status com cronômetro e branch git
- Tema claro disponível
- Overlay de observabilidade para subagentes

### Arquitetura de Transporte
- Nova camada `agent/transports/` com arquitetura plugável
- Transportes: AnthropicTransport, ChatCompletionsTransport, ResponsesApiTransport, BedrockTransport
- Suporte nativo a AWS Bedrock via Converse API

### Novos Provedores de Inferência
1. NVIDIA NIM (nativo)
2. Arcee AI
3. Step Plan
4. Google Gemini CLI OAuth
5. Vercel AI Gateway (com pricing e descoberta dinâmica)

### Outras Melhorias
- Plugin surface expandido
- GPT-5.5 via Codex OAuth
- Suporte a QQBot (17ª plataforma de mensagens)

## Customizações Preservadas

### Injeção Semântica do Vault
A customização de injeção de contexto semântico do Obsidian foi preservada:

- **Arquivo modificado:** `run_agent.py`
- **Localização:** Após prefetch do memory_manager
- **Funcionalidade:** Injeta notas relevantes do vault no contexto quando `HERMES_SEMANTIC_CONTEXT=true`
- **Script utilizado:** `search_semantic.py`

### Scripts do Vault Preservados
Todos os scripts em `~/.hermes/skills/obsidian/scripts/` foram mantidos:
- save_note.py
- daily_note.py
- search_semantic.py
- search_vault.py
- reindex_vault.py
- append_note.py
- E demais scripts de automação

## Backup Realizado

Local: `~/.hermes/backups/hermes-agent-v0.10.0-customizations/`
- Patch da injeção semântica: `run_agent_semantic_injection.patch`
- Scripts do vault: todos os arquivos .py

## Procedimento de Update

1. Stash das modificações locais: `git stash`
2. Fetch das tags: `git fetch --tags`
3. Checkout da nova versão: `git checkout v2026.4.23`
4. Reaplicação do patch: `git apply run_agent_semantic_injection.patch`
5. Verificação de sintaxe: `python3 -m py_compile run_agent.py` ✓

## Verificação Pós-Update

- [x] Versão atualizada: `__version__ = "0.11.0"`
- [x] Sintaxe do run_agent.py validada
- [x] Customizações preservadas
- [x] Scripts do vault intactos

## Referências

- Release Notes: https://github.com/NousResearch/hermes-agent/releases/tag/v2026.4.23
- Backup local: `~/.hermes/backups/hermes-agent-v0.10.0-customizations/`
