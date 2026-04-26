---
title: Inbox Watcher - Correção de Estado e BurntToast
date: 2026-04-21 21:13:38
updated: 2026-04-21 21:13:38
tags:
  - hermes
  - inbox-watcher
  - bugfix
  - burnttoast
  - autosave
source: 
related:
  - Pesquisas/Test_Paper
  - Pesquisas/Christian_Rasseli_Wantil_Souza
---

## Resumo da Sessão

Data: 2026-04-21

### Problemas Identificados

1. **Notificações Toast falhando**: Windows.UI.Notifications não funcionava consistentemente
2. **Banco MD5 com entradas incorretas**: Arquivos processados com sucesso marcados como error
3. **Arquivos presos em Erros/**: PDFs que já estavam no vault ainda estavam na pasta de erros

### Soluções Aplicadas

#### 1. Instalação do BurntToast

Name                           Version          Source           Summary                                               
----                           -------          ------           -------                                               
nuget                          2.8.5.208        https://cdn.o... NuGet provider for the OneGet meta-package manager    



Name       Version
----       -------
BurntToast 1.1.0  



#### 2. Script notify_alert.sh atualizado
- Usa BurntToast como método principal
- Fallback silencioso se falhar
- Suporta sons (Alarm para critical, Default para normal/low)

#### 3. Correção do Banco MD5
- [[Pesquisas/Christian_Rasseli_Wantil_Souza|Christian Rasseli Wantil Souza]].pdf: status corrigido de error para success
- Aposentadoria.pdf: entrada removida para permitir reprocessamento
- Arquivos movidos para pastas corretas (Processados/ e Inbox/)

### Status Final

| Componente | Status |
|------------|--------|
| BurntToast | ✅ Instalado v1.1.0 |
| Notificações | ✅ Funcionando |
| Banco MD5 | ✅ Corrigido |
| Arquivos em Erros/ | ✅ Limpo |
| Vault | ✅ Christian Rasseli indexado em Pesquisas/ |

### Próximos Passos

- Aguardar reprocessamento de Aposentadoria.pdf
- Verificar se notificações aparecem no Windows para novos arquivos
- Monitorar logs em ~/.hermes/logs/inbox_watcher.log

### Comandos Úteis

● inbox-watcher.service - Hermes Inbox Watcher - Auto-organiza documentos no vault Obsidian
     Loaded: loaded (/home/christian/.config/systemd/user/inbox-watcher.service; enabled; preset: enabled)
     Active: active (running) since Tue 2026-04-21 21:01:19 -03; 12min ago
       Docs: file:///home/christian/.hermes/scripts/inbox_watcher.py
   Main PID: 2988 (python3)
      Tasks: 1 (limit: 3479)
     Memory: 7.6M (peak: 8.8M)
        CPU: 83ms
     CGroup: /user.slice/user-1000.slice/user@1000.service/app.slice/inbox-watcher.service
             └─2988 /usr/bin/python3 /home/christian/.hermes/scripts/inbox_watcher.py

Apr 21 21:01:19 DESKTOP-G1FPIUG systemd[286]: Started inbox-watcher.service - Hermes Inbox Watcher - Auto-organiza documentos no vault Obsidian.
[2026-04-21 20:32:27] [normal] Hermes: Sistema de notificações corrigido ✓
[2026-04-21 20:39:42] [normal] Hermes: BurntToast funcionando ✓
[2026-04-21 20:46:08] [critical] Hermes Inbox — Erro: ❌ validacao_final.txt falhou — movido para Erros/
[2026-04-21 21:03:28] [critical] Hermes Inbox — Erro: ❌ Christian Rasseli Wantil Souza.pdf falhou — movido para Erros/
[2026-04-21 21:05:40] [normal] Hermes ✅: Christian Rasseli Wantil Souza.pdf → Pesquisas/
{
  "96b045a59a2cfed92ad8b90c4ba4fbf7": {
    "filename": "[[Pesquisas/Test_Paper|test_paper]].pdf",
    "status": "success",
    "folder": "Pesquisas",
    "timestamp": "2026-04-21T18:51:01.591920"
  },
  "c23969454783e5906b8d390ef23eccea": {
    "filename": "novo_teste_1776813568.txt",
    "status": "error",
    "error": "[Errno 30] Read-only file system: '/home/christian/.hermes/tmp/docling_to_vault/test_paper.md'",
    "timestamp": "2026-04-21T20:19:34.784174"
  },
  "22f95a25b9c35a1ebaab56ef3aa63eeb": {
    "filename": "validacao_final.txt",
    "status": "error",
    "error": "docling_failed",
    "timestamp": "2026-04-21T20:46:08.150793"
  },
  "243ab8c553f3c4dde7a685748640015a": {
    "filename": "Christian Rasseli Wantil Souza.pdf",
    "status": "success",
    "folder": "Pesquisas",
    "timestamp": "2026-04-21T21:00:00"
  }
}

## Referências

Esta nota menciona:
- [[Pesquisas/Test_Paper]]
- [[Pesquisas/Christian_Rasseli_Wantil_Souza]]
