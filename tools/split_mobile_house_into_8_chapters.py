"""
Split the full Markdown manuscript into an 8-chapter reorganized edition.

Input:
  docs/移动住房时代凤凰来仪/移动住房时代凤凰来仪-全文.md

Output:
  docs/移动住房时代凤凰来仪/8章版/
    README.md
    01-问题与愿景.md
    02-移动住房的概念与基本形态.md
    03-制度与人口流动约束.md
    04-核心产品方案：电动房车公寓.md
    05-移动空间的扩展应用.md
    06-关键支撑技术.md
    07-空中交通与居住半径扩张.md
    08-社会影响、风险与未来展望.md
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "docs" / "移动住房时代凤凰来仪" / "移动住房时代凤凰来仪-全文.md"
OUT_DIR = ROOT / "docs" / "移动住房时代凤凰来仪" / "8章版"


@dataclass(frozen=True)
class Chapter:
    filename: str
    title: str
    summary: str
    body: str


def load_lines(path: Path) -> list[str]:
    return path.read_text(encoding="utf-8").splitlines()


def take(lines: list[str], start: int, end: int) -> str:
    """1-indexed inclusive line slice."""
    return "\n".join(lines[start - 1 : end]).strip()


def normalize_links(text: str) -> str:
    # The split files live in `8章版/`, so image links must go one level up.
    return text.replace("(assets/", "(../assets/")


def section(heading: str, text: str) -> str:
    normalized = normalize_links(text).strip()
    lines = normalized.splitlines()
    if lines and lines[0].strip() == heading.strip():
        normalized = "\n".join(lines[1:]).lstrip()
    return f"## {heading}\n\n{normalized}\n"


def promote_exact_headings(
    text: str,
    replacements: list[tuple[str, str]],
) -> str:
    """
    Replace exact standalone lines with markdown headings.
    Each replacement is (original_line, heading_prefix).
    """
    lines = text.splitlines()
    out: list[str] = []
    for line in lines:
        stripped = line.strip()
        replaced = False
        for original, prefix in replacements:
            if stripped == original or stripped.startswith(original):
                out.append(f"{prefix} {original}")
                replaced = True
                break
        if not replaced:
            out.append(line)
    return "\n".join(out)


def format_image_captions(text: str) -> str:
    """
    Convert short standalone lines after images into explicit blockquote captions.
    This keeps figure labels/sources visually distinct from正文小标题.
    """
    lines = text.splitlines()
    out: list[str] = []
    prev_nonempty = ""

    for line in lines:
        stripped = line.strip()
        if not stripped:
            out.append(line)
            continue

        should_caption = False
        if prev_nonempty.startswith("!["):
            if not stripped.startswith(("#", ">", "-", "*", "|", "![")) and not stripped.startswith(
                ("1. ", "2. ", "3. ", "4. ", "5. ")
            ):
                source_like = (
                    stripped.startswith("图片源自")
                    or stripped.startswith("视频")
                    or stripped.startswith("官网")
                    or stripped.startswith("示例来自")
                    or stripped.startswith("国家标准")
                )
                generic_like = (
                    len(stripped) <= 16
                    and not any(p in stripped for p in "。！？；：")
                )
                if source_like or generic_like:
                    should_caption = True

        if should_caption:
            clean = stripped.strip("*").strip()
            out.append(f"> 图注：{clean}")
        else:
            out.append(line)

        prev_nonempty = stripped

    return "\n".join(out)


def dedupe_adjacent_headings(text: str) -> str:
    """
    Collapse repeated markdown headings when the same heading appears twice
    with only blank lines in between.
    """
    lines = text.splitlines()
    out: list[str] = []

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("#") and out:
            j = len(out) - 1
            while j >= 0 and not out[j].strip():
                j -= 1
            if j >= 0 and out[j].strip() == stripped:
                continue
        out.append(line)

    return "\n".join(out)


def polish_generated_content(text: str) -> str:
    """Apply a few stable cleanup rules for stubborn pseudo-headings."""
    text = text.replace(
        "\n电动房车公寓\n\n![IMG_256]",
        "\n### 电动房车公寓\n\n![IMG_256]",
    )
    text = text.replace("### 水\n\n### 水", "### 水")
    return text


def write(path: Path, content: str) -> None:
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def build_chapters(lines: list[str]) -> list[Chapter]:
    chapter1 = Chapter(
        filename="01-问题与愿景.md",
        title="第1章 问题与愿景",
        summary="从摘要与开篇引子入手，先回答这本书试图解决什么现实问题，以及为何需要一种新的住房形态。",
        body="\n\n".join(
            [
                section("摘要", take(lines, 93, 117)),
                section("Abstract", take(lines, 119, 137)),
                section("问题的提出", take(lines, 141, 180)),
            ]
        ),
    )

    chapter2 = Chapter(
        filename="02-移动住房的概念与基本形态.md",
        title="第2章 移动住房的概念与基本形态",
        summary="围绕四代住房演变、移动化/模块化/接口化与基础设计展开，是全书的概念核心。",
        body="\n\n".join(
            [
                section("住房的种类和功能", take(lines, 181, 216)),
                promote_exact_headings(
                    section("移动房什么样？", take(lines, 219, 343)),
                    [
                        ("1、移动化", "###"),
                        ("2、模块化", "###"),
                        ("3、接口化", "###"),
                    ],
                ),
                promote_exact_headings(
                    section("移动房概要设计", take(lines, 345, 429)),
                    [],
                ),
            ]
        ),
    )

    chapter3 = Chapter(
        filename="03-制度与人口流动约束.md",
        title="第3章 制度与人口流动约束",
        summary="讨论户口、教育、高考与人口流动对居住方式选择的影响。",
        body="\n\n".join(
            [
                section("户口和户籍", take(lines, 433, 455)),
                promote_exact_headings(
                    section("户口相关的资质", take(lines, 457, 473)),
                    [
                        ("1. 车牌摇号", "###"),
                        ("2. 房子", "###"),
                        ("3. 教育", "###"),
                    ],
                ),
                promote_exact_headings(
                    section("高考", take(lines, 475, 531)),
                    [
                        ("高考路线", "###"),
                        ("非高考路线", "###"),
                    ],
                ),
            ]
        ),
    )

    chapter4 = Chapter(
        filename="04-核心产品方案：电动房车公寓.md",
        title="第4章 核心产品方案：电动房车公寓",
        summary="集中呈现电动房车公寓的用户定位、内部设计、补给、驾驶、停放与通勤方案。",
        body="\n\n".join(
            [
                promote_exact_headings(
                    section("方案概述", take(lines, 533, 559)),
                    [
                        ("电动房车公寓", "###"),
                        ("用户群体", "###"),
                        ("居住成本费用明细表", "###"),
                        ("居住在房车，已经不是新鲜话题。看似方便，实则痛点不少，比如：", "###"),
                    ],
                ),
                promote_exact_headings(
                    section("车内布局设计", take(lines, 561, 638)),
                    [
                        ("三室分离卫生间", "###"),
                        ("开放式厨房", "###"),
                        ("卧室", "###"),
                        ("燃油房车", "###"),
                    ],
                ),
                promote_exact_headings(
                    section("水、电、燃气等怎么补充", take(lines, 640, 686)),
                    [
                        ("补给方式有两种：", "###"),
                        ("水", "###"),
                        ("电", "###"),
                        ("燃气", "###"),
                        ("冬季取暖", "###"),
                        ("上网", "###"),
                        ("安全", "###"),
                    ],
                ),
                section("怎么驾驶", take(lines, 688, 695)),
                section("怎么停放", take(lines, 697, 716)),
                section("如何减少上班通勤的时间？", take(lines, 718, 722)),
            ]
        ),
    )

    chapter5 = Chapter(
        filename="05-移动空间的扩展应用.md",
        title="第5章 移动空间的扩展应用",
        summary="把居住之外的移动空间场景归为一组，包括酒店民宿影响、移动会议室与 mini 电动巴士公寓等案例。",
        body="\n\n".join(
            [
                promote_exact_headings(
                    section("酒店、民宿与移动居住服务", take(lines, 723, 757)),
                    [
                        ("对酒店、民宿的影响", "###"),
                    ],
                ),
                promote_exact_headings(
                    section("移动会议室", take(lines, 760, 825)),
                    [
                        ("移动会议室概要设计", "###"),
                        ("模型图", "###"),
                        ("移动鲜花店", "###"),
                        ("移动咖啡馆", "###"),
                        ("移动工作室", "###"),
                    ],
                ),
                section("mini 电动巴士公寓", take(lines, 910, 924)),
            ]
        ),
    )

    chapter6 = Chapter(
        filename="06-关键支撑技术.md",
        title="第6章 关键支撑技术",
        summary="把自动驾驶、人工智能与电池/氢能重新组合为支撑移动住房普及的技术底座。",
        body="\n\n".join(
            [
                promote_exact_headings(
                    section("自动驾驶", take(lines, 828, 909) + "\n\n" + take(lines, 926, 983)),
                    [
                        ("自动驾驶分类等级", "###"),
                        ("自动驾驶带来的便利", "###"),
                        ("自动驾驶技术路线和进展", "###"),
                        ("1、政策法规", "####"),
                        ("2、量产成本", "####"),
                    ],
                ),
                promote_exact_headings(
                    section("人工智能", take(lines, 987, 1300)),
                    [
                        ("0和1的二元世界", "###"),
                        ("二进制", "####"),
                        ("声音、图片、视频，如何表示", "####"),
                        ("机器学习", "###"),
                        ("感知机", "####"),
                        ("神经网络", "####"),
                        ("卷积神经网络", "####"),
                        ("AI寄语", "###"),
                    ],
                ),
                promote_exact_headings(
                    section("电池与氢能", take(lines, 1304, 1452)),
                    [
                        ("锂电池家族", "###"),
                        ("氢燃料电池", "###"),
                        ("其他电池", "###"),
                        ("铅酸电池", "####"),
                        ("一次性干电池（又叫锌锰电池）", "####"),
                        ("固态电池", "####"),
                        ("钠离子电池", "####"),
                        ("镁电池", "####"),
                        ("铝离子电池", "####"),
                        ("钾离子电池", "####"),
                        ("生物燃料电池", "####"),
                        ("太阳能电池", "####"),
                    ],
                ),
            ]
        ),
    )

    chapter7 = Chapter(
        filename="07-空中交通与居住半径扩张.md",
        title="第7章 空中交通与居住半径扩张",
        summary="保留飞行器谱系与“如何改变住行”的核心论述，用来解释未来居住半径为何会被重新定义。",
        body="\n\n".join(
            [
                promote_exact_headings(
                    section("电动飞行器谱系", take(lines, 1456, 1578)),
                    [
                        ("电动垂直起降飞行器", "###"),
                        ("电动固定翼飞行器", "###"),
                        ("仿生扑翼飞行器", "###"),
                        ("地效飞行器", "###"),
                        ("东山再起的飞艇", "###"),
                    ],
                ),
                section("电动飞行器如何改变住行", take(lines, 1580, 1630)),
            ]
        ),
    )

    chapter8 = Chapter(
        filename="08-社会影响、风险与未来展望.md",
        title="第8章 社会影响、风险与未来展望",
        summary="收束全书，对社会影响、现实约束与作者性的结语进行整合。",
        body="\n\n".join(
            [
                section("社会影响", take(lines, 1634, 1679)),
                section("实施路径与产业条件", take(lines, 1680, 1699)),
                section(
                    "风险与现实约束",
                    (
                        "移动住房与相关技术并不会自动完成社会替代，它仍受到政策、基础设施、公众接受度与技术成熟度的共同约束。"
                        "\n\n"
                        + take(lines, 1700, 1708)
                    ),
                ),
                section("未来展望与结语", take(lines, 1710, 1732)),
            ]
        ),
    )

    return [chapter1, chapter2, chapter3, chapter4, chapter5, chapter6, chapter7, chapter8]


def build_index(chapters: list[Chapter]) -> str:
    links = "\n".join(f"- [{c.title}]({c.filename})" for c in chapters)
    return (
        "# 《移动住房时代，凤凰来仪》8章版\n\n"
        "> 本目录基于 `移动住房时代凤凰来仪-全文.md` 按 8 章重构方案拆分生成。\n\n"
        "## 目录\n\n"
        f"{links}\n\n"
        "## 说明\n\n"
        "- 本版本保留原书正文与图片，尽量少做内容改写。\n"
        "- 图片资源统一复用上级目录中的 `assets/`。\n"
        "- 拆分以“论证主线”而非原始章号为准，因此个别内容做了并章或移位。\n"
    )


def main() -> int:
    if not SOURCE.is_file():
        raise FileNotFoundError(f"Source manuscript not found: {SOURCE}")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for old_md in OUT_DIR.glob("*.md"):
        old_md.unlink()
    lines = load_lines(SOURCE)
    chapters = build_chapters(lines)

    for chapter in chapters:
        content = (
            f"# {chapter.title}\n\n"
            f"> {chapter.summary}\n\n"
            f"{chapter.body.strip()}\n"
        )
        content = format_image_captions(content)
        content = dedupe_adjacent_headings(content)
        content = polish_generated_content(content)
        write(OUT_DIR / chapter.filename, content)

    write(OUT_DIR / "README.md", build_index(chapters))
    print(f"Wrote {len(chapters)} chapter files to: {OUT_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
