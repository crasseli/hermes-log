---
title: OS-005 — Governança do Obsidian: Prevenção de Spam e Padronização
date: 2026-04-25 21:19:21
updated: 2026-04-25 21:19:21
tags:
  - inbox-auto
  - md
source: 
related: []
---

---
title: "OS-005 — Governança do Obsidian: Prevenção de Spam e Padronização"
date: 2026-04-25
tipo: ordem-de-servico
prioridade: alta
status: pendente-execução
agente: Hermes
solicitante: Christian
vault_destino: Hermes/OS/Ativas/
tags:
  - os-005
  - obsidian
  - governança
  - soul
  - cron
  - skill
  - padronização
referencias:
  - https://hermes-agent.nousresearch.com/docs/user-guide/features/personality
  - https://hermes-agent.nousresearch.com/docs/user-guide/features/cron
  - https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/note-taking/note-taking-obsidian
---

# OS-005 — Governança do Obsidian: Prevenção de Spam e Padronização

> **LEIA ANTES DE EXECUTAR**: Esta OS resolve a causa raiz do problema
> identificado em 25/04/2026 — 73 arquivos de spam gerados automaticamente
> no vault. O objetivo é prevenir que isso se repita, não apenas remediar.
> Três frentes em sequência obrigatória: SOUL.md → Cron → Skill.
> Nenhuma frente pode ser iniciada sem a anterior estar concluída e confirmada.

---

## Contexto

A limpeza executada na OS-003/004 removeu 73 arquivos de spam do vault.
Diagnóstico da causa raiz:

- O Hermes não tem protocolo definido de **o que**, **quando** e **onde**
  salvar no Obsidian
- O cron de autosave gera notas sem critério de conteúdo mínimo
- Cada sessão improvisa nomenclatura e pasta de destino
- O orquestrador não tem referência de template — inventa estrutura a cada vez

**Resultado sem esta OS:** o vault voltará ao estado de spam em semanas.

---

## FASE 1 — Protocolo de Escrita no SOUL.md

**Objetivo**: definir regras permanentes e invioláveis de como o Hermes
interage com o Obsidian. Estas regras ficam no SOUL.md e são lidas
pelo orquestrador em toda sessão.

### 1.1 — Ler o SOUL.md atual

```bash
cat ~/.hermes/SOUL.md
```

Registrar no relatório:
- [ ] Existe alguma seção sobre Obsidian ou escrita de notas?
- [ ] Se sim, copiar o trecho para referência

### 1.2 — Fazer backup do SOUL.md antes de editar

```bash
cp ~/.hermes/SOUL.md ~/.hermes/SOUL_pre_os005_$(date +%Y-%m-%d).md
echo "Backup: SOUL_pre_os005_$(date +%Y-%m-%d).md"
```

### 1.3 — Adicionar seção de Governança do Obsidian ao SOUL.md

Inserir a seguinte seção no SOUL.md, após a seção de RECALL:

```markdown
## OBSIDIAN: PROTOCOLO DE ESCRITA — REGRAS INVIOLÁVEIS

### O QUE NUNCA DEVE SER SALVO COMO NOTA
- Logs de cron sem decisão ou descoberta documentada
- Autosaves de sessão com apenas metadados (ID, timestamp, tags)
- Notas com menos de 300 palavras de conteúdo analítico real
- Duplicatas de notas já existentes no vault

### CRITÉRIO MÍNIMO PARA CRIAR UMA NOTA
Uma nota só deve ser criada se contiver ao menos UMA das seguintes:
- Decisão tomada com justificativa documentada
- Descoberta técnica com evidência
- Instrução ou procedimento reutilizável
- Análise com conclusão registrada
- Relatório de OS com achados e recomendações

### ESTRUTURA DE PASTAS — DESTINO POR TIPO

| Tipo de Conteúdo | Pasta Destino |
|-----------------|---------------|
| Ordens de Serviço ativas | Hermes/OS/Ativas/ |
| Ordens de Serviço concluídas | Hermes/OS/Concluidas/ |
| Relatórios de diagnóstico | Hermes/OS/Ativas/Diagnosticos/ |
| Documentação de skills | Hermes/Tecnologia/Skills/ |
| Configurações do sistema | Hermes/Tecnologia/Configuracoes/ |
| Projetos e APIs | Hermes/Projetos/ |
| Conhecimento técnico geral | Hermes/Tecnologia/ |
| Sessões com conteúdo real | Hermes/Conhecimento/Sessoes/ |
| Referências e glossário | Hermes/Referencias/ |

### CONVENÇÃO DE NOMENCLATURA

Formato obrigatório: `Titulo_Descritivo_YYYY-MM-DD.md`

Regras:
- SEM acentos no nome do arquivo
- SEM espaços — usar underscore
- SEM prefixos como "Autosave_", "Sessao_Cron_", "Sessao_Hermes_"
- Título deve descrever o CONTEÚDO, não o evento que gerou a nota
- Data no formato YYYY-MM-DD ao final, separada por underscore

Exemplos CORRETOS:
- `Diagnostico_Protocolo_Recall_2026-04-25.md`
- `Configuracao_Modelo_DeepSeek_Flash_2026-04-25.md`
- `Analise_Vault_Obsidian_Estrutura_2026-04-25.md`

Exemplos INCORRETOS:
- `Autosave_Sessao_Cron_20260425_181704.md`
- `Sessão_Hermes_20260425_151915.md`
- `Sessao_Cron_Obsidian_Skill.md`

### REGRA DE VERIFICAÇÃO ANTES DE SALVAR
Antes de criar qualquer nota no Obsidian, responder internamente:
1. Esta nota tem critério mínimo de conteúdo? (300+ palavras analíticas)
2. O nome segue a convenção sem acentos e com data?
3. A pasta de destino está correta para este tipo de conteúdo?
4. Já existe uma nota similar no vault que deveria ser atualizada
   em vez de criar uma nova?

Se qualquer resposta for NÃO — não criar a nota.
```

### 1.4 — Verificar SOUL.md após edição

```bash
grep -A50 "OBSIDIAN: PROTOCOLO" ~/.hermes/SOUL.md
```

Confirmar:
- [ ] Seção inserida corretamente
- [ ] Nenhuma seção anterior foi removida acidentalmente
- [ ] Backup do SOUL anterior confirmado

### ✅ TRAVA FASE 1

Só avançar após:
1. Backup do SOUL.md confirmado
2. Seção de governança inserida e verificada
3. Reportar ao Christian o SOUL.md atualizado para aprovação

---

## FASE 2 — Auditoria e Ajuste do Cron de Autosave

**Objetivo**: identificar qual job de cron está gerando o spam e ajustar
o critério de disparo para evitar notas vazias.

### 2.1 — Listar todos os jobs de cron ativos

```bash
ls -la ~/.hermes/cron/
cat ~/.hermes/cron/*.yaml 2>/dev/null || cat ~/.hermes/cron/*.json 2>/dev/null
```

### 2.2 — Identificar o job responsável pelo autosave

Procurar por jobs que:
- Mencionam Obsidian, vault, autosave ou save_note
- Têm intervalo menor que 60 minutos
- Não têm critério de conteúdo mínimo

```bash
grep -rn "obsidian\|autosave\|vault\|save_note\|Sessao\|Sessão" \
  ~/.hermes/cron/ 2>/dev/null
```

Registrar no relatório:
- [ ] Nome do job responsável pelo spam
- [ ] Intervalo atual de execução
- [ ] Critério atual (se houver) para criar nota

### 2.3 — Propor ajuste ao Christian antes de modificar

Com base no achado, redigir proposta com:
- Intervalo recomendado (sugestão: mínimo 6 horas)
- Critério de conteúdo mínimo a adicionar
- Confirmação de que o job não será deletado, apenas ajustado

**AGUARDAR APROVAÇÃO DO CHRISTIAN antes de qualquer modificação no cron.**

### 2.4 — Aplicar ajuste aprovado

Após aprovação, editar o job conforme especificado e confirmar:

```bash
# Verificar sintaxe do arquivo após edição
cat ~/.hermes/cron/<nome_do_job>

# Listar crons ativos para confirmar mudança
hermes cron list 2>/dev/null || ls ~/.hermes/cron/
```

### ✅ TRAVA FASE 2

Só avançar após:
1. Job de spam identificado com evidência
2. Proposta apresentada e aprovada pelo Christian
3. Ajuste aplicado e confirmado
4. Christian informado do novo comportamento do cron

---

## FASE 3 — Skill de Escrita Padronizada no Obsidian

**Objetivo**: criar uma skill que o Hermes usa como intermediário obrigatório
para qualquer escrita no vault, garantindo template, pasta e nomenclatura
consistentes.

### 3.1 — Verificar skill atual do Obsidian

```bash
cat ~/.hermes/skills/obsidian/SKILL.md 2>/dev/null | head -100
ls ~/.hermes/skills/obsidian/
```

Registrar:
- [ ] O que a skill atual faz e não faz
- [ ] Existe algum template de criação de nota?

### 3.2 — Criar template de nota padrão

Criar arquivo de template em:
`~/.hermes/skills/obsidian/templates/nota_padrao.md`

```markdown
---
title: "{{TITULO}}"
date: {{DATA}}
tipo: {{TIPO}}
tags:
  - {{TAG_1}}
  - {{TAG_2}}
status: {{STATUS}}
---

# {{TITULO}}

## Contexto
{{CONTEXTO}}

## Conteúdo Principal
{{CONTEUDO}}

## Conclusão / Próximos Passos
{{CONCLUSAO}}

---
*Criado em {{DATA}} | Sessão: {{SESSION_ID}}*
```

### 3.3 — Atualizar SKILL.md do Obsidian

Adicionar ao `SKILL.md` da skill obsidian as seguintes instruções:

```markdown
## PROTOCOLO OBRIGATÓRIO DE CRIAÇÃO DE NOTAS

Antes de criar qualquer nota, verificar:
1. O conteúdo tem critério mínimo? (ver SOUL.md — seção OBSIDIAN)
2. Usar o template em templates/nota_padrao.md
3. Destino correto conforme tabela de pastas no SOUL.md
4. Nomenclatura sem acentos, sem prefixos de cron/autosave

Comando padrão de criação:
  cat > "$VAULT/<PASTA>/<TITULO>_<DATA>.md" << 'EOF'
  [conteúdo do template preenchido]
  EOF
```

### 3.4 — Testar a skill com uma nota de exemplo

Criar uma nota de teste seguindo o novo protocolo:

```bash
VAULT="/mnt/e/Obsidian/Cofre/Hermes"
DATA=$(date +%Y-%m-%d)
cat > "$VAULT/Tecnologia/Configuracoes/Teste_Governanca_Obsidian_$DATA.md" << 'EOF'
---
title: "Teste Governança Obsidian"
date: 2026-04-25
tipo: teste
tags:
  - teste
  - governança
  - os-005
status: concluído
---

# Teste Governança Obsidian

## Contexto
Nota criada para validar o novo protocolo de escrita definido na OS-005.

## Conteúdo Principal
Validação do template, pasta de destino e nomenclatura padronizada.

## Conclusão
Protocolo funcionando corretamente.

---
*Criado em 2026-04-25 | OS-005*
EOF

echo "Nota criada:"
ls -lh "$VAULT/Tecnologia/Configuracoes/Teste_Governanca_Obsidian_$DATA.md"
```

Confirmar:
- [ ] Nota criada na pasta correta
- [ ] Nome sem acentos e com data
- [ ] Template preenchido corretamente

### ✅ TRAVA FASE 3

Só encerrar após:
1. Template criado em `templates/nota_padrao.md`
2. SKILL.md atualizado com protocolo obrigatório
3. Nota de teste criada e verificada
4. Christian confirmou que o resultado está correto

---

## FASE 4 — Documentação e Encerramento

### 4.1 — Salvar relatório final no vault

```bash
VAULT="/mnt/e/Obsidian/Cofre/Hermes"
mkdir -p "$VAULT/OS/Concluidas"
cat > "$VAULT/OS/Concluidas/Relatorio_OS-005_$(date +%Y-%m-%d).md" << 'EOF'
---
title: "Relatório OS-005 — Governança do Obsidian"
date: 2026-04-25
tags: os-005, obsidian, governança, soul, cron, skill
---

# Relatório OS-005 — Governança do Obsidian

## Resumo
[preencher]

## Fase 1 — SOUL.md
- Seção de governança inserida: SIM/NÃO
- Backup anterior: [caminho]

## Fase 2 — Cron
- Job identificado: [nome]
- Intervalo anterior: [valor]
- Intervalo novo: [valor]
- Critério adicionado: [descrição]

## Fase 3 — Skill
- Template criado: SIM/NÃO
- SKILL.md atualizado: SIM/NÃO
- Teste validado: SIM/NÃO

## Status Final
Governança ativa: SIM/NÃO
Próxima revisão recomendada: [data]
Solicitante: Christian
Executor: Hermes
EOF
```

### 4.2 — Mover OS-005 para Concluídas

```bash
VAULT="/mnt/e/Obsidian/Cofre/Hermes"
mv "$VAULT/OS/Ativas/OS-005_Governanca_Obsidian.md" \
   "$VAULT/OS/Concluidas/" 2>/dev/null && echo "OS-005 movida para Concluidas"
```

---

## Checklist Final

- [ ] Fase 1 — SOUL.md atualizado com protocolo de governança
- [ ] Fase 2 — Cron auditado e ajustado com aprovação do Christian
- [ ] Fase 3 — Skill atualizada com template e protocolo obrigatório
- [ ] Fase 4 — Relatório salvo e OS movida para Concluídas
- [ ] Nenhuma modificação foi feita sem aprovação prévia
- [ ] Christian confirmou que o vault está organizado e o protocolo ativo

---

## Resultado Esperado

Após esta OS, o Hermes:
- Nunca mais criará notas de autosave vazias ou com menos de 300 palavras
- Sempre usará a pasta correta por tipo de conteúdo
- Sempre seguirá a convenção de nomenclatura sem acentos
- O cron só salvará sessões com conteúdo analítico real
- O orquestrador terá referência clara de template em toda sessão

---

*OS emitida em 2026-04-25 | Solicitante: Christian | Agente executor: Hermes*
*Versão: 1.0 | Prerequisito: OS-003 e OS-004 concluídas*
