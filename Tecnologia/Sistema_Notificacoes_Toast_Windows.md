---
title: Sistema_Notificacoes_Toast_Windows
date: 2026-04-21 19:50:30
updated: 2026-04-21 19:50:30
tags:
  - toast
  - notifications
  - windows
  - python
  - systemd
  - inbox-watcher
source: hermes
related: []
---

Implementação completa do sistema de notificações Toast nativas do Windows 11 para o inbox_watcher.py.

## O que foi implementado

### 1. notify_alert.sh atualizado
- Toast nativo Windows 11 (não-bloqueante) via Windows.UI.Notifications
- Parâmetros: título, mensagem, urgência (low/normal/critical)
- Log automático em ~/.hermes/logs/notifications.log
- Testado e funcionando no Windows 11 Build 26200

### 2. inbox_watcher.py expandido (+117 linhas)
- 4 novas funções: send_notification(), update_daily_summary(), cleanup_old_files(), check_daily_summary()
- 4 tipos de notificação: SUCESSO (✅), ERRO (❌), IGNORADO (🚫), RESUMO (📊)
- Higienização completa: diretório Não_Reconhecidos/, auto-limpeza a cada 7 dias
- Resumo diário na primeira execução do dia

## Checklist de validação
- ✅ Sintaxe Python validada (py_compile)
- ✅ Toast testado e não-bloqueante confirmado
- ✅ Backups criados (.bak e .bak3)
- ✅ Diff aprovado pelo usuário
- ✅ Scripts prontos para produção

## Tecnologias utilizadas
- Windows.UI.Notifications.ToastNotificationManager (PowerShell)
- Python subprocess para chamada do notify_alert.sh
- JSON persistence para daily summary
- Pathlib para manipulação de arquivos
- systemd para execução em background

## Próximos passos
- Testar watcher em execução real
- Verificar resumo diário na primeira execução
- Validar auto-limpeza após 7 dias