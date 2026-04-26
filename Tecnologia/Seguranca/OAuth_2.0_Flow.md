---
title: OAuth 2.0 Flow
date: 2026-04-19 23:17:34
updated: 2026-04-19 23:17:34
tags:
  - oauth
  - auth
  - jwt
  - security
source: 
related: []
---

OAuth 2.0 e um protocolo de autorizacao que permite a aplicacoes obter acesso limitado a contas de usuario.

## Fluxos Comuns

1. **Authorization Code**: Mais seguro, para apps servidor-side
2. **Implicit**: Para SPA (deprecated)
3. **Client Credentials**: Para comunicacao server-to-server
4. **Device Code**: Para dispositivos sem browser

## Integracao com JWT

JWT Authentication pode ser usado em conjunto com OAuth 2.0:
- Access tokens em formato JWT
- Self-contained claims
- Assinatura verificavel pelo resource server

Isso elimina a necessidade de introspecao no authorization server.

## Implementacao Segura

Nunca exponha client secrets em aplicativos publicos.
Use PKCE para mobile apps.

## Referencias

- RFC 6749
- RFC 7636 (PKCE)