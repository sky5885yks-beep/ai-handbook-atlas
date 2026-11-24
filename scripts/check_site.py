#!/usr/bin/env python3
"""零依赖静态站点检查：标题、描述、H1、重复 id、空链接。"""
from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"


class Collector(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: list[str] = []
        self.hrefs: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if values.get("id"):
            self.ids.append(values["id"] or "")
        if tag == "a" and "href" in values:
            self.hrefs.append(values.get("href") or "")


def main() -> int:
    if not INDEX.exists():
        print("缺少 index.html")
        return 1

    html = INDEX.read_text(encoding="utf-8")
    errors: list[str] = []

    for label, pattern in (
        ("<title>", r"<title>\s*[^<\s].*?</title>"),
        ("meta description", r'<meta\s+name="description"\s+content="[^"]+"'),
        ("<h1>", r"<h1[^>]*>\s*\S"),
    ):
        if not re.search(pattern, html, re.I | re.S):
            errors.append(f"缺少 {label}")

    collector = Collector()
    collector.feed(html)

    duplicates = sorted({x for x in collector.ids if collector.ids.count(x) > 1})
    if duplicates:
        errors.append("重复 id: " + ", ".join(duplicates))

    empty = [href for href in collector.hrefs if not href.strip()]
    if empty:
        errors.append(f"存在 {len(empty)} 个空 href")

    if re.search(r'<script[^>]+src="https?://', html, re.I):
        errors.append("存在外链 JS，单文件部署会失效")
    if re.search(r'<link[^>]+rel="stylesheet"[^>]+href="https?://', html, re.I):
        errors.append("存在外链 CSS，单文件部署会失效")

    if errors:
        print("\n".join(errors))
        return 1

    print(
        f"OK: {len(html)} bytes, {len(collector.ids)} ids, "
        f"{len(collector.hrefs)} links"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
