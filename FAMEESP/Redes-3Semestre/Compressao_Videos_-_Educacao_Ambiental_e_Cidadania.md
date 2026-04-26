# Compressao de Videos - Educacao Ambiental e Cidadania

**Data:** 23/04/2026
**Status:** CONCLUIDO

## Resumo da Operacao

Compactacao de videos da disciplina Educacao Ambiental e Cidadania.2026.1 (Bloco 3 - Semanas 9 a 12) com foco em qualidade de audio podcast mono.

## Videos Processados

| Video | Tamanho Original | Tamanho Compactado | Reducao |
|-------|-----------------|-------------------|---------|
| A Camada de Ozonio.mp4 | ~479MB | 6.3MB | 98.7% |
| A Hipotese Gaia.mp4 | ~490MB | 8.3MB | 98.3% |
| Efeito Estufa.mp4 | ~466MB | 7.0MB | 98.5% |
| Matrizes Energeticas I.mp4 | ~529MB | 8.8MB | 98.3% |
| v4-educacao-ambiental-e-cidadania.mp4 | ~55MB | 9.3MB | 83.1% |

**Espaco total liberado:** ~2.0GB

## Configuracao FFmpeg Utilizada

ffmpeg -i input.mp4 -c:v libx264 -crf 28 -preset fast -vf scale=-2:480 -b:v 150k -c:a aac -b:a 64k -ac 1 -ar 44100 -movflags +faststart -y output.mp4

Parametros:
- Video: H.264, CRF 28, 480p, 150kbps
- Audio: AAC, 64kbps, Mono, 44.1kHz
- Minutagem: Preservada integralmente

## Scripts Criados

1. PowerShell: C:/Users/Christian/compactar_videos_educacao_ambiental.ps1
2. Batch: C:/Users/Christian/compactar_videos_educacao_ambiental.bat

## Localizacao dos Arquivos

- Entrada: G:/Meu Drive/3_Semestre_Redes_2026.1/Educacao Ambiental e Cidadania.2026.1/Bloco 3 - Semanas 9 a 12
- Saida: Mesma pasta (arquivos substituiram os originais)
- Backup: backup_originals (removido apos validacao)

## Status dos Arquivos

- Todos os videos compactados
- Originais removidos
- Qualidade de audio verificada
- Minutagem preservada
- Pasta organizada

## Observacoes

- Videos ja estavam compactados de operacao anterior
- Scripts mantidos para uso futuro em outras disciplinas
- Qualidade de audio priorizada para consumo tipo podcast
- Video reduzido para 480p (suficiente para conteudo educacional)

Tags: faculdade, fameesp, videos, ffmpeg, compactacao, educacao-ambiental, 3-semestre
