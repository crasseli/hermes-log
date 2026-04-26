**HERMES AGENT**

Plano de Memória, Obsidian &amp; Config por Demanda

Instruções completas para execução passo a passo

Versão 1.0  ·  Abril 2026

Vault: /mnt/e/Obsidian/Cofre/Hermes/

Provider recomendado: Holographic (SQLite local)

## 1. Contexto e Arquitetura de Memória

O Hermes opera com três camadas de memória independentes que precisam funcionar em sincronia. Compreender cada camada é obrigatório antes de qualquer configuração.

### 1.1 As três camadas

| **Camada**                  | **Tecnologia**       | **Papel**                                                                                                       |
|-----------------------------|----------------------|-----------------------------------------------------------------------------------------------------------------|
| Camada 0 — Sessão           | MEMORY.md / USER.md  | Sempre ativa. Memória de curto prazo da sessão atual. Não persiste entre sessões. Built-in, não é um provider.  |
| Camada 1 — Provider         | Holographic (SQLite) | Índice e cache de longo prazo. Apenas 1 provider ativo por vez. Persiste entre sessões. Busca rápida via FTS5.  |
| Camada 2 — Fonte da Verdade | Obsidian Vault       | Memória definitiva em markdown. Obsidian SEMPRE vence em conflitos (obsidian_wins). Versionada pelo filesystem. |

**⚠️ Regra crítica:** Só um provider externo pode estar ativo por vez. O built-in (MEMORY.md) funciona sempre ao lado do provider escolhido, de forma aditiva — nunca o substitui.

### 1.2 Hierarquia de conflito

Quando Obsidian e SQLite divergirem (ex: arquivo renomeado sem reindex), a regra é:

- Obsidian → fonte da verdade (obsidian\_wins)
- SQLite → índice derivado, sempre reconstruível a partir do vault
- MEMORY.md → cache de sessão, descartável ao final de cada conversa

## 2. Diagnóstico Pré-Configuração

Execute estes comandos ANTES de qualquer alteração. Registre os resultados no diário do Obsidian.

### 2.1 Verificar estado atual

hermes memory status

Resultado esperado: indica qual provider está ativo (ou nenhum). Se já houver um provider ativo diferente do Holographic, anote antes de continuar.

cat ~/.hermes/config.yaml

Verifique se já existe configuração de memória. Se existir, faça backup antes de editar:

cp ~/.hermes/config.yaml ~/.hermes/config.yaml.bak.$(date +%Y%m%d)

### 2.2 Verificar integridade do vault após reorganização

find "/mnt/e/Obsidian/Cofre/Hermes/" -type f -name "*.md" | sort

Confirme que os arquivos renomeados (Sessão → Sessao) estão no lugar correto e sem duplicatas.

find "/mnt/e/Obsidian/Cofre/Hermes/" -name "*Sessão*" -o -name "*Correção*" 2&gt;/dev/null

Este comando deve retornar VAZIO. Se retornar arquivos, há remanescentes com acento que precisam ser renomeados.

### 2.3 Verificar se SQLite existente tem referências quebradas

ls -la ~/.hermes/*.db 2&gt;/dev/null || echo 'Nenhum banco encontrado'

Se houver um .db existente, o reindex será necessário após ativar o Holographic.

## 3. Configuração do Provider Holographic

### 3.1 Por que Holographic

| **Atributo**         | **Detalhe**                                            |
|----------------------|--------------------------------------------------------|
| Armazenamento        | SQLite local — sem dependências externas               |
| Custo                | Gratuito — sem API keys, sem cloud                     |
| Busca                | FTS5 full-text + queries algébricas HRR                |
| Compatibilidade      | Funciona perfeitamente com scripts Obsidian existentes |
| Trust scoring        | Pontua facts por confiabilidade (ajustável)            |
| Detecção de conflito | Identifica facts contraditórios automaticamente        |

### 3.2 Ativação via wizard (recomendado)

hermes memory setup

Selecione "holographic" na lista interativa. O wizard instala dependências e cria a configuração inicial automaticamente.

### 3.3 Ativação manual (alternativa)

hermes config set memory.provider holographic

### 3.4 Verificar ativação

hermes memory status

Deve exibir: provider: holographic — active: true

## 4. Bloco config.yaml Completo

Adicione ou mescle este bloco no ~/.hermes/config.yaml. Não substitua configurações existentes de outras seções.

**📋 Instrução:** Copie o bloco abaixo e cole no config.yaml, substituindo qualquer chave memory: já existente. Manténha as demais configurações do arquivo intactas.

memory:

provider: holographic          # único provider externo ativo

plugins:

hermes-memory-store:           # configuração do Holographic

db\_path: ~/.hermes/memory\_store.db

auto\_extract: true           # extrai fatos ao fim de cada sessão

default\_trust: 0.7           # score inicial elevado (Obsidian é confiável)

obsidian:

vault\_path: /mnt/e/Obsidian/Cofre/Hermes/

autosync: true

sync\_interval: 300             # 5 minutos entre sincronizações automáticas

conflict\_resolution: obsidian\_wins

watch\_filesystem: true         # reage a mudanças no vault em tempo real

backup\_before\_sync: true       # backup automático antes de sincronizar

role: primary                  # Obsidian = fonte da verdade

sqlite:

path: ~/.hermes/memory\_store.db

role: index                    # apenas índice derivado do Obsidian

mirror\_obsidian\_structure: true

### 4.1 Significado de cada parâmetro

| **Parâmetro**                      | **Componente**   | **Efeito prático**                                                                                  |
|------------------------------------|------------------|-----------------------------------------------------------------------------------------------------|
| auto_extract: true                 | Holographic      | Extrai automaticamente fatos das conversões ao encerrar a sessão e armazena no SQLite.              |
| default_trust: 0.7                 | Holographic      | Facts recém-adicionados começam com 70% de confiança. Sobe com feedback positivo, cai com negativo. |
| conflict_resolution: obsidian_wins | Obsidian         | Em qualquer conflito de conteúdo, o arquivo .md do vault prevalece sobre o SQLite.                  |
| watch_filesystem: true             | Obsidian         | Daemon monitora o vault e dispara reindex sempre que um arquivo é criado, movido ou renomeado.      |
| backup_before_sync: true           | Obsidian         | Cria cópia do vault antes de operações em massa (evita perda por conflito de sync).                 |
| mirror_obsidian_structure: true    | SQLite           | O esquema do SQLite espelha a hierarquia de pastas do vault (mesmos caminhos relativos).            |

## 5. Script de Reindex do Vault

Este script deve ser executado SEMPRE que houver reorganização de arquivos no vault (renomeios, movições, exclusões). Salve em ~/.hermes/skills/obsidian/scripts/reindex\_vault.py

### 5.1 Criação do script

cat &gt; ~/.hermes/skills/obsidian/scripts/reindex\_vault.py &lt;&lt; 'PYEOF'

#!/usr/bin/env python3

"""Reindex completo do vault Obsidian no SQLite do Holographic.

Uso: python3 reindex\_vault.py [--dry-run]"""

import os, sys, sqlite3, hashlib, json, argparse

from pathlib import Path

from datetime import datetime

VAULT = Path("/mnt/e/Obsidian/Cofre/Hermes")

DB    = Path.home() / ".hermes" / "memory\_store.db"

def md5(path):

return hashlib.md5(path.read\_bytes()).hexdigest()

def extract\_frontmatter(text):

if not text.startswith('---'): return {}, text

end = text.find('---', 3)

if end == -1: return {}, text

fm\_raw = text[3:end].strip()

meta = {}

for line in fm\_raw.splitlines():

if ':' in line:

k, \_, v = line.partition(':')

meta[k.strip()] = v.strip()

return meta, text[end+3:].strip()

def main():

ap = argparse.ArgumentParser()

ap.add\_argument('--dry-run', action='store\_true')

args = ap.parse\_args()

con = sqlite3.connect(DB)

cur = con.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS obsidian\_index (

filepath TEXT PRIMARY KEY,

title TEXT, folder TEXT, tags TEXT,

checksum TEXT, last\_modified REAL,

synced\_at TEXT)''')

md\_files = list(VAULT.rglob('*.md'))

print(f'Encontrados {len(md\_files)} arquivos .md')

updated = removed = skipped = 0

# Remover entradas de arquivos que não existem mais

cur.execute('SELECT filepath FROM obsidian\_index')

existing = {r[0] for r in cur.fetchall()}

for fp in existing:

if not Path(fp).exists():

if not args.dry\_run:

cur.execute('DELETE FROM obsidian\_index WHERE filepath=?', (fp,))

removed += 1

print(f'  REMOVIDO: {fp}')

# Inserir/atualizar arquivos do vault

for f in md\_files:

chk = md5(f)

cur.execute('SELECT checksum FROM obsidian\_index WHERE filepath=?', (str(f),))

row = cur.fetchone()

if row and row[0] == chk:

skipped += 1

continue

text = f.read\_text(encoding='utf-8', errors='replace')

meta, \_ = extract\_frontmatter(text)

folder = str(f.relative\_to(VAULT).parent)

title  = meta.get('title', f.stem)

tags   = meta.get('tags', '')

mtime  = f.stat().st\_mtime

now    = datetime.now().isoformat()

if not args.dry\_run:

cur.execute('''INSERT OR REPLACE INTO obsidian\_index

(filepath,title,folder,tags,checksum,last\_modified,synced\_at)

VALUES (?,?,?,?,?,?,?)''',

(str(f), title, folder, tags, chk, mtime, now))

updated += 1

print(f'  OK: {f.relative\_to(VAULT)}')

if not args.dry\_run: con.commit()

con.close()

print(f'\nReindex concluído: {updated} atualizados, {removed} removidos, {skipped} sem alteração')

if \_\_name\_\_ == '\_\_main\_\_': main()

PYEOF

chmod +x ~/.hermes/skills/obsidian/scripts/reindex\_vault.py

### 5.2 Execução

# Simulação (sem gravar)

python3 ~/.hermes/skills/obsidian/scripts/reindex\_vault.py --dry-run

# Execução real

python3 ~/.hermes/skills/obsidian/scripts/reindex\_vault.py

### 5.3 Quando executar o reindex

- Após qualquer reorganização de pastas no vault
- Após renomear arquivos (especialmente remoção de acentos)
- Após importar arquivos externos para o vault
- Sempre que hermes memory status reportar inconsistências
- Como primeira ação ao iniciar uma nova sessão de reorganização

## 6. Rotina de Inicialização de Sessão

Adicione este bloco ao daily\_note.py ou execute manualmente no início de cada sessão de trabalho com o vault.

### 6.1 Checklist de startup

- Verificar status do provider: hermes memory status
- Verificar integridade do vault: find vault -name '*.md' | wc -l
- Executar reindex se houve mudanças desde a última sessão
- Confirmar que backup\_before\_sync está ativo antes de operações em massa

### 6.2 Bloco para daily\_note.py (startup automático)

# Adicionar ao final do daily\_note.py na função de inicialização:

import subprocess, os

def startup\_checks():

vault = "/mnt/e/Obsidian/Cofre/Hermes"

reindex = os.path.expanduser(

"~/.hermes/skills/obsidian/scripts/reindex\_vault.py")

# Só faz reindex se vault foi modificado nas últimas 24h

result = subprocess.run(

["find", vault, "-newer",

os.path.expanduser("~/.hermes/memory\_store.db"),

"-name", "*.md"],

capture\_output=True, text=True)

if result.stdout.strip():

print("Vault modificado. Executando reindex...")

subprocess.run(["python3", reindex])

else:

print("✅ Índice SQLite sincronizado com o vault.")

## 7. Estrutura do Vault (Referência)

Esta é a estrutura oficial do vault após a reorganização de 2026-04-20. Qualquer novo arquivo deve seguir estas convenções.

### 7.1 Árvore de pastas

Hermes/

├── README.md                  ← índice central, sempre atualizado

├── Conhecimento/

│   ├── Skills/                ← documentação de skills do Hermes

│   └── Seguranca/             ← segurança da informação

├── Conversas/

│   └── 2026/                  ← diários, sessões, retrospectivas

├── Inbox/

│   └── Processados/           ← arquivos já triados

├── NotebookLM/

│   └── Documentacao/          ← docs da integração NotebookLM

├── Pesquisas/

│   └── Arxiv/                 ← papers e artigos

├── Pessoas/                   ← contatos e perfis

├── Projetos/                  ← projetos em andamento

├── Tarefas/                   ← listas de tarefas e TODOs

└── Tecnologia/

└── Seguranca/             ← JWT, OAuth, REST APIs

### 7.2 Convenções de nomenclatura

| **Elemento**   | **Convenção**                                                        |
|----------------|----------------------------------------------------------------------|
| Acentos        | NUNCA usar em nomes de arquivo. Sessão → Sessao, Correção → Correcao |
| Separador      | Underscore _ (nunca espaço ou hífen isolado)                         |
| Data           | Formato AAAA-MM-DD (ex: 2026-04-20)                                  |
| Diário         | Diario_AAAA-MM-DD.md                                                 |
| Sessões        | Sessoes_AAAA-MM-DD.md                                                |
| Retrospectivas | Sessao_AAAA-MM-DD_-_Tema.md                                          |
| Skills         | Skill_Nome_da_Skill.md                                               |
| Segurança      | Nome_Tecnico_Sem_Acento.md                                           |

## 8. Ferramentas do Holographic (Uso em Sessão)

Quando o Holographic está ativo, o Hermes ganha acesso a duas ferramentas nativas. Use-as para interação direta com a memória SQLite.

### 8.1 fact\_store — 9 ações

| **Ação**   | **Descrição**                                         |
|------------|-------------------------------------------------------|
| add        | Adiciona um fato novo com trust score inicial         |
| search     | Busca full-text FTS5 por termo ou frase               |
| probe      | Recall algébrico de todos os fatos sobre uma entidade |
| related    | Fatos semanticamente relacionados a um termo          |
| reason     | Query AND compositional entre múltiplas entidades     |
| contradict | Detecta fatos contraditórios automaticamente          |
| update     | Atualiza conteúdo ou trust score de um fato           |
| remove     | Remove um fato específico pelo ID                     |
| list       | Lista todos os fatos com filtro opcional              |

### 8.2 fact\_feedback — rating de trust

Use fact\_feedback(helpful=true) para aumentar o trust de um fato em +0.05 e fact\_feedback(helpful=false) para reduzir em -0.10. Trust varia de 0.0 a 1.0.

**💡 Dica:** Após executar o reindex, rode fact\_store(search='obsidian') para confirmar que os metadados do vault foram indexados corretamente no SQLite.

## 9. Plano de Execução por Demanda

Execute as fases na ordem. Cada fase é independente — pare ao final de qualquer uma e retome na próxima sessão sem perda.

### Fase 1 — Diagnóstico (5 min)

- hermes memory status → anotar resultado
- cat ~/.hermes/config.yaml → fazer backup se existir
- find vault -name '*Sessão*' -o -name '*Correção*' → deve retornar vazio

### Fase 2 — Ativação do Holographic (5 min)

- hermes memory setup → selecionar holographic
- hermes memory status → confirmar ativo
- Adicionar bloco da Seção 4 ao config.yaml

### Fase 3 — Reindex do Vault (10 min)

- Criar script reindex\_vault.py conforme Seção 5
- Executar --dry-run e revisar saída
- Executar versão real e confirmar contagens
- fact\_store(search='obsidian') → validar index

### Fase 4 — Integração com daily\_note.py (10 min)

- Adicionar função startup\_checks() ao daily\_note.py
- Testar execução manual
- Registrar conclusão no diário do Obsidian

### Fase 5 — Validação final (5 min)

- Abrir nova sessão do Hermes
- Confirmar que startup\_checks() executa automaticamente
- Testar fact\_store(probe='obsidian') e fact\_store(search='vault')
- Confirmar que Obsidian segue como fonte da verdade

## 10. Resolução de Problemas

### Provider não ativa

- Verificar: pip install --user sqlite3 (raramente necessário, SQLite é built-in no Python)
- Verificar: hermes plugins → Provider Plugins → Memory Provider
- Alternativa: hermes config set memory.provider holographic (manual)

### Reindex reporta arquivos não encontrados

- Significa que o SQLite tinha referências de antes da reorganização
- Normal após a reorganização de 2026-04-20 — o reindex remove essas entradas
- Confirmar com: SELECT COUNT(*) FROM obsidian\_index; no sqlite3 ~/.hermes/memory\_store.db

### Conflito Obsidian vs SQLite

- Por definição: Obsidian SEMPRE vence
- Para forçar resolução: python3 reindex\_vault.py (reconstrói SQLite a partir do vault)
- Nunca editar o .db diretamente para resolver conflitos

### watch\_filesystem não detecta mudanças

- Verificar se o vault está em drive montado (Windows ↔ WSL pode ter delay)
- Solução: aumentar sync\_interval ou executar reindex manual após reorganizações

Hermes Agent v0.10.0  ·  Vault: /mnt/e/Obsidian/Cofre/Hermes/  ·  Provider: Holographic (SQLite local)