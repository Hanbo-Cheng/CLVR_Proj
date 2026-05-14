#!/usr/bin/env python3
"""Export single-page paper figures from PDF to SVG for static hosting.

Requires: pip install pymupdf

Usage (from repo root or this directory):
  python3 CLVR/web_page/scripts/pdf_figures_to_svg.py
"""
from __future__ import annotations

import sys
from pathlib import Path

try:
    import fitz  # PyMuPDF
except ImportError as e:
    print("Install PyMuPDF:  python3 -m pip install --user pymupdf", file=sys.stderr)
    raise SystemExit(1) from e

WEB_PAGE = Path(__file__).resolve().parents[1]
FIGURES = WEB_PAGE / "assets" / "figures"
OUT = FIGURES / "svg"

PDF_NAMES = [
    "overall_pipeline_draft4.pdf",
    "datapipeline_2_simple.pdf",
    "trace_showcase.pdf",
    "CoT_case_2.pdf",
    "compare_w_baseline.pdf",
]


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for name in PDF_NAMES:
        src = FIGURES / name
        if not src.is_file():
            print("skip (missing):", src)
            continue
        dst = OUT / (src.stem + ".svg")
        doc = fitz.open(src)
        if doc.page_count != 1:
            print("warning:", name, "has", doc.page_count, "pages; exporting page 0 only")
        svg = doc[0].get_svg_image()
        doc.close()
        dst.write_text(svg, encoding="utf-8")
        print("wrote", dst, "(%d bytes)" % dst.stat().st_size)


if __name__ == "__main__":
    main()
