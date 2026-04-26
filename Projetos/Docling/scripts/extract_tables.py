#!/usr/bin/env python3
"""
extract_tables.py — Extract all tables from a document using Docling for Hermes Agent.

Outputs each table as Markdown (default) or CSV.

Usage:
    python scripts/extract_tables.py --source <file_or_url> [--format markdown|csv] [--output <dir>]

Examples:
    python scripts/extract_tables.py --source report.pdf
    python scripts/extract_tables.py --source financial.xlsx --format csv --output ./tables/
"""

import argparse
import sys
from pathlib import Path


def extract_tables(source: str, fmt: str, output_dir: str | None) -> None:
    try:
        from docling.document_converter import DocumentConverter
    except ImportError:
        print("ERROR: Docling is not installed. Run: pip install docling", file=sys.stderr)
        sys.exit(1)

    print(f"Extracting tables from: {source}")
    converter = DocumentConverter()

    try:
        result = converter.convert(source)
    except Exception as e:
        print(f"ERROR during conversion: {e}", file=sys.stderr)
        sys.exit(1)

    tables = list(result.document.tables)

    if not tables:
        print("No tables found in document.")
        return

    print(f"Found {len(tables)} table(s).")

    out_path = Path(output_dir) if output_dir else None
    if out_path:
        out_path.mkdir(parents=True, exist_ok=True)

    source_stem = Path(source).stem if not source.startswith("http") else "document"

    for i, table in enumerate(tables, start=1):
        if fmt == "csv":
            try:
                df = table.export_to_dataframe()
                text = df.to_csv(index=False)
                ext = ".csv"
            except ImportError:
                print("WARNING: pandas not installed. Falling back to Markdown.", file=sys.stderr)
                text = table.export_to_markdown()
                ext = ".md"
        else:
            text = table.export_to_markdown()
            ext = ".md"

        if out_path:
            out_file = out_path / f"{source_stem}_table_{i:02d}{ext}"
            out_file.write_text(text, encoding="utf-8")
            print(f"  Table {i} → {out_file.name}")
        else:
            print(f"\n--- Table {i} ---")
            print(text)


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract tables from documents using Docling.")
    parser.add_argument("--source", required=True, help="Path or URL of the document.")
    parser.add_argument(
        "--format",
        choices=["markdown", "csv"],
        default="markdown",
        help="Output format for tables (default: markdown).",
    )
    parser.add_argument("--output", default=None, help="Output directory. Prints to stdout if omitted.")
    args = parser.parse_args()
    extract_tables(args.source, args.format, args.output)


if __name__ == "__main__":
    main()
