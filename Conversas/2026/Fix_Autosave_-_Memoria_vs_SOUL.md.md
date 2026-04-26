---
title: Fix Autosave - Memoria vs SOUL.md
date: 2026-04-20 00:39:27
updated: 2026-04-20 00:39:27
tags:
  - autosave
  - fix
  - obsidian
  - memoria
  - soul-md
source: hermes
related: []
---

## Problema
O autosave do Obsidian parou de funcionar. Investigação revelou que a regra estava apenas na memória dinâmica (target="memory") que tem limite de ~2.200 caracteres.

## Diagnóstico
Quando a memória atingiu 99% de capacidade, entradas menos recentes foram removidas/substituídas, incluindo a regra crítica de autosave.

## Solução
Duas camadas de persistência necessárias:

1. **Memória dinâmica** - para sessão atual (limitada)
2. **SOUL.md** (~/.hermes/SOUL.md) - system prompt carregado em TODAS as sessões

Verificado que SOUL.md já contém a seção AUTOSAVE OBSIDIAN nas linhas 29-37.

## Ação Tomada
Atualizada skill obsidian com novo pitfall documentando a lição aprendida sobre dupla persistência.

## Arquivos Modificados
- ~/.hermes/skills/obsidian/SKILL.md (novo pitfall)

## Verificação Futura
Se autosave falhar, checar:
- [ ] Existência em ~/.hermes/SOUL.md
- [ ] Capacidade da memória dinâmica
- [ ] Skill obsidian carregada corretamente