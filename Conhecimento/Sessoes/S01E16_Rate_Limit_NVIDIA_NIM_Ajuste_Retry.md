# S01E16 - Ajuste de Rate Limit NVIDIA NIM via Retry Config

**Data:** 18/05/2026  
**Status:** ✅ Concluído  
**Tipo:** Troubleshooting / Otimização de API

---

## Resumo Executivo

**Problema:** Erros HTTP 429 (Too Many Requests) recorrentes da NVIDIA NIM API durante requisições ao modelo `qwen/qwen3.5-397b-a17b` (400B MoE).

**Solução:** Ajuste agressivo dos parâmetros de retry no `config.yaml` do Hermes, aumentando delays para reduzir frequência de requisições.

**Resultado:** Mecanismo de retry calibrado para backoff exponencial com delays maiores, reduzindo probabilidade de gatilho de rate limit.

---

## Diagnóstico Inicial

### Monitoramento (últimas 1000 linhas do agent.log)
| Métrica | Valor |
|---------|-------|
| Erros 429 encontrados | 146 |
| Tentativas de retry | 104 |
| Retries bem-sucedidos | 0 (100% falha) |

### Padrão de Falhas (Fase 1)
- 56 ocorrências na tentativa 1/3
- 22 ocorrências na tentativa 2/3
- 3 ocorrências na tentativa 3/3

**Conclusão:** O mecanismo de retry estava funcional (backoff exponencial), mas o rate limit da NVIDIA era tão agressivo que mesmo após 3 retries, a API continuava retornando 429.

---

## Solução Implementada

### Fase 1 - Implementação Inicial (09:00)
```yaml
agent:
  api_max_retries: 10      # Aumentado de 3 → 10
  retry_base_delay: 1.0    # Base: 1 segundo
  retry_max_delay: 60      # Teto: 60 segundos
  retry_jitter: true       # Adiciona aleatoriedade
```

**Resultado:** Mecanismo de retry funcional, mas rate limit persiste.

### Fase 2 - Ajuste de Delays (09:22)
```yaml
agent:
  api_max_retries: 10      # Mantido
  retry_base_delay: 5.0    # Aumentado: 1.0 → 5.0 segundos
  retry_max_delay: 120     # Aumentado: 60 → 120 segundos
  retry_jitter: true       # Mantido
```

**Justificativa:** Reduzir frequência de requisições para evitar gatilho de rate limit da NVIDIA.

### Backoff Resultante (Fase 2)
| Tentativa | Janela de Tempo |
|-----------|-----------------|
| 1 | 5-10s |
| 2 | 10-20s |
| 3 | 20-40s |
| 4 | 40-80s |
| 5+ | 80-120s (teto) |

### Comparativo: Fase 1 vs Fase 2
| Parâmetro | Fase 1 | Fase 2 (Atual) | Mudança |
|-----------|--------|----------------|---------|
| `retry_base_delay` | 1.0s | 5.0s | +400% |
| `retry_max_delay` | 60s | 120s | +100% |
| `api_max_retries` | 10 | 10 | Mantido |

---

## Próximos Passos

1. **Reiniciar o Hermes** para aplicar as novas configurações:
   ```bash
   /reset
   ```

2. **Monitorar** por 24h usando:
   ```bash
   python C:/Users/User/AppData/Local/hermes/monitor_rate_limit.py
   ```

3. **Ajustar se necessário** - Se ainda houver muitos erros 429, considerar:
   - Aumentar ainda mais o `retry_base_delay` para 10s
   - Reduzir frequência de mensagens no Telegram
   - Solicitar aumento de rate limit na NVIDIA
   - Implementar credential pooling (múltiplas API keys)

---

## Lições Aprendidas

1. **Gateway.log vs Agent.log:** O gateway.log não grava erros de API, apenas conexões de plataforma. O agent.log contém os erros 429 e retries.

2. **Backoff exponencial:** Funciona bem, mas precisa de delays iniciais maiores para APIs com rate limit agressivo.

3. **Credential pooling:** Seria a próxima solução se o ajuste de delays não for suficiente (múltiplas API keys).

---

## Arquivos Modificados

1. `C:\Users\User\AppData\Local\hermes\config.yaml` - Configurações de retry
2. `C:\Users\User\AppData\Local\hermes\RATELIMIT_NVIDIA_RESOLUCAO.md` - Documentação técnica
3. `C:\Users\User\AppData\Local\hermes\monitor_rate_limit.py` - Corrigido para usar agent.log
4. `E:\Obsidian\Cofre\Hermes\Conhecimento\Sessoes\S01E16_Rate_Limit_NVIDIA_NIM_Ajuste_Retry.md` - Esta nota

---

## Referências

- **Modelo:** qwen/qwen3.5-397b-a17b (400B MoE)
- **Provider:** NVIDIA NIM
- **Endpoint:** https://integrate.api.nvidia.com/v1
- **Sessão relacionada:** `resumo_sessao_18052026.md`

---

**Tags:** #NVIDIA #NIM #API #RateLimit #Retry #Troubleshooting #Homelab
