# Tutorial: Manutenção e Validação de config.yaml em Agentes Hermes

**Tipo:** Tutorial genérico
**Público:** Desenvolvedores e mantenedores de agentes autônomos baseados em Hermes Agent
**Data:** 2026-04-29

---

## 1. Por que Validar config.yaml é Crítico

O arquivo `config.yaml` é o coração de um agente Hermes. Ele define modelo, provedor, credenciais, plugins, ferramentas e todas as configurações operacionais. Um YAML inválido -- mesmo um único espaço de indentação incorreto -- impede o parser de carregar o config, e o gateway do agente falha silenciosamente ou crasha ao iniciar.

O problema é que YAML não é JSON: a estrutura depende de indentação, e o parser não perdoa. Um erro visualmente sutil (como uma chave de mapping na indentação errada) pode derrubar todo o serviço.

---

## 2. O Problema Clássico: Mapping vs Lista em YAML

O erro mais frequente em configs de agentes Hermes é misturar chaves de mapping com itens de lista na mesma indentação. Isso acontece tipicamente na seção `plugins`.

### Exemplo INVÁLIDO (o que NÃO fazer)

```yaml
# ERRO: hermes-memory-store na indentação da lista "enabled"
plugins:
  enabled:
  - yolo-vision
  hermes-memory-store:      # Parser entende como continuação da lista!
  auto_extract: 'true'      # Sem indentação = nível raiz, não filho
  db_path: ~/.hermes/...    # Mesmo problema
  default_trust: '0.5'      # Mesmo problema
```

**O que o parser faz:** Ao encontrar `- yolo-vision`, ele inicia uma sequência (indentless sequence). Ao encontrar `hermes-memory-store:` na mesma indentação, ele tenta interpretar como valor da sequência -- mas o `:` indica mapping, o que gera conflito. Resultado: ScannerError.

### Exemplo VÁLIDO (como fazer)

```yaml
# CORRETO: hermes-memory-store como chave irmã de "enabled"
plugins:
  enabled:
  - yolo-vision
  hermes-memory-store:      # Mesmo nível de "enabled" (2 espaços)
    auto_extract: 'true'    # Filhos com 4 espaços
    db_path: ~/.hermes/data/memoria.db
    default_trust: '0.5'
```

**Por que funciona:** `enabled:` e `hermes-memory-store:` são ambas chaves do mapping `plugins:`, com indentação de 2 espaços. Os campos `auto_extract`, `db_path` e `default_trust` são filhos de `hermes-memory-store:`, com indentação de 4 espaços. O parser consegue desambiguar corretamente.

### Regra de ouro

> Se uma chave de mapping aparece depois de uma lista (`- item`), ela deve estar no nível do mapping pai, não no nível dos itens da lista. A indentação é o único mecanismo que o parser tem para determinar a estrutura.

---

## 3. Script de Validação Pre-Save

Antes de salvar qualquer edição em config.yaml, rode este script:

```python
#!/usr/bin/env python3
"""
validate_config.py - Valida config.yaml do agente Hermes antes de salvar.

Uso: python3 validate_config.py [caminho_para_config.yaml]

Retorna:
  - Código 0 + "YAML VALIDO" se o config parsear corretamente
  - Código 1 + mensagem de erro se houver problema

Integre como:
  - Hook de pre-commit git
  - File watcher (inotifywait, watchdog)
  - Alias de shell: alias vconfig='python3 validate_config.py'
"""

import sys
import yaml

def validate(path="config.yaml"):
    try:
        with open(path, "r") as f:
            config = yaml.safe_load(f)

        # Verificações básicas de sanidade
        if not isinstance(config, dict):
            print(f"ERRO: config não é um dicionário (tipo: {type(config).__name__})")
            return 1

        # Verificar se model está definido
        model = config.get("model", {})
        if not model.get("default"):
            print("AVISO: nenhum modelo default definido em model.default")

        if not model.get("provider"):
            print("AVISO: nenhum provedor definido em model.provider")

        # Verificar plugins se existirem
        plugins = config.get("plugins", {})
        if isinstance(plugins, dict):
            for key, value in plugins.items():
                if isinstance(value, dict):
                    # Verificar se campos do plugin tem indentação correta
                    # (se chegou aqui via safe_load, a indentação está OK)
                    pass

        print("YAML VALIDO - config parseado com sucesso")
        return 0

    except yaml.scanner.ScannerError as e:
        print(f"ERRO DE SINTAXE YAML: {e}")
        return 1
    except yaml.parser.ParserError as e:
        print(f"ERRO DE PARSE YAML: {e}")
        return 1
    except FileNotFoundError:
        print(f"ERRO: arquivo não encontrado: {path}")
        return 1
    except Exception as e:
        print(f"ERRO INESPERADO: {e}")
        return 1

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "config.yaml"
    sys.exit(validate(path))
```

### Como integrar como git pre-commit hook

```bash
# No repositório do agente (se versionar config)
cp validate_config.py .git/hooks/validate_config.py
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
python3 .git/hooks/validate_config.py config.yaml
if [ $? -ne 0 ]; then
    echo "COMMIT BLOQUEADO: config.yaml inválido"
    exit 1
fi
EOF
chmod +x .git/hooks/pre-commit
```

### Como integrar como file watcher

```bash
# Com inotifywait (Linux)
inotifywait -m -e modify ~/.hermes/config.yaml |
  while read path action file; do
    python3 validate_config.py ~/.hermes/config.yaml
    if [ $? -ne 0 ]; then
      echo "ALERTA: config.yaml inválido após modificação!"
      # Opcional: reverter para backup
      # cp ~/.hermes/config.yaml.backup ~/.hermes/config.yaml
    fi
  done
```

---

## 4. Checklist de Manutenção de Config

Antes de qualquer edição manual em config.yaml:

- [ ] Fazer backup: `cp config.yaml config.yaml.backup`
- [ ] Editar com editor que mostra indentação (VS Code, nano com --tabstospaces)
- [ ] NÃO usar tabs -- YAML requer espaços
- [ ] Rodar validação: `python3 validate_config.py`
- [ ] Se validação falhar: reverter para backup e refazer a edição
- [ ] Se validação passar: reiniciar o gateway do agente
- [ ] Confirmar que o gateway subiu: `systemctl --user is-active hermes-gateway`
- [ ] Testar inferência: enviar mensagem de teste ao agente
- [ ] Se o gateway não subir: reverter para backup e investigar

---

## 5. Recuperação de Config Corrompido -- Passo a Passo

Quando o config.yaml está inválido e o agente não inicia:

### Passo 1: Identificar o erro

```bash
# Parser YAML aponta a linha e coluna exatas
python3 -c "import yaml; yaml.safe_load(open('config.yaml'))"
```

A saída será algo como:
```
yaml.scanner.ScannerError: mapping values are not allowed here
  in "config.yaml", line 489, column 22
```

### Passo 2: Inspecionar a região do erro

```bash
# Mostrar 10 linhas antes e depois da linha indicada
sed -n '480,500p' config.yaml
```

### Passo 3: Corrigir a indentação

A correção mais confiável é reescrever o bloco inteiro com `head`/`tail`:

```bash
# Preservar tudo antes do bloco problemático
head -485 config.yaml > config_fixed.yaml

# Escrever o bloco corrigido (CUIDADO: usar espaços reais, não tabs)
cat >> config_fixed.yaml << 'BLOCK'
plugins:
  enabled:
  - yolo-vision
  hermes-memory-store:
    auto_extract: 'true'
    db_path: ~/.hermes/data/memoria.db
    default_trust: '0.5'
BLOCK

# Adicionar o restante do arquivo (após o bloco problemático)
tail -n +493 config.yaml >> config_fixed.yaml

# Validar o arquivo corrigido
python3 -c "import yaml; yaml.safe_load(open('config_fixed.yaml'))"
```

### Passo 4: Aplicar e reiniciar

```bash
# Se a validação passou, substituir o config
cp config_fixed.yaml config.yaml

# Reiniciar o gateway
systemctl --user restart hermes-gateway

# Verificar estado
systemctl --user is-active hermes-gateway
```

### Passo 5: Testar

```bash
# Enviar mensagem de teste ao agente via CLI
hermes chat -q "Responda apenas: OK e qual modelo você está usando"
```

---

## 6. Armadilhas Comuns

### 6.1 sed colapsa indentação

```bash
# NÃO FAZER ISTO: sed pode colapsar espaços
sed -i 's/^auto_extract/  auto_extract/' config.yaml
```

O `sed` funciona com padrões de texto, mas não entende YAML. Dependendo do terminal e do SSH, espaços podem ser interpretados como separadores de argumentos. Prefira `head`/`tail` + heredoc ou script Python em arquivo.

### 6.2 Scripts Python inline falham com aspas

```bash
# NÃO FAZER ISTO: aspas dentro de aspas causam erro de parse
ssh servidor "python3 -c \"import yaml; ...\""
```

Quando o comando passa por SSH e pelo shell, aspas e escapes se acumulam e quebram. Sempre escreva o script em arquivo primeiro e execute-o:

```bash
# FAZER ISTO: script em arquivo executado remotamente
cat > /tmp/fix_yaml.py << 'SCRIPT'
import yaml
# ... lógica de correção ...
SCRIPT

scp /tmp/fix_yaml.py servidor:/tmp/fix_yaml.py
ssh servidor "python3 /tmp/fix_yaml.py"
```

### 6.3 Campos inexistentes em plugins

Adicionar campos que o plugin não reconhece não causa erro de parse, mas pode causar falha silenciosa ou crash em runtime. Sempre verificar a documentação do plugin antes de adicionar campos.

---

## 7. Automação Avançada: Wrapper de Edição

Para equipes que frequentemente editam configs de agentes, um wrapper script é a solução mais robusta:

```bash
#!/bin/bash
# safe_edit_config.sh - Edita config.yaml com validação automática
#
# Uso: ./safe_edit_config.sh [editor]
# Exemplo: ./safe_edit_config.sh nano
#          ./safe_edit_config.sh vim

CONFIG="${HERMES_CONFIG:-$HOME/.hermes/config.yaml}"
BACKUP="${CONFIG}.backup.$(date +%Y%m%d_%H%M%S)"
EDITOR="${1:-${VISUAL:-nano}}"

# Backup
cp "$CONFIG" "$BACKUP"
echo "Backup criado: $BACKUP"

# Abrir editor
$EDITOR "$CONFIG"

# Validar após edição
python3 -c "import yaml; yaml.safe_load(open('$CONFIG'))" 2>/dev/null

if [ $? -eq 0 ]; then
    echo "YAML VÁLIDO - config ok"
    read -p "Reiniciar gateway? [s/N] " confirm
    if [ "$confirm" = "s" ] || [ "$confirm" = "S" ]; then
        systemctl --user restart hermes-gateway
        sleep 3
        if systemctl --user is-active hermes-gateway > /dev/null; then
            echo "Gateway reiniciado com sucesso"
        else
            echo "ERRO: gateway não subiu. Revertendo..."
            cp "$BACKUP" "$CONFIG"
            systemctl --user restart hermes-gateway
        fi
    fi
else
    echo "YAML INVÁLIDO - revertendo para backup"
    cp "$BACKUP" "$CONFIG"
    echo "Config revertido. Edição descartada."
fi
```

---

## Conclusão

A manutenção de `config.yaml` em agentes Hermes exige o mesmo rigor que a edição de código fonte em produção. Validação automatizada, backups antes de edição, e teste pós-edição são os três pilares que previnem quedas de serviço. O custo de implementar essas práticas é mínimo comparado ao custo de um agente offline por horas.

---

Tutorial genérico -- adaptável a qualquer setup Hermes Agent
29/04/2026