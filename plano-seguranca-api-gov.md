# PLANO DE SEGURANCA - Integracao APIs Governamentais

> **Objetivo:** Garantir que dados do Hermes NAO vazem para o governo brasileiro durante consultas a APIs publicas.
> **Data:** 23/04/2026
> **Classificacao:** CONFIDENCIAL

---

## 1. ANALISE DE RISCOS IDENTIFICADOS

### 1.1 Risco CRITICO - API Key Vinculada a Identidade
**Vetor:** A API Portal de Dados Abertos exige header `chave-api-dados-abertos`
**Impacto:** CADA requisicao e rastreavel ao cidadao especifico (CPF vinculado)
**Dados expostos:**
- IP de origem
- Timestamp preciso
- Datasets consultados
- Frequencia de acesso
- Padrao de busca (interesses)

### 1.2 Risco ALTO - Telemetria HTTP
**Vetor:** Headers padrao (User-Agent, Accept, etc)
**Impacto:** Identificacao do ambiente (Python, WSL, versao)
**Dados expostos:**
- User-Agent: "python-requests/2.31.0"
- Sistema operacional
- Versao do cliente

### 1.3 Risco MEDIO - Perfilamento por Padroes
**Vetor:** Analise de comportamento de consultas
**Impacto:** Correlacao de multiplas consultas revela intencao
**Exemplo perigoso:**
```
Consulta 1: orgao="PF", ano="2024" → interesse em policia
Consulta 2: tema="licitacao", valor_min="1000000" → investigacao
Consulta 3: municipio="Brasilia", orgao="CGU" → foco em auditoria
```
Resultado: Perfil criado = "Possivel jornalista investigando corrupcao"

### 1.4 Risco CRITICO - Endpoints de Escrita
**Vetor:** POST /dados/api/reuso/salvar
**Impacto:** Dados do Hermes hospedados em infra governamental
**Consequencia:** Perda total de controle sobre dados

---

## 2. ESTRATEGIA DE DEFESA EM CAMADAS

### Camada 1: Anonimizacao de Rede
```
Hermes → Tor/VPN → API Gov
         ↑
    Rotacao de exit nodes
```
- Usar Tor para ocultar IP real
- Rotacionar circuitos a cada sessao
- Considerar VPN com no-logs policy

### Camada 2: Ofuscacao de Cliente
```python
# Headers rotativos
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0"
]
```
- Rotacionar User-Agent
- Remover headers identificaveis (X-Forwarded-For)
- Simular comportamento de browser real

### Camada 3: Throttling e Jitter
```python
import random
import time

def safe_request():
    time.sleep(random.uniform(2, 8))  # Jitter aleatorio
    # fazer requisicao
```
- Delay aleatorio entre requisicoes (2-8s)
- Evitar padroes detectaveis (ex: exatamente 1s entre calls)
- Limitar taxa para < 10 req/minuto

### Camada 4: Cache Local Agressivo
```
Requisicao → Cache Hit? → Sim: Retorna local
                |
                Nao: Consulta API → Salva no cache
```
- TTL de 24h para dados estaveis
- Cache em SQLite local
- Minimizar requisicoes repetidas

---

## 3. ARQUITETURA SEGURA PROPOSTA

### Opcao A: Modo PARANOICO (Recomendado)
```
┌─────────────────────────────────────────────────────────────┐
│  HERMES                                                     │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐   │
│  │ Cliente API  │───→│  Tor Proxy   │───→│ dados.gov.br │   │
│  │ (sem auth)   │    │ (rotativo)   │    │ (apenas GET) │   │
│  └──────────────┘    └──────────────┘    └──────────────┘   │
│         │                                              │     │
│         ↓                                              │     │
│  ┌──────────────┐                                      │     │
│  │ Cache Local  │←───────────────────────────────────────┘     │
│  │ (SQLite)     │                                            │
│  └──────────────┘                                            │
└─────────────────────────────────────────────────────────────┘
```
**Caracteristicas:**
- NAO usa API key (limita a endpoints publicos)
- Todas as requisicoes via Tor
- Cache local de 7 dias
- Throttling de 5s entre requisicoes

### Opcao B: Modo ESPelhado (Mais Seguro)
```
┌─────────────────────────────────────────────────────────────┐
│  HERMES                                                     │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐   │
│  │ Agendador    │───→│  Download    │───→│ dados.gov.br │   │
│  │ (cron/semanal│    │  Dumps CSV   │    │ (HTTP direto)│   │
│  └──────────────┘    └──────────────┘    └──────────────┘   │
│         │                                              │     │
│         ↓                                              │     │
│  ┌──────────────┐                                      │     │
│  │ Banco Local  │←───────────────────────────────────────┘     │
│  │ (SQLite/Parquet)                                         │
│  └──────────────┘                                            │
└─────────────────────────────────────────────────────────────┘
```
**Caracteristicas:**
- Download semanal de dumps completos
- Consultas 100% offline
- Zero telemetria de consultas
- Sincronizacao em horarios aleatorios

---

## 4. IMPLEMENTACAO TECNICA

### 4.1 Cliente com Tor
```python
import requests
import random

class GovAPIClientParanoid:
    """Cliente anonimo para APIs governamentais"""
    
    TOR_PROXY = {
        'http': 'socks5h://127.0.0.1:9050',
        'https': 'socks5h://127.0.0.1:9050'
    }
    
    USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0"
    ]
    
    def __init__(self):
        self.session = requests.Session()
        self.session.proxies = self.TOR_PROXY
        self.cache = {}
    
    def _get_headers(self):
        return {
            'User-Agent': random.choice(self.USER_AGENTS),
            'Accept': 'application/json',
            'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
        }
    
    def get(self, endpoint, params=None):
        # Verificar cache primeiro
        cache_key = f"{endpoint}:{str(params)}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        # Throttling
        time.sleep(random.uniform(2, 8))
        
        # Requisicao via Tor
        response = self.session.get(
            f"https://dados.gov.br{endpoint}",
            params=params,
            headers=self._get_headers(),
            timeout=30
        )
        
        # Salvar no cache
        self.cache[cache_key] = response.json()
        return self.cache[cache_key]
```

### 4.2 Verificacao de Anonimato
```python
def check_anonymity():
    """Verifica se IP esta realmente oculto"""
    response = requests.get(
        'https://check.torproject.org/api/ip',
        proxies=TOR_PROXY
    )
    data = response.json()
    
    if data.get('IsTor'):
        print(f"[OK] Conectado via Tor: {data['IP']}")
        return True
    else:
        print(f"[ERRO] IP exposto: {data['IP']}")
        return False
```

---

## 5. CHECKLIST DE SEGURANCA

### Pre-implementacao
- [ ] Configurar Tor local (apt install tor)
- [ ] Testar conectividade via Tor
- [ ] Verificar IP de saida (check.torproject.org)
- [ ] Implementar cache local
- [ ] Configurar throttling

### Durante uso
- [ ] Nunca usar API key (evita rastreamento)
- [ ] Verificar headers antes de cada request
- [ ] Monitorar logs para vazamentos acidentais
- [ ] Rotacionar exit nodes periodicamente

### Post-consulta
- [ ] Limpar cache sensivel
- [ ] Verificar logs de acesso
- [ ] Confirmar anonimato mantido

---

## 6. DECISAO

| Criterio            | API Direta | Modo Paranoico | Modo Espelhado |
|---------------------|------------|----------------|----------------|
| Privacidade         | RUIM       | BOM            | EXCELENTE      |
| Performance         | EXCELENTE  | RUIM           | BOM            |
| Dados atualizados   | SIM        | SIM            | ATRASADO      |
| Complexidade        | BAIXA      | MEDIA          | ALTA           |

**RECOMENDACAO:** Iniciar com Modo Paranoico. Se necessario maior privacidade, migrar para Modo Espelhado.

---

## 7. PROXIMOS PASSOS

1. [ ] Configurar Tor no WSL
2. [ ] Implementar cliente paranoid
3. [ ] Testar anonimato
4. [ ] Criar cache local
5. [ ] Documentar uso seguro

---

**Nota:** Este plano prioriza privacidade sobre performance. Em caso de conflito, privacidade sempre vence.
