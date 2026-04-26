---
title: Obsidian_SAVE_FIX_Conteudo_Complexo_via_CLI
date: 2026-04-25 01:23:02
updated: 2026-04-25 01:23:02
tags:
  - obsidian
  - skill
  - bugfix
  - cli
  - shell-escaping
source: 
related:
  - Projetos/Docling/SKILL
---

**Problema identificado:** Ao usar save_note.py --content com texto markdown contendo aspas duplas e quebras de linha, o bash interpreta o conteudo como parte do comando, causando erro de sintaxe.

**Solucao documentada:** Usar write_file diretamente para conteudo complexo, com frontmatter manual.

**Checklist:**
- Conteudo com aspas → write_file
- Conteudo com quebras → write_file
- Conteudo >500 chars → considerar write_file

**Skill atualizada:** Pitfall adicionado em /home/christian/.hermes/skills/obsidian/[[Projetos/Docling/SKILL|SKILL]].md

## Referências

Esta nota menciona:
- [[Projetos/Docling/SKILL]]
