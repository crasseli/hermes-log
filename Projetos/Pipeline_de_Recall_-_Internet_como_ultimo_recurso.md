---
title: Pipeline de Recall - Internet como último recurso
date: 2026-04-21 14:58:18
updated: 2026-04-21 14:58:18
tags:
  - pendencias
  - recall
  - pipeline
  - web_search
source: 
related: []
---

## Objetivo
Criar pipeline hierárquico de recall:
1. search_vault.py --combined (vault Obsidian)
2. session_search (SQLite)
3. web_search APENAS se 1 e 2 retornarem zero resultados

## Implementação
- Localizar onde web_search é registrada (tools/web_search_tool.py ou similar)
- Criar wrapper similar ao que foi feito no session_search_tool.py
- Verificar vault antes de chamar web_search real
- Threshold: se search_vault retornar 2+ resultados relevantes, não chamar web