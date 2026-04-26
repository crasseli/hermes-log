---
title: Seguranca APIs REST
date: 2026-04-19 23:16:49
updated: 2026-04-19 23:16:49
tags:
  - api
  - security
  - jwt
  - rest
source: 
related: []
---

Ao projetar APIs REST, a seguranca e fundamental. Existem varias estrategias de autenticacao.\n\n## Metodos de Auth\n\n1. **API Keys**: Simples mas limitado\n2. **OAuth 2.0**: Padrao para apps de terceiros \n3. **JWT**: JSON Web Tokens para stateless auth\n4. **Session Cookies**: Tradicional para web apps\n\n## Implementacao JWT\n\nJWT Authentication e ideal para APIs modernas porque:\n- Stateless (servidor nao armazena sessao)\n- Escalavel horizontalmente\n- Suporta claims customizadas\n\n## Refresh Tokens\n\nPara seguranca extra, usar refresh tokens com duracao maior que access tokens.