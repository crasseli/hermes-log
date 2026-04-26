---
title: WSL Voice Mode Setup
date: 2026-04-24 11:16:41
updated: 2026-04-24 11:16:41
tags:
  - wsl
  - audio
  - voice
  - hermes
  - autosave
source: 
related: []
---

Configuracao de Voice Mode no WSL: Instalado libportaudio2, pulseaudio, alsa-utils, sounddevice e numpy. Criado .asoundrc com configuracao ALSA->PulseAudio. PulseAudio rodando via systemd user. Limitacao identificada: WSL2 requer suporte de audio no Windows host (WSL2_AUDIO_SUPPORT=1 ou PulseAudio para Windows) para captura de audio funcionar.