#!/usr/bin/env python3
"""
chunk_for_rag.py — Chunk a document into AI-ready pieces using Docling for Hermes Agent.

Splits the document using HybridChunker and prints or saves chunks as JSON (with metadata) or plain text.

Usage:
    python scripts/chunk_for_rag.py --source <file_or_url> [--format text|json] [--output <file>]

Examples:
    python scripts/chunk_for_rag.py --source paper.pdf
    python scripts/chunk_for_rag.py --source report.pdf --format json --output chunks.json
"""

import argparse
import json
import sys
from pathlib import Path


def chunk_document(source: str, fmt: str, output_file: str | None) -> None:
    try:
        from docling.document_converter import DocumentConverter
        from docling.chunking import HybridChunker
    except ImportError:
        print("ERROR: Docling is not installed. Run: pip install docling", file=sys.stderr)
        sys.exit(1)

    print(f"Converting and chunking: {source}")
    converter = DocumentConverter()

    try:
        result = converter.convert(source)
    except Exception as e:
        print(f"ERROR during conversion: {e}", file=sys.stderr)
        sys.exit(1)

    chunker = HybridChunker()
    chunks = list(chunker.chunk(result.document))

    print(f"Generated {len(chunks)} chunk(s).")

    if fmt == "json":
        data = []
        for i, chunk in enumerate(chunks):
            entry = {
                "index": i,
                "text": chunk.text,
                "meta": chunk.meta.model_dump() if hasattr(chunk, "meta") and chunk.meta else {},
            }
            data.append(entry)
        output_text = json.dumps(data, indent=2, ensure_ascii=False)
    else:
        lines = []
        for i, chunk in enumerate(chunks):
            lines.append(f"--- Chunk {i + 1} ---")
            lines.append(chunk.text)
            lines.append("")
        output_text = "\n".join(lines)

    if output_file:
        Path(output_file).write_text(output_text, encoding="utf-8")
        print(f"Saved to: {output_file}")
    else:
        print("\n" + output_text)


def main() -> None:
    parser = argparse.ArgumentParser(description="Chunk documents for RAG using Docling.")
    parser.add_argument("--source", required=True, help="Path or URL of the document.")
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text). Use json to include metadata.",
    )
    parser.add_argument("--output", default=None, help="Output file path. Prints to stdout if omitted.")
    args = parser.parse_args()
    chunk_document(args.source, args.format, args.output)


if __name__ == "__main__":
    main()
