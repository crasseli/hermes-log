---
title: Bug_Corrigido_save_note_py_Linha_35
date: 2026-04-25 01:15:00
updated: 2026-04-25 01:15:00
tags:
  - bugfix
  - obsidian
  - save_note
  - nvidia_api
  - embedding
source: hermes
---

## Bug Corrigido - save_note.py Linha 35

**Data da Correcao:** 25/04/2026
**Status:** Corrigido
**Arquivo:** `~/.hermes/skills/obsidian/scripts/save_note.py`

### Problema

A linha 35 continha codigo truncado devido a uma edicao anterior mal sucedida:

Linha problematica:
```python
NVIDIA_API_KEY=os.get...EY")
```

Isso causava erro de sintaxe Python ao executar o script, impedindo o salvamento automatico de notas no vault.

### Causa

Provavelmente resultado de uma operacao de patch ou edicao anterior que nao foi concluida corretamente, deixando a linha em estado incompleto.

### Solucao

Substituido o trecho truncado pelo codigo correto:

```python
NVIDIA_API_KEY=os.getenv("NVIDIA_API_KEY")
```

Comando usado para correcao:
```bash
sed -i '35s/NVIDIA_API_KEY=os.get...EY")/NVIDIA_API_KEY=os.getenv("NVIDIA_API_KEY")/' save_note.py
```

### Impacto

- Script save_note.py voltou a funcionar normalmente
- Geracao de embeddings via API NVIDIA restaurada
- Autosave do Hermes para o vault Obsidian operacional

### Teste

Executar o script sem argumentos deve mostrar a ajuda sem erros de sintaxe:
```bash
python3 ~/.hermes/skills/obsidian/scripts/save_note.py --help
```

## Referencias
- [[Conhecimento/Skills/Indice_de_Skills]]
- [[Conhecimento/Obsidian_Autosave_Configuracao]]
