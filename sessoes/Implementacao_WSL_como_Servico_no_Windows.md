---
title: Implementação WSL como Serviço no Windows
date: 2026-05-01
updated: 2026-05-01
tags:
  - wsl
  - windows
  - systemd
  - gateway
  - servico
  - autoinit
  - configuracao
tipo: base-de-conhecimento
---

# Implementação WSL como Serviço no Windows

## Resumo

Documentação completa de como o WSL2 foi configurado para operar como um serviço persistente no Windows 11, permitindo que um agente AI Gateway funcione 24/7 sem necessidade de um terminal aberto. A solução combina três camadas: configuração do WSL, systemd user service e script anchor no Windows.

**Data de implementação:** 01/05/2026
**Ambiente:** Windows 11 + WSL2 Ubuntu 24.04
**Caso de uso:** Agente AI com integração mensageira (gateway persistente)

---

## O Problema

Um agente AI Gateway precisa rodar continuamente para manter integrações com plataformas de mensageria. No entanto, o WSL2 por padrão:

1. **Encerra a VM** quando nenhum terminal está aberto (comportamento padrão do `vmIdleTimeout`)
2. **Não inicia automaticamente** com o Windows — requer que o usuário abra um terminal WSL manualmente
3. **Serviços user do systemd** são encerrados quando a sessão do usuário termina, a menos que `linger` esteja habilitado

Isso significava que, toda vez que o notebook reiniciava ou o usuário fechava o terminal, o gateway morria.

---

## A Solução — 3 Camadas

### Camada 1: Configuração do WSL (`.wslconfig` e `/etc/wsl.conf`)

#### `.wslconfig` (no diretório do usuário Windows)

Arquivo: `C:\Users\<usuario>\.wslconfig`

```ini
[wsl2]
memory=3GB            # Reserva 3GB para o Linux
processors=2          # Dedica 2 núcleos lógicos para o WSL
guiApplications=false  # Sem apps GUI (economia de recursos)
autoProxy=true        # Herda proxy do Windows
vmIdleTimeout=-1      # MANTÉM WSL rodando mesmo sem terminal aberto
```

**Ponto-chave:** `vmIdleTimeout=-1` é a configuração crítica que impede o Windows de desligar a VM WSL quando não há terminais conectados. Sem isso, toda a solução abaixo seria inútil.

#### `/etc/wsl.conf` (dentro do WSL)

Arquivo: `/etc/wsl.conf`

```ini
[boot]
systemd=true

[user]
default=<usuario>
```

**Ponto-chave:** `systemd=true` habilita o init system completo dentro do WSL2, permitindo que serviços systemd funcionem normalmente. Sem isso, não há como rodar o gateway como serviço.

---

### Camada 2: Systemd User Service + Linger

#### Service Unit: `hermes-gateway.service`

Arquivo: `~/.config/systemd/user/hermes-gateway.service`

```ini
[Unit]
Description=Hermes Agent Gateway - Messaging Platform Integration
After=network.target
StartLimitIntervalSec=600
StartLimitBurst=5

[Service]
Type=simple
ExecStart=/path/to/hermes-agent/venv/bin/python -m hermes_cli.main gateway run --replace
WorkingDirectory=/path/to/hermes-agent
Environment=PATH=/path/to/hermes-agent/venv/bin:...
Environment=VIRTUAL_ENV=/path/to/hermes-agent/venv
Environment=HERMES_HOME=/path/to/hermes-home
Restart=on-failure
RestartSec=30
RestartForceExitStatus=75
KillMode=mixed
KillSignal=SIGTERM
ExecReload=/bin/kill -USR1 $MAINPID
TimeoutStopSec=90
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=default.target
```

**Comandos de ativação:**

```bash
systemctl --user enable hermes-gateway.service
systemctl --user start hermes-gateway.service
```

#### Linger — O Segredo da Persistência

```bash
loginctl enable-linger <usuario>
```

**Por que é essencial:** O `linger=yes` garante que a instância `user@<uid>.service` do systemd inicie no boot e **continue rodando mesmo quando não há sessão de login ativa**. Sem linger, os serviços user morrem junto com a sessão.

**Verificação:**

```bash
$ loginctl show-user <usuario> | grep Linger
Linger=yes

$ systemctl --user is-enabled hermes-gateway.service
enabled
```

---

### Camada 3: Script Anchor no Windows (Auto-Start)

O systemd com linger já mantém o gateway rodando dentro do WSL, mas **a VM WSL precisa ser iniciada pelo Windows no boot**. Para isso, criamos dois scripts:

#### Script VBS Invisível: `start-hermes-anchor.vbs`

Arquivo: `C:\Users\<usuario>\Documents\Scripts\start-hermes-anchor.vbs`

```vbscript
Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "wsl.exe -d Ubuntu -- bash -c ""systemctl --user is-active hermes-gateway.service >/dev/null 2>&1 || systemctl --user start hermes-gateway.service; exec sleep infinity""", 0, False
```

**Função:** Roda o WSL em background completamente invisível (janela 0 = hidden). O `sleep infinity` mantém o processo WSL vivo indefinidamente, o que por sua vez mantém a VM WSL ativa.

#### Script CMD Completo: `Hermes-Gateway-WSL.cmd`

Arquivo: `C:\Users\<usuario>\Documents\Scripts\Hermes-Gateway-WSL.cmd`

```cmd
@echo off
:: Hermes-Gateway-WSL.cmd
:: Inicia WSL e Hermes Gateway - com âncora para manter VM viva

:: Iniciar WSL e verificar gateway
wsl -d Ubuntu -- bash -c "systemctl --user is-active hermes-gateway.service >/dev/null 2>&1 || systemctl --user start hermes-gateway.service" 2>nul

:: Aguardar gateway ficar online (max 30s)
set CHECKS=0
:healthcheck
wsl -d Ubuntu -- bash -c "systemctl --user is-active hermes-gateway.service >/dev/null 2>&1" >nul 2>&1
if %ERRORLEVEL%==0 (
    echo [%date% %time%] Hermes Gateway online >> "%USERPROFILE%\Documents\Scripts\gateway-startup.log"
    goto anchor
)
set /a CHECKS+=1
if %CHECKS% GEQ 10 (
    echo [%date% %time%] Hermes Gateway FALHOU apos 30s >> "%USERPROFILE%\Documents\Scripts\gateway-startup.log"
    goto anchor
)
timeout /t 3 /nobreak >nul
goto healthcheck

:anchor
:: Processo âncora: mantém a sessão WSL viva
wsl -d Ubuntu -- bash -c "echo 'Hermes Gateway anchor running' && exec sleep infinity"
```

**Função:** Versão completa com health check (até 10 tentativas de 3s = 30s), logging em `gateway-startup.log` e âncora `sleep infinity`.

---

## Fluxo de Inicialização Completo

```
Windows Boot
  └─> start-hermes-anchor.vbs (auto-start invisível)
       └─> wsl.exe -d Ubuntu -- bash -c "..."
            ├─> Inicia VM WSL2 (se não estiver rodando)
            ├─> systemd inicia (wsl.conf: systemd=true)
            ├─> user@<uid>.service inicia (linger=yes)
            ├─> hermes-gateway.service inicia (enabled)
            └─> sleep infinity (mantém processo WSL ativo)
                 └─> VM WSL nunca é encerrada (vmIdleTimeout=-1)
```

## Diagrama das 3 Camadas

```
┌─────────────────────────────────────────────────┐
│              CAMADA 3 — WINDOWS                  │
│  start-hermes-anchor.vbs (auto-start invisível) │
│  → wsl.exe -d Ubuntu → inicia VM WSL2          │
│  → sleep infinity → mantém VM viva              │
├─────────────────────────────────────────────────┤
│            CAMADA 2 — SYSTEMD (WSL)             │
│  loginctl linger=yes                            │
│  → user@<uid>.service ativo sem sessão          │
│  → hermes-gateway.service (enabled, restart)    │
├─────────────────────────────────────────────────┤
│             CAMADA 1 — WSL CONFIG               │
│  /etc/wsl.conf: systemd=true                    │
│  ~/.wslconfig: vmIdleTimeout=-1                 │
│  → VM WSL nunca morre por inatividade           │
└─────────────────────────────────────────────────┘
```

---

## Comandos Úteis para Gerenciamento

### Verificar status do gateway

```bash
systemctl --user status hermes-gateway.service
```

### Reiniciar o gateway

```bash
systemctl --user restart hermes-gateway.service
```

### Ver logs do gateway

```bash
journalctl --user -u hermes-gateway.service -f
```

### Verificar se o linger está ativo

```bash
loginctl show-user <usuario> | grep Linger
```

### Verificar se a VM WSL está rodando (no Windows)

```cmd
wsl --list --running
```

---

## Problemas Conhecidos e Soluções

### 1. Gateway morre ao fechar o terminal
**Causa:** `vmIdleTimeout` padrão do WSL encerra a VM.
**Solução:** `vmIdleTimeout=-1` no `.wslconfig`.

### 2. Gateway não sobe no boot do Windows
**Causa:** WSL não inicia automaticamente.
**Solução:** Script VBS no auto-start do Windows que chama `wsl.exe`.

### 3. Serviço morre ao sair da sessão
**Causa:** `linger` desabilitado.
**Solução:** `loginctl enable-linger <usuario>`.

### 4. Bridge de mensageria crash ao restart
**Causa:** O restart do systemd mata o bridge process com SIGTERM.
**Solução:** O gateway tem `Restart=on-failure` com `RestartSec=30`, então ele se recupera automaticamente. O bridge é reiniciado pelo próprio gateway.

---

## Comparação: WSL2 vs Bare-Metal

Quando o agente roda em bare-metal (servidor local com Ubuntu nativo), não precisa das Camadas 1 e 3 — o systemd nativo com linger já é suficiente. A configuração via WSL é mais complexa exatamente porque adiciona uma camada de indireção que precisa ser gerenciada.

| Aspecto | WSL2 (notebook) | Bare-metal (servidor) |
|---|---|---|
| Init system | systemd via WSL | systemd nativo |
| Linger necessário | Sim | Sim |
| vmIdleTimeout | -1 (crítico) | N/A |
| Script anchor | Necessário | N/A |
| Auto-start Windows | VBS invisível | N/A (BIOS boot) |
| Restart automático | on-failure + 30s | on-failure + 30s |

---

## Lições Aprendidas

1. **`vmIdleTimeout=-1` é tão importante quanto `systemd=true`** — sem ele, toda a cadeia systemd/linger/service é inútil porque a VM morre.
2. **O `sleep infinity` como anchor** é a forma mais simples e confiável de manter uma sessão WSL ativa sem consumir CPU.
3. **VBS com `Run(..., 0, False)`** é a forma mais limpa de rodar um script invisível no startup do Windows — sem janela, sem splash.
4. **Health check no CMD** com logging dá visibilidade do que está acontecendo durante o boot, mesmo que seja invisível para o usuário.
5. **Linger é o diferencial** entre "funciona com terminal aberto" e "funciona 24/7 sem intervenção".
