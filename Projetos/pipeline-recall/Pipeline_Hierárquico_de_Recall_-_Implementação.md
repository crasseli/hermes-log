---
title: Pipeline Hierárquico de Recall - Implementação
date: 2026-04-21 16:10:15
updated: 2026-04-21 16:10:15
tags:
  - pipeline
  - recall
  - vault
  - web_search
  - implementação
source: 
related: []
---

# Pipeline Hierárquico de Recall - Implementação

## Resumo
Sistema implementado para consultar fontes de conhecimento em ordem de prioridade antes de buscar na internet.

## Hierarquia de Recall
1. **Vault Obsidian** (primeiro) — via 
2. **Sessões SQLite** (fallback) — via 
3. **Web search** (último recurso) — via 

## Arquivos Modificados

### 1. web_tools.py
- **Linhas**: ~45 (imports), ~1033 (helper), ~1102 (vault-first)
- **Alterações**:
  - Adicionados  e 
  - Criada função 
  - Inserido bloco vault-first no início de , antes do dispatch para backend

### 2. prompt_builder.py
- **Linha**: ~224
- **Alteração**: Adicionadas 2 linhas de guidance sobre vault-first
- **Texto adicionado**:
  - BEFORE web_search: vault is checked automatically
  - results from obsidian_vault mean web was skipped
  - web_search only reaches the internet if vault returned 0 results

## Comportamento
- **Threshold padrão**: 2 resultados para considerar vault relevante
- **Timeout**: 5 segundos para subprocess do vault
- **Falha silenciosa**: se vault falhar, não bloqueia fallback para web
- **Retorno JSON**: 

## Testes Validados
| Cenário | Query | Resultado Esperado | Status |
|---------|-------|-------------------|--------|
| Vault | 'sqlite obsidian integração' | source: obsidian_vault | ✓ PASS |
| Web | 'previsão do tempo Vitória ES' | success: true (web) | ✓ PASS |
| Ambíguo | 'projeto KAIROS' | web (count < threshold) | ✓ PASS |

## Data
Implementado em: 21/04/2026