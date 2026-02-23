import re
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class PatchFile:
    path: str
    code: str


PATCH_RE = re.compile(
    r"#\s*file:\s*(?P<path>.+?)\s*\n```python\s*\n(?P<code>.*?)(?:\n```)",
    re.DOTALL | re.IGNORECASE,
)


def extract_patch_files(text: str) -> List[PatchFile]:
    out: List[PatchFile] = []
    for m in PATCH_RE.finditer(text):
        path = m.group("path").strip()
        code = m.group("code").rstrip() + "\n"
        out.append(PatchFile(path=path, code=code))
    return out


def extract_summary(text: str) -> Optional[str]:
    m = re.search(r"\[SUMMARY\]\s*(.*?)(?:\n\s*\[PATCH\]|\Z)", text, re.DOTALL | re.IGNORECASE)
    if not m:
        return None
    return m.group(1).strip()