---
title: Evolução - Injeção de Código para SOUL.md Instrucional
date: 2026-04-25 11:37:31
updated: 2026-04-25 11:37:31
tags:
  - evolucao
  - arquitetura
  - soul
  - recall
  - cancelado
source: 
related:
  - OS/Ativas/OS_patch_run_agent
---

# Evolução: Injeção de Código → SOUL.md Instrucional

**Data:** 2026-04-26
**Contexto:** Reorganização da pasta OS após identificação de conteúdo obsoleto

---

## Abordagem Arquivada: Injeção Direta no run_agent.py

### O que era
A OS `[[OS/Ativas/OS_patch_run_agent|OS_patch_run_agent]].md` (sessão 23/04/2026) propunha modificar o código-fonte do Hermes injetando Python diretamente em `~/.hermes/hermes-agent/run_agent.py`.

### Como funcionava
```python
# Injeção após memory_manager.prefetch_all()
if os.getenv('HERMES_SEMANTIC_CONTEXT') == 'true':
    try:
        sys.path.insert(0, os.path.expanduser('~/.hermes/skills/obsidian/scripts'))
        from search_semantic import get_semantic_context
        sem_ctx = get_semantic_context(original_user_message, limit=3, max_chars=2000)
        # ... injetar contexto no prefetch
```

### Por que foi abandonada
1. **Fragilidade:** Modificações no código-fonte são perdidas em `git pull`
2. **Complexidade de rollback:** Erros de indentação causavam falha total do sistema
3. **Acoplamento:** Misturava lógica de negócio com infraestrutura do agente
4. **Manutenção:** Cada update exigiria re-aplicar patch manualmente

---

## Abordagem Atual: Separação de Concerns

### Estrutura (Injeção Declarativa)
| Componente | Função | Local |
|------------|--------|-------|
| **SOUL.md** | Instruções ao modelo interpretativo | `~/.hermes/SOUL.md` |
| **datura_checkpointer.py** | Hooks técnicos de execução | `~/.hermes/shell/` |
| **Scripts obsidian** | Implementação concreta | `~/.hermes/skills/obsidian/scripts/` |

### Vantagens
1. **Persistente:** SOUL.md é injetado em cada sessão via `run_agent.py` nativo
2. **Separação:** Lógica de negócio (recall) separada de infraestrutura (hooks)
3. **Manutenível:** Atualizações do agente não afetam customizações
4. **Previsível:** Instruções claras ao modelo vs. código imperativo

---

## Arquivos Afetados

### Reclassificados
| Arquivo | Destino Anterior | Destino Novo | Status |
|---------|------------------|--------------|--------|
| `hermes_sessao_23_04_2026.pdf` | `OS/Ativas/` | `Conversas/2026/` | Preservado como histórico |
| `OS_patch_run_agent.md` | `OS/Ativas/` | `OS/Arquivadas/canceladas/` | Marcado como obsoleto |

### Referências
- Nova implementação: [[Pipeline Hierárquico de Recall - Implementação]]
- SOUL.md atual: `~/.hermes/SOUL.md`
- Scripts: `~/.hermes/skills/obsidian/scripts/`

---

## Lição Aprendida
> **Prefira instruções interpretativas sobre modificação de código.**
> 
> Quando o ambiente permite (modelo com injeção de contexto via arquivo de instruções),
> use declaração em vez de implementação. É mais resiliente a mudanças de versão.

## Referências

Esta nota menciona:
- [[OS/Ativas/OS_patch_run_agent]]
