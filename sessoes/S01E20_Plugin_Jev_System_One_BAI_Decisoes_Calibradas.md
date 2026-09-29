# S01E20 — Plugin Jev (System One) na B.AI — Decisoes Calibradas no Hermes

**Data:** 28/09/2026
**Autor:** Christian Rasseli (Homelab)
**Agente:** Hermes (DELL Latitude 3400/Windows)
**Modelo:** qwen3.8-flash via B.AI (orquestrador) + jev-1.13.0 via B.AI (decisor)

---

## Resumo

Avaliamos o ecossistema de decisoes calibradas ("System One") para o Hermes, instalamos o plugin `jev` (hermes-jev-plugin v0.1.0) com patch proprio para rotear pela B.AI, validamos as 4 tools ao vivo e registramos a politica de gates. Resultado: triagem N2, gate anti-retry e revisao de mudanca agora tem julgamento probabilistico fora do LLM de texto, custando fracao de centavo por decisao.

---

## 1. Contexto

Hermes decide tudo por LLM generico: lento, caro e sem probabilidade calibrada. TypeSafe Jev e um modelo de decisao que NAO gera texto — avalia perguntas tipadas (noul/choice/score) contra um state e devolve distribuicao de probabilidade + confianca. O plugin `ajensenwaud/hermes-jev-plugin` expoe isso ao Hermes como 4 tools.

## 2. Pesquisa comparativa

Cinco alternativas MCP mapeadas (jkudish/jev-mcp 11 tools, thedv91 5 tools com pipeline de review, minhgv 8 tools de coding-loop, wangkuangkuang Python 7 tools, daf-jev toolkit com calibracao ECE/Brier). Nenhuma official da NousResearch — os 5 plugins oficiais nao cobrem decisao. Decisao: plugin nativo enxuto > MCP rico, porque a **B.AI rejeita parametros extras do TypeSafe** (escape_hatch → HTTP 400) e os MCPs de 11 tools dependem deles.

## 3. Implementacao

1. `hermes plugins install ajensenwaud/hermes-jev-plugin` (clone em `plugins/jev`, source=git).
2. Patch em `client.py`:
   - `_api_url()`: com `B_AI_API_KEY` no `.env` → `https://api.b.ai/v1/decisions`; senao TypeSafe direto; `JEV_API_BASE_URL` sobrescreve.
   - `_get_key()`: fallback `TYPESAFE_API_KEY` → `B_AI_API_KEY` (mesma chave da sessao).
3. `hermes plugins enable jev` — tools carregam na proxima sessao (confirmado no reboot).

## 4. Testes ao vivo (pos-reboot, modelo jev-1.13.0 via B.AI)

| Tool | Cenario | Resultado |
|------|---------|-----------|
| jev_check | diff remove verify_signature? | 0.85 → `yes` |
| jev_score | severidade do diff | 3.9/4 (Critico), conf 0.91 |
| jev_route | ConnectionRefused db:5432 pos-reboot | `network` 0.80, conf 0.74 |
| jev_evaluate | gate de PR, 4 perguntas | blocks_merge 0.73 / has_tests 0.04 / sec_risk 0.79 / sev 1.88 |

Custo do evaluate completo: 391 tokens de entrada. As 4 perguntas rodam em paralelo numa chamada.

## 5. Politica de gates adotada

- `yes_probability >= 0.8` ou `confidence >= 0.7` → age automaticamente
- `0.3–0.7` → mostra a distribuicao ao operador, pede direcao
- `<= 0.2` → age na negacao
- Nunca hard-branch em ~0.55 (moeda ao ar)
- Threshold calibrado em caso real → pinar `jev-1.13.0` (alias `jev-latest` pode mover)

## 6. Falha de protocolo e correcao

Primeiro registro pos-teste pulou a camada CP (Honcho) — foi direto ao vault (MP). O operador cobrou; as duas conclusoes (config + validacao) foram gravadas no Honcho na hora e confirmadas por `list` (indexacao semantica e assincrona via cron insights-extract 120min — `search` so reflete depois do tick).

---

## Resultado Final

| Item | Estado |
|------|--------|
| Plugin jev | ativo, source git, v0.1.0 patched |
| 4 tools | validadas ao vivo via B.AI |
| Chave | reutilizada B_AI_API_KEY existente (zero custo novo) |
| Docs | vault `Tecnologia/Configuracoes/jev-plugin_config.md` + Honcho + hermes-log |
| Risco conhecido | `hermes plugins update jev` sobrescreve o patch (backup em plugins-backup/; reaplicacao < 1 min) |

---

## Proximos Passos

- Usar jev_check como gate anti-retry em toda falha de comando
- Triagem N2 de tickets com jev_route + jev_score antes de propor acao
- Avaliar pin de versao se comecar a calibrar thresholds
- LP pendente das sessoes 06/08 e 06/09 no backlog do hermes-log

---

## Metricas da Sessao

- Tool calls estimados: ~35
- Artefatos criados: 1 plugin patchado, 1 nota vault, 2 conclusoes Honcho, 2 arquivos hermes-log
- Testes: 4/4 ferramentas validadas (5/5 chamadas OK)
- Custo incremental: R$ 0 (chave existente)
