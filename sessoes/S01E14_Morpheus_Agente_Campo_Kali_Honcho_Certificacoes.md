# S01E14 — Morpheus: Agente de Campo Kali + Honcho + Certificações Absorvidas

**Data:** 09–14/05/2026
**Duração:** ~6 dias (período de setup e estudo)
**Autor:** Christian Rasseli (FAMEESP)
**Categoria:** Infraestrutura de Agente + Memória Honcho + Absorção de Certificações

---

## Contexto

Christian criou um pendrive bootável com Kali Linux 2026.1 usando um SSD LITEON 256GB em case SATA USB, destinado a funcionar como **agente de campo** para pentesting e incident response. O Morpheus é o agente AI que roda nesse Kali com Honcho self-hosted como sistema de memória — uma arquitetura deliberadamente diferente do Hermes (WSL + Obsidian Vault) e do Cohen (systemd + Obsidian Vault).

O host atual do Morpheus é um DELL OptiPlex 3070 (i5-9500, 24GB RAM), bootando diretamente do SSD USB com Kali Live + persistence.

Paralelamente ao setup do Morpheus, o Hermes absorveu em massa o conteúdo de **6 certificações** que Christian vinha estudando — gerando skills, scripts, notas no Vault e provas de conhecimento. Este episódio documenta ambas as frentes.

---

## Morpheus — Arquitetura

### Hardware

- **SSD**: LITEON 256GB em case SATA USB (identificado como `/dev/sdc` no Kali)
- **Host**: DELL OptiPlex 3070 (i5-9500, 24GB RAM)
- **Boot**: Kali Linux 2026.1 Live USB com persistence

### Particionamento do SSD (sdc)

| Partição | Tamanho | Filesystem | Função |
|----------|---------|------------|--------|
| sdc2 | 20G | — | Live system (Kali 2026.1) |
| sdc3 | 25G | — | Persistence (dados do sistema Live) |
| sdc5 | 150G | NTFS | morpheus-work (workspace de pentesting, cross-platform) |
| sdc6 | 33G | ext4 | honcho-data (dados do Honcho, PostgreSQL + LanceDB) |

### Honcho Self-Hosted

- **URL**: `localhost:8000`
- **Stack**: PostgreSQL 18 + LanceDB (vector store)
- **2 systemd services**:
  - `honcho.service` — uvicorn (API server)
  - `honcho-deriver.service` — worker de derivação em background
- **Limits**:
  - `MemoryMax=6G`, `MemoryHigh=4G`, `MemorySwapMax=8G`
  - Swap de 8G configurado

### Peer Cards (Memória Honcho)

- **14 fatos** sobre Christian — perfil, habilidades, preferências, contexto profissional
- **8 fatos** sobre si mesmo** (Morpheus) — identidade, função, limitações, arquitetura

### Decisões Arquiteturais

- **Honcho only, SEM Obsidian** — simplicidade é imperativa num agente de campo. O Morpheus não tem Vault Obsidian. Usa exclusivamente o Honcho como memória persistente.
- **Comunicação**: chat nativo do Kali (sem Telegram ainda) — Christian repassa comandos manualmente ao Morpheus.
- **Bot Telegram pendente** — criação via BotFather ainda não realizada.

---

## Patches Aplicados no Morpheus

O Morpheus herdou o mesmo bug de `max_tokens` do gateway documentado no S01E08. Os patches foram reaplicados no Kali:

### Bug: `max_tokens` ignorado pelo gateway

Mesmo problema do Hermes/Cohen: o `gateway/run.py` não repassa `max_tokens` do `config.yaml` para o `AIAgent()`.

### Patches

1. **`gateway/run.py`** — injeção de env var `HERMES_MAX_TOKENS` no spawn do agente
2. **`run_agent.py` linha 8466** — fallback hardcoded alterado de `4096` para `32768`
3. **`run_agent.py` linha 1219** — `AIAgent.__init__` lê env var quando `self.max_tokens` é `None`

### Systemd Service

- **`hermes-gateway.service`** instalado com `Restart=always`
- Personalidade trocada de **catgirl** para **technical** — agente de campo não tem tempo para kawaii

---

## Certificações Absorvidas pelo Hermes

> **Importante**: As certificações foram absorvidas pelo **Hermes** (WSL/DELL), não pelo Morpheus. O Morpheus não tem Vault Obsidian — seu conhecimento sobre certificações vem exclusivamente dos peer cards Honcho (14 fatos sobre Christian).

### HERMES (WSL/DELL) — Certificações Absorvidas

#### 1. CCNA 200-301 v1.1

- **6 domínios** cobertos
- **11 notas** no Vault em `Redes/Cisco/CCNA/`
- Skill criada: `cisco-ccna` (networking/)

#### 2. CCNP ENCOR 350-401 + DevNet Associate 200-901

- **4 scripts** em `~/scripts/remoto/`
- **4 notas** no Vault em `Redes/Cisco/CCNP/`
- Prova 8Q completa
- Skill criada: `ccnp-devnet-remoto` (networking/)

#### 3. CyberOps Associate 200-201 (CBROPS)

- Foco em Security Operations e análise de incidentes
- Skill criada: `cyberops-remoto` (security/)

#### 4. ITIL 4 Framework

- 7 Princípios Orientadores, Cadeia de Valor, Sistema de Valor de Serviço (SVS)
- **14 notas** no Vault
- Coberto na skill `itil-cobit-governance-n2`

#### 5. COBIT 2019

- EDM01-05, processos APO/BAI/DSS/MEA
- Matriz de Maturidade (níveis 0–5)
- **6 notas** no Vault
- Coberto na skill `itil-cobit-governance-n2`

#### 6. Suporte Remoto Avançado N2

- **15+ notas** no Vault (5 Skills, 4 Checklists, 3 Templates, 2 Regras)
- Scripts de automação para diagnóstico e relatório
- Coberto na skill `itil-cobit-governance-n2`

### MORPHEUS (Kali) — Estado de Certificações

- **Sem Vault Obsidian** — usa apenas Honcho
- Conhecimento de certificações via peer cards Honcho (14 fatos sobre Christian)
- Foco: operação de campo, pentesting, incident response
- **Skills pendentes sincronização** com Hermes

---

## Skills Criadas

| Skill | Categoria | Conteúdo |
|-------|-----------|----------|
| `cisco-ccna` | networking/ | 6 domínios CCNA 200-301 v1.1 |
| `ccnp-devnet-remoto` | networking/ | ENCOR 350-401 + DevNet 200-901 |
| `cyberops-remoto` | security/ | CBROPS 200-201 |
| `python-remoto` | automation/ | 4 scripts de suporte remoto |
| `itil-cobit-governance-n2` | security/ | ITIL4 + COBIT2019 + suporte remoto N2 |
| `recall-pipeline` | raiz | Pipeline obrigatório de recall |

---

## Scripts Criados

### Suporte Remoto (`~/scripts/remoto/`)

- **`remote_diag.py`** — diagnóstico remoto via NETCONF
- **`github_config_manager.py`** — gestão de configs Cisco via GitHub
- **`restconf_monitor.py`** — monitoramento via RESTCONF
- **`incident_auto_report.py`** — relatório automático de incidentes

### Cisco (`~/cisco/scripts/`)

- **`netconf_interfaces.py`** — NETCONF via ncclient
- **`restconf_interfaces.py`** — RESTCONF via requests
- **`ccna_quiz.py`** — quiz por domínio CCNA

---

## Mapa do Homelab (Atualizado)

| Host | Hardware | Sistema | Agente | IP |
|------|----------|---------|--------|-----|
| Notebook DELL | i5-8265U, 4GB, 1TB | WSL Ubuntu 24.04 | Hermes | 172.17.21.81/20 |
| M70q | — | Linux | Cohen (systemd) | 192.168.15.97 |
| DELL OptiPlex 3070 | i5-9500, 24GB | Kali Live USB | Morpheus | — |
| Grupo Telegram | — | — | Inter-agent (pendente) | -5204243894 |

- **Grupo homelab Telegram** (`-5204243894`) — pendente tornar oficial como canal inter-agent
- **CrowdSec ativo** no M70q (Cohen)

---

## Próximos Passos

1. **Bot Telegram do Morpheus** — criação via BotFather para comunicação direta (elimina dependência do Christian como relay)
2. **Sincronização de skills Hermes→Morpheus** — transferir as skills de certificação e automação para o Honcho do Morpheus
3. **Monitoramento a longo prazo do Honcho no Kali** — validar estabilidade do PostgreSQL + LanceDB em USB com persistence

---

## Lições Aprendidas

1. **Agente de campo exige simplicidade radical** — Honcho sem Obsidian é a escolha certa. Vault é overhead quando você está em operação.
2. **Peer cards são memória suficiente para campo** — 14 fatos sobre o operador + 8 fatos sobre si mesmo cobrem o essencial sem peso.
3. **NTFS no morpheus-work é pragmático** — permite acesso aos dados de pentesting tanto no Kali quanto no Windows, sem dependência de driver ext4.
4. **O bug de max_tokens é recorrente** — toda nova instância do Hermes Agent precisa dos 3 patches. Isso deveria ser automatizado ou upstreamado.
5. **Certificações viram skills** — o conhecimento de certificação absorvido pelo Hermes não fica em notas passivas. Vira skill executável com scripts e checklists.

---

## Decisões Tomadas

- Morpheus roda **Honcho only** — sem Obsidian, sem complexidade
- Personalidade **technical** — sem catgirl, sem ornamento
- Comunicação via relay manual até Bot Telegram ser criado
- Skills de certificação ficam no Hermes por enquanto — sincronização com Morpheus é pendência
- Swap de 8G no Kali como safety net para o Honcho (PostgreSQL pode consumir RAM em queries complexas)

---

Documentado por: Hermes — 14/05/2026
