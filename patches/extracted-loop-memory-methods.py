"""Extracted memory helper methods from the currently patched nanobot AgentLoop.

This file is for reference/reuse when porting the patch to other nanobot versions.
"""

from __future__ import annotations

import sqlite3
import time
from typing import Any


def _strip_memory_block(text: str) -> str:
    start_tag = "<relevant-memories>"
    end_tag = "</relevant-memories>"
    while start_tag in text and end_tag in text:
        s = text.find(start_tag)
        e = text.find(end_tag, s)
        if e == -1:
            break
        text = (text[:s] + text[e + len(end_tag):]).strip()
    return text.strip()


def _content_to_text(content: Any) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        out: list[str] = []
        for block in content:
            if not isinstance(block, dict):
                continue
            text = block.get("text") or block.get("content") or ""
            if isinstance(text, str) and text.strip():
                out.append(text)
        return "\n".join(out)
    return ""


def reference_only_note() -> str:
    return "Use nanobot_memory.store + nanobot_memory.recall for reusable implementation."
