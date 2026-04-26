---
title: Skill Obsidian Atualizada - Suporte a CLI
date: 2026-04-19 22:55:35
updated: 2026-04-19 22:55:35
tags:
  - obsidian
  - cli
  - uri-scheme
  - update
source: 
related: []
---

## Atualizacao da Skill Obsidian

Adicionado suporte a CLI nativa do Obsidian + URI scheme fallback.

### Novo Script

**open_in_obsidian.py** - Abre notas diretamente no app:
- Tenta CLI nativa primeiro (se disponivel)
- Fallback automatico para URI scheme
- Converte caminhos WSL → Windows automaticamente
- Suporte a flag --wait para sincronizacao

### Como Funciona



### URI Scheme

Formato: 

Executado via: 

### CLI Nativa

Requer:
1. Obsidian 1.12.4+ (ativar em Settings → General → CLI)
2. CLI registrada no PATH do Windows
3. Obsidian em execucao

### Comparativo

| Recurso | Scripts Python | CLI Nativa | URI |
|---------|---------------|------------|-----|
| Criar nota | ✅ Offline | ✅ Online | ❌ Nao |
| Abrir nota | ✅ Via URI | ✅ Nativo | ✅ Sim |
| Buscar full-text | ✅ Custom | ✅ Nativo | ❌ Nao |
| Funciona sem Obsidian | ✅ Sim | ❌ Nao | ✅ Sim (abre) |

### Workflow Completo

Salvar → Daily → Abrir (opcional)

