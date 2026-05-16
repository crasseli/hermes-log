# Sessão: Certificação Completa + Otimização Delegação

> **Data:** 2026-05-15 | **Módulo:** Certificação + Performance

## Decisões Documentadas

### 1. Otimização de Delegação de Subagentes
- **Problema:** Subagentes herdavam todos os toolsets MCP do pai (~36K tokens de schema inútil)
- **Mudança:** Modelo de delegação trocado de GLM-5.1 para Nemotron Nano 9B (NVIDIA NIM)
- **Config aplicada:** `inherit_mcp_toolsets=false`, `reasoning_effort=low`, `default_toolsets=[terminal]`
- **Resultado:** -83% input tokens, -24% tempo por subagente
- **Modelo rejeitado:** DeepSeek V4 Flash (latência NIM inaceitável: 175s vs 20s)
- **Skill criada:** `delegation-optimization`

### 2. Programa de Certificação Completo
- Python PCEP→PCAP→PCPP: 92/100
- CCNP ENCOR + DevNet: 8.6/10
- CyberOps Associate: 8.8/10
- 8 skills criadas/atualizadas, 5 scripts validados

### 3. Pipeline de Recall Ampliado
- Ponteiros de ativação adicionados para CCNA/CCNP, CyberOps e Python
- Gatilhos por palavras-chave obrigatórias com fallback para skill_view
- Pipeline v1 (fact #391) continua como referência

## Descobertas

- `config.yaml` tem `reasoning_effort` em 2 posições (linha ~50 e ~372) — sed por número de linha para mudança precisa
- `yaml.dump()` corrompe config.yaml — NUNCA usar. Replace direto no conteúdo como string
- Gateway restart necessário após mudanças na seção `delegation`
- `bool` é subclasse de `int` em Python — `isinstance(True, int)` retorna True
- Exponenciação é associativa à direita: `2**3**2 = 512`, não 64
- `itertools.groupby` requer dados previamente ordenados pela chave de agrupamento

## Métricas

| Métrica | Valor |
|---|---|
| Skills criadas/atualizadas | 9 |
| Scripts validados | 5 |
| Facts no holographic | 11 (#407–#417) |
| Notas no Vault | 7 |
| Provas respondidas | 4 |
| Tokens economizados/subagente | -83% |
