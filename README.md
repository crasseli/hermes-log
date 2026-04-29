# Hermes-Log

[![Licença: MIT](https://img.shields.io/badge/licen%C3%A7a-MIT-blue.svg)](LICENSE)
[![Código de Conduta](https://img.shields.io/badge/conduta-Contributor%20Covenant%20v2.1-purple.svg)](CODE_OF_CONDUCT.md)

Diário de bordo do desenvolvimento e evolução do **Hermes Agent** — por Christian Rasseli.

## Sobre

Este repositório **não contém código-fonte** do Hermes. Registra apenas a trajetória operacional: decisões técnicas, diagnósticos, configurações, sessões relevantes e métricas de evolução.

O Hermes Agent é um assistente de IA especializado em suporte TI N2 e pesquisa de segurança da informação, desenvolvido pela empresa Nous Research e personalizado por Christian Rasseli.

## Estrutura

| Diretório | Conteúdo |
|-----------|----------|
| `diario/` | Entradas cronológicas do diário de bordo (`YYYY-MM-DD.md`) |
| `relatorios/` | Relatórios de OS e diagnósticos finalizados |
| `sessoes/` | Resumos de sessões com decisão ou descoberta documentada |
| `metricas/` | Métricas de uso, custos, performance e evolução |
| `assets/` | Gráficos SVG e recursos visuais das sessões |

## Como usar

- Navegue pelo `diario/` para acompanhar a evolução dia a dia
- Consulte `relatorios/` para diagnósticos e ordens de serviço finalizadas
- Veja `metricas/` para dados de performance e custos operacionais
- Leia `sessoes/` para decisões técnicas e descobertas documentadas

## Sessões Documentadas

| Sessão | Título | Conteúdo |
|--------|--------|----------|
| S01E01 | Lições Aprendidas na Implementação | Erros comuns, validação de entrada, memória persistente |
| S01E02 | Testes de Visão Dedicada | Experimento com modelo multimodal NVIDIA NIM, comparação especializado vs genérico |
| S01E03 | Incidente YAML — Recuperação Inter-Agente | Diagnóstico remoto, correção de config, métricas de resolução |
| S01E04 | Testes de Transcrição de Áudio | Whisper vs modelo multimodal, thinking mode e áudio, literal vs semântico |
| S01E05 | Análise Técnica: Hermes-Desktop vs CLI + WSL2 | Projeto comunitário RedWoodOG, comparação de arquitetura, cobertura funcional, veredito |
| Tutorial | Manutenção de config.yaml | Guia genérico de validação, correção e prevenção de erros YAML |

## Convenção

- Commits em português
- Uma entrada por dia no diário
- Sessões e relatórios nomeados como `Titulo_Descritivo_YYYY-MM-DD.md`
- Sem acentos nos nomes de arquivo, underscore no lugar de espaços

## Contribuindo

Consulte o arquivo [CONTRIBUTING.md](CONTRIBUTING.md) para orientações sobre como reportar problemas, sugerir melhorias e enviar pull requests.

## Código de Conduta

Este projeto segue o [Código de Conduta](CODE_OF_CONDUCT.md) baseado no Contributor Covenant v2.1. Ao participar, você concorda em seguir suas regras.

## Segurança

Consulte [SECURITY.md](SECURITY.md) para informações sobre como reportar vulnerabilidades.

## Licença

Este projeto está licenciado sob a [Licença MIT](LICENSE).

---

Gerado automaticamente pelo Hermes Agent como parte da rotina de documentação autonômica.
