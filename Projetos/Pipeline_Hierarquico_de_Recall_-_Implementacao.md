---
title: Pipeline Hierárquico de Recall - Implementação
date: 2026-04-21 15:36:32
updated: 2026-04-21 15:36:32
tags:
  - pipeline
  - recall
  - vault
  - obsidian
  - web-search
  - memory
  - hierarchical
  - implementado
source: 
related:
  - Projetos/Docling/SKILL
---

# Pipeline Hierárquico de Recall - Internet como último recurso

## Status: IMPLEMENTADO
Data: 2026-04-21
[[Projetos/Docling/SKILL|Skill]]: hierarchical-recall-pipeline

## Arquitetura
Pergunta do usuário
    ↓
1. **Vault Search** (Obsidian FTS5) ← Rápido, privado
    ↓ se 0 resultados
2. **Session Search** (SQLite state.db) ← Contexto histórico  
    ↓ se 0 resultados
3. **Web Search** (Internet) ← Último recurso

## Arquivos Criados/Modificados

### Novos
-  — Utilitário isolado
-  — Skill completa

### Modificados (planejado)
-  — Wrapper em web_search_tool()
-  — Guidance atualizado

## Implementação do Wrapper



## Testes Planejados

| Query | Esperado | Status |
|-------|----------|--------|
| "sqlite obsidian integração" | Vault | ☐ |
| "previsão tempo Vitória" | Web | ☐ |
| "projeto KAIROS" | Vault se existir | ☐ |

## Comandos de Diagnóstico

        })

    return results


def web_search_tool(query: str, limit: int = 5) -> str:
    """
    Search the web for information using available search API backend.

    This function provides a generic interface for web search that can work
    with multiple backends (Parallel or Firecrawl).

    Note: This function returns search result metadata only (URLs, titles, descriptions).
    Use web_extract_tool to get full content from specific URLs.
    
    Args:
        query (str): The search query to look up
        limit (int): Maximum number of results to return (default: 5)
    
    Returns:
        str: JSON string containing search results with the following structure:
             {
                 "success": bool,
                 "data": {
                     "web": [
                         {
                             "title": str,
                             "url": str,
                             "description": str,
                             "position": int
                         },
                         ...
                     ]
                 }
             }
    
    Raises:
        Exception: If search fails or API key is not set
    """
    debug_call_data = {
        "parameters": {
            "query": query,
            "limit": limit
        },
        "error": None,
        "results_count": 0,
        "original_response_size": 0,
        "final_response_size": 0
    }
    
    try:
    try:
        from tools.interrupt import is_interrupted
        if is_interrupted():
            return tool_error("Interrupted", success=False)

        # Dispatch to the configured backend
        backend = _get_backend()
        if backend == "parallel":
            response_data = _parallel_search(query, limit)
            debug_call_data["results_count"] = len(response_data.get("data", {}).get("web", []))
            result_json = json.dumps(response_data, indent=2, ensure_ascii=False)
            debug_call_data["final_response_size"] = len(result_json)
            _debug.log_call("web_search_tool", debug_call_data)
            _debug.save()
            return result_json

        if backend == "exa":
            response_data = _exa_search(query, limit)
            debug_call_data["results_count"] = len(response_data.get("data", {}).get("web", []))
            result_json = json.dumps(response_data, indent=2, ensure_ascii=False)
            debug_call_data["final_response_size"] = len(result_json)
            _debug.log_call("web_search_tool", debug_call_data)
            _debug.save()
            return result_json

        if backend == "tavily":
            logger.info("Tavily search: '%s' (limit: %d)", query, limit)
            raw = _tavily_request("search", {
                "query": query,
                "max_results": min(limit, 20),
                "include_raw_content": False,
                "include_images": False,
            })
            response_data = _normalize_tavily_search_results(raw)
            debug_call_data["results_count"] = len(response_data.get("data", {}).get("web", []))
            result_json = json.dumps(response_data, indent=2, ensure_ascii=False)
            debug_call_data["final_response_size"] = len(result_json)
            _debug.log_call("web_search_tool", debug_call_data)
            _debug.save()
            return result_json

        logger.info("Searching the web for: '%s' (limit: %d)", query, limit)

        response = _get_firecrawl_client().search(
            query=query,
            limit=limit
        )

        web_results = _extract_web_search_results(response)
        results_count = len(web_results)
        logger.info("Found %d search results", results_count)
248:    "web_search",
8503:                    # to abort, but tools without interrupt checks (web_search,

## Rollback



## Insights Chave

1. **Isolamento:** vault_check.py é standalone
2. **Silent Fail:** Try/except evita quebra
3. **JSON Compatible:** Mesma estrutura de resposta
4. **Automático:** Usuário não precisa aprender nada novo
5. **Configurável:** Threshold ajustável

## Tags
#pipeline #recall #vault #obsidian #web-search #memory #hierarchical

## Referências

Esta nota menciona:
- [[Projetos/Docling/SKILL]]
