---
title: Gov API Client - Cliente Seguro
date: 2026-04-23 13:04:40
updated: 2026-04-23 13:04:40
tags:
  - gov
  - api
  - security
  - tor
  - python
  - client
source: 
related: []
---

# Gov API Client - Cliente Seguro para APIs Governamentais

## Resumo
Cliente Python implementado para acessar APIs do Portal de Dados Abertos (dados.gov.br) com proteções de anonimato via Tor.

## Características de Segurança
- **Tor**: Requisições via SOCKS5 proxy (127.0.0.1:9050)
- **Headers rotativos**: User-Agent aleatório a cada requisição
- **Throttling**: Delay com jitter (2-8s) entre requisições
- **Cache local**: SQLite em ~/.hermes/cache/gov_api/cache.db
- **Sem logs sensíveis**: Não armazena dados pessoais

## Endpoints Disponíveis
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| list_themes() | /dados/api/temas | Lista temas/categorias |
| list_datasets() | /dados/api/publico/conjuntos-dados | Conjuntos de dados |
| get_dataset() | /dados/api/publico/conjuntos-dados/{id} | Detalhes de dataset |
| list_organizations() | /dados/api/publico/organizacao | Órgãos/entidades |
| list_formats() | /dados/api/publico/conjuntos-dados/formatos | Formatos disponíveis |
| list_ods() | /dados/api/publico/conjuntos-dados/objetivos-desenvolvimento-sustentavel | ODS |
| list_legal_observances() | /dados/api/publico/conjuntos-dados/observancia-legal | Observâncias legais |

## Arquivos
- Cliente: ~/.hermes/scripts/gov_api_client.py
- Config: ~/.hermes/scripts/.env.example
- Cache: ~/.hermes/cache/gov_api/cache.db

## Próximos Passos
1. Configurar GOV_API_KEY no arquivo .env
2. Testar endpoints com autenticação
3. Documentar casos de uso específicos
