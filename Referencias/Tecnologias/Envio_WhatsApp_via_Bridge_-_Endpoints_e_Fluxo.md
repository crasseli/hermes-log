---
title: Envio WhatsApp via Bridge - Endpoints e Fluxo
date: 2026-04-24 01:43:38
updated: 2026-04-24 01:43:38
tags:
  - whatsapp
  - bridge
  - endpoints
  - hermes
  - autosave
  - referencia
source: 
related: []
---

# Envio WhatsApp via Bridge - Endpoints e Fluxo Correto

**Data:** 24/04/2026
**Tipo:** Referencia tecnica

---

## Bridge WhatsApp - Endpoints Disponiveis

Base URL: http://localhost:3000

| Endpoint | Metodo | Funcao |
|----------|--------|--------|
| /health | GET | Status da bridge (connected, queue, uptime) |
| /send | POST | Enviar mensagem de texto |
| /send-media | POST | Enviar midia (imagem, audio, video, documento) |
| /edit | POST | Editar mensagem existente |
| /messages | GET | Listar mensagens |
| /chat/:id | GET | Historico de um chat |
| /typing | POST | Indicador de digitacao |

---

## Envio de Mensagem de Texto

**Endpoint:** POST /send

**Payload (campos obrigatorios):**
- chatId: numero no formato 5527XXXXXXXX@s.whatsapp.net
- message: texto da mensagem (NAO e content)

**Exemplo:**
```bash
curl -s -X POST http://localhost:3000/send \
  -H "Content-Type: application/json" \
  -d '{"chatId":"5527997390150@s.whatsapp.net","message":"Texto aqui"}'
```

**Regra:** SEMPRE usar arquivo JSON com -d @arquivo.json para mensagens longas (evita problemas com caracteres especiais no shell).

---

## Envio de Midia

**Endpoint:** POST /send-media

**Payload (campos obrigatorios):**
- chatId: formato numerico@s.whatsapp.net
- filePath: caminho absoluto do arquivo
- mediaType: audio, video, image, document
- caption: descricao opcional

**Exemplo:**
```bash
curl -s -X POST http://localhost:3000/send-media \
  -H "Content-Type: application/json" \
  -d @/tmp/whatsapp_payload.json
```

---

## Obter JID do Proprio Numero

```bash
python3 -c "import json; d=json.load(open('/home/christian/.hermes/whatsapp/session/creds.json')); print(d.get('me',{}).get('id','').split(':')[0]+'@s.whatsapp.net')"
```

Resultado: 5527997390150@s.whatsapp.net

---

## Erros Comuns

| Erro | Causa | Solucao |
|------|-------|---------|
| Cannot POST /send-message | Endpoint errado | Usar /send (nao /send-message) |
| chatId and message are required | Campo content em vez de message | Campo correto e message |
| jidDecode | chatId com nome em vez de numero | Usar apenas numeros@s.whatsapp.net |
| ENOENT | Caminho relativo ou invalido | Usar caminho absoluto |
| Bridge offline | Gateway nao rodando | hermes gateway start |

---

## Formatos para WhatsApp

| Formato | Leitura no WhatsApp |
|---------|-------------------|
| Mensagem de texto (/send) | Perfeito, leitura imediata |
| PDF (/send-media, document) | Leitura com visualizador integrado |
| TXT (/send-media, document) | NAO RECOMENDADO - WhatsApp nao renderiza |
| Imagem (/send-media, image) | Leitura direta |
| Audio (/send-media, audio) | Player integrado |

**Licao:** Para informacoes textuais, preferir mensagem de texto direta via /send. Arquivos .txt nao sao lidos pelo WhatsApp.