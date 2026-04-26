---
title: Config Voice Mode
date: 2026-04-24 10:54:05
updated: 2026-04-24 10:54:05
tags:
  - hermes
  - autosave
  - voice-mode
  - configuracao
source: 
related: []
---

Ativacao do Voice Mode no Hermes:\n\n## Alteracoes Realizadas\n- voice_enabled: false → true (linha 154)\n\n## Dependencias Instaladas\n- sounddevice 0.5.5 (Python)\n- cffi 2.0.0\n\n## Pendencias\n- portaudio19-dev (apt) - aguardando sudo\n- espeak-ng (apt) - aguardando sudo\n\n## Configuracao Atual\n- STT: local (faster-whisper, base model)\n- TTS: edge (pt-BR-DonatoNeural)\n- Record key: Ctrl+B\n- Silence threshold: 200\n- Silence duration: 3.0s\n\n## Dependencias ja OK\n- ffmpeg ✓\n- libopus0 ✓\n- numpy ✓