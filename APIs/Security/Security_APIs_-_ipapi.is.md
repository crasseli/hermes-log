---
title: Security APIs - ipapi.is
date: 2026-04-23 02:29:15
updated: 2026-04-23 02:29:15
tags:
  - api
  - security
  - threat-intelligence
  - ip-lookup
  - osint
source: 
related: []
---

## IP Data API (ipapi.is)

**Status:** Aprovado e documentado
**Data:** 23/04/2026
**Categoria:** Threat Intelligence / OSINT

### Descrição
API gratuita para análise de IPs com detecção de VPN, proxy, Tor, datacenter e histórico de abuso. Inclui geolocalização, dados de ASN e contatos de abuse.

### Endpoint


### Métricas
- Health Score: 100%
- Reliability: 100%
- Avg Response: ~78ms
- CORS: Enabled

### Capacidades
- Geolocalização de IPs
- Detecção de anonimização (VPN/Proxy/Tor)
- Identificação de datacenters
- Dados de ASN e ISP
- Contatos de abuse
- Score de abuser

### Uso
============================================================
IP DATA API - Resultado da Consulta
============================================================
IP: 8.8.8.8
RIR: ARIN

--- Flags de Segurança ---
  Bogon: Não
  Mobile: Não
  Satélite: Não
  Crawler/Bot: Não
  Datacenter: SIM ⚠️
  Tor: Não
  Proxy: Não
  VPN: Não
  Abuser: SIM ⚠️

--- Localização ---
  País: United States (US)
  Cidade: Mountain View
  Estado: California
  CEP: 95196
  Fuso: America/Los_Angeles

--- ISP/Empresa ---
  Nome: Google LLC
  Tipo: hosting
  Domínio: google.com

--- ASN ---
  ASN: 15169
  Organização: Google LLC
  País: US

--- Contato de Abuse ---
  Nome: Google LLC
  Email: network-abuse@google.com
  Telefone: +1-650-253-0000

============================================================
============================================================
IP DATA API - Resultado da Consulta
============================================================
IP: 179.164.36.35
RIR: LACNIC

--- Flags de Segurança ---
  Bogon: Não
  Mobile: Não
  Satélite: Não
  Crawler/Bot: Não
  Datacenter: Não
  Tor: Não
  Proxy: Não
  VPN: Não
  Abuser: Não

--- Localização ---
  País: Brazil (BR)
  Cidade: Vila Velha
  Estado: Espirito Santo
  CEP: 29100-000
  Fuso: America/Sao_Paulo

--- ISP/Empresa ---
  Nome: TELEF*NICA BRASIL S.A
  Tipo: isp
  Domínio: telefonica.com.br

--- ASN ---
  ASN: 26599
  Organização: TELEF*NICA BRASIL S.A
  País: BR

--- Contato de Abuse ---
  Nome: TELEF*NICA BRASIL S.A
  Email: abuse.br@telefonica.com
  Telefone: 

============================================================
{
  "ip": "1.1.1.1",
  "rir": "APNIC",
  "is_bogon": false,
  "is_mobile": false,
  "is_satellite": false,
  "is_crawler": false,
  "is_datacenter": false,
  "is_tor": false,
  "is_proxy": false,
  "is_vpn": true,
  "is_abuser": true,
  "vpn": {
    "ip": "1.1.1.1",
    "service": "PublicVpnConfigs",
    "type": "vpn_server",
    "last_seen": 1776699720273,
    "last_seen_str": "2026-04-20T15:42:00.273Z"
  },
  "company": {
    "name": "APNIC Research and Development",
    "abuser_score": "0.0234 (Elevated)",
    "domain": "apnic.net",
    "type": "business",
    "network": "1.1.1.0 - 1.1.1.255",
    "whois": "https://api.ipapi.is/?whois=1.1.1.0"
  },
  "abuse": {
    "name": "APNIC Research and Development",
    "address": "6 Cordelia St",
    "email": "helpdesk@apnic.net",
    "phone": "+61-7-38583100"
  },
  "asn": {
    "asn": 13335,
    "abuser_score": "0.0165 (Elevated)",
    "route": "1.1.1.0/24",
    "descr": "CLOUDFLARENET - Cloudflare, Inc., US",
    "country": "us",
    "active": true,
    "org": "Cloudflare, Inc.",
    "domain": "cloudflare.com",
    "abuse": "abuse@cloudflare.com",
    "type": "hosting",
    "created": "2010-07-14",
    "updated": "2017-02-17",
    "rir": "ARIN",
    "whois": "https://api.ipapi.is/?whois=AS13335"
  },
  "location": {
    "is_eu_member": false,
    "calling_code": "61",
    "currency_code": "AUD",
    "continent": "OC",
    "country": "Australia",
    "country_code": "AU",
    "state": "Queensland",
    "city": "Brisbane",
    "latitude": -27.46754,
    "longitude": 153.02809,
    "zip": "4000",
    "timezone": "Australia/Brisbane",
    "local_time": "2026-04-23T15:29:16+10:00",
    "local_time_unix": 1776922156,
    "is_dst": false
  },
  "elapsed_ms": 0.37
}

### Skill Criada
- Local: 
- Script: 
- Documentação: 

### Casos de Uso
1. Análise de logs de firewall
2. Detecção de ataques anonimizados
3. Forense e incident response
4. Prevenção de fraude
5. Enriquecimento de threat intel

**Aprovado para uso em produção.**