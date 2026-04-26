#!/usr/bin/env python3
"""
batch_convert.py — Batch document conversion helper for Hermes Agent using Docling.

Converts all supported documents in an input directory and saves results to an output directory.

Usage:
    python scripts/batch_convert.py --input-dir ./documents/ --output-dir ./output/ [--format markdown|json|html]

Examples:
    python scripts/batch_convert.py --input-dir ./pdfs/ --output-dir ./converted/
    python scripts/batch_convert.py --input-dir ./reports/ --output-dir ./out/ --format json
"""

import argparse
import sys
from pathlib import Path

SUPPORTED_EXTENSIONS = {
    ".pdf", ".docx", ".pptx", ".xlsx",
    ".html", ".htm", ".md",
    ".png", ".jpg", ".jpeg", ".tiff", ".tif", ".bmp", ".webp",
    ".txt", ".text",
}


def batch_convert(input_dir: str, output_dir: str, fmt: str) -> None:
    try:
        from docling.document_converter import DocumentConverter
    except ImportError:
        print("ERROR: Docling is not installed. Run: pip install docling", file=sys.stderr)
        sys.exit(1)

    in_path = Path(input_dir)
    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    files = [f for f in in_path.iterdir() if f.suffix.lower() in SUPPORTED_EXTENSIONS]

    if not files:
        print(f"No supported files found in: {in_path}")
        return

    ext_map = {"markdown": ".md", "json": ".json", "html": ".html"}
    ext = ext_map[fmt]

    converter = DocumentConverter()
    success, failed = 0, 0

    for file in sorted(files):
        print(f"  Converting: {file.name} ... ", end="", flush=True)
        try:
            result = converter.convert(str(file))
            doc = result.document

            if fmt == "json":
                import json
                text = json.dumps(doc.export_to_dict(), indent=2, ensure_ascii=False)
            elif fmt == "html":
                text = doc.export_to_html()
            else:
                text = doc.export_to_markdown()

            out_file = out_path / f"{file.stem}{ext}"
            out_file.write_text(text, encoding="utf-8")
            print(f"OK → {out_file.name}")
            success += 1
        except Exception as e:
            print(f"FAILED ({e})")
            failed += 1

    print(f"\nDone. {success} converted, {failed} failed.")
    print(f"Output directory: {out_path.resolve()}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Batch convert documents with Docling.")
    parser.add_argument("--input-dir", required=True, help="Directory containing documents to convert.")
    parser.add_argument("--output-dir", required=True, help="Directory to save converted files.")
    parser.add_argument(
        "--format",
        choices=["markdown", "json", "html"],
        default="markdown",
        help="Output format (default: markdown).",
    )
    args = parser.parse_args()
    batch_convert(args.input_dir, args.output_dir, args.format)


if __name__ == "__main__":
    main()
