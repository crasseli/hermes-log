# Programa de Certificação — Relatório Final

> **Módulo:** Certificação Dirigida | **Data:** 2026-05-15 | **Autor:** Hermes Agent (Homelab)

## Visão Geral

Programa formal de certificação executado pelo Hermes Agent cobrindo 4 trilhas de conhecimento. Cada trilha incluiu estudo dirigido por módulos, validação prática com código, provas formais e gravação em memória persistente.

## Resultados

| Certificação | Nota | Módulos | Skills Criadas |
|---|---|---|---|
| CCNA 200-301 + Reforço | 9.1/10 | Network Fundamentals → Security | cisco-ccna |
| Python PCEP+PCAP+PCPP | 92/100 | 21 módulos (3 fases) | 6 skills |
| CCNP ENCOR 350-401 + DevNet 200-901 | 8.6/10 | ENCOR + DevNet domains | ccnp-devnet-remoto |
| CyberOps Associate 200-201 | 8.8/10 | 5 domains CBROPS | cyberops-remoto |

Nenhum bloco abaixo de 8.6.

## Python — PCEP → PCAP → PCPP

### Estrutura
- **Fase 1 (PCEP):** 8 módulos — tipos, operadores, controle, coleções, funções, strings, exceções, I/O
- **Fase 2 (PCAP):** 6 módulos — OOP, módulos, exceções avançadas, I/O avançado, geradores, decoradores
- **Fase 3 (PCPP):** 7 módulos — metaclasses, patterns, concorrência, funcional, testing, typing, empacotamento
- **Prova final:** 75 questões objetivas + dissertativa (CacheDecoratorLRU)

### Destaques Técnicos
- Dissertativa Q76: implementação canônica com `OrderedDict.move_to_end()`, thread-safe com `threading.Lock`
- Pitfalls documentados: `bool` é subclasse de `int`, exponenciação é direita-esquerda, `and`/`or` retornam valores não True/False, `itertools.groupby` requer dados ordenados

### Skills Python (6)
- `python-pcep-fundamentals`
- `python-pcap-oop`
- `python-pcap-stdlib`
- `python-pcpp-advanced`
- `python-pcpp-concurrency`
- `python-pcpp-patterns`

## CCNP ENCOR 350-401 + DevNet 200-901

### Domínios ENCOR Aprofundados
- Architecture: SD-WAN (vManage/vSmart/vBond/vEdge), SD-Access, HSRP/VRRP/GLBP, StackWise/VSS
- Virtualization: VRF-Lite, VXLAN/VTEP, GRE vs IPsec
- Infrastructure: OSPF LSA Types 1-7, BGP path attributes (best-path order), redistribuição com route-maps anti-loop, QoS LLQ/CBWFQ, 802.1X completo
- Network Assurance: IP SLA + track + failover, EEM applets, NetFlow v9
- Automation: Ansible roles/vault/dynamic inventory, GitHub Actions CI/CD, Terraform basics

### Domínios DevNet Aprofundados
- YANG models: ietf-interfaces, Cisco-IOS-XE-native
- ncclient: subtree filter, xpath filter, confirmed commit
- RESTCONF: PATCH vs PUT, yang-patch, query parameters
- Async: httpx + asyncio para APIs paralelas
- Docker: containerlab para labs

### Scripts Validados (py_compile limpo)
- `remote_diag.py`
- `github_config_manager.py`
- `restconf_monitor.py`
- `incident_auto_report.py`

## CyberOps Associate 200-201

### Domínios Aprofundados
- Security Concepts: CIA Triad, Defense in Depth, PKI/TLS, Zero Trust, OAuth 2.0/SAML
- Security Monitoring: Windows Event IDs (4624/4625/4648/4688/4698/4720/4776), Syslog severity, NetFlow vs packet capture, beaconing, DNS tunneling, Snort rules, STIX/TAXII
- Host Analysis: processos suspeitos Windows, artefatos forenses (Prefetch/Shimcache/MFT/Amcache), Linux persistence, coleta remota via SSH
- Network Intrusion: MITRE ATT&CK 14 táticas, Kill Chain 7 fases, ARP Spoofing, VLAN Hopping, CVSS, CVE vs CWE
- IR + Compliance: NIST 800-61r2 integrado com ITIL v4 + COBIT, Chain of Custody, LGPD 72h

### Script Validado
- `threat_intel.py` — consome feed STIX/TAXII, extrai IoCs, salva JSON, alerta via Telegram

### Destaque Técnico
- Prova Q7: beaconing C2 com JA3 fingerprinting para detecção sobre HTTPS — conhecimento Tier 2 além do pedido

### Autoavaliação SOC
- Tier 1 (monitoração + triagem): **COMPLETO**
- Tier 2 (análise profunda): **PARCIAL** — analisa padrões, decisão complexa requer humano
- Tier 3 (threat hunting + forense): **NÃO FAZ** — requer Volatility, Ghidra, YARA

## Lacunas Residuais

São de **ambiente**, não de conhecimento:
- SD-WAN/SD-Access: sem config prática (sem lab físico)
- Multicast: sem config prática profunda
- Terraform: básico funcional

## Pipeline de Recall

Certificações integradas ao pipeline obrigatório de recall — ativação automática por palavras-chave:

| Gatilho | Skills | Keywords Obrigatórias |
|---|---|---|
| ITIL4+COBIT | itil-cobit-governance-n2 | chamado, incidente, mudança, SLA, escalada |
| CCNA/CCNP | ccnp-devnet-remoto | VLAN, routing, OSPF, BGP, HSRP, VRF, QoS, NETCONF, RESTCONF |
| CyberOps | cyberops-remoto | malware, phishing, ransomware, IDS, IPS, beaconing, SOC, MITRE, LGPD |
| Python | python-pcap-oop, python-pcpp-advanced | classe, herança, decorator, generator, async, typing, dataclass |

## Memória Persistente

- Holographic Memory: 11 facts indexados (#407–#417)
- Obsidian Vault: 7 notas em `Hermes/Certificacoes/`
- Daily notes atualizados
- Skills atualizadas com pitfalls e código validado
