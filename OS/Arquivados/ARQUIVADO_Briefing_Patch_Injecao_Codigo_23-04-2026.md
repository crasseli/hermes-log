---
title: ARQUIVADO - Briefing Patch run_agent.py via Injeção de Código (23/04/2026)
status: arquivado
tipo: evolucao-tecnica
data_original: 2026-04-23
data_arquivamento: 2026-04-25
abordagem: injecao-codigo-run_agent.py
resultado: abandonada-em-favor-de-soul.md
tags: [arquivado, evolucao, injecao-codigo, run_agent, semantica]
referencia: OS_patch_run_agent.md
---

# ARQUIVADO - Briefing Patch run_agent.py via Injeção de Código

**Atenção:** Este documento representa uma abordagem TÉCNICA ABANDONADA. O sistema atual usa SOUL.md com instruções ao modelo, não alteração de código-fonte.

---

## Resumo da Evolução

| Data | Abordagem | Status |
|------|-----------|--------|
| 23/04/2026 | Injeção de código Python em run_agent.py | **ABANDONADA** |
| 25/04/2026 | SOUL.md com instruções semânticas | **IMPLEMENTADA** |

## Por que foi abandonado?

1. **Acoplamento forte:** Modificação direta no código-fonte via `str_replace`
2. **Fragilidade:** O patch quebrou com erro de indentação mista (tabs + espaços)
3. **Rollback necessário:** Reverteu via git checkout
4. **Complexidade de manutenção:** Cada update do hermes-agent exigiria re-aplicação

## Solução arquitetural atual

A funcionalidade desejada foi implementada via:

- **SOUL.md** (`~/.hermes/SOUL.md`): Instruções injetadas em cada sessão
- **datura_checkpointer.py**: Wrapper para checkpoints automáticos
- **vault_check.py**: Validação prévia antes de recall
- **search_vault.py**: Busca combinada no vault

## Conteúdo Original (Preservado para Histórico)

See abaixo a documentação original da sessão 23/04/2026:

---

## Hermes - Briefing Sessão 23/04/2026

Continuação da implementação do patch run_agent.py - injeção semântica automática

## Estado do sistema (fim de 22/04)

| Componente | Status | Detalhe |
|-----------------------|------------|---------------------------------------------|
| vault-first | OK | Funcionando, SOUL.md atualizado |
| reindex_vault | OK | 172/173 notas indexadas - MAX_CHARS=3500 |
| embeddings semanticos | OK | vec_obsidian populada, limite API corrigido |
| patch run_agent.py | PENDENTE | Tarefa desta sessão |
| populate_sessions | OK parcial | 1 sessão migrada (dry-run) |
| compactação | N/A | Parâmetro é ratio, não tokens |

## Tarefa desta sessão: patch run_agent.py

Objetivo: injetar automaticamente contexto semântico do vault antes de cada chamada ao modelo Kimi. Quando pronto, o Hermes chegará em cada conversa já sabendo o que estava sendo feito na sessão anterior.

## O que já está pronto

- get_semantic_context() criada e testada com sucesso
- HERMES_SEMANTIC_CONTEXT=true adicionado ao ~/.hermes/.env
- Ponto de injeção identificado: após memory_manager.prefetch_all()
- 172 notas indexadas e prontas para busca semântica

## O que falhou na última tentativa

O patch foi aplicado via script de injeção por linha (/tmp/inject_semantic.py) mas gerou problema de indentação mista (tabs + espaços). Foi revertido via git checkout.

## Abordagem correta para esta sessão

Usar str_replace cirúrgico - não injeção por linha. Fazer git commit de backup ANTES de qualquer mudança.

## Instruções para o Hermes

### Passo 1 - Backup obrigatório

cd ~/.hermes/hermes-agent && git add -A && git commit -m "pre-semantic-inject backup $(date +%Y%m%d_%H%M)"

### Passo 2 - Localizar ponto de injeção

```bash
grep -n "prefetch_all|original_user_message|ext_prefetch" ~/.hermes/hermes-agent/run_agent.py | head -20
```

Procurar o bloco exato que contém memory_manager.prefetch_all() e o bloco ephemeral onde ext_prefetch_cache é injetado. Anotar os números de linha.

### Passo 3 - Mostrar old_str ANTES de aplicar

Antes de qualquer str_replace: mostrar o trecho exato que será substituído (old_str completo) e o novo trecho (new_str). Aguardar confirmação lógica antes de aplicar.

### Passo 4 - O new_str deve ter este formato

```python
# --- injeção semântica ---
if os.getenv('HERMES_SEMANTIC_CONTEXT') == 'true':
    try:
        sys.path.insert(0, os.path.expanduser('~/.hermes/skills/obsidian/scripts'))
        from search_semantic import get_semantic_context
        sem_ctx = get_semantic_context(original_user_message, limit=3, max_chars=2000)
        if sem_ctx:
            notas = '\n\n'.join(f"### {n['title']}\n{n['content']}" for n in sem_ctx)
            ext_prefetch_cache += f'\n\n## Notas relevantes do vault\n{notas}'
    except Exception:
        pass
# --- fim injeção semântica ---
```

### Passo 5 - Verificar sintaxe após patch

```bash
python3 -m py_compile ~/.hermes/hermes-agent/run_agent.py && echo "OK"
```

### Passo 6 - Rollback se qualquer erro

```bash
cd ~/.hermes/hermes-agent && git checkout run_agent.py
```

Se houver erro de indentação, IndentationError, ou SyntaxError: executar rollback imediatamente. NÃO tentar corrigir manualmente. Registrar o erro e parar.

## Formato do relatório final

| Campo | O que reportar |
|------------------|------------------------------------------------------------|
| Commit de backup | Hash do commit pre-patch |
| old_str aplicado | Primeiras e últimas 2 linhas do trecho substituído |
| new_str aplicado | Primeiras e últimas 2 linhas do trecho inserido |
| Linhas alteradas | Output do git diff --stat após patch |
| Sintaxe | python3 -m py_compile - OK ou erro exato |
| Teste funcional | Resultado de get_semantic_context("embeddings") após patch |
| Rollback? | Sim/Não - se sim, motivo e estado final |

## Contexto técnico relevante

### Arquivos importantes

- run_agent.py - ~/.hermes/hermes-agent/run_agent.py (~10k linhas)
- search_semantic.py - ~/.hermes/skills/obsidian/scripts/search_semantic.py
- .env - ~/.hermes/.env (contém HERMES_SEMANTIC_CONTEXT=true)
- memory_store.db - ~/.hermes/memory/memory_store.db (vec_obsidian com 172 registros)

### Assinatura da função get_semantic_context

```python
get_semantic_context(query: str, folder: str = None, limit: int = 5, max_chars: int = 3000) -> list[dict]
```

Retorna lista de dicts com: filepath, title, folder, tags, score, content

### Variável original_user_message

Contém a mensagem original do usuário antes de qualquer processamento. É a variável correta para passar para get_semantic_context como query.

Lembrete: o patch do run_agent.py é a última pendência crítica. Quando entrar, o Hermes vai chegar em cada conversa já com contexto semântico pré-carregado. Sistema estimado em 8.0/10 - este patch leva para 9.0.

---

**Arquivado em:** 2026-04-25
**Motivo do arquivamento:** Abordagem substituída por SOUL.md
**Responsável:** Christian/Hermes
