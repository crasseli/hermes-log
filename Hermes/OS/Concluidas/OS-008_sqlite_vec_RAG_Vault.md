---
title: "OS-008 — Implementação sqlite-vec e RAG sobre o Vault Obsidian"
date: 2026-04-26
tipo: ordem-de-servico
prioridade: alta
status: pendente-execução
agente: Hermes
solicitante: Christian
vault_destino: Hermes/OS/Ativas/
tags:
  - os-008
  - sqlite-vec
  - rag
  - embeddings
  - obsidian
  - nvidia-nim
referencias:
  - OS-006 (restauração vault)
  - OS-007 (bugs corrigidos)
  - sqlite-vec 0.1.9 PyPI
  - nv-embed-v2 NVIDIA NIM
---

# OS-008 — Implementação sqlite-vec e RAG sobre o Vault Obsidian

> **LEIA ANTES DE EXECUTAR**: Esta OS implementa busca vetorial semântica
> real sobre o vault Obsidian usando sqlite-vec + embeddings via NVIDIA NIM.
> É uma integração nova — não altera nada que já funciona. Cada fase tem
> trava obrigatória. Ao final, o vault será consultável semanticamente
> pelo protocolo de recall.

---

## Contexto

O vault tem ~290 notas indexadas via FTS5 (busca textual). A busca semântica
nunca funcionou porque `sqlite-vec` não estava instalado e o modelo de
embeddings `nv-embedcode-7b-v1` era voltado para código, não para texto em
português.

**Objetivo desta OS:**
1. Instalar `sqlite-vec` corretamente no ambiente WSL
2. Criar tabela vetorial `vec_obsidian` no `memory_store.db`
3. Gerar embeddings de todas as notas com `nv-embed-v2` (modelo generalista)
4. Criar script `search_semantic.py` funcional
5. Integrar ao protocolo de recall do SOUL.md
6. Testar end-to-end com query real em português

**Modelo de embeddings:** `nvidia/llama-nemotron-embed-1b-v2`
- Generalista, multilingual, 2048 dimensões
- Disponível via NVIDIA NIM na mesma chave atual
- Superior ao `nv-embedcode-7b-v1` para prosa em português

---

## FASE 1 — Instalação do sqlite-vec

### 1.1 — Instalar via pip

```bash
pip install sqlite-vec --break-system-packages
python3 -c "import sqlite_vec; print('sqlite-vec OK:', sqlite_vec.__version__)"
```

### 1.2 — Verificar compatibilidade com o SQLite do sistema

```bash
python3 -c "
import sqlite3
import sqlite_vec

conn = sqlite3.connect(':memory:')
conn.enable_load_extension(True)
sqlite_vec.load(conn)
conn.enable_load_extension(False)

version = conn.execute('SELECT vec_version()').fetchone()[0]
print(f'sqlite-vec carregado com sucesso: {version}')
conn.close()
"
```

### 1.3 — Verificar se memory_store.db aceita a extensão

```bash
python3 -c "
import sqlite3, sqlite_vec
from pathlib import Path

db_path = Path.home() / '.hermes/memory_store.db'
conn = sqlite3.connect(str(db_path))
conn.enable_load_extension(True)
sqlite_vec.load(conn)
conn.enable_load_extension(False)

version = conn.execute('SELECT vec_version()').fetchone()[0]
print(f'memory_store.db: sqlite-vec OK ({version})')
conn.close()
"
```

### ✅ TRAVA FASE 1

```bash
python3 -c "import sqlite_vec; print('OK:', sqlite_vec.__version__)"
```

Só avançar se retornar `OK: 0.1.x` sem erro.

---

## FASE 2 — Criação da Tabela Vetorial

### 2.1 — Verificar estado atual do banco

```bash
python3 -c "
import sqlite3, sqlite_vec
from pathlib import Path

db = sqlite3.connect(str(Path.home() / '.hermes/memory_store.db'))
db.enable_load_extension(True)
sqlite_vec.load(db)
db.enable_load_extension(False)

tables = db.execute(
    \"SELECT name FROM sqlite_master WHERE type='table' ORDER BY name\"
).fetchall()
print('Tabelas existentes:')
for t in tables:
    count = db.execute(f'SELECT COUNT(*) FROM \"{t[0]}\"').fetchone()[0]
    print(f'  {t[0]}: {count} registros')
db.close()
"
```

### 2.2 — Criar tabela vec_obsidian

```bash
python3 << 'EOF'
import sqlite3, sqlite_vec
from pathlib import Path

db = sqlite3.connect(str(Path.home() / '.hermes/memory_store.db'))
db.enable_load_extension(True)
sqlite_vec.load(db)
db.enable_load_extension(False)

# Verificar se já existe
existing = db.execute(
    "SELECT name FROM sqlite_master WHERE type='table' AND name='vec_obsidian'"
).fetchone()

if existing:
    count = db.execute('SELECT COUNT(*) FROM vec_obsidian').fetchone()[0]
    print(f'Tabela vec_obsidian já existe com {count} registros')
else:
    # nv-embed-v2 gera embeddings de 2048 dimensões
    db.execute('''
        CREATE VIRTUAL TABLE vec_obsidian USING vec0(
            filepath TEXT PRIMARY KEY,
            embedding FLOAT[2048]
        )
    ''')
    db.commit()
    print('Tabela vec_obsidian criada com sucesso (2048 dimensões)')

db.close()
EOF
```

### 2.3 — Verificar criação

```bash
python3 -c "
import sqlite3, sqlite_vec
from pathlib import Path
db = sqlite3.connect(str(Path.home() / '.hermes/memory_store.db'))
db.enable_load_extension(True)
sqlite_vec.load(db)
db.enable_load_extension(False)
result = db.execute('SELECT COUNT(*) FROM vec_obsidian').fetchone()[0]
print(f'vec_obsidian: {result} embeddings')
db.close()
"
```

### ✅ TRAVA FASE 2

Tabela `vec_obsidian` deve existir e estar acessível sem erro.

---

## FASE 3 — Geração de Embeddings

### 3.1 — Verificar disponibilidade do nv-embed-v2 via NVIDIA NIM

```bash
python3 << 'EOF'
import os, json
from pathlib import Path

# Carregar a API key do config do Hermes
config_path = Path.home() / '.hermes/config.yaml'
import yaml
config = yaml.safe_load(config_path.read_text())
api_key = config['model']['api_key']
base_url = config['model']['base_url']

# Teste de embedding com nv-embed-v2
import urllib.request
payload = json.dumps({
    "model": "nvidia/llama-nemotron-embed-1b-v2",
    "input": ["teste de embedding em português para o vault Hermes"],
    "encoding_format": "float",
        "input_type": "passage"
}).encode()

req = urllib.request.Request(
    f"{base_url}/embeddings",
    data=payload,
    headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
)

try:
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read())
        embedding = data['data'][0]['embedding']
        print(f'nv-embed-v2: OK')
        print(f'Dimensões: {len(embedding)}')
        print(f'Primeiros 5 valores: {embedding[:5]}')
except Exception as e:
    print(f'ERRO: {e}')
EOF
```

### 3.2 — Criar script de indexação do vault

Salvar em `~/.hermes/skills/obsidian/scripts/index_vault_embeddings.py`:

```python
#!/usr/bin/env python3
"""
index_vault_embeddings.py
Gera embeddings de todas as notas do vault e armazena no sqlite-vec.
Usa nv-embed-v2 via NVIDIA NIM para embeddings multilingual generalistas.
"""
import json, sqlite3, sys, time
from pathlib import Path
import yaml, sqlite_vec

# Configuração
HOME = Path.home()
VAULT_PATH = Path("/mnt/e/Obsidian/Cofre/Hermes")
DB_PATH = HOME / ".hermes/memory_store.db"
CONFIG_PATH = HOME / ".hermes/config.yaml"
BATCH_SIZE = 10          # notas por lote de embedding
EMBEDDING_DIM = 2048
EMBEDDING_MODEL = "nvidia/llama-nemotron-embed-1b-v2"

def load_config():
    config = yaml.safe_load(CONFIG_PATH.read_text())
    return config['model']['api_key'], config['model']['base_url']

def get_embedding(texts: list[str], api_key: str, base_url: str) -> list[list[float]]:
    """Gera embeddings via NVIDIA NIM nv-embed-v2."""
    import urllib.request
    # Truncar textos para 8192 tokens (~32KB chars)
    texts = [t[:32000] for t in texts]
    payload = json.dumps({
        "model": EMBEDDING_MODEL,
        "input": texts,
        "encoding_format": "float",
        "input_type": "passage"
    }).encode()
    req = urllib.request.Request(
        f"{base_url}/embeddings",
        data=payload,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = json.loads(resp.read())
    return [item['embedding'] for item in sorted(data['data'], key=lambda x: x['index'])]

def get_indexed_paths(conn) -> set:
    """Retorna o conjunto de filepaths já indexados."""
    try:
        rows = conn.execute("SELECT filepath FROM vec_obsidian").fetchall()
        return {r[0] for r in rows}
    except Exception:
        return set()

def index_vault():
    api_key, base_url = load_config()

    conn = sqlite3.connect(str(DB_PATH))
    conn.enable_load_extension(True)
    sqlite_vec.load(conn)
    conn.enable_load_extension(False)

    # Encontrar todas as notas .md
    notes = list(VAULT_PATH.rglob("*.md"))
    indexed = get_indexed_paths(conn)

    # Filtrar notas não indexadas
    to_index = [n for n in notes if str(n) not in indexed]
    total = len(to_index)

    if total == 0:
        print("Vault já está totalmente indexado.")
        conn.close()
        return

    print(f"Indexando {total} notas ({len(indexed)} já indexadas)...")

    processed = 0
    errors = 0

    # Processar em lotes
    for i in range(0, total, BATCH_SIZE):
        batch = to_index[i:i + BATCH_SIZE]
        texts = []
        valid_notes = []

        for note in batch:
            try:
                content = note.read_text(encoding='utf-8', errors='ignore')
                if len(content.strip()) < 50:
                    continue  # Pular notas muito curtas
                # Combinar filepath + conteúdo para embedding mais rico
                text = f"{note.name}\n\n{content}"
                texts.append(text)
                valid_notes.append(note)
            except Exception as e:
                print(f"  ERRO ao ler {note.name}: {e}")
                errors += 1

        if not texts:
            continue

        try:
            embeddings = get_embedding(texts, api_key, base_url)

            for note, embedding in zip(valid_notes, embeddings):
                conn.execute(
                    "INSERT OR REPLACE INTO vec_obsidian(filepath, embedding) VALUES (?, ?)",
                    (str(note), json.dumps(embedding))
                )
            conn.commit()
            processed += len(valid_notes)
            print(f"  Lote {i//BATCH_SIZE + 1}: {processed}/{total} notas indexadas")
            time.sleep(0.5)  # Rate limiting

        except Exception as e:
            print(f"  ERRO no lote {i//BATCH_SIZE + 1}: {e}")
            errors += 1
            time.sleep(2)  # Backoff em caso de erro

    print(f"\nIndexação concluída: {processed} notas indexadas, {errors} erros")
    final_count = conn.execute("SELECT COUNT(*) FROM vec_obsidian").fetchone()[0]
    print(f"Total no banco: {final_count} embeddings")
    conn.close()

if __name__ == "__main__":
    index_vault()
```

### 3.3 — Testar o script com 5 notas primeiro

```bash
# Teste com lote pequeno antes de indexar tudo
python3 << 'EOF'
import sys
sys.path.insert(0, str(__import__('pathlib').Path.home() / '.hermes/skills/obsidian/scripts'))
# Modificar BATCH_SIZE para teste
import index_vault_embeddings as iv
iv.BATCH_SIZE = 5

# Pegar apenas 5 notas para teste
from pathlib import Path
vault = Path("/mnt/e/Obsidian/Cofre/Hermes")
notes = list(vault.rglob("*.md"))[:5]
print(f"Notas para teste: {[n.name for n in notes]}")

api_key, base_url = iv.load_config()
texts = [n.read_text(errors='ignore')[:1000] for n in notes]
embeddings = iv.get_embedding(texts, api_key, base_url)
print(f"Embeddings gerados: {len(embeddings)} x {len(embeddings[0])} dimensões")
print("TESTE OK — pronto para indexação completa")
EOF
```

### 3.4 — Executar indexação completa

```bash
python3 ~/.hermes/skills/obsidian/scripts/index_vault_embeddings.py 2>&1 | tee /tmp/indexacao_log.txt
tail -5 /tmp/indexacao_log.txt
```

**Estimativa de tempo:** ~290 notas ÷ 10 por lote = ~29 lotes. Com 0.5s de delay = ~15 minutos.

### ✅ TRAVA FASE 3

```bash
python3 -c "
import sqlite3, sqlite_vec
from pathlib import Path
db = sqlite3.connect(str(Path.home() / '.hermes/memory_store.db'))
db.enable_load_extension(True)
sqlite_vec.load(db)
db.enable_load_extension(False)
count = db.execute('SELECT COUNT(*) FROM vec_obsidian').fetchone()[0]
print(f'Embeddings no banco: {count}')
db.close()
"
```

Só avançar se count > 200 (maioria das notas indexadas).

---

## FASE 4 — Script de Busca Semântica

### 4.1 — Criar search_semantic.py

Salvar em `~/.hermes/skills/obsidian/scripts/search_semantic.py`:

```python
#!/usr/bin/env python3
"""
search_semantic.py
Busca semântica no vault Obsidian via sqlite-vec + nv-embed-v2.
Uso: python3 search_semantic.py "sua query aqui" [--top N]
"""
import json, sqlite3, sys, argparse
from pathlib import Path
import yaml, sqlite_vec

HOME = Path.home()
DB_PATH = HOME / ".hermes/memory_store.db"
CONFIG_PATH = HOME / ".hermes/config.yaml"
EMBEDDING_MODEL = "nvidia/llama-nemotron-embed-1b-v2"

def load_config():
    config = yaml.safe_load(CONFIG_PATH.read_text())
    return config['model']['api_key'], config['model']['base_url']

def get_query_embedding(query: str, api_key: str, base_url: str) -> list[float]:
    import urllib.request
    payload = json.dumps({
        "model": EMBEDDING_MODEL,
        "input": [query],
        "encoding_format": "float",
        "input_type": "passage"
    }).encode()
    req = urllib.request.Request(
        f"{base_url}/embeddings",
        data=payload,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read())
    return data['data'][0]['embedding']

def search(query: str, top_n: int = 5) -> list[dict]:
    api_key, base_url = load_config()
    query_embedding = get_query_embedding(query, api_key, base_url)

    conn = sqlite3.connect(str(DB_PATH))
    conn.enable_load_extension(True)
    sqlite_vec.load(conn)
    conn.enable_load_extension(False)

    # Busca KNN no sqlite-vec
    results = conn.execute('''
        SELECT
            v.filepath,
            v.distance,
            i.title,
            i.folder,
            i.tags
        FROM vec_obsidian v
        LEFT JOIN obsidian_index i ON i.filepath = v.filepath
        WHERE v.embedding MATCH ?
        AND k = ?
        ORDER BY v.distance
    ''', (json.dumps(query_embedding), top_n)).fetchall()

    conn.close()

    output = []
    for row in results:
        filepath, distance, title, folder, tags = row
        note_path = Path(filepath)
        try:
            snippet = note_path.read_text(errors='ignore')[:300]
        except Exception:
            snippet = "(arquivo não encontrado)"
        output.append({
            'filepath': filepath,
            'distance': round(distance, 4),
            'title': title or note_path.stem,
            'folder': folder or str(note_path.parent),
            'tags': tags or '',
            'snippet': snippet
        })

    return output

def main():
    parser = argparse.ArgumentParser(description='Busca semântica no vault Obsidian')
    parser.add_argument('query', help='Query de busca em linguagem natural')
    parser.add_argument('--top', type=int, default=5, help='Número de resultados (default: 5)')
    args = parser.parse_args()

    print(f"Buscando: '{args.query}'\n")
    results = search(args.query, args.top)

    if not results:
        print("Nenhum resultado encontrado.")
        return

    for i, r in enumerate(results, 1):
        print(f"[{i}] {r['title']}")
        print(f"    📁 {r['folder']}")
        print(f"    📏 Distância: {r['distance']}")
        print(f"    🔖 Tags: {r['tags']}")
        print(f"    📄 {r['snippet'][:150]}...")
        print()

if __name__ == "__main__":
    main()
```

### 4.2 — Tornar executável

```bash
chmod +x ~/.hermes/skills/obsidian/scripts/search_semantic.py
python3 -m py_compile ~/.hermes/skills/obsidian/scripts/search_semantic.py \
  && echo "SINTAXE OK"
```

### ✅ TRAVA FASE 4

```bash
python3 ~/.hermes/skills/obsidian/scripts/search_semantic.py \
  "protocolo de recall memória" --top 3 2>&1
```

Deve retornar 3 resultados com distâncias e snippets. Se retornar resultados
relevantes (notas sobre recall, SOUL, memória), o RAG está funcional.

---

## FASE 5 — Atualizar search_vault.py para Busca Híbrida

**Objetivo:** o `search_vault.py` atual usa apenas FTS5. Atualizar para
fazer busca híbrida: FTS5 + semântica, combinando os resultados.

### 5.1 — Verificar search_vault.py atual

```bash
cat ~/.hermes/skills/obsidian/scripts/search_vault.py | head -80
```

### 5.2 — Adicionar modo semântico ao search_vault.py

Localizar a função principal e adicionar flag `--semantic`:

```bash
grep -n "def search\|argparse\|add_argument\|--combined" \
  ~/.hermes/skills/obsidian/scripts/search_vault.py | head -20
```

Adicionar ao argparse existente:

```python
parser.add_argument('--semantic', action='store_true',
    help='Usar busca semântica via sqlite-vec (requer embeddings indexados)')
```

E na lógica de busca, se `--semantic` ou `--combined`:

```python
if args.semantic or args.combined:
    try:
        from search_semantic import search as semantic_search
        semantic_results = semantic_search(query, top_n=5)
        # Merge com FTS5 results, deduplicar por filepath
        for r in semantic_results:
            if r['filepath'] not in seen_paths:
                results.append(r)
                seen_paths.add(r['filepath'])
    except Exception as e:
        print(f"[WARN] Busca semântica indisponível: {e}", file=sys.stderr)
```

### ✅ TRAVA FASE 5

```bash
python3 ~/.hermes/skills/obsidian/scripts/search_vault.py \
  "OS-006 restauração vault" --combined 2>&1 | head -30
```

Deve retornar resultados combinados FTS5 + semântica.

---

## FASE 6 — Atualizar SOUL.md e Criar Cron de Reindexação

### 6.1 — Atualizar protocolo de recall no SOUL.md

Adicionar `search_semantic.py` como opção no Passo 2 do recall:

```bash
cp ~/.hermes/SOUL.md ~/.hermes/SOUL_pre_os008_$(date +%Y-%m-%d).md
```

Atualizar a seção RECALL para:

```markdown
### PASSO 2 — Buscar no vault Obsidian (se fact_store vazio)
Segunda tool call obrigatória:

  terminal: python3 ~/.hermes/skills/obsidian/scripts/search_vault.py "<termo>" --combined

O flag --combined ativa busca híbrida: FTS5 (textual) + semântica (vetorial).
Se sqlite-vec indisponível, cai automaticamente para FTS5 apenas.
```

### 6.2 — Criar cron de reindexação incremental

```bash
# Verificar se há um cron para indexação
hermes cron list 2>/dev/null | grep -i "index\|embed\|vec"
```

Se não existir, criar via Hermes CLI:
- Nome: `reindex-vault-embeddings`
- Schedule: `0 3 * * *` (3h da manhã, diariamente)
- Prompt: indexar apenas notas novas/modificadas desde a última indexação

### ✅ TRAVA FASE 6

```bash
grep -c "combined\|search_semantic\|semântica" ~/.hermes/SOUL.md
```

Deve retornar > 0.

---

## FASE 7 — Teste End-to-End

### 7.1 — Teste de query semântica real em português

```bash
echo "=== Query 1: conceito técnico ==="
python3 ~/.hermes/skills/obsidian/scripts/search_semantic.py \
  "como funciona o sistema de memória do Hermes" --top 5

echo ""
echo "=== Query 2: projeto específico ==="
python3 ~/.hermes/skills/obsidian/scripts/search_semantic.py \
  "integração SQLite vault Obsidian embeddings" --top 5

echo ""
echo "=== Query 3: busca híbrida via search_vault ==="
python3 ~/.hermes/skills/obsidian/scripts/search_vault.py \
  "protocolo recall fact_store" --combined --top 5
```

### 7.2 — Validar relevância dos resultados

Para cada query, verificar se os resultados fazem sentido semanticamente —
não apenas correspondência de palavras-chave.

Registrar no relatório:
- [ ] Query 1 retornou notas relevantes sobre memória do Hermes?
- [ ] Query 2 retornou notas sobre SQLite/Obsidian?
- [ ] Query 3 combinou FTS5 + semântica sem erro?
- [ ] Distâncias são < 1.0 para resultados relevantes?

### ✅ TRAVA FASE 7

Pelo menos 2 das 3 queries devem retornar resultados semanticamente
relevantes (não apenas correspondência de palavras).

---

## FASE 8 — Documentação e Encerramento

### 8.1 — Salvar relatório no vault

```bash
VAULT="/mnt/e/Obsidian/Cofre/Hermes"
cat > "$VAULT/OS/Concluidas/Relatorio_OS-008_$(date +%Y-%m-%d).md" << 'EOF'
---
title: "Relatório OS-008 — sqlite-vec e RAG Vault"
date: 2026-04-26
tags: os-008, sqlite-vec, rag, embeddings, nv-embed-v2
---

# Relatório OS-008

## Resumo
[preencher]

## Resultados por Fase

| Fase | Status | Detalhes |
|------|--------|----------|
| 1 | ✅/❌ | sqlite-vec [versão] instalado |
| 2 | ✅/❌ | vec_obsidian criada com 2048 dims |
| 3 | ✅/❌ | [N] embeddings gerados |
| 4 | ✅/❌ | search_semantic.py funcional |
| 5 | ✅/❌ | search_vault.py híbrido |
| 6 | ✅/❌ | SOUL.md e cron atualizados |
| 7 | ✅/❌ | E2E validado |

## Modelo de Embeddings
- Modelo: nvidia/llama-nemotron-embed-1b-v2
- Dimensões: 4096
- Notas indexadas: [N]

## Qualidade da Busca
[Exemplos de queries e resultados]

## Status Final
RAG funcional: SIM/NÃO
Solicitante: Christian | Executor: Hermes
EOF
```

### 8.2 — Commit git e fact_store

```bash
cd /mnt/e/Obsidian/Cofre/Hermes
git add OS/Concluidas/Relatorio_OS-008_*.md
git commit -m "OS-008: implementação sqlite-vec e RAG sobre o vault"
```

```
fact_store(action="add"):
  "OS-008 concluída em [data]. sqlite-vec [versão] instalado.
  [N] notas indexadas com nv-embed-v2 (2048 dims).
  search_semantic.py e search_vault.py --combined funcionais.
  RAG sobre o vault Obsidian ativo e integrado ao protocolo de recall."
```

### 8.3 — Mover OS para Concluídas

```bash
VAULT="/mnt/e/Obsidian/Cofre/Hermes"
mv "$VAULT/OS/Ativas/OS-008_sqlite_vec_RAG_Vault.md" \
   "$VAULT/OS/Concluidas/" 2>/dev/null && echo "OS-008 arquivada"
```

---

## Checklist Final

- [ ] Fase 1 — sqlite-vec instalado e testado no memory_store.db
- [ ] Fase 2 — vec_obsidian criada com 2048 dimensões
- [ ] Fase 3 — 200+ notas indexadas com nv-embed-v2
- [ ] Fase 4 — search_semantic.py funcional com resultados relevantes
- [ ] Fase 5 — search_vault.py --combined híbrido operacional
- [ ] Fase 6 — SOUL.md atualizado + cron de reindexação criado
- [ ] Fase 7 — E2E validado com 3 queries em português
- [ ] Fase 8 — Relatório salvo, git commit, fact_store atualizado
- [ ] Christian informado do resultado

---

## Arquitetura Final Após Esta OS

```
Query do usuário
       │
       ▼
  fact_store ──── Holographic (fatos estruturados)
       │ vazio
       ▼
search_vault --combined
       ├── FTS5 (busca textual exata)
       └── search_semantic (busca vetorial)
                │
                ▼
         sqlite-vec (vec_obsidian)
                │
                ▼
         nv-embed-v2 (2048 dims)
       │ vazio
       ▼
  session_search (histórico)
       │ vazio
       ▼
  web_search (externo)
```

---

*OS emitida em 2026-04-26 | Solicitante: Christian | Agente executor: Hermes*
*Prerequisitos: OS-006 e OS-007 concluídas*
*Versão: 1.0*
