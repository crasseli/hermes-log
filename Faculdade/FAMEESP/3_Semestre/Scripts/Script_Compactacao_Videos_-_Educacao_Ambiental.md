---
title: Script Compactacao Videos - Educacao Ambiental
date: 2026-04-23 19:33:06
updated: 2026-04-23 19:33:06
tags:
  - faculdade
  - ffmpeg
  - videos
  - compactacao
  - powershell
  - batch
source: 
related: []
---

Script criado para compactar videos da disciplina Educacao Ambiental e Cidadania

Configuracao:
- Audio: AAC 64kbps Mono (qualidade podcast)
- Video: H.264 480p @ 150kbps
- Minutagem: Preservada

Arquivos gerados:
1. compactar_videos_educacao_ambiental.ps1 (PowerShell)
2. compactar_videos_educacao_ambiental.bat (Batch)

Local de execucao: C:\Users\ChristianPasta de entrada: G:\Meu Drive\3_Semestre_Redes_2026.1\Educação Ambiental e Cidadania.2026.1\Bloco 3 - Semanas 9 a 12
Pasta de saida: ...\output

Videos a processar:
- A Camada de Ozonio.mp4 (6.5MB)
- A Hipotese Gaia.mp4 (8.6MB)
- Efeito Estufa.mp4 (7.3MB)
- Matrizes Energeticas I.mp4 (9.2MB)
- v4-educacao-ambiental-e-cidadania.mp4 (9.7MB)

Comando ffmpeg usado:
ffmpeg -i input.mp4 -c:v libx264 -crf 28 -preset fast -vf scale=-2:480 -b:v 150k -c:a aac -b:a 64k -ac 1 -ar 44100 -movflags +faststart -y output.mp4