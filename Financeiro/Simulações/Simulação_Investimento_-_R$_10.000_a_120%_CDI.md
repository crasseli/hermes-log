---
title: Simulação Investimento - R$ 10.000 a 120% CDI
date: 2026-04-23 16:05:32
updated: 2026-04-23 16:30:00
tags:
 - investimento
 - renda-fixa
 - CDI
 - simulação
 - IR
 - Banco_Central
 - SELIC
source: 
  - "Banco Central do Brasil - Taxa SELIC"
  - "Receita Federal - Tabela regressiva IR Renda Fixa"
  - "Anbima - Convenção CDI"
related: []
---

> **Status:** Documento validado em 23/04/2026
> **Próxima revisão:** Quando houver alteração na taxa SELIC


# Simulação de Investimento - R$ 10.000 a 120% do CDI

## Dados do Investimento
- **Capital investido:** R$ 10.000,00
- **Taxa CDI atual:** 14,25% ao ano
- **Taxa aplicada:** 120% do CDI = **17,10% ao ano**
- **Data da simulação:** 23/04/2026

---

## Rendimentos Brutos (sem IR)

| Período | Taxa | Rendimento |
|---------|------|------------|
| Diário (252 dias úteis) | 0,062662% | R$ 6,27 |
| Semanal (5 dias úteis) | 0,313702% | R$ 31,37 |
| Mensal (21 dias úteis) | 1,3242% | R$ 132,42 |
| Anual (252 dias úteis) | 17,10% | R$ 1.710,00 |

---

## Rendimentos Líquidos (após IR)

### Tabela Regressiva de IR na Renda Fixa

| Prazo | Alíquota IR |
|-------|-------------|
| Até 180 dias | 22,5% |
| 181 a 360 dias | 20,0% |
| 361 a 720 dias | 17,5% |
| Acima de 720 dias | 15,0% |

### Simulação por Prazo (CDB/LC)

| Prazo | Rend. Bruto | IR | Rend. Líquido | Rent. Líq. |
|-------|-------------|-----|---------------|------------|
| 6 meses | R$ 821,28 | R$ 184,79 (22,5%) | R$ 636,49 | 6,36% |
| 1 ano | R$ 1.710,00 | R$ 256,50 (15%) | R$ 1.453,50 | 14,53% |
| 2 anos | R$ 3.712,41 | R$ 556,86 (15%) | R$ 3.155,55 | 31,56% |

---

## Comparativo: CDB vs LCI/LCA (1 ano)

| Tipo | Bruto | IR | Líquido | Rent. Líq. |
|------|-------|-----|---------|------------|
| CDB/LC | R$ 1.710,00 | R$ 256,50 | R$ 1.453,50 | 14,53% |
| LCI/LCA | R$ 1.710,00 | R$ 0,00 | R$ 1.710,00 | 17,10% |

**Diferença:** R$ 256,50 a favor do LCI/LCA (isenção de IR)

---

## Observações Importantes

- LCI, LCA e LC são **isenas de IR** para pessoa física
- IR é retido na fonte (não precisa declarar no ajuste anual)
- Cálculo considera juros compostos com capitalização diária
- Taxa SELIC/CDI atual: 14,25% a.a. (Banco Central)

---

## Conclusão

Para maximizar rendimentos com 120% do CDI:
- **Prefira LCI/LCA** (isenção de IR)
- Se optar por CDB/LC, mantenha por mais de 720 dias para pagar apenas 15% de IR

---

## Fontes e Referências

### Taxa de Juros (SELIC/CDI)
| Fonte | URL | Data de consulta |
|-------|-----|------------------|
| Banco Central - Taxa SELIC | https://www.bcb.gov.br/controleinflacao/taxaselic | 23/04/2026 |
| BCB - Histórico de taxas | https://www.bcb.gov.br/controleinflacao/historicotaxasjuros | 23/04/2026 |
| Anbima - Taxas DI | https://www.anbima.com.br/pt_br/informacoes/mercados/mercados-de-capital/indices/taxas-d.htm | 23/04/2026 |

**Taxa SELIC/CDI vigente:** 14,25% ao ano
> A taxa CDI é definida pelo Banco Central e geralmente é igual à SELIC menos 0,10% (atualmente CDI = SELIC = 14,25%)

### Tabela de IR na Renda Fixa
| Fonte | Descrição |
|-------|-----------|
| Receita Federal | Lei 9.779/99 - Tabela regressiva para renda fixa |
| CVM | Instrução CVM 555/14 sobre isenção de LCI/LCA |

**Base legal:** Art. 3º da Lei nº 9.779, de 19 de janeiro de 1999

### Isenção de IR
- **LCI (Letra de Crédito Imobiliário):** Isenta de IR para PF (Lei 9.779/99)
- **LCA (Letra de Crédito do Agronegócio):** Isenta de IR para PF (Lei 11.076/2004)
- **LC (Letra de Câmbio):** Isenta de IR para PF (Lei 9.779/99)

### Metodologia de Cálculo
- **Capitalização:** Juros compostos, capitalização diária
- **Dias úteis:** 252 dias úteis por ano (convenção mercado)
- **Dias úteis por mês:** 21 dias (média)
- **Fórmula:** Fator = (1 + taxa_anual)^(1/252) - 1
