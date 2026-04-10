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
    return f"## {heading}\n\n{normalize_links(text).strip()}\n"


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
        body=normalize_links(take(lines, 181, 429)),
    )

    chapter3 = Chapter(
        filename="03-制度与人口流动约束.md",
        title="第3章 制度与人口流动约束",
        summary="讨论户口、教育、高考与人口流动对居住方式选择的影响。",
        body=normalize_links(take(lines, 430, 532)),
    )

    chapter4 = Chapter(
        filename="04-核心产品方案：电动房车公寓.md",
        title="第4章 核心产品方案：电动房车公寓",
        summary="集中呈现电动房车公寓的用户定位、内部设计、补给、驾驶、停放与通勤方案。",
        body=normalize_links(take(lines, 533, 722)),
    )

    chapter5 = Chapter(
        filename="05-移动空间的扩展应用.md",
        title="第5章 移动空间的扩展应用",
        summary="把居住之外的移动空间场景归为一组，包括酒店民宿影响、移动会议室与 mini 电动巴士公寓等案例。",
        body="\n\n".join(
            [
                section("酒店、民宿与移动居住服务", take(lines, 723, 757)),
                section("移动会议室", take(lines, 760, 825)),
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
                section("自动驾驶", take(lines, 828, 909) + "\n\n" + take(lines, 926, 983)),
                section("人工智能", take(lines, 986, 1300)),
                section("电池与氢能", take(lines, 1304, 1452)),
            ]
        ),
    )

    chapter7 = Chapter(
        filename="07-空中交通与居住半径扩张.md",
        title="第7章 空中交通与居住半径扩张",
        summary="保留飞行器谱系与“如何改变住行”的核心论述，用来解释未来居住半径为何会被重新定义。",
        body="\n\n".join(
            [
                section("电动飞行器谱系", take(lines, 1456, 1578)),
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
        write(OUT_DIR / chapter.filename, content)

    write(OUT_DIR / "README.md", build_index(chapters))
    print(f"Wrote {len(chapters)} chapter files to: {OUT_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
