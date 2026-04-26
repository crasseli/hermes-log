---
title: JWT Authentication
date: 2026-04-19 23:16:20
updated: 2026-04-19 23:16:20
tags:
  - jwt
  - auth
  - api
  - security
source: 
related: []
---

JSON Web Tokens sao um padrao aberto RFC 7519 para transmitir informacoes entre partes de forma segura.\n\n## Caracteristicas\n- Compacto: via URL, POST ou header HTTP\n- Autocontido: payload contem claims\n- Assinado: verificacao de integridade\n\n## Estrutura\nHeader.Payload.Signature\n\n## Uso em APIs\nTokens sao enviados no header Authorization: Bearer <token>