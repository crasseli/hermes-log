---
title: Hermes — Projeto de Evolução: Recall Semântico e Classificação Inteligente
date: 2026-04-22 09:15:02
updated: 2026-04-22 09:15:02
tags:
  - hermes
  - evolução
  - embeddings
  - nvidia
  - recall-semântico
  - roadmap
  - fase1
  - fase2
  - fase3
  - fase4
source: 
related:
  - Conhecimento/Manuais/Docling
---

# Hermes — Projeto de Evolução: Recall Semântico e Classificação Inteligente

## Contexto

Este documento descreve as próximas 4 features que elevarão o Hermes de 8.5 para 10/10. Gerado pelo copiloto Claude (Anthropic) em 21/04/2026 após implementação completa do Pipeline Hierárquico de Recall e do Sistema de Ingestão Automática via [[Conhecimento/Manuais/Docling|Docling]].

**Leia este arquivo completo antes de iniciar qualquer implementação.**

O copiloto desta implementação é o Claude. Reporte tudo a ele.

---

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
  ~/.hermes/hermes-agent/tools/web_tools.py — vault-first hardcoded
  ~/.hermes/hermes-agent/agent/prompt_builder.py — guidance vault-first
  ~/.hermes/skills/obsidian/scripts/vault_check.py — subprocess isolado
  ~/.hermes/skills/obsidian/scripts/save_note.py — salva + indexa FTS5
  ~/.hermes/skills/obsidian/scripts/search_vault.py — busca FTS5/BM25
  ~/.hermes/skills/obsidian/scripts/reindex_vault.py — reindexação
  ~/.hermes/skills/docling/scripts/docling_to_vault.py — converte documentos
  ~/.hermes/scripts/inbox_watcher.py — watcher systemd
  ~/.hermes/logs/inbox_processed.json — controle MD5
```

---

## FASE 1 — Classificador Inteligente Real

**Prioridade: Alta | Complexidade: Baixa**

### Problema atual

O inbox_watcher.py usa classificador heurístico baseado em palavras-chave. Não usa o modelo de verdade porque a API local em localhost:30000 pode não estar disponível no contexto do systemd.

### Solução

Substituir a função classify_content() no inbox_watcher.py para usar a API real do Hermes — mesma API usada pelo agente principal.

### Diagnóstico inicial

```bash
# Verificar qual API o agente usa
grep -n 'base_url\|api_key\|ANTHROPIC\|openai'   ~/.hermes/hermes-agent/run_agent.py | head -20

# Verificar se localhost:30000 está ativo quando o agente roda
curl -s http://localhost:30000/v1/models | head -5

# Ver como outras tools fazem chamadas ao modelo
grep -rn 'openai\|anthropic\|client\.'   ~/.hermes/hermes-agent/tools/ | grep -v '.venv' | head -20
```

### Implementação

```python
def classify_content(content: str) -> str:
    '''
    Classifica usando API real do Hermes.
    Fallback para heurística se API indisponível.
    '''
    sample = get_first_n_tokens(content, 800)
    prompt = '''Dado este conteúdo, escolha UMA pasta entre:
Pesquisas, Conhecimento, Projetos, Tecnologia, Pessoas, Conversas, Tarefas.
Responda APENAS o nome exato da pasta. Sem explicações.

Conteúdo: ''' + sample
    
    try:
        from openai import OpenAI
        client = OpenAI(
            base_url='http://localhost:30000/v1',
            api_key='dummy'
        )
        response = client.chat.completions.create(
            model='hermes',
            messages=[{'role': 'user', 'content': prompt}],
            temperature=0.1,
            max_tokens=20
        )
        folder = response.choices[0].message.content.strip()
        for valid in VALID_FOLDERS:
            if folder.lower() == valid.lower():
                return valid
    except Exception:
        pass  # fallback para heurística
    
    return classify_heuristic(content)  # função heurística atual como fallback
```

### Critério de sucesso

Jogar PDF técnico, currículo e contrato na Inbox. Os três devem ir para pastas diferentes e corretas sem heurística.

---

## FASE 2 — Embeddings Semânticos

**Prioridade: Alta | Complexidade: Média**

### Problema atual

O recall é puramente lexical — BM25 encontra 'sqlite' mas não encontra 'banco de dados local do agente'. Perguntas conceituais caem para a web silenciosamente sem o usuário perceber.

### Solução

Adicionar índice vetorial paralelo ao FTS5 existente. Busca híbrida: BM25 + cosine similarity. O FTS5 continua para matches exatos, embeddings para matches semânticos.

### Stack definida

- **Modelo:** nvidia/nv-embedcode-7b-v1
- **Endpoint:** https://integrate.api.nvidia.com/v1/embeddings
- **Chave:** mesma NVIDIA_API_KEY já configurada no Hermes
- **Especialidade:** código e documentação técnica — ideal para o vault
- **Fallback local:** all-MiniLM-L6-v2 (22MB) se API indisponível

### Exemplo oficial NVIDIA adaptado para o Hermes

```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.environ.get('NVIDIA_API_KEY'),
    base_url='https://integrate.api.nvidia.com/v1'
)

# Para INDEXAR uma nota no vault (save_note.py, reindex_vault.py)
def embed_passage(text: str) -> list[float]:
    response = client.embeddings.create(
        input=[text],
        model='nvidia/nv-embedcode-7b-v1',
        encoding_format='float',
        extra_body={'input_type': 'passage', 'truncate': 'NONE'}
    )
    return response.data[0].embedding

# Para BUSCAR no vault (search_vault.py, vault_check.py)
def embed_query(text: str) -> list[float]:
    response = client.embeddings.create(
        input=[text],
        model='nvidia/nv-embedcode-7b-v1',
        encoding_format='float',
        extra_body={'input_type': 'query', 'truncate': 'NONE'}
    )
    return response.data[0].embedding
```

### ATENÇÃO — input_type é crítico

- **passage** → ao SALVAR nota no vault (save_note.py, reindex_vault.py)
- **query** → ao BUSCAR (search_vault.py, vault_check.py)

Usar errado degrada severamente a qualidade do recall semântico.

### Diagnóstico inicial

```bash
# 1. Confirmar NVIDIA_API_KEY disponível
echo $NVIDIA_API_KEY | head -c 20

# 2. Testar endpoint NV-EmbedCode-7B
python3 -c 

## Referências

Esta nota menciona:
- [[Conhecimento/Manuais/Docling]]
