---
title: API Key OpenWeatherMap Test
date: 2026-04-23 02:09:16
updated: 2026-04-23 02:09:16
tags:
  - api
  - weather
  - openweathermap
  - teste
source: 
related: []
---

## OpenWeatherMap API Key Analysis

**Key:** 24bf7ab8d6a97fef6122c33b94a99953  
**Status:** ATIVA - Free Tier confirmado

### Endpoints Funcionais (Free)
- Current Weather (/data/2.5/weather) - OK
- 5-Day/3-Hour Forecast (/data/2.5/forecast) - OK  
- Geocoding API (/geo/1.0/direct) - OK

### Endpoints Bloqueados (Requer plano pago)
- One Call 3.0 - 401 Unauthorized
- 16-Day Forecast - 401 Unauthorized
- Historical Weather - 401 Unauthorized
- Air Pollution - 404 (endpoint pode estar em outra URL)

### Limites do Plano Gratuito
- 60 chamadas/minuto
- 1.000.000 chamadas/mês
- Sem forecast estendido
- Sem dados históricos

### Uso Recomendado
- Previsão atual e 5 dias para automações
- Geocoding para conversão cidade/coordenadas
- Monitoramento de rate limit

**Data do teste:** 23/04/2026