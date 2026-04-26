---
title: AVISO: OpenRouteService - Requer API Key
date: 2026-04-23 01:02:25
updated: 2026-04-23 01:02:25
tags:
  - aviso
  - api
  - geocoding
  - rejeitado
  - teste
source: 
related: []
---

# OpenRouteService (ORS) - Biblioteca Python

**Status:** ❌ NÃO USAR para scripts pessoais/automação

## Problema
A biblioteca  **exige API key obrigatória** desde a primeira requisição. Não há modo demo ou anônimo.



## Por que não serve para nós
- Adiciona complexidade desnecessária (criar conta, gerenciar credenciais)
- Free tier limitado (2.000 req/dia)
- Overkill para scripts pessoais ocasionais

## Alternativa funcional
**WazeRouteCalculator** - API não-oficial do Waze:
- ✅ Sem API key
- ✅ Setup instantâneo ()
- ✅ Dados de tráfego em tempo real (superior no Brasil)
- ⚠️ Risco: pode quebrar se Waze mudar API (aceitável para uso pessoal)

## Quando reconsiderar ORS
- Projeto comercial/crítico
- Volume > 2.000 requisições/dia
- Necessidade de features avançadas (isócronas, otimização multi-ponto, elevação)

## Teste realizado
- Data: 2026-04-23
- Resultado: Falha na inicialização (sem API key)
- Ambiente: WSL Ubuntu 24.04, Python 3.12

---
**Conclusão:** Manter WazeRouteCalculator. Migrar para ORS apenas se ele falhar permanentemente.