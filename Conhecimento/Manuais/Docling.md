Aqui está o manual completo de uso do Docling em Python no WSL2, com contexto de integração com o Hermes Agent:

***

# Manual de Uso do Docling em Python no WSL2

## 1. Introdução ao Docling

Docling é uma biblioteca open source (licença MIT) para conversão de documentos voltada para GenAI. Suporta PDF, DOCX, PPTX, XLSX, HTML, Markdown, LaTeX, imagens e até áudio/vídeo [[1]](https://app.dosu.dev/097760a8-135e-4789-8234-90c8837d7f1c/documents/30f358d9-e4a4-4dd8-a4c5-5cb25bd4a380). As principais capacidades incluem:

- Extração avançada de layout e tabelas com modelos de deep learning
- OCR para documentos escaneados
- Chunking otimizado para RAG (Retrieval-Augmented Generation)
- Exportação para Markdown, JSON, HTML e texto puro
- Integrações oficiais com LlamaIndex e LangChain

***

## 2. Pré-requisitos e Configuração do WSL2

### Habilitando WSL2 no Windows

```powershell
# No PowerShell como Administrador
wsl --install
wsl --set-default-version 2
```

Reinicie o computador e instale o Ubuntu pela Microsoft Store.

### Instalando dependências no WSL2 (Ubuntu)

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-venv \
    tesseract-ocr libtesseract-dev leptonica-dev \
    pkg-config ffmpeg build-essential
```

**Requisito**: Python 3.9 ou superior [[2]](https://app.dosu.dev/097760a8-135e-4789-8234-90c8837d7f1c/documents/5cf33ffc-a9ed-485c-9a8c-b7b534c38ce2).

### Criando um ambiente virtual

```bash
python3 -m venv ~/docling-env
source ~/docling-env/bin/activate
```

***

## 3. Instalação do Docling

### Instalação básica

```bash
pip install docling
```

### Extras opcionais [[1]](https://app.dosu.dev/097760a8-135e-4789-8234-90c8837d7f1c/documents/30f358d9-e4a4-4dd8-a4c5-5cb25bd4a380)

```bash
# OCR com Tesseract (alta qualidade)
pip install "docling[tesserocr]"

# Vision-Language Models (tabelas avançadas e descrição de imagens)
pip install "docling[vlm]"

# HTML com renderização headless (Playwright)
pip install "docling[htmlrender]"

# Transcrição de áudio/vídeo
pip install "docling[asr]"

# Instalação completa
pip install "docling[tesserocr,vlm,htmlrender,asr]"
```

### Download de modelos

```bash
pip install docling-tools
docling-tools models download --all -o ~/docling-models
```

### Aceleração GPU (opcional)

```bash
export DOCLING_DEVICE=cuda  # NVIDIA com CUDA no WSL2
```

### Verificação da instalação

```python
from docling.document_converter import DocumentConverter
converter = DocumentConverter()
print("Docling instalado com sucesso!")
```

***

## 4. Uso Básico em Python

### Conversão simples de PDF [[3]](https://github.com/docling-project/docling/blob/075fa69491826a0b295a3022f64c568822a3f68d/README.md#L78-L85)

```python
from docling.document_converter import DocumentConverter

converter = DocumentConverter()
result = converter.convert("documento.pdf")

# Exportar para Markdown
print(result.document.export_to_markdown())
```

### Exportação em diferentes formatos [[4]](https://app.dosu.dev/097760a8-135e-4789-8234-90c8837d7f1c/documents/d4d670cd-8b56-4ca4-ae72-6be60441fba7)

```python
# Markdown
md = result.document.export_to_markdown()

# Texto puro
texto = result.document.export_to_text()

# HTML
html = result.document.export_to_html()

# Salvar em arquivos
result.document.save_as_markdown("saida.md")
result.document.save_as_json("saida.json")
result.document.save_as_html("saida.html")
```

### Conversão de múltiplos documentos [[5]](https://github.com/docling-project/docling/blob/075fa69491826a0b295a3022f64c568822a3f68d/docling/document_converter.py#L391-L468)

```python
fontes = ["doc1.pdf", "doc2.docx", "apresentacao.pptx"]
resultados = converter.convert_all(fontes)

for res in resultados:
    print(f"Arquivo: {res.input.file}")
    print(res.document.export_to_markdown()[:500])
    print("---")
```

### Diferentes formatos de entrada

```python
# DOCX
result = converter.convert("relatorio.docx")

# PPTX
result = converter.convert("apresentacao.pptx")

# Imagem com OCR
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.document_converter import PdfFormatOption

converter = DocumentConverter(
    format_options={
        InputFormat.IMAGE: PdfFormatOption(
            pipeline_options=PdfPipelineOptions(do_ocr=True)
        )
    }
)
result = converter.convert("imagem.png")
```

***

## 5. Uso Avançado

### Configuração de OCR [[6]](https://app.dosu.dev/097760a8-135e-4789-8234-90c8837d7f1c/documents/d50f0b52-1ecf-4bd0-b9ff-93f88d6ef14a)

```python
from docling.datamodel.pipeline_options import PdfPipelineOptions, EasyOcrOptions
from docling.datamodel.base_models import InputFormat
from docling.document_converter import DocumentConverter, PdfFormatOption

pipeline_options = PdfPipelineOptions()
pipeline_options.do_ocr = True
pipeline_options.ocr_options = EasyOcrOptions(
    lang=["en", "pt"],         # Inglês e Português
    use_gpu=True,
    confidence_threshold=0.6,
)

converter = DocumentConverter(
    format_options={
        InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
    }
)
result = converter.convert("documento_escaneado.pdf")

# Para PDFs escaneados, use traverse_pictures=True
texto = result.document.export_to_text(traverse_pictures=True)
```

### Extração de tabelas [[1]](https://app.dosu.dev/097760a8-135e-4789-8234-90c8837d7f1c/documents/30f358d9-e4a4-4dd8-a4c5-5cb25bd4a380)

```python
from docling.datamodel.pipeline_options import PdfPipelineOptions, TableStructureV2Options

pipeline_options = PdfPipelineOptions()
pipeline_options.do_table_structure = True
pipeline_options.table_structure_options = TableStructureV2Options(
    do_cell_matching=True
)

converter = DocumentConverter(
    format_options={
        InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
    }
)
result = converter.convert("relatorio_com_tabelas.pdf")
```

### Pipeline completo com todas as opções

```python
pdf_options = PdfPipelineOptions()
pdf_options.do_ocr = True
pdf_options.do_table_structure = True
pdf_options.do_code_enrichment = True
pdf_options.do_formula_enrichment = True
pdf_options.generate_page_images = True
pdf_options.generate_picture_images = True

converter = DocumentConverter(
    format_options={
        InputFormat.PDF: PdfFormatOption(pipeline_options=pdf_options)
    }
)
```

### Chunking para RAG [[7]](https://app.dosu.dev/097760a8-135e-4789-8234-90c8837d7f1c/documents/fe4d019c-b418-4fe9-b585-bfc46e4c648f)

```python
from docling.chunking import HybridChunker

result = converter.convert("documento.pdf")
doc = result.document

chunker = HybridChunker(max_tokens=512)
chunks = list(chunker.chunk(dl_doc=doc))

for chunk in chunks:
    # Texto contextualizado para embeddings
    texto_enriquecido = chunker.contextualize(chunk=chunk)
    print(texto_enriquecido[:200])
```

### Integração com LlamaIndex [[8]](https://github.com/docling-project/docling/blob/075fa69491826a0b295a3022f64c568822a3f68d/docs/examples/rag_llamaindex.ipynb)

```bash
pip install llama-index-readers-docling llama-index-node-parser-docling
```

```python
from llama_index.readers.docling import DoclingReader
from llama_index.node_parser.docling import DoclingNodeParser

reader = DoclingReader()
docs = reader.load_data(file_path="documento.pdf")

parser = DoclingNodeParser()
nodes = parser.get_nodes_from_documents(docs)
```

### Integração com LangChain [[9]](https://github.com/docling-project/docling/blob/075fa69491826a0b295a3022f64c568822a3f68d/docs/usage/processing_audio_media.md)

```bash
pip install langchain-docling
```

```python
from langchain_docling import DoclingLoader

loader = DoclingLoader("documentos/")
docs = loader.load()
```

***

## 6. Integração com Hermes Agent

O [Hermes Agent](https://hermes-agent.nousresearch.com/docs/) suporta integração com ferramentas externas via MCP servers e scripts Python [[10]](https://hermes-agent.nousresearch.com/docs/). Existem duas abordagens principais para integrar o Docling:

### Abordagem 1: Script Python como Skill do Hermes

Crie um script que o Hermes Agent pode invocar:

```python
#!/usr/bin/env python3
"""docling_convert.py - Skill para o Hermes Agent converter documentos."""

import sys
import json
from docling.document_converter import DocumentConverter
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.document_converter import PdfFormatOption

def convert_document(file_path: str, output_format: str = "markdown") -> dict:
    """Converte um documento usando Docling e retorna o resultado."""
    
    pipeline_options = PdfPipelineOptions()
    pipeline_options.do_ocr = True
    pipeline_options.do_table_structure = True
    
    converter = DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
        }
    )
    
    result = converter.convert(file_path)
    
    exporters = {
        "markdown": result.document.export_to_markdown,
        "text": result.document.export_to_text,
        "html": result.document.export_to_html,
    }
    
    content = exporters.get(output_format, exporters["markdown"])()
    
    return {
        "status": "success",
        "format": output_format,
        "content": content,
    }

if __name__ == "__main__":
    file_path = sys.argv[1]
    fmt = sys.argv[2] if len(sys.argv) > 2 else "markdown"
    resultado = convert_document(file_path, fmt)
    print(json.dumps(resultado, ensure_ascii=False, indent=2))
```

Uso pelo Hermes: `python docling_convert.py documento.pdf markdown`

### Abordagem 2: docling-serve como API HTTP

Esta é a abordagem mais robusta — o Hermes Agent faz chamadas HTTP para o Docling rodando como serviço [[11]](https://app.dosu.dev/097760a8-135e-4789-8234-90c8837d7f1c/documents/1aff9a3b-5df0-4e3f-bb74-2485b6101bfc):

```bash
# Inicie o servidor no WSL2
pip install "docling-serve[ui]"
docling-serve run --host 0.0.0.0 --port 5001
```

O Hermes Agent pode então chamar a API:

```python
import requests

# Converter arquivo via upload
with open("documento.pdf", "rb") as f:
    response = requests.post(
        "http://localhost:5001/v1/convert/file",
        files={"files": ("documento.pdf", f, "application/pdf")},
        data={"to_formats": "md"},
    )

resultado = response.json()
print(resultado)
```

```python
# Converter via URL
response = requests.post(
    "http://localhost:5001/v1/convert/source",
    json={
        "options": {"to_formats": ["md"]},
        "sources": [{"kind": "http", "url": "https://arxiv.org/pdf/2408.09869"}],
    },
)
```

### Workflow Exemplo: Hermes + Docling

1. O Hermes Agent recebe um documento (via Telegram, Discord, etc.)
2. Salva o arquivo localmente ou obtém a URL
3. Chama `docling-serve` via HTTP ou executa o script Python
4. Recebe o Markdown/texto convertido
5. Processa o conteúdo (resumo, Q&A, análise, etc.)

***

## 7. Uso via CLI [[1]](https://app.dosu.dev/097760a8-135e-4789-8234-90c8837d7f1c/documents/30f358d9-e4a4-4dd8-a4c5-5cb25bd4a380)

```bash
# Conversão simples
docling --progress documento.pdf

# Download de modelos específicos
docling models download --model tableformer

# Extração de gráficos
docling convert --enrich-chart-extraction documento.pdf
```

***

## 8. Resolução de Problemas no WSL2

### Docling trava/congela no WSL2

Problema reportado: Docling pode travar após inicialização [[12]](https://github.com/docling-project/docling/discussions/2532). **Solução** — use o backend `pypdfium2`:

```python
from docling.backend.pypdfium2_backend import PyPdfiumDocumentBackend

converter = DocumentConverter(
    format_options={
        InputFormat.PDF: PdfFormatOption(backend=PyPdfiumDocumentBackend)
    }
)
```

### Erros de PyTorch/CUDA no WSL2

Erros do tipo "Could not load custom kernel" [[13]](https://github.com/docling-project/docling/issues/799#issuecomment-2685548355). **Soluções**:

- Fixar versão do PyTorch: `pip install torch==2.5.1`
- Verificar que `CUDA_HOME` está configurado corretamente
- Preferir EasyOCR ao invés de Tesseract no Windows 11

### Vazamento de memória em conversões sucessivas

Memória cresce a cada conversão [[14]](https://github.com/docling-project/docling/issues/2788#issuecomment-3685938572). **Workaround**:

```python
import gc
import torch

# Na configuração do pipeline
pipeline_options.generate_parsed_pages = False

# Após cada conversão
gc.collect()
if torch.cuda.is_available():
    torch.cuda.empty_cache()
```

### Performance do sistema de arquivos

**Importante**: Sempre trabalhe no filesystem nativo do Linux (`~/documentos/`) e **não** em `/mnt/c/`. O acesso ao filesystem do Windows via WSL2 é significativamente mais lento.

### Docker no WSL2 [[15]](https://github.com/docling-project/docling-serve/issues/261#issuecomment-3040883825)

Use `localhost` ao acessar containers do host:

```bash
docker run -p 5001:5001 quay.io/docling-project/docling-serve
# Acesse em: http://localhost:5001
```

### Limitações de memória

Configure a memória do WSL2 editando `%USERPROFILE%\.wslconfig`:

```ini
[wsl2]
memory=8GB
swap=4GB
```

***

## 9. Referências e Links Úteis

| Recurso | URL |
|---------|-----|
| Docling GitHub | https://github.com/docling-project/docling |
| docling-core | https://github.com/docling-project/docling-core |
| docling-serve | https://github.com/docling-project/docling-serve |
| Hermes Agent Docs | https://hermes-agent.nousresearch.com/docs/ |
| LangChain Docling | https://pypi.org/project/langchain-docling/ |
| LlamaIndex Docling | https://pypi.org/project/llama-index-readers-docling/ |

***

**Nota**: O suporte oficial a Windows/WSL2 é limitado — a equipe do Docling recomenda Linux nativo para uso em produção [[16]](https://github.com/docling-project/docling/issues/1120). Os workarounds acima são mantidos pela comunidade.