---
title: Hermes Agent v0.11.0 - Interface Release
date: 2026-04-24 02:44:57
updated: 2026-04-24 02:44:57
tags:
  - hermes
  - release-notes
  - v0.11.0
  - update
  - tui
  - aws-bedrock
  - plugins
source: 
related: []
---

# Hermes Agent v0.11.0 - "The Interface Release"

**Data de Release:** 23/04/2026  
**Versão Anterior:** v0.10.0 (16/04/2026)  
**Código:** v2026.4.23

---

## Resumo Executivo

A v0.11.0 traz uma reescrita completa da interface CLI em React/Ink, arquitetura de transporte plugável, suporte nativo AWS Bedrock, 5 novos provedores de inferência, e expansão significativa do sistema de plugins.

**Estatísticas desde v0.9.0:**
- 1.556 commits | 761 PRs mergeadas | 1.314 arquivos alterados
- 224.174 inserções | 29 contribuidores (290 incluindo co-autores)

---

## 1. Nova Interface TUI (Terminal User Interface)

```bash
hermes --tui
```

- **Reescrita completa** em React/Ink do CLI interativo
- Backend Python JSON-RPC (`tui_gateway`)
- ~310 commits para `ui-tui/` + `tui_gateway/`

### Recursos:
- Sticky composer (campo de entrada fixo)
- Live streaming com suporte OSC-52 (clipboard)
- Teclas de seleção estáveis
- Status bar com cronômetro por turno e branch git
- Confirmação `/clear`
- Tema claro disponível
- Overlay de observabilidade para subagents

---

## 2. Arquitetura de Transporte Plugável

Nova camada `agent/transports/` extrai conversão de formato e transporte HTTP de `run_agent.py`:

| Transporte | Descrição |
|------------|-----------|
| `AnthropicTransport` | API Messages da Anthropic |
| `ChatCompletionsTransport` | Provedores compatíveis OpenAI |
| `ResponsesApiTransport` | OpenAI Responses API + Codex |
| `BedrockTransport` | **AWS Bedrock Converse API** (novo!) |

**PRs:** #10549, #13347

---

## 3. Novos Provedores de Inferência (5 novos)

1. **NVIDIA NIM** - provider nativo (#11774)
2. **Arcee AI** - provider direto (#9276)
3. **Step Plan** - provider de planejamento (#13893)
4. **Google Gemini CLI OAuth** - autenticação OAuth (#11270)
5. **Vercel ai-gateway** - com preços e descoberta dinâmica (#13223)

**Suporte GPT-5.5:** Via ChatGPT Codex OAuth com descoberta live de modelos (#14720)

---

## 4. Nova Plataforma de Mensageria (17ª plataforma)

**QQBot** - via QQ Official API v2 (#9364):
- QR scan para configuração
- Streaming cursor
- Reações com emoji
- DM/group policy gating

**Plataformas existentes:** Telegram, Discord, Slack, WhatsApp, Signal, Matrix, Email (IMAP/SMTP), SMS (Twilio), DingTalk, Feishu/Lark, WeCom, Mattermost, Home Assistant, Webhooks, iMessage (BlueBubbles), WeChat.

---

## 5. Expansão do Sistema de Plugins

Plugins agora podem:
- Registrar comandos slash (`register_command`)
- Despachar ferramentas diretamente (`dispatch_tool`)
- **Bloquear execução** de ferramentas (`pre_tool_call` pode vetar)
- **Reescrever resultados** de ferramentas (`transform_tool_result`)
- Transformar saída do terminal (`transform_terminal_output`)
- Fornecer backends de geração de imagem
- Adicionar abas personalizadas ao dashboard

**Plugin de exemplo:** `disk-cleanup` (opt-in) incluído como referência.

---

## 6. Novos Comandos

| Comando | Descrição |
|---------|-----------|
| `/steer <prompt>` | Injeta nota que o agent vê após próxima tool call sem interromper o turno ou quebrar prompt cache (#12116) |
| **Shell hooks** | Scripts shell como hooks de lifecycle (`pre_tool_call`, `post_tool_call`, `on_session_start`) sem escrever plugin Python (#13296) |

---

## 7. Dashboard Web Melhorado

- **Sistema de plugins** - terceiros podem adicionar abas/widgets sem fork
- **Temas** - switching live de cores, fontes, layout, densidade
- **i18n** - Inglês e Chinês
- **Mobile-responsive**
- **Deploy Vercel**
- Tracking real de chamadas API por sessão
- Botões one-click: update + restart gateway

---

## 8. Atualização Realizada

**Data da atualização:** 24/04/2026  
**Status:** Concluído com sucesso  
**Backup:** Realizado em `~/.hermes/backups/`  
**Customizações preservadas:** Sim

---

## Links de Referência

- [GitHub Releases](https://github.com/NousResearch/hermes-agent/releases)
- [Documentação Oficial](https://hermes-agent.nousresearch.com/)
- [AGENTS.md Atualizado](https://github.com/NousResearch/hermes-agent/blob/main/AGENTS.md)

---

#hermes #release-notes #v0.11.0 #update #tui #aws-bedrock #plugins
