"""Generate skills/_generated/choice-values.md from schema_def.py (single source of truth).

Usage: python scripts/gen_skill_resources.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import schema_def as S  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "skills", "submit-agentic-use-case", "choice-values.md")


def column_rows(table):
    rows = [f"| `{S.PREFIX}_{table['primary'][0].lower()}` | {table['primary'][1]} | text (max {table['primary'][2]}) | **required** |"]
    for suffix, display, kind, extra in table["columns"]:
        logical = f"{S.PREFIX}_{suffix.lower()}"
        if kind == "autonumber":
            t = "auto-number (read-only, do not set)"
        elif kind in ("choice", "multichoice"):
            t = f"{'multi-select ' if kind == 'multichoice' else ''}choice `{extra['set']}`"
        elif kind == "int":
            t = f"whole number {extra.get('min', 0)}–{extra.get('max')}"
        elif kind in ("string", "email", "memo"):
            t = f"{'email' if kind == 'email' else 'text'} (max {extra.get('max', 320 if kind == 'email' else 100)})"
        elif kind == "bool":
            t = "yes/no (true/false)"
        elif kind == "date":
            t = "date only (YYYY-MM-DD)"
        else:
            t = kind
        note = "**required**" if extra.get("required") else ""
        rows.append(f"| `{logical}` | {display} | {t} | {note} |")
    return rows


def main():
    lines = [
        "# Agentic Use Case Intake — column and choice reference",
        "",
        "Generated from `scripts/schema_def.py`. Do not edit by hand.",
        "",
        "## sams_usecase (Agentic Use Case)",
        "",
        "| Logical name | Display name | Type | Notes |",
        "|---|---|---|---|",
        *column_rows(S.USECASE),
        "",
        "## sams_usecasesystem (Target System)",
        "",
        "| Logical name | Display name | Type | Notes |",
        "|---|---|---|---|",
        *column_rows(S.USECASESYSTEM),
        f"| `{S.RELATIONSHIP['lookup_schema'].lower()}` | {S.RELATIONSHIP['lookup_display']} | lookup to sams_usecase | **required** |",
        "",
        "## Choice values",
        "",
    ]
    for name, (display, options) in S.CHOICES.items():
        lines.append(f"### {name} ({display})")
        lines.append("")
        lines.append(" · ".join(f"`{v}` = {label}" for v, label in options))
        lines.append("")
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines))
    print(f"Wrote {OUT} ({os.path.getsize(OUT)} bytes)")


if __name__ == "__main__":
    main()
