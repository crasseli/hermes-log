---
title: Script Compressor Videos Multi-Disciplinas - 3o Semestre
date: 2026-04-23 16:57:32
updated: 2026-04-23 16:57:32
tags:
  - fameesp
  - videos
  - ffmpeg
  - compressao
  - multi-disciplinas
  - automation
  - batch
source: 
related: []
---

Script PowerShell atualizado para processar videos de 4 disciplinas do 3o Semestre Redes FAMEESP.

**Disciplinas incluidas:**
1. Redes sem fio e Comunicacao Movel
2. Empreendedorismo
3. Roteamento
4. Sistemas Operacionais de Redes Abertas

**Caminhos:** Todas em G:\Meu Drive\3_Semestre_Redes_2026.1\[Disciplina]\Bloco 3 - Semanas 9 a 12

**Features:**
- Verifica automaticamente existencia de pasta output/outputs/Output/Outputs
- Cria pasta output se nao existir
- Pula disciplinas sem videos
- Relatorio detalhado por disciplina
- Arquivos originais preservados
- Configuracao: 480p @ 12fps, AAC 64kbps mono

**Arquivos:**
- comprimir_todos_videos.ps1 (script principal)
- executar_todos_videos.bat (executavel)

**Saida:** G:\Meu Drive\3_Semestre_Redes_2026.1\relatorio_compressao_videos.txt