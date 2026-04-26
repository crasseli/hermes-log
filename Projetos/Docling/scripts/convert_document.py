#!/usr/bin/env python3
"""
convert_document.py — Docling document conversion helper for Hermes Agent.

Usage:
    python scripts/convert_document.py --source <file_or_url> [--format markdown|json|html] [--output <dir>]

Examples:
    python scripts/convert_document.py --source report.pdf
    python scripts/convert_document.py --source https://arxiv.org/pdf/2408.09869 --format json
    python scripts/convert_document.py --source scan.pdf --format markdown --output ./out/
"""

import argparse
import sys
from pathlib import Path


def convert(source: str, fmt: str, output_dir: str | None) -> None:
    try:
        from docling.document_converter import DocumentConverter
    except ImportError:
        print("ERROR: Docling is not installed. Run: pip install docling", file=sys.stderr)
        sys.exit(1)

    print(f"Converting: {source}")
    converter = DocumentConverter()

    try:
        result = converter.convert(source)
    except Exception as e:
        print(f"ERROR during conversion: {e}", file=sys.stderr)
        sys.exit(1)

    doc = result.document

    # Choose export method
    if fmt == "json":
        content = doc.export_to_dict()
        import json
        text = json.dumps(content, indent=2, ensure_ascii=False)
        ext = ".json"
    elif fmt == "html":
        text = doc.export_to_html()
        ext = ".html"
    else:
        text = doc.export_to_markdown()
        ext = ".md"

    # Determine output path
    if output_dir:
        out_path = Path(output_dir)
        out_path.mkdir(parents=True, exist_ok=True)
        # Derive filename from source
        source_stem = Path(source).stem if not source.startswith("http") else "document"
        out_file = out_path / f"{source_stem}{ext}"
        out_file.write_text(text, encoding="utf-8")
        print(f"Saved to: {out_file}")
    else:
        # Print to stdout
        print("\n" + "=" * 60)
        print(text)


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert documents with Docling.")
    parser.add_argument("--source", required=True, help="Path or URL of the document to convert.")
    parser.add_argument(
        "--format",
        choices=["markdown", "json", "html"],
        default="markdown",
        help="Output format (default: markdown).",
    )
    parser.add_argument("--output", default=None, help="Output directory. Prints to stdout if omitted.")
    args = parser.parse_args()

    convert(args.source, args.format, args.output)


if __name__ == "__main__":
    main()
