---
name: docling
description: Convert and extract structured data from documents (PDF, DOCX, PPTX, XLSX, HTML, images, audio, and more) using Docling. Supports OCR, table extraction, formula detection, reading order, and export to Markdown, JSON, or HTML for AI/RAG pipelines.
version: 1.0.0
author: community
license: MIT
platforms: [macos, linux]
metadata:
 hermes:
 tags: [Documents, OCR, PDF, Conversion, RAG, Extraction, AI]
 related_skills: [arxiv, ocr-and-documents]
 requires_tools: [terminal]
linked_files:
 scripts/convert_document.py: Document conversion helper
 scripts/batch_convert.py: Batch conversion for multiple files
 scripts/extract_tables.py: Table extraction utility
 scripts/chunk_for_rag.py: Document chunking for RAG
 scripts/setup.sh: Automated installation script
 scripts/verify.sh: Installation verification
 scripts/docling-wrapper.sh: Wrapper for venv activation
 templates/config.yaml: Configuration template
---

# Docling — Document Intelligence

Docling converts messy documents into structured, AI-ready data. It handles PDF (including scanned), DOCX, PPTX, XLSX, HTML, Markdown, images (PNG, JPEG, TIFF, WEBP), audio (MP3, WAV), LaTeX, and more — detecting tables, formulas, reading order, and running OCR automatically.

## When to Use

Load this skill when the user asks to:
- Convert a document (PDF, Word, PowerPoint, Excel, image, etc.) to Markdown, JSON, or HTML
- Extract text, tables, formulas, or images from a file or URL
- Process documents for RAG, LLM ingestion, or AI pipelines
- Run OCR on a scanned PDF or image
- Chunk a document into pieces ready for embedding
- Analyze the structure or layout of a document

## Quick Reference

| Task | Command |
|---|---|
| Install Docling | `pip install docling` |
| Convert a file to Markdown | `docling path/to/file.pdf` |
| Convert from URL | `docling https://arxiv.org/pdf/2206.01062` |
| Export to JSON | `docling file.pdf --to json` |
| Export to HTML | `docling file.pdf --to html` |
| Force full-page OCR | `docling file.pdf --ocr-mode force_all` |
| Convert multiple files | `docling *.pdf --output ./out/` |
| Run via Python | See Python procedure below |

## Procedure

### 1. Install Docling (First Time Setup)

Run the automated setup script:

```bash
cd ~/.hermes/skills/docling
bash scripts/setup.sh
```

This will:
- Check Python version (requires 3.9+)
- Install system dependencies (tesseract-ocr, poppler-utils)
- Create a dedicated virtual environment at `~/.hermes/skills/docling/.venv`
- Install Docling with all required dependencies

Verify the installation:

```bash
bash scripts/verify.sh
```

### 2. Simple CLI Conversion

For a single file or URL, use the CLI directly via `terminal`:

```bash
# Activate the virtual environment first
source ~/.hermes/skills/docling/.venv/bin/activate

# Convert a local PDF to Markdown (default output)
docling /path/to/document.pdf

# Convert a file and save to a specific output directory
docling /path/to/document.pdf --output ./output/

# Convert from a URL
docling https://example.com/report.pdf

# Export as JSON (structured, lossless)
docling /path/to/document.pdf --to json --output ./output/

# Export as HTML
docling /path/to/document.pdf --to html --output ./output/

# Convert multiple files at once
docling *.pdf --output ./output/
```

Or use the wrapper script (auto-activates venv):

```bash
bash scripts/docling-wrapper.sh /path/to/document.pdf
```

The default output format is **Markdown**, which is the best choice for LLM ingestion.

### 3. Python API — Basic Conversion

For programmatic use (e.g., to pass content directly to the agent), use the Python API:

```python
from docling.document_converter import DocumentConverter

source = "/path/to/document.pdf" # or a URL
converter = DocumentConverter()
result = converter.convert(source)

# Export to Markdown
print(result.document.export_to_markdown())
```

Run with the helper script:

```bash
# Ensure venv is activated
source ~/.hermes/skills/docling/.venv/bin/activate

python ~/.hermes/skills/docling/scripts/convert_document.py --source /path/to/file.pdf --format markdown
```

### 4. Python API — Table Extraction

To extract all tables from a document:

```bash
source ~/.hermes/skills/docling/.venv/bin/activate
python ~/.hermes/skills/docling/scripts/extract_tables.py --source /path/to/document.pdf --format markdown
```

Or programmatically:

```python
from docling.document_converter import DocumentConverter

converter = DocumentConverter()
result = converter.convert("/path/to/document.pdf")

for table in result.document.tables:
    print(table.export_to_dataframe()) # requires pandas
    # or
    print(table.export_to_markdown())
```

### 5. Python API — Chunking for RAG

To split a document into chunks ready for vector embedding:

```bash
source ~/.hermes/skills/docling/.venv/bin/activate
python ~/.hermes/skills/docling/scripts/chunk_for_rag.py --source /path/to/document.pdf --format json --output chunks.json
```

Or programmatically:

```python
from docling.document_converter import DocumentConverter
from docling.chunking import HybridChunker

converter = DocumentConverter()
result = converter.convert("/path/to/document.pdf")

chunker = HybridChunker()
chunks = list(chunker.chunk(result.document))

for chunk in chunks:
    print(chunk.text)
```

### 6. Batch Conversion

To convert a directory of files:

```bash
source ~/.hermes/skills/docling/.venv/bin/activate
python ~/.hermes/skills/docling/scripts/batch_convert.py --input-dir ./documents/ --output-dir ./output/ --format markdown
```

Or via CLI:

```bash
docling ./documents/ --output ./output/ --to markdown
```

### 7. OCR Options

Docling uses OCR automatically on scanned pages. To control behavior:

```bash
# Force OCR on all pages (even text-based PDFs)
docling file.pdf --ocr-mode force_all

# Disable OCR (faster, text-only PDFs)
docling file.pdf --ocr-mode disabled
```

### 8. Audio Transcription (ASR)

Docling supports audio files using ASR (Automatic Speech Recognition):

```bash
source ~/.hermes/skills/docling/.venv/bin/activate
pip install docling[audio]
docling recording.mp3 --to markdown
```

## Output Formats

| Format | Flag | Best for |
|---|---|---|
| Markdown | `--to md` (default) | LLM ingestion, RAG, reading |
| JSON | `--to json` | Structured extraction, programmatic access |
| HTML | `--to html` | Web rendering, visual inspection |
| DocTags | `--to doctags` | Structured AI training data |

## Pitfalls

- **Slow on first run:** Docling downloads layout models (~500MB) on first use. This is expected — subsequent runs are fast.
- **Scanned PDFs without OCR flag:** If text is missing from a scanned PDF, ensure OCR is enabled (it is by default, but verify with `--ocr-mode auto`).
- **Large files:** Very large PDFs (100+ pages) may be slow without GPU. Use `--pages 1-20` to limit page range during testing.
- **PPTX/XLSX:** Slide and spreadsheet conversion is supported but may flatten complex layouts. Inspect the Markdown output before using in RAG.
- **Audio:** Audio support requires `pip install docling[audio]`. Do not use audio conversion without this extra.
- **Python version:** Docling requires Python 3.9 or higher. Verify with `python --version` before installing.

## Verification

After conversion, confirm success by checking:

```bash
# List output files
ls -lh ./output/

# Preview the first 50 lines of a converted Markdown
head -50 ./output/document.md

# Validate JSON output is well-formed
python -c "import json; json.load(open('./output/document.json')); print('JSON OK')"
```

A successful Markdown output will contain readable text with headings, paragraphs, and — for PDFs with tables — Markdown table syntax.

## Resources

- Documentation: https://docling-project.github.io/docling/
- GitHub: https://github.com/docling-project/docling
- Supported formats: https://docling-project.github.io/docling/usage/supported_formats/
- MCP server (for agentic use): https://docling-project.github.io/docling/usage/mcp/
- Chunking guide: https://docling-project.github.io/docling/concepts/chunking/
