# Hermes-Log

Diario de bordo do desenvolvimento e evolucao do Hermes Agent na FAMEESP.

Este repositorio NAO contem codigo-fonte do Hermes. Registra apenas a trajetoria operacional: decisoes tecnicas, diagnosticos, configuracoes, sessoes relevantes e metricas de evolucao.

## Estrutura

| Diretorio | Conteudo |
|-----------|----------|
| `diario/` | Entradas cronologicas do diario de bordo (YYYY-MM-DD.md) |
| `relatorios/` | Relatorios de OS e diagnosticos finalizados |
| `sessoes/` | Resumos de sessoes com decisao ou descoberta documentada |
| `metricas/` | Metricas de uso, custos, performance e evolucao |

## Convencao

- Commits em portugues
- Uma entrada por dia no diario
- Sessoes e relatorios nomeados como `Titulo_Descritivo_YYYY-MM-DD.md`
- Sem acentos nos nomes de arquivo, underscore no lugar de espacos

## Origem

Gerado automaticamente pelo Hermes Agent (cron job) como parte da rotina de documentacao autonomica.
