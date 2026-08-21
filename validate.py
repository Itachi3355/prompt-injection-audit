#!/usr/bin/env python3
"""Validate this skill repo: manifests parse, SKILL.md frontmatter is sane,
referenced files exist, evals parse. Run: python validate.py"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).parent
DESC_LIMIT = 1024
errors = []


def check(cond, msg):
    if not cond:
        errors.append(msg)


def frontmatter(text):
    """Parse the leading --- block. Only top-level `key: value` lines."""
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return None
    fields = {}
    for line in m.group(1).splitlines():
        if line.startswith(("  ", "\t")) or ":" not in line:
            continue
        k, v = line.split(":", 1)
        fields[k.strip()] = v.strip()
    return fields


# --- manifests ---
for name in ("plugin.json", "marketplace.json"):
    path = ROOT / ".claude-plugin" / name
    if not path.exists():
        errors.append(f"{name}: missing")
        continue
    try:
        json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        errors.append(f"{name}: invalid JSON - {e}")

# --- skills ---
skill_files = sorted(ROOT.glob("skills/*/SKILL.md"))
check(skill_files, "no skills/*/SKILL.md found")

for skill in skill_files:
    rel = skill.relative_to(ROOT)
    text = skill.read_text(encoding="utf-8")
    fm = frontmatter(text)
    if fm is None:
        errors.append(f"{rel}: no YAML frontmatter block")
        continue
    name = fm.get("name", "")
    desc = fm.get("description", "")
    check(name, f"{rel}: frontmatter missing `name`")
    check(desc, f"{rel}: frontmatter missing `description`")
    check(
        name == skill.parent.name,
        f"{rel}: frontmatter name '{name}' != directory '{skill.parent.name}'",
    )
    check(
        len(desc) <= DESC_LIMIT,
        f"{rel}: description is {len(desc)} chars, limit {DESC_LIMIT}",
    )
    # every `references/foo.md` the skill tells the agent to read must exist
    for ref in sorted(set(re.findall(r"`(references/[\w./-]+)`", text))):
        check((skill.parent / ref).exists(), f"{rel}: references missing file {ref}")

# --- evals ---
for path in sorted(ROOT.glob("evals/*.json")):
    rel = path.relative_to(ROOT)
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        errors.append(f"{rel}: invalid JSON - {e}")
        continue
    evals = data.get("evals")
    if not isinstance(evals, list) or not evals:
        errors.append(f"{rel}: `evals` must be a non-empty list")
        continue
    seen = set()
    for ev in evals:
        eid = ev.get("id")
        for field in ("id", "name", "prompt", "expected_output"):
            check(ev.get(field), f"{rel}: eval {eid!r} missing `{field}`")
        check(eid not in seen, f"{rel}: duplicate eval id {eid!r}")
        seen.add(eid)

if errors:
    print("FAIL")
    for e in errors:
        print(f"  - {e}")
    sys.exit(1)

print(f"OK - {len(skill_files)} skill(s), manifests and evals valid")
