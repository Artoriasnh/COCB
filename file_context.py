import os
from dataclasses import dataclass
from typing import Iterable, List, Optional, Set, Tuple


@dataclass
class LoadedFile:
    path: str
    content: str
    truncated: bool


def _safe_read_text(path: str) -> str:
    """
    安全读取文本文件（忽略编码错误）
    """
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def load_files(
    paths: Iterable[str],
    allowed_ext: Optional[Set[str]] = None,
    max_chars_per_file: int = 8000,
    max_total_chars: int = 80000,
) -> Tuple[List[LoadedFile], int]:
    """
    读取文件或文件夹中的代码文件。
    返回:
        loaded_files: 文件列表
        total_chars: 总字符数
    """

    if allowed_ext is None:
        allowed_ext = {".py", ".html", ".txt", ".md", ".js", ".css"}

    collected_files: List[str] = []

    # 收集文件路径
    for p in paths:
        if not p:
            continue

        p = os.path.abspath(p)

        if os.path.isfile(p):
            collected_files.append(p)

        elif os.path.isdir(p):
            for root, _, files in os.walk(p):
                for filename in files:
                    ext = os.path.splitext(filename)[1].lower()
                    if ext in allowed_ext:
                        collected_files.append(
                            os.path.join(root, filename)
                        )

    collected_files = sorted(set(collected_files))

    loaded_files: List[LoadedFile] = []
    total_chars = 0

    for filepath in collected_files:

        if total_chars >= max_total_chars:
            break

        ext = os.path.splitext(filepath)[1].lower()
        if ext not in allowed_ext:
            continue

        try:
            content = _safe_read_text(filepath)
        except Exception:
            continue

        truncated = False

        # 限制单文件大小
        if len(content) > max_chars_per_file:
            content = content[:max_chars_per_file]
            truncated = True

        block_size = len(content)

        # 限制总上下文大小
        if total_chars + block_size > max_total_chars:
            remaining = max_total_chars - total_chars
            if remaining <= 0:
                break
            content = content[:remaining]
            truncated = True

        loaded_files.append(
            LoadedFile(
                path=filepath,
                content=content,
                truncated=truncated,
            )
        )

        total_chars += len(content)

    return loaded_files, total_chars


def build_context_text(loaded_files: List[LoadedFile]) -> str:
    """
    将文件列表拼接成模型上下文文本
    """
    parts = []

    for lf in loaded_files:
        truncated_note = " (TRUNCATED)" if lf.truncated else ""
        parts.append(
            f"# FILE: {lf.path}{truncated_note}\n"
            f"{lf.content}\n"
        )

    return "\n".join(parts)