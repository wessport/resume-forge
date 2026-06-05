#!/usr/bin/env python3
"""Render a role-specific cover letter Markdown file to a styled PDF.

The layout intentionally matches the existing Asurion Staff Data Engineer cover
letter: A4 page, inset green accent line, compact header, justified body copy,
and muted email/website links in the signature block.
"""

from __future__ import annotations

import argparse
import html
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


DEFAULT_CHROME_PATHS = (
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
)

SIGNATURE_LINES = (
    "Best regards,",
    "Wesley Porter",
    "wesporter92@gmail.com",
    "www.geoalchemist.com",
)

CSS = """
@page { size: A4; margin: 0; }
* { box-sizing: border-box; }
body {
  margin: 0;
  padding: 0;
  font-family: Arial, Helvetica, sans-serif;
  color: #333333;
  background: white;
  -webkit-print-color-adjust: exact;
  print-color-adjust: exact;
}
.page {
  width: 210mm;
  min-height: 297mm;
  padding: 13.5mm 22mm 13mm 22mm;
}
.accent {
  width: 100%;
  height: 4px;
  background: #70c041;
  margin: 0 0 9.3mm 0;
}
h1 {
  margin: 0 0 2.2mm 0;
  font-size: 18px;
  line-height: 1.15;
  font-weight: 700;
  color: #1c1d36;
}
.subtitle {
  margin: 0 0 9.8mm 0;
  font-size: 12px;
  line-height: 1.2;
  color: #666666;
  font-weight: 400;
}
p {
  margin: 0 0 5.0mm 0;
  font-size: 10.6pt;
  line-height: 1.48;
  text-align: justify;
}
strong {
  font-weight: 700;
  color: #1c1d36;
}
.signature {
  margin-top: 7mm;
  line-height: 1.34;
  text-align: left;
  color: #333333;
}
a {
  color: inherit;
  text-decoration: none;
}
.muted {
  color: #666666;
}
""".strip()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Render a cover letter Markdown file to a styled PDF."
    )
    parser.add_argument("markdown", type=Path, help="Input cover letter Markdown file")
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        help="Output PDF path. Defaults to the input path with .pdf suffix.",
    )
    parser.add_argument(
        "--subtitle",
        help="Role/company subtitle. Defaults to the first heading after 'Cover Letter - '.",
    )
    parser.add_argument(
        "--chrome",
        type=Path,
        help="Path to a Chrome/Chromium executable. Auto-detected by default.",
    )
    parser.add_argument(
        "--keep-html",
        action="store_true",
        help="Write the generated HTML next to the output PDF for debugging.",
    )
    return parser.parse_args()


def detect_chrome(explicit_path: Path | None) -> Path:
    if explicit_path:
        if explicit_path.exists():
            return explicit_path
        raise FileNotFoundError(f"Chrome executable does not exist: {explicit_path}")

    for path in DEFAULT_CHROME_PATHS:
        chrome = Path(path)
        if chrome.exists():
            return chrome

    for name in ("google-chrome", "chrome", "chromium", "chromium-browser"):
        resolved = shutil.which(name)
        if resolved:
            return Path(resolved)

    raise FileNotFoundError(
        "Could not find Chrome/Chromium. Pass --chrome with the executable path."
    )


def split_blocks(markdown: str) -> tuple[str, list[str]]:
    lines = markdown.splitlines()
    title = "Cover Letter"
    body_lines = lines
    if lines and lines[0].startswith("# "):
        title = lines[0].removeprefix("# ").strip()
        body_lines = lines[1:]

    blocks: list[str] = []
    current: list[str] = []
    for line in body_lines:
        stripped = line.strip()
        if not stripped:
            if current:
                blocks.append(" ".join(current))
                current = []
            continue
        current.append(stripped)
    if current:
        blocks.append(" ".join(current))

    return title, blocks


def default_subtitle(title: str) -> str:
    prefix = "Cover Letter - "
    if title.startswith(prefix):
        return title.removeprefix(prefix).strip()
    return title


def inline_markdown(text: str) -> str:
    escaped = html.escape(text)
    return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", escaped)


def render_block(block: str) -> str:
    normalized_signature = " ".join(SIGNATURE_LINES)
    if block == normalized_signature:
        return (
            '<p class="signature">'
            "Best regards,<br>"
            "Wesley Porter<br>"
            '<a class="muted" href="mailto:wesporter92@gmail.com">'
            "wesporter92@gmail.com</a><br>"
            '<a class="muted" href="https://www.geoalchemist.com">'
            "www.geoalchemist.com</a>"
            "</p>"
        )
    return f"<p>{inline_markdown(block)}</p>"


def build_html(markdown: str, subtitle: str | None) -> str:
    title, blocks = split_blocks(markdown)
    subtitle_text = subtitle if subtitle is not None else default_subtitle(title)
    body = "\n  ".join(render_block(block) for block in blocks)

    return f"""<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>{html.escape(title)}</title>
<style>
{CSS}
</style>
</head>
<body>
<div class="page">
  <div class="accent"></div>
  <h1>Cover Letter</h1>
  <div class="subtitle">{html.escape(subtitle_text)}</div>
  {body}
</div>
</body>
</html>
"""


def render_pdf(chrome: Path, html_path: Path, pdf_path: Path) -> None:
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    command = [
        str(chrome),
        "--headless",
        "--disable-gpu",
        "--no-sandbox",
        f"--print-to-pdf={pdf_path}",
        html_path.resolve().as_uri(),
    ]
    subprocess.run(command, check=True)


def main() -> int:
    args = parse_args()
    markdown_path = args.markdown.expanduser().resolve()
    if not markdown_path.exists():
        raise FileNotFoundError(f"Input Markdown file does not exist: {markdown_path}")

    output_path = (args.output or markdown_path.with_suffix(".pdf")).expanduser().resolve()
    chrome = detect_chrome(args.chrome)
    html_text = build_html(markdown_path.read_text(), args.subtitle)

    if args.keep_html:
        html_path = output_path.with_suffix(".html")
        html_path.write_text(html_text)
        render_pdf(chrome, html_path, output_path)
    else:
        with tempfile.TemporaryDirectory(prefix="cover-letter-") as tmpdir:
            html_path = Path(tmpdir) / "cover_letter.html"
            html_path.write_text(html_text)
            render_pdf(chrome, html_path, output_path)

    print(output_path)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(1)
