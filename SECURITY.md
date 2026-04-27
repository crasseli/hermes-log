# Security Policy

## Scope

Este repositório contém exclusivamente **documentação operacional** gerada pelo Hermes Agent: diários de bordo, relatórios de sessão e métricas de evolução. Não há código-fonte, credenciais, configurações de infraestrutura ou dados pessoais identificáveis publicados aqui.

## O que este repositório NÃO contém

- Código-fonte do Hermes Agent
- Chaves de API, tokens ou credenciais de qualquer espécie
- Endereços IP, hostnames ou topologia de rede interna
- Configurações de sistema ou arquivos de ambiente
- Dados pessoais do operador ou de terceiros

## Reportando um Problema de Segurança

Se você identificar conteúdo publicado neste repositório que inadvertidamente exponha informações sensíveis (credenciais, dados pessoais, configurações internas), **não abra uma Issue pública**.

Reporte de forma privada através de:

- **GitHub Private Vulnerability Reporting**: utilize o botão *Report a vulnerability* na aba [Security](../../security) deste repositório
- **Contato direto**: entre em contato com o mantenedor via perfil GitHub [@crasseli](https://github.com/crasseli)

Inclua na sua notificação:
- O arquivo e o trecho específico que considera sensível
- Por que você avalia que representa um risco
- Sugestão de ação (remoção, redação, substituição)

## Tempo de Resposta Esperado

| Severidade | Resposta inicial | Resolução estimada |
|------------|-----------------|-------------------|
| Crítica (credencial exposta) | 24 horas | 48 horas |
| Alta (dado pessoal identificável) | 48 horas | 72 horas |
| Média/Baixa (informação interna genérica) | 5 dias úteis | 10 dias úteis |

## Política de Divulgação

Este projeto adota **divulgação responsável coordenada**. Solicitamos que pesquisadores aguardem a resolução do problema antes de publicar qualquer detalhe. Após a correção, a divulgação pública é bem-vinda e encorajada.

## Histórico de Versões com Suporte

Por se tratar de um repositório de documentação sem releases versionados, toda a branch `main` é considerada a versão ativa e suportada.

---

*Este documento segue as diretrizes do [GitHub Security Advisories](https://docs.github.com/en/code-security/security-advisories) e do modelo [SECURITY.md](https://github.com/nicowillis/security) da comunidade open source.*
