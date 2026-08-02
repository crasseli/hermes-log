# S01E17 — Updates em Massa: winget + Chocolatey no Latitude 3400

**Data:** 01/08/2026
**Autor:** Christian Rasseli (Homelab)
**Agente:** Hermes (Hermes Desktop/Windows)
**Modelo:** deepseek-v4-flash

---

## Resumo

Auditoria de updates no Latitude 3400 (Dell, Windows 11 Pro 25H2) encontrou 22 aplicativos desatualizados. `winget upgrade --all` atualizou 19; Microsoft Edge (bloqueado no winget por mudanca de tecnologia de instalacao) foi contornado via Chocolatey com MSI 151.0.4129.59. Claude Desktop ficou pendente (pacote MSIX exigia privilegios de admin). Resultado: 20/22 apps atualizados, PostgreSQL 16.4 -> 16.14 com servico saudavel.

---

## 1. Contexto

O Latitude 3400 (hostname DESKTOP-1T36FLI, Win11 Pro build 26200) tinha 22 apps com update disponivel segundo o winget. Decisao do usuario: usar winget como gerenciador principal (visao completa), com Chocolatey como fallback.

---

## 2. Levantamento

- **winget:** 22 upgrades (Chrome, Edge, Telegram, Proton VPN 4.4.1->5.1.6, PostgreSQL 16.4->16.14, LibreOffice, 7-Zip, Notepad++, FFmpeg, ripgrep, TigerVNC, Claude, OpenCode, Temurin JRE 21, .NET 8.0.29 x2, App Installer, VC++ 2010/2015/2022)
- **choco:** gerencia apenas 9 pacotes instalados por ele; desatualizados: chocolatey 2.7.2 e registro GoogleChrome defasado

---

## 3. Execucao — winget

`winget upgrade --all --accept-source-agreements --accept-package-agreements` em background (log `C:\tmp\winget_upgrade_20260801_2015.log`).

**Resultado: 19/21 instalados.** Falhas:
- **Claude 1.24012.9** — `0x80073d28`: pacote MSIX exige privilegios de administrador; terminal nao-elevado
- **Microsoft Edge 151** — bloqueado: "novas versoes usam tecnologia de instalacao diferente" (MSIX vs MSI antigo)

---

## 4. Execucao — Chocolatey (Edge)

`choco install microsoft-edge -y` direto: **falhou** com `UnauthorizedAccessException` em `C:\ProgramData\chocolatey\lib-bad` (sem elevacao nao ha acesso a ProgramData).

**Solucao:** script `C:\tmp\choco_edge_elevated.ps1` disparado via `Start-Process powershell -Verb RunAs` (UAC):
- MSI `MicrosoftEdgeEnterpriseX64.msi` (200.27 MB) baixado, hash validado
- Edge **151.0.4129.59** instalado como MSI — sai da lista do winget
- Chrome confirmado pelo usuario em 151.0.7922.72

---

## 5. Aprendizados

1. **MSIX + winget em terminal nao-elevado = 0x80073d28.** Pacotes AppX exigem admin real no processo de instalacao; UAC do instalador nao resolve. Alternativas: shell elevada ou instalador EXE classico (Squirrel, per-user) via choco.
2. **Edge: contorno via choco.** Winget recusa upgrade quando a nova versao muda de MSI para MSIX. `choco install microsoft-edge` entrega exatamente a versao MSI alvo.
3. **choco precisa de elevacao para ProgramData.** Sem token admin, falha em `lib-bad`. Padrao correto: script + `Start-Process -Verb RunAs` com log para arquivo.
4. **Cobertura:** choco so enxerga o que instalou; winget tem visao completa — winget para auditoria, choco para casos especificos.

---

## Resultado Final

| Item | Resultado |
|---|---|
| Atualizados | **20/22** (19 winget + 1 Edge choco) |
| Pendente | Claude 1.24012.9 (decisao do usuario) |
| PostgreSQL | 16.14, servico Running |
| Reboot | VC++ 2010 x86 pediu restart |

---

## Proximos Passos

- Reboot para finalizar VC++ 2010 x86 (e PATH novo de rg/ffmpeg)
- Claude: decidir entre winget elevado, `choco install claude` (1.24012.1, EXE Squirrel) ou auto-update
- `choco upgrade chocolatey -y` (2.7.2 -> 2.7.3)

---

## Metricas da Sessao

- Tool calls estimados: ~20
- Artefatos criados: 2 logs + 1 script elevado (`C:\tmp\`)
- Apps atualizados: 20
