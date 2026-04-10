"""
Convert extracted DOCX (document.xml + word/media) to HTML and Markdown with images and captions.
Run `main()` to write paired `.html` / `.md` and an `assets/` folder under the configured output directory.
"""
from __future__ import annotations

import html
import os
import re
import shutil
import sys
import xml.etree.ElementTree as ET

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
REL = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
REL_PKG = "{http://schemas.openxmlformats.org/package/2006/relationships}"
EMBED = f"{REL}embed"
BLIP_FILL = "{http://schemas.openxmlformats.org/drawingml/2006/main}blip"

# Default document title when core.xml and heuristics do not yield a sensible heading.
DEFAULT_DOC_TITLE = "移动住房时代，凤凰来仪"
_SKIP_HEADINGS = frozenset({"摘要", "前言", "序言", "内容简介", "内容提要"})


def load_relationships(rels_path: str) -> dict[str, str]:
    tree = ET.parse(rels_path)
    root = tree.getroot()
    out: dict[str, str] = {}
    for rel in root:
        rid = rel.get("Id")
        target = rel.get("Target")
        if not rid or not target:
            continue
        # normalize: media/image1.jpeg
        t = target.replace("\\", "/")
        if t.startswith("../"):
            t = t[3:]
        out[rid] = t
    return out


def _sanitize_image_description(s: str) -> str:
    """Turn Word file paths into filenames; drop useless hash-only tokens."""
    if not s:
        return ""
    s = s.strip()
    if re.match(r"^[A-Za-z]:[/\\]", s):
        s = os.path.basename(s.replace("\\", "/"))
    elif ":\\" in s or (len(s) > 2 and s[1] == ":"):
        tail = s.replace("\\", "/").split("/")[-1]
        s = tail or s
    if re.fullmatch(r"[a-fA-F0-9]{32}", s):
        return ""
    return s[:500]


def extract_caption_from_drawing_container(container: ET.Element) -> str:
    """
    Word stores optional labels in wp:docPr (title, descr) and pic:cNvPr (name, descr).
    Insert Caption (题注) as separate paragraphs is handled by normal text extraction.
    """
    doc_desc = ""
    doc_title = ""
    cnv_desc = ""
    cnv_name = ""
    for node in container.iter():
        if node.tag.endswith("}docPr"):
            doc_desc = (node.get("descr") or "").strip() or doc_desc
            doc_title = (node.get("title") or "").strip() or doc_title
        elif node.tag.endswith("}cNvPr"):
            cnv_desc = (node.get("descr") or "").strip() or cnv_desc
            cnv_name = (node.get("name") or "").strip() or cnv_name

    for candidate in (doc_desc, doc_title, cnv_desc):
        out = _sanitize_image_description(candidate)
        if out:
            return out
    if cnv_name and not re.match(r"^(文本框|形状|图片)\s*\d+$", cnv_name):
        out = _sanitize_image_description(cnv_name)
        if out:
            return out
    return ""


def find_blip_embeds(element: ET.Element) -> list[str]:
    """Collect r:embed / r:id relationship ids from blip / VML imagedata under this subtree."""
    ids: list[str] = []
    r_id = f"{REL}id"
    for el in element.iter():
        if el.tag == BLIP_FILL or el.tag.endswith("}blip"):
            eid = el.get(EMBED)
            if eid:
                ids.append(eid)
            else:
                for k, v in el.attrib.items():
                    if k.endswith("embed") or k == "embed":
                        ids.append(v)
                        break
        # VML: v:imagedata r:id="rId5"
        elif el.tag.endswith("}imagedata") or "imagedata" in el.tag:
            iid = el.get(r_id) or el.get("r:id")
            if iid:
                ids.append(iid)
    return ids


def paragraph_blocks(p: ET.Element) -> list[tuple[str, str] | tuple[str, str, str]]:
    """
    Document-order blocks: ('text', str) or ('img', rId, caption_from_ooxml).
    Walks direct w:r children only to preserve text/image interleaving.
    """
    blocks: list[tuple[str, str] | tuple[str, str, str]] = []

    for r in p:
        if r.tag != f"{W}r":
            continue
        for el in r:
            if el.tag == f"{W}t":
                blocks.append(("text", el.text or ""))
            elif el.tag == f"{W}br":
                blocks.append(("text", "\n"))
            elif el.tag == f"{W}tab":
                blocks.append(("text", "\t"))
            elif "AlternateContent" in el.tag:
                cap = extract_caption_from_drawing_container(el)
                for rid in find_blip_embeds(el):
                    blocks.append(("img", rid, cap))
            elif el.tag.endswith("}drawing") or "drawing" in el.tag:
                cap = extract_caption_from_drawing_container(el)
                for rid in find_blip_embeds(el):
                    blocks.append(("img", rid, cap))
            elif el.tag.endswith("}pict") or el.tag.endswith("}object"):
                cap = extract_caption_from_drawing_container(el)
                for rid in find_blip_embeds(el):
                    blocks.append(("img", rid, cap))

    return blocks


def paragraph_plain_text(p: ET.Element) -> str:
    """All text in paragraph (for titles), ignoring structure."""
    parts: list[str] = []
    for r in p.findall(f".//{W}r"):
        for t in r.findall(f"{W}t"):
            parts.append(t.text or "")
        for br in r.findall(f"{W}br"):
            parts.append("\n")
    return "".join(parts)


def cell_paragraphs(tc: ET.Element) -> list[ET.Element]:
    return tc.findall(f".//{W}p")


def process_table(tbl: ET.Element, rels: dict[str, str], word_dir: str, media_dst: str) -> str:
    rows_html: list[str] = []
    for tr in tbl.findall(f"{W}tr"):
        cells: list[str] = []
        for tc in tr.findall(f"{W}tc"):
            inner: list[str] = []
            for p in cell_paragraphs(tc):
                inner.append(process_paragraph(p, rels, word_dir, media_dst, wrap_p=False))
            cells.append(f"<td>{''.join(inner)}</td>")
        rows_html.append("<tr>" + "".join(cells) + "</tr>")
    return '<table class="docx-table">' + "".join(rows_html) + "</table>"


def copy_media_file(rels: dict[str, str], word_dir: str, media_dst: str, rid: str) -> str | None:
    """Relationship Target paths are relative to the word/ folder (e.g. media/image1.jpeg)."""
    target = rels.get(rid)
    if not target:
        return None
    src = os.path.join(word_dir, target.replace("/", os.sep))
    if not os.path.isfile(src):
        return None
    dst = os.path.join(media_dst, os.path.basename(target))
    os.makedirs(os.path.dirname(dst) or ".", exist_ok=True)
    if not os.path.isfile(dst):
        shutil.copy2(src, dst)
    return os.path.basename(target)


def process_paragraph(
    p: ET.Element,
    rels: dict[str, str],
    word_dir: str,
    media_dst: str,
    wrap_p: bool = True,
) -> str:
    blocks = paragraph_blocks(p)
    chunks: list[str] = []
    for block in blocks:
        if block[0] == "text":
            val = block[1]
            if val:
                chunks.append(html.escape(val).replace("\n", "<br>\n"))
        elif block[0] == "img":
            val, cap = block[1], block[2]
            fname = copy_media_file(rels, word_dir, media_dst, val)
            if fname:
                alt = html.escape(cap) if cap else ""
                cap_html = (
                    f"<figcaption>{html.escape(cap)}</figcaption>"
                    if cap
                    else ""
                )
                chunks.append(
                    f'<figure class="inline-fig"><img src="assets/{html.escape(fname)}" alt="{alt}"/>{cap_html}</figure>'
                )
    inner = "".join(chunks)
    if not inner:
        return ""
    if wrap_p:
        style = ""
        ppr = p.find(f"{W}pPr")
        if ppr is not None:
            jc = ppr.find(f"{W}jc")
            if jc is not None:
                val = jc.get(f"{W}val")
                if val in ("center", "right", "both"):
                    style = f' style="text-align:{val if val != "both" else "justify"}"'
        return f"<p{style}>{inner}</p>\n"
    return inner


def body_content(
    body: ET.Element,
    rels: dict[str, str],
    word_dir: str,
    media_dst: str,
) -> str:
    parts: list[str] = []
    for child in body:
        tag = child.tag
        if tag == f"{W}p":
            h = process_paragraph(child, rels, word_dir, media_dst)
            if h:
                parts.append(h)
        elif tag == f"{W}tbl":
            parts.append(process_table(child, rels, word_dir, media_dst) + "\n")
        # skip sectPr etc.
    return "".join(parts)


def _escape_md_inline(text: str) -> str:
    if not text:
        return ""
    text = text.replace("\\", "\\\\")
    for a, b in (("`", "\\`"), ("*", "\\*"), ("_", "\\_"), ("[", "\\["), ("]", "\\]")):
        text = text.replace(a, b)
    return text


def _format_md_inline_text(text: str) -> str:
    """Preserve line breaks as GFM hard breaks (two trailing spaces)."""
    return _escape_md_inline(text).replace("\n", "  \n")


def process_paragraph_md(
    p: ET.Element,
    rels: dict[str, str],
    word_dir: str,
    media_dst: str,
    wrap_p: bool = True,
) -> str:
    blocks = paragraph_blocks(p)
    parts: list[str] = []
    for block in blocks:
        if block[0] == "text":
            val = block[1]
            if val:
                parts.append(_format_md_inline_text(val))
        elif block[0] == "img":
            val, cap = block[1], block[2]
            fname = copy_media_file(rels, word_dir, media_dst, val)
            if fname:
                alt = (cap or "image").replace("\n", " ").strip()
                alt = alt.replace("]", "")
                parts.append(f"![{alt}](assets/{fname})")
    if not parts:
        return ""

    merged_chunks: list[str] = []
    i = 0
    while i < len(parts):
        if parts[i].startswith("!["):
            merged_chunks.append("\n\n" + parts[i] + "\n\n")
            i += 1
        else:
            j = i
            buf: list[str] = []
            while j < len(parts) and not parts[j].startswith("!["):
                buf.append(parts[j])
                j += 1
            merged_chunks.append("".join(buf))
            i = j
    merged = "".join(merged_chunks).strip()
    while "\n\n\n" in merged:
        merged = merged.replace("\n\n\n", "\n\n")
    if not merged:
        return ""
    if wrap_p:
        return merged + "\n\n"
    return merged


def _md_escape_cell(s: str) -> str:
    s = " ".join(s.split())
    return s.replace("|", "\\|")


def process_table_md(tbl: ET.Element, rels: dict[str, str], word_dir: str, media_dst: str) -> str:
    rows_data: list[list[str]] = []
    for tr in tbl.findall(f"{W}tr"):
        row: list[str] = []
        for tc in tr.findall(f"{W}tc"):
            cell_parts: list[str] = []
            for p in cell_paragraphs(tc):
                c = process_paragraph_md(p, rels, word_dir, media_dst, wrap_p=False)
                if c:
                    cell_parts.append(c.strip())
            row.append(_md_escape_cell(" ".join(cell_parts)))
        rows_data.append(row)
    if not rows_data:
        return ""
    num_cols = max(len(r) for r in rows_data)
    lines: list[str] = []
    for i, row in enumerate(rows_data):
        padded = row + [""] * (num_cols - len(row))
        lines.append("| " + " | ".join(padded) + " |")
        if i == 0:
            lines.append("| " + " | ".join(["---"] * num_cols) + " |")
    return "\n".join(lines) + "\n\n"


def body_content_md(
    body: ET.Element,
    rels: dict[str, str],
    word_dir: str,
    media_dst: str,
) -> str:
    parts: list[str] = []
    for child in body:
        tag = child.tag
        if tag == f"{W}p":
            h = process_paragraph_md(child, rels, word_dir, media_dst)
            if h:
                parts.append(h)
        elif tag == f"{W}tbl":
            parts.append(process_table_md(child, rels, word_dir, media_dst))
    return "".join(parts)


def resolve_document_title(body: ET.Element, core_path: str) -> str:
    title = load_core_title(core_path) or extract_title_from_first_paragraph(body)
    if (
        title == "文档"
        or len(title) > 80
        or _looks_like_toc_heading(title)
        or title in _SKIP_HEADINGS
    ):
        title = DEFAULT_DOC_TITLE
    return title


def load_core_title(core_xml: str) -> str | None:
    if not os.path.isfile(core_xml):
        return None
    try:
        tree = ET.parse(core_xml)
        root = tree.getroot()
        dc = "{http://purl.org/dc/elements/1.1/}"
        for child in root:
            if child.tag == dc + "title" and (child.text or "").strip():
                return (child.text or "").strip()[:200]
    except ET.ParseError:
        return None
    return None


def _looks_like_toc_heading(s: str) -> bool:
    n = "".join(s.split())
    return n in ("目录", "目次", "CONTENTS", "Contents")


def extract_title_from_first_paragraph(body: ET.Element) -> str:
    """Prefer short first line; skip huge cover blocks and TOC-only headings."""
    for child in body:
        if child.tag == f"{W}p":
            t = paragraph_plain_text(child).strip()
            if t and len(t) < 120 and not _looks_like_toc_heading(t):
                return t[:200]
    for child in body:
        if child.tag == f"{W}p":
            t = paragraph_plain_text(child).strip()
            if t and not _looks_like_toc_heading(t):
                line = t.split("\n", 1)[0].strip()
                return line[:200] if len(line) < 100 else line[:80] + "…"
    return "文档"


def main() -> int:
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    extract_dir = os.path.join(base, "docx_extract_temp")
    if len(sys.argv) >= 2:
        extract_dir = sys.argv[1]

    doc_xml = os.path.join(extract_dir, "word", "document.xml")
    rels_path = os.path.join(extract_dir, "word", "_rels", "document.xml.rels")
    word_dir = os.path.join(extract_dir, "word")

    if not os.path.isfile(doc_xml):
        print("Missing document.xml; extract .docx first.", file=sys.stderr)
        return 1

    rels = load_relationships(rels_path)
    tree = ET.parse(doc_xml)
    root = tree.getroot()
    body = root.find(f"{W}body")
    if body is None:
        print("No body in document", file=sys.stderr)
        return 1

    core_path = os.path.join(extract_dir, "docProps", "core.xml")
    title = resolve_document_title(body, core_path)
    out_dir = os.path.join(base, "docs", "移动住房时代凤凰来仪")
    assets = os.path.join(out_dir, "assets")
    os.makedirs(assets, exist_ok=True)

    main_html = body_content(body, rels, word_dir, assets)
    main_md = body_content_md(body, rels, word_dir, assets)

    # Optional: heading detection — first short centered line as h1
    safe_title = html.escape(title)

    full = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>{safe_title}</title>
  <style>
    :root {{
      --text: #1a1a1a;
      --muted: #444;
      --border: #ddd;
      --bg: #fafafa;
    }}
    body {{
      font-family: "Segoe UI", "Microsoft YaHei", "PingFang SC", sans-serif;
      line-height: 1.75;
      max-width: 48rem;
      margin: 0 auto;
      padding: 2rem 1.25rem 4rem;
      color: var(--text);
      background: var(--bg);
    }}
    h1 {{
      font-size: 1.65rem;
      font-weight: 700;
      margin-bottom: 1.5rem;
      line-height: 1.35;
      border-bottom: 1px solid var(--border);
      padding-bottom: 0.75rem;
    }}
    p {{ margin: 0.65rem 0; text-align: justify; }}
    .docx-table {{
      border-collapse: collapse;
      width: 100%;
      margin: 1rem 0;
      font-size: 0.95rem;
      background: #fff;
    }}
    .docx-table td {{
      border: 1px solid var(--border);
      padding: 0.45rem 0.6rem;
      vertical-align: top;
    }}
    figure.inline-fig {{
      margin: 1rem auto;
      text-align: center;
      max-width: 100%;
    }}
    figure.inline-fig img {{
      max-width: 100%;
      height: auto;
      border-radius: 4px;
      box-shadow: 0 2px 12px rgba(0,0,0,0.08);
    }}
    figure.inline-fig figcaption {{
      font-size: 0.9rem;
      color: var(--muted);
      margin-top: 0.35rem;
      line-height: 1.45;
    }}
    .doc-meta {{
      color: var(--muted);
      font-size: 0.9rem;
      margin-bottom: 2rem;
    }}
  </style>
</head>
<body>
  <h1>{safe_title}</h1>
  <p class="doc-meta">由 Word 文档转换，正文与插图按原顺序排版。</p>
  <article class="doc-body">
{main_html}
  </article>
</body>
</html>
"""

    out_path = os.path.join(out_dir, "移动住房时代凤凰来仪-全文.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(full)

    md_lines = [
        f"# {title}\n\n",
        "> 由 Word 文档转换；插图路径为 `assets/` 下相对本文件的引用；图片说明在 `![说明](assets/文件名)` 的方括号内。\n\n",
        "---\n\n",
        main_md,
    ]
    md_path = os.path.join(out_dir, "移动住房时代凤凰来仪-全文.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("".join(md_lines))

    print(f"Wrote: {out_path}")
    print(f"Wrote: {md_path}")
    print(f"Assets: {assets}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
