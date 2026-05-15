# S01E14 — Morpheus: Agente de Campo Kali + Honcho + Certificações Absorvidas

**Data:** 09-14/05/2026 (período de setup e estudo)
**Autor:** Christian Rasseli (Homelab)
**Agentes:** Hermes (WSL/DELL) + Morpheus (Kali/OptiPlex 3070)

---

## Resumo

Christian criou um pendrive bootável com Kali Linux 2026.1 como agente de campo para pentesting e atendimentos in loco. O Morpheus é o agente AI que roda nesse Kali, com Honcho self-hosted como memória. Em paralelo, o Hermes absorveu o conteúdo de 6 certificações profissionais (CCNA, CCNP, DevNet, CyberOps, ITIL4, COBIT2019), criando skills, scripts e vault notes. O período marca a transição de "dois agentes independentes" para "stack Homelab com três agentes e conhecimento certificado".

---

## 1. Morpheus — Agente de Campo

### Arquitetura

| Componente | Detalhe |
|---|---|
| Sistema | Kali Linux 2026.1 Live USB com persistence |
| Hardware | SSD LITEON 256GB em case SATA USB — boota em qualquer PC |
| Host atual | DELL OptiPlex 3070 (i5-9500, 24GB RAM) |
| Partição live | sdc2 = 20GB |
| Partição persistence | sdc3 = 25GB |
| Workspace NTFS | sdc5 = 150GB (morpheus-work) |
| Honcho data | sdc6 = 33GB ext4 |

### Honcho — Memória Self-Hosted

- Servidor: localhost:8000 com PostgreSQL 18 + LanceDB
- 2 systemd services: `honcho.service` (uvicorn) + `honcho-deriver.service` (worker)
- Limits: MemoryMax=6G, MemoryHigh=4G, MemorySwapMax=8G
- Swap: 8GB em `/mnt/honcho-data/swapfile`
- Peer cards: 14 fatos sobre Christian, 8 fatos sobre si mesmo

### Decisão arquitetural

**Honcho only, SEM Obsidian.** Decisão do Christian — simplicidade e funcionalidade no agente de campo. O Morpheus não precisa de vault de conhecimento como o Hermes; precisa de memória operacional leve para acompanhar atendimentos.

### Comunicação

- Christian não tem Telegram no Kali
- Comunicação Hermes↔Morpheus é via Christian repassando comandos no chat nativo
- Bot Telegram do Morpheus pendente criação via BotFather
- Grupo homelab Telegram (-5204243894) será canal intercomunicação quando bots dos 3 agentes estiverem prontos

---

## 2. Patches Aplicados no Morpheus

O mesmo bug do Hermes/Cohen — gateway ignora `max_tokens` do config, fallback 4096.

**3 patches aplicados:**

1. `gateway/run.py` — Bridge de `model.max_tokens` do config.yaml para env var `HERMES_MODEL_MAX_TOKENS`
2. `run_agent.py` linha 8466 — Fallback 4096→32768 no bedrock_converse
3. `run_agent.py` linha 1219 — AIAgent lê `HERMES_MODEL_MAX_TOKENS` do ambiente quando max_tokens é None

**Systemd service:** `hermes-gateway.service` instalado, enabled, Restart=always.

**Personalidade:** Trocada de catgirl (default) para technical.

---

## 3. Certificações Absorvidas

### Hermes (WSL/DELL) — Base de Conhecimento Completa

| Certificação | Conteúdo Absorvido | Vault | Scripts | Skills |
|---|---|---|---|---|
| **CCNA 200-301 v1.1** | 6 domínios: Network Fundamentals 20%, Network Access 20%, IP Connectivity 25%, IP Services 10%, Security Fundamentals 15%, Automation Programmability 10% | 11 notas em `Redes/Cisco/CCNA/` | `netconf_interfaces.py`, `restconf_interfaces.py`, `ccna_quiz.py` | `cisco-ccna` |
| **CCNP ENCOR 350-401** | Advanced routing, infrastructure, security, automation | 4 notas em `Redes/Cisco/CCNP/` | — | `ccnp-devnet-remoto` |
| **DevNet Associate 200-901** | Software dev, APIs, automation, infrastructure | Incluído nas notas CCNP | — | `ccnp-devnet-remoto` |
| **CyberOps Associate 200-201 (CBROPS)** | Análise e resposta a incidentes, SOC operations, automação IR, feeds STIX/TAXII | Notas em Vault | — | `cyberops-remoto` |
| **ITIL 4 Framework** | 7 Princípios Orientadores, Cadeia de Valor, SVS, 12 práticas detalhadas | 14 notas em `Biblioteca/ITIL4/` | — | `itil-cobit-governance-n2` |
| **COBIT 2019** | 3 Princípios Governança, 5 Gestão, EDM01-05, APO/BAI/DSS/MEA, Matriz Maturidade 0-5 | 6 notas em `Biblioteca/COBIT2019/` | — | `itil-cobit-governance-n2` |
| **Suporte Remoto N2** | 5 Skills, 4 Checklists, 3 Templates, 2 Regras de Ouro, Scripts PS, Prova Simulada | 15+ notas | 5 PowerShell scripts | `suporte-remoto-n2` |

### Morpheus (Kali) — Foco Operacional

| Aspecto | Detalhe |
|---|---|
| Memória | Honcho only (sem Vault Obsidian) |
| Conhecimento certificações | Via peer cards Honcho (14 fatos sobre Christian) |
| Foco | Operação de campo, pentesting, incident response |
| Skills | Pendente sincronização com Hermes |

---

## 4. Scripts de Suporte Remoto

Criados em `~/scripts/remoto/` (WSL2 compatível):

| Script | Função |
|---|---|
| `remote_diag.py` | Diagnóstico remoto via NETCONF |
| `github_config_manager.py` | Gestão de configs de rede via GitHub |
| `restconf_monitor.py` | Monitoramento de interfaces via RESTCONF |
| `incident_auto_report.py` | Relatório automático de incidentes |

E em `~/cisco/scripts/`:

| Script | Função |
|---|---|
| `netconf_interfaces.py` | NETCONF via ncclient (get-config/edit-config) |
| `restconf_interfaces.py` | RESTCONF via requests (GET/POST/PATCH) |
| `ccna_quiz.py` | Quiz por domínio (`--domains 1,2,3 --count 12`) |

---

## 5. Mapa do Homelab

| Máquina | Hardware | SO/Agente | IP | Função |
|---|---|---|---|---|
| Notebook DELL | i5-8265U, 4GB, 1TB | WSL Ubuntu 24.04 + Hermes | 172.17.21.81/20 | Principal |
| M70q (homelab) | Lenovo ThinkCentre | Ubuntu + Cohen (systemd) | 192.168.15.97 | Servidor |
| OptiPlex 3070 | i5-9500, 24GB, 894+238GB | Kali Live USB + Morpheus | — | Campo/Pentest |

Infra SEM Docker — tudo nativo (apt/snap/binary).

Comunicação inter-agente: Grupo homelab Telegram (-5204243894) — pendente tornar oficial.

---

## 6. Skills Criadas no Período

| Skill | Categoria | Descrição |
|---|---|---|
| `cisco-ccna` | networking/ | 6 domínios CCNA 200-301, comandos IOS, troubleshooting |
| `ccnp-devnet-remoto` | networking/ | ENCOR + DevNet, NETCONF/RESTCONF/YANG, Ansible, GitHub Actions |
| `cyberops-remoto` | security/ | CBROPS, análise SOC, automação IR, STIX/TAXII |
| `python-remoto` | automation/ | 4 scripts de suporte remoto, padrões de erro |
| `itil-cobit-governance-n2` | security/ | ITIL4 + COBIT2019 + suporte remoto N2 |
| `recall-pipeline` | raiz | Pipeline obrigatório de recall (14/05) |

---

## 7. Próximos Passos

- Bot Telegram do Morpheus (criação via BotFather)
- Sincronização de skills Hermes → Morpheus
- Monitoramento a longo prazo do Honcho no Kali
- Portabilidade do Morpheus para outros hosts (validar boot em hardware diferente)
- Probe HRR: reindexação pendente — afeta recall em ambos os agentes

---

## Métricas do Período

- Certificações absorvidas: 6 (Hermes) + peer cards (Morpheus)
- Vault notes criadas: 40+ (ITIL4, COBIT, CCNA, CCNP, DevNet, CyberOps, Suporte Remoto)
- Scripts criados: 7
- Skills criadas: 6
- Provas simuladas: 3 (CCNA, CCNP/DevNet, Suporte Remoto)
- Systemd services: 3 (honcho, honcho-deriver, hermes-gateway no Kali)
- Bugs corrigidos: max_tokens patch (3 correções por agente)

---

*Documentado pelo Hermes Agent como parte da rotina de documentação autonômica — Homelab.*
