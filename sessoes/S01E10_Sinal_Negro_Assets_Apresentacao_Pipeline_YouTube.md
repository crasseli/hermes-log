# S01E10 — Canal Sinal Negro: Assets, Apresentação e Pipeline YouTube Upload

**Data:** 2026-05-02  
**Autoria:** Christian Rasseli, Cohen (agente no M70q), Hermes (agente no notebook DELL)  
**Categoria:** Infraestrutura de Canal + Validação Pipeline

## Contexto

O canal Sinal Negro (YouTube @sinalnegro) nasceu em 02/05/2026 — anteriormente chamado CanalDark, foi renomeado para refletir a identidade cyberpunk de ficção científica narrada por vozes de IA com roteiro humano. O primeiro episódio já está no ar: **https://youtu.be/1tA4jRknUlE**

O canal precisava de identidade visual completa, apresentação na comunidade Telegram e um pipeline validado para upload de vídeos via Composio. Este episódio documenta o nascimento do canal, a criação dos assets, a configuração do MCP Composio no Hermes DELL, a apresentação na comunidade e a validação definitiva do pipeline de upload.

## Nascimento do Canal

- **Nome**: Sinal Negro (ex-CanalDark)
- **Handle**: @sinalnegro
- **URL**: https://www.youtube.com/@sinalnegro
- **Primeiro episódio**: https://youtu.be/1tA4jRknUlE
- **Identidade visual**: Banner com onda verde sobre circuit board, avatar circular "SN" em ciano sobre fundo azul escuro, tagline "TRANSMISSÃO INTERCEPTADA"
- **Paleta**: #0A0A1A (fundo), #00F0FF (ciano), #FF00AA (magenta), #CC0000 (vermelho), #00FF40 (verde), #E0E0E0 (branco sujo)
- **Fontes**: Neuropol/Orbitron (títulos), Rajdhani (corpo/HUD)
- **Personagens**: Cohen (mordomo digital, M70q), Hermes (analista N2, Dell), Narrador
- **Conceito**: Ficção cyberpunk que nasceu de infraestrutura real — dois agentes de IA com personalidades distintas, roteiro escrito por Christian Rasseli, vozes e visuais gerados por IA

## Assets Visuais — Geração via Composio + Gemini

- **13 assets gerados** via GEMINI_GENERATE_IMAGE (Composio MCP):
  - 3 logos (1920x1080, 800x800, 512x512)
  - 5 ícones 256x256 (sininho, antena, caveira, olho, cadeado)
  - 4 cards 1920x1080 (transmissão, capítulo, deep web, barra inferior)
  - 1 end card 1920x1080
- **Pós-processamento Pillow**: redimensionamento LANCZOS, pixels RGB < (15,15,30) → transparente, conversão para PNG RGBA
- **Transferência SCP** para M70q: `/mnt/storage/CanalDark/canal_assets/sinal_negro/`
- **Paleta validada**: `#0A0A1A`, `#00F0FF`, `#FF00AA`, `#CC0000`, `#00FF40`, `#E0E0E0`

## MCP Composio no Hermes DELL

- Configurado no `config.yaml` com URL `https://connect.composio.dev/mcp`
- Transport: `streamablehttp_client` (nativo do Hermes v0.12.0)
- **Bug de indentação YAML**: `x-consumer-api-key` precisa estar dentro de `headers:` com 6 espaços de indentação. Se ficar como sibling com 4 espaços, o header não é enviado e resulta em HTTP 401
- 7 tools disponíveis: COMPOSIO_MANAGE_CONNECTIONS, COMPOSIO_MULTI_EXECUTE_TOOL, COMPOSIO_REMOTE_BASH_TOOL, COMPOSIO_REMOTE_WORKBENCH, COMPOSIO_SEARCH_TOOLS, COMPOSIO_WAIT_FOR_CONNECTIONS, COMPOSIO_GET_TOOL_SCHEMAS
- GEMINI_GENERATE_IMAGE acessado via COMPOSIO_MULTI_EXECUTE_TOOL com `tool_slug` (não `tool`)

## Apresentação do Hermes na Comunidade Telegram

- **Comunidade**: Café com Dados e Gatos (chat_id: -1003797971645)
- **Aba Hermes**: topic_id 744
- **Bot**: @Hermes3400_bot (ID: 8633367645)
- **Áudio**: Edge TTS com voz `pt-BR-AntonioNeural` + ffmpeg filter chain robótica
  - `atempo=1.25, aecho=0.8:0.88:60:0.27, lowpass=f=2500, highpass=f=300, acompressor, volume=1.2, apad=whole_dur=0.5`
  - Saída: OGG codec libopus, 42s
- **Envio**: curl Bot API `sendVoice` com message_thread_id=744
- **Regra**: Hermes NÃO responde mensagens diretas na comunidade. Só posta quando Christian solicita

## Banner de Lançamento

- Gerado via Gemini com avatares do Cohen e Hermes como referência
- Composição: título SINAL NEGRO em ciano neon, subtítulo em magenta, avatares simétricos, onda de sinal central
- Postado na comunidade com caption curto + links (YouTube e episódio)
- **Pitfall Telegram**: caption de sendPhoto tem limite de 1024 chars. Usar caption curto + mensagem separada para textos longos

## Pipeline YouTube Upload — VALIDADO

### O Problema

O Cohen tentava fazer upload de vídeos gerados pelo Gemini passando a URL S3 diretamente como `videoFilePath`. A tool `YOUTUBE_UPLOAD_VIDEO` exige caminho LOCAL no filesystem.

### A Solução

1. Gerar vídeo via Gemini → receber URL S3 na resposta
2. **Baixar o vídeo da URL S3** para disco local: `wget -O /mnt/storage/CanalDark/video.mp4 "$S3URL"`
3. Passar caminho local no `videoFilePath` da tool

### Validação Real

- Vídeo de teste (3s, 23KB) subiu com sucesso como privado no canal Sinal Negro
- videoId: n6lutzERtwA
- Resultado: `successful=true`, `uploadStatus=uploaded`
- Deletado posteriormente via `YOUTUBE_DELETE_VIDEO`

### Regras Invioláveis

- `videoFilePath` é SEMPRE um caminho LOCAL — nunca URL
- URLs S3 do Gemini são para DOWNLOAD, não para upload direto
- Sempre subir como private primeiro, mudar para public/unlisted depois de checar
- categoryId 22 = People & Blogs (padrão Sinal Negro)
- Conexão YouTube ativa: `youtube_petite-mudd` (Christian Rasseli)

### Skill Criada

- `youtube-upload-composio` — instalada nos dois agentes (Hermes + Cohen)
- Contém passo a passo, erros conhecidos e soluções

## Composio CLI no Cohen

- Login falhou via flow OAuth (CLI key expirava antes da autorização no browser)
- Login via `--user-api-key` dava HTTP 401
- **Solução**: copiar `~/.composio/user_data.json` do Hermes com mesma API key (`uak_...`)
- Versão 0.2.27 instalada (0.2.28 disponível mas `composio upgrade` não aplicou)
- PATH: `~/.composio/` precisa ser exportado em sessões SSH não-interativas

## Lições Aprendidas

1. **YOUTUBE_UPLOAD_VIDEO exige caminho local** — isso não está documentado claramente no Composio e causa confusão recorrente
2. **Indentação YAML é crítica** — 2 espaços de diferença na indentação do `x-consumer-api-key` causam HTTP 401 silencioso
3. **Composio CLI login pode ser contornado** — copiando user_data.json entre agentes da mesma organização
4. **Telegram sendPhoto caption limit** — 1024 chars. Separar em duas mensagens quando necessário
5. **Gemini TTS via Composio** — geração funciona (retorna base64 PCM 24kHz) mas extração do sandbox é complexa. Edge TTS local é fallback funcional

## Decisões Tomadas

- Mesma chave API Composio usada nos dois agentes (uso esporádico, por enquanto só imagens)
- Edge TTS como fallback para áudio (Gemini TTS sandbox extraction problemático)
- Bot Hermes no Telegram NÃO responde diretamente membros — só posta quando Christian solicita
- Skill youtube-upload-composio como fonte de verdade para o pipeline de upload

---

Documentado por: Hermes — 02/05/2026
