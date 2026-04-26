---
title: Workflow_Correcao_em_Lotes_Obsidian
date: 2026-04-25 02:07:00
tags:
 - skill
 - obsidian
 - workflow
 - auditoria
 - padrao
source: skill_update
---

# Workflow de Correcao em Lotes: Uma por Vez com Aprovacao

## Contexto
Quando ha multiplas correcoes tecnicas a serem aplicadas em scripts do vault (ex: relatorio de auditoria com N bugs em varios scripts), o usuario prefere execucao sequencial e controlada.

## Padrao Identificado

1. **UMA correcao por vez** - nunca em lote automatico
2. **Report detalhado apos cada conclusao** - status completo do que foi feito
3. **Aprovacao explicita entre etapas** - aguardar resposta (sim/nao/nao) antes de prosseguir
4. **Checkpoint entre tarefas** - backup do arquivo original permite rollback

## Fluxo do Workflow

Escolher tarefa do report
       |
       v
Executar correcao especifica
       |
       v
Criar checkpoint (backup)
       |
       v
Reportar status detalhado
       |
       v
AGUARDAR APROVACAO (parada obrigatoria)
       |
       v
Proxima tarefa?

## Elementos Obrigatorios do Report

| Elemento | Incluir? |
|----------|----------|
| Nome do arquivo modificado | Sim |
| Linha(s) alterada(s) | Sim |
| Tipo de correcao | Sim (critico/logica/qualidade) |
| Validacao sintatica | Sim (py_compile) |
| Teste executado | Se aplicavel |
| Proxima tarefa sugerida | Sim |

## Checklist Entre Tarefas

- [ ] Script validado (python3 -m py_compile OK)
- [ ] Backup criado antes da modificacao
- [ ] Teste rapido executado (se houver)
- [ ] Report enviado ao usuario
- [ ] Aguardando resposta explicita

## Exemplo de Report

[TAREFA 1/11] BUG CRITICO - append_note.py
Arquivo: ~/.hermes/skills/obsidian/scripts/append_note.py
Problema: Dupla escrita - open(a) + open(w) causavam duplicacao
Correcao: Removido bloco open(a), unificado em open(w) unico
Linhas: 45-52 (removidas), 46-56 (novo bloco)
Validacao: python3 -m py_compile OK
Checkpoint: append_note.py.backup_20260425_143022 criado
Status: CONCLUIDO

Proxima tarefa sugerida: [2/11] save_note.py
Aprovar para continuar? (sim/nao/nao)

## Diferenca do Autosave

Este workflow e EXPLICITAMENTE INTERATIVO - oposto ao autosave automatico. Cada etapa requer aprovacao manual do usuario.
