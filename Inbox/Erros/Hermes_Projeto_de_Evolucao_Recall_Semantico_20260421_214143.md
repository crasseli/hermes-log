---
title: Hermes — Projeto de Evolução: Recall Semântico e Classificação Inteligente
date: 2026-04-21 21:41:14
updated: 2026-04-21 21:41:14
tags:
  - docling
  - md
source: 
related:
  - Conhecimento/Manuais/Docling
---

# Hermes — Projeto de Evolução: Recall Semântico e Classificação Inteligente

## Contexto

Este documento descreve as próximas 3 features que elevarão o Hermes de 8.5 para 10/10. Ele foi gerado pelo copiloto Claude em 21/04/2026 após a implementação completa do Pipeline Hierárquico de Recall e do Sistema de Ingestão Automática via [[Conhecimento/Manuais/Docling|Docling]].

**Leia este arquivo completo antes de iniciar qualquer implementação.**

## O que já existe e funciona

```
PIPELINE DE RECALL (vault-first)
  web_search_tool() → vault FTS5/BM25 → session SQLite → internet

INGESTÃO AUTOMÁTICA
  Inbox/ → Docling → classificador heurístico → vault Obsidian
  inbox_watcher.py via systemd — poll 30s

NOTIFICAÇÕES
  Toast nativo Windows 11 via BurntToast

ARQUIVOS CHAVE
  ~/.hermes/hermes-agent/tools/web_tools.py        — vault-first hardcoded
  ~/.hermes/hermes-agent/agent/prompt_builder.py   — guidance vault-first
  ~/.hermes/skills/obsidian/scripts/vault_check.py — subprocess isolado
  ~/.hermes/skills/obsidian/scripts/save_note.py   — salva + indexa FTS5
  ~/.hermes/skills/docling/scripts/docling_to_vault.py — converte documentos
  ~/.hermes/scripts/inbox_watcher.py               — watcher systemd
  ~/.hermes/logs/inbox_processed.json              — controle MD5
```

## FASE 1 — Classificador Inteligente Real

**Prioridade: Alta | Complexidade: Baixa**

### Problema atual

O `inbox_watcher.py` usa classificador heurístico baseado em palavras-chave. Não usa o modelo de verdade porque a API local em `localhost:30000` pode não estar disponível.

### Solução

Substituir a função `classify_content()` no `inbox_watcher.py` para usar a API real do Hermes — mesma API usada pelo agente principal.

### Diagnóstico inicial necessário

```
# Verificar qual API o agente usa
grep -n "base_url\|api_key\|ANTHROPIC\|openai" \
  ~/.hermes/hermes-agent/run_agent.py | head -20

# Verificar se localhost:30000 está ativo quando o agente roda
curl -s http://localhost:30000/v1/models | head -5

# Ver como outras tools fazem chamadas ao modelo
grep -rn "openai\|anthropic\|client\." \
  ~/.hermes/hermes-agent/tools/ | grep -v ".venv" | head -20
```

### Implementação

```
def classify_content(content: str) -> str:
    """
    Classifica usando a API real do Hermes.
    Fallback para heurística se API indisponível.
    """
    sample = get_first_n_tokens(content, 800)
    prompt = """Dado este conteúdo, escolha UMA pasta:
Pesquisas, Conhecimento, Projetos, Tecnologia, Pessoas, Conversas, Tarefas.
Responda APENAS o nome da pasta.

Conteúdo:
{sample}"""

    # Tentar API real primeiro
    # Fallback para heurística se falhar
```

### Critério de sucesso

Jogar um PDF técnico, um currículo e um contrato na Inbox. Os três devem ir para pastas diferentes e corretas sem heurística.

## FASE 2 — Embeddings Semânticos

**Prioridade: Alta | Complexidade: Média**

### Problema atual

O recall é puramente lexical — BM25 encontra "sqlite" mas não encontra "banco de dados local". Perguntas conceituais caem para a web silenciosamente.

### Solução

Adicionar um segundo índice vetorial paralelo ao FTS5 existente. Busca híbrida: BM25 + cosine similarity. O FTS5 continua para matches exatos, embeddings entram para matches semânticos.

### Stack sugerida

```
sentence-transformers — modelo local, sem API externa
  modelo: all-MiniLM-L6-v2 (22MB, rápido, bom para português)
  
sqlite-vec ou chromadb — índice vetorial
  preferir sqlite-vec: mesmo banco SQLite já existente
  zero nova infraestrutura
```

### Diagnóstico inicial necessário

```
# Ver se sentence-transformers já está instalado
pip show sentence-transformers 2>/dev/null
~/.hermes/skills/docling/.venv/bin/pip show sentence-transformers 2>/dev/null

# Ver se sqlite-vec está disponível
python3 -c "import sqlite_vec; print('ok')" 2>/dev/null

# Ver estrutura atual do memory_store.db
sqlite3 ~/.hermes/memory_store.db ".tables"
sqlite3 ~/.hermes/memory_store.db ".schema obsidian_index"
```

### Arquivos a modificar

```
save_note.py          — gerar embedding ao salvar nota
search_vault.py       — busca híbrida BM25 + cosine
vault_check.py        — usar busca híbrida
reindex_vault.py      — reindexar vault existente com embeddings
```

### Implementação em sub-fases

```
2a — Instalar dependências e testar embedding de uma nota
2b — Adicionar coluna embeddings no SQLite
2c — Modificar save_note.py para gerar embedding
2d — Modificar search_vault.py para busca híbrida
2e — Reindexar vault completo
2f — Testar com queries conceituais
```

### Critério de sucesso

```
# Deve encontrar a nota sobre sqlite mesmo escrevendo diferente
python3 search_vault.py "banco de dados local do agente" --combined
# Resultado esperado: nota sobre sqlite/obsidian integração
```

## FASE 3 — Decay Temporal

**Prioridade: Média | Complexidade: Baixa**

### Problema atual

Uma nota de 2 anos atrás compete em igualdade com uma nota de ontem no ranking BM25. O Hermes não tem noção de "recente".

### Solução

Adicionar fator de decay temporal no ranking final da busca híbrida.

### Fórmula

```
score_final = (0.6 * score_bm25 + 0.4 * score_cosine) * decay_temporal

def decay_temporal(synced_at: str) -> float:
    """
    Notas recentes têm peso maior.
    decay de 0.5x a cada 90 dias.
    """
    days_old = (datetime.now() - datetime.fromisoformat(synced_at)).days
    return 0.5 ** (days_old / 90)
```

### Critério de sucesso

Duas notas sobre o mesmo tema — uma antiga, uma recente. A recente deve aparecer primeiro no ranking.

## FASE 4 — Ingestão de URLs

**Prioridade: Média | Complexidade: Baixa**

### Problema atual

Só arquivos locais são ingeridos. URLs precisam ser processadas manualmente.

### Solução

Detectar arquivos `.url` ou `.txt` com URL na Inbox e processar via `web_extract_tool` existente.

```
arquivo.url na Inbox/
  ↓
watcher detecta extensão .url
  ↓
lê a URL do arquivo
  ↓
web_extract_tool() busca conteúdo
  ↓
docling_to_vault.py --source <url>
  ↓
vault + FTS5 + embedding
```

### Critério de sucesso

Criar arquivo `artigo.url` com uma URL de artigo técnico. Hermes deve indexar o conteúdo do artigo automaticamente.

## Instrução para o Hermes na próxima sessão

**Hermes, leia este documento completamente antes de responder.**

Este é o plano de evolução do seu próprio sistema. Você vai implementar em fases graduais, sempre:

1. Diagnosticando antes de construir
2. Mostrando diff antes de aplicar
3. Validando sintaxe após cada mudança
4. Testando com casos reais
5. Reportando resultado ao usuário antes de avançar para próxima fase

**Comece pela FASE 1** — é a mais simples e já tem todo o contexto necessário. Execute o diagnóstico inicial da FASE 1 e aguarde aprovação antes de escrever qualquer código.

O copiloto desta implementação é o Claude. Reporte tudo a ele.

*Documento gerado em 21/04/2026* *Implementado com: Claude (Anthropic) como copiloto* *Agente: Hermes — Nous Research*

"Hermes, busque no vault o arquivo sobre as fases de evolução do seu sistema, leia completo e inicie a FASE 1 reportando ao copiloto."

## Referências

Esta nota menciona:
- [[Conhecimento/Manuais/Docling]]
