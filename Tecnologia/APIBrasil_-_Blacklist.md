---
title: APIBrasil - Blacklist
date: 2026-04-23 01:41:21
updated: 2026-04-23 01:41:21
tags:
  - blacklist
  - api
  - brasil
  - cep
  - cnpj
  - cadastro-obrigatorio
source: 
related: []
---

## APIBrasil

**Status:** BLACKLIST
**Motivo:** Requer cadastro obrigatório para qualquer uso, mesmo sandbox
**Data:** 23/04/2026

### APIs prometidas como gratuitas
- CEP, CNPJ, Feriados, DDD, IP, Geo

### Problema real
- SDK existe ()
- **Impossível testar sem criar conta** em app.apibrasil.io
- Barreira de entrada: email + verificação + token
- Na prática: tudo é pago ou requer cadastro

### Veredito
**NÃO USAR.** Para CEP/CNPJ ocasional, usar alternativas diretas:
- ViaCEP (sem cadastro)
- ReceitaWS (sem cadastro)
- BrasilAPI (sem cadastro)

### Categoria
blacklist, api, brasil, cep, cnpj