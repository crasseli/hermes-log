---
title: Geolocation - API Nominatim (OpenStreetMap)
date: 2026-04-22 23:23:17
updated: 2026-04-22 23:23:17
tags:
  - hermes
  - geolocation
  - nominatim
  - openstreetmap
  - api
  - gratuito
  - serra-es
  - helio-ferraz
  - skill
  - autosave
source: 
related:
  - Projetos/Docling/SKILL
---

# Geolocation - API Nominatim (OpenStreetMap)

## Status
**Implementado e testado** em 22/04/2026

## Contexto

Substituída a HERE WeGo (que exigia cartão de crédito) pela **OpenStreetMap Nominatim API** - completamente gratuita, sem autenticação, sem cartão de crédito.

## Localização da Skill

```
~/.hermes/skills/productivity/geolocation/
├── [[Projetos/Docling/SKILL|SKILL]].md
└── scripts/
    └── geolocation_client.py
```

## Funcionalidades

| Funcionalidade | Descrição | Status |
|----------------|-----------|--------|
| Geocoding | Endereço → Coordenadas | ✅ Testado |
| Reverse Geocoding | Coordenadas → Endereço | ✅ Testado |
| Busca de lugares | Sugestões de endereços | ✅ Implementado |
| Rate limiting | Controle automático 1 req/s | ✅ Implementado |

## Exemplos Reais Testados

### Teste 1: Avenida Paulista, 1000 - São Paulo

**Input:** `Avenida Paulista, 1000, São Paulo, Brasil`

**Resultado:**
```
Latitude:  -23.5648865
Longitude: -46.6519180
Endereço:  1000, Avenida Paulista, Morro dos Ingleses, Bela Vista, 
           São Paulo, Região Sudeste, 01310-100, Brasil
```

### Teste 2: Rua Rio Paraná, 20 - Serra ES (Endereço Real)

**Input:** `Rua Rio Paraná, 20, Hélio Ferraz, Serra, ES, Brasil`

**Resultado:**
```
Latitude:  -20.2407139
Longitude: -40.2695856
CEP:       29160-630 (próximo do original 29160-531)
Endereço:  Rua Rio Paraná, Hélio Ferraz, Região de Carapina, Serra,
           Espírito Santo, Região Sudeste, Brasil
Região:    Região Metropolitana da Grande Vitória
```

**Reverse Geocoding confirmou:** mesmo endereço com hierarquia administrativa completa.

## Uso Rápido

```python
from scripts.geolocation_client import GeolocationClient

client = GeolocationClient()

# Geocoding
result = client.geocode("Rua Rio Paraná, 20, Serra, ES")
lat, lon = result['lat'], result['lon']

# Reverse geocoding
address = client.reverse_geocode(-20.2407139, -40.2695856)
print(address['display_name'])
```

## Especificações da API

| Aspecto | Detalhe |
|---------|---------|
| Base URL | `https://nominatim.openstreetmap.org/` |
| Autenticação | Nenhuma |
| Rate Limit | 1 requisição por segundo |
| User-Agent | Obrigatório (HermesAgent/1.0) |
| Idioma | pt-BR configurado |
| Licença | ODbL 1.0 |

## Referências

- Documentação oficial: https://nominatim.org/release-docs/develop/api/Search/
- OpenStreetMap: https://www.openstreetmap.org
- Política de uso: https://operations.osmfoundation.org/policies/nominatim/

## Histórico

| Data | Evento |
|------|--------|
| 22/04/2026 | Tentativa HERE WeGo - abortada (exige cartão) |
| 22/04/2026 | Implementação Nominatim - concluída |
| 22/04/2026 | Testes com endereços reais - validados |

## Tags

#geolocation #nominatim #openstreetmap #api #gratuito #serra-es #helio-ferraz #hermes-skill

## Referências

Esta nota menciona:
- [[Projetos/Docling/SKILL]]
