---
title: Geolocation Skill - Implementação Nominatim
date: 2026-04-22 23:12:40
updated: 2026-04-22 23:12:40
tags:
  - hermes
  - geolocation
  - nominatim
  - openstreetmap
  - autosave
source: 
related:
  - Projetos/Docling/SKILL
---

# Geolocation Skill - Implementação Nominatim

## Status
Concluído em 22/04/2026

## Resumo
Substituída a HERE WeGo (que exigia cartão de crédito) pela OpenStreetMap Nominatim API - completamente gratuita, sem autenticação, sem cartão.

## O que foi feito
1. Removida skill here-positioning (HERE WeGo)
2. Desinstalada biblioteca here-location-services
3. Criada nova skill geolocation em ~/.hermes/skills/productivity/geolocation/
4. Implementado cliente Python usando Nominatim API

## Funcionalidades implementadas
- Geocoding: endereço → coordenadas
- Reverse geocoding: coordenadas → endereço
- Busca de lugares com rate limiting (1 req/s)

## Teste realizado
- Avenida Paulista, 1000, São Paulo → lat: -23.5648865, lon: -46.6519180
- Reverse: coordenadas → Edifício Paulista Mil, Avenida Paulista

## Arquivos
- [[Projetos/Docling/SKILL|SKILL]].md: documentação
- scripts/geolocation_client.py: implementação Python

## Referências
- API: https://nominatim.openstreetmap.org
- Docs: https://nominatim.org/release-docs/develop/api/Search/
- Licença: ODbL 1.0

## Referências

Esta nota menciona:
- [[Projetos/Docling/SKILL]]
