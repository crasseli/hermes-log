---
title: AVISO: google-maps-scraper - Blacklist
date: 2026-04-23 01:22:27
updated: 2026-04-23 01:22:27
tags:
  - aviso
  - blacklist
  - scraping
  - frágil
  - rejeitado
  - google-maps
source: 
related: []
---

# google-maps-scraper (conor-is-my-name)

**Status:** ❌ BLACKLIST - NÃO USAR

**Repositório:** https://github.com/conor-is-my-name/google-maps-scraper

## Por que está na blacklist

### 1. Fragilidade arquitetural
- Baseado em scraping de HTML do Google Maps
- Quebra frequentemente quando Google atualiza UI
- Seletores CSS podem falhar a qualquer momento

### 2. Limitações severas
- **Rate limit:** Máximo 500 lugares/dia por IP
- **Bloqueio:** Google detecta e bloqueia rapidamente
- **Sem reviews:** Só extrai metadados (nota/contagem), não texto das avaliações
- **ToS:** Viola termos de uso do Google Maps

### 3. Manutenção insustentável
- Requer constante atualização de seletores
- Depende de Playwright + Chromium (~200MB)
- Código complexo para tratamento de edge cases

## Alternativas recomendadas

| Caso de uso | Solução |
|-------------|---------|
| Dados de estabelecimentos | Google Places API oficial (pago, estável) |
| Geocoding simples | Nominatim (OpenStreetMap, gratuito) |
| Rotas com tráfego | WazeRouteCalculator (sem API key) |

## Quando reconsiderar

NUNCA para projetos sérios. Só aceitável para:
- Experimentos descartáveis de uma única vez
- Projetos pessoais onde falha é aceitável

## Teste realizado
- Data: 2026-04-23
- Avaliação: Funciona, mas é inerentemente instável
- Decisão: Rejeitar

---
**Conclusão:** Arquitetura de scraping em Google Maps é anti-padrão. Sempre preferir APIs oficiais ou fontes abertas (OSM).