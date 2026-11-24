"""Build world-of-warcraft.index and validate all content files.

Checks: well-formed XML, unique ids, every referenced ID_ exists in our
files or in the Aurora Legacy / core repos checked out locally.
"""
import pathlib, re, sys
import xml.etree.ElementTree as ET
sys.path.insert(0, "/home/claude/tools")
from common import ROOT, BASE, REPO

root = pathlib.Path(ROOT)
content = root / "world-of-warcraft"
VERSION = sys.argv[1] if len(sys.argv) > 1 else "0.1.0"

files = sorted(p for p in content.rglob("*.xml"))
ours, errors = {}, []
refs = []
for f in files:
    try:
        tree = ET.parse(f)
    except ET.ParseError as e:
        errors.append(f"PARSE {f.relative_to(root)}: {e}")
        continue
    for el in tree.getroot().iter("element"):
        i = el.get("id")
        if i in ours:
            errors.append(f"DUP id {i} in {f.name} and {ours[i]}")
        ours[i] = f.name
        for a in ("name", "type", "source", "id"):
            if not el.get(a):
                errors.append(f"MISSING {a} on element in {f.name}")
    txt = f.read_text()
    upd = re.search(r'<update[^>]*>\s*<file name="([^"]+)" url="([^"]+)"', txt)
    rel = f.relative_to(root).as_posix()
    if not upd or upd.group(1) != f.name or upd.group(2) != f"{BASE}/{rel}":
        errors.append(f"SELF-UPDATE url/name mismatch in {rel}")
    for m in re.finditer(r"ID_[A-Z0-9_]+", txt):
        refs.append((m.group(0), f.name))

# external ids
ext = set()
for repo in ("/home/claude/legacy", "/home/claude/aurora-elements"):
    for p in pathlib.Path(repo).rglob("*.xml"):
        ext.update(re.findall(r'id="(ID_[A-Z0-9_]+)"', p.read_text(errors="ignore")))

missing = sorted({(r, f) for r, f in refs if r not in ours and r not in ext})
for r, f in missing:
    errors.append(f"UNKNOWN ref {r} in {f}")

# index
lines = [f'<?xml version="1.0" encoding="utf-8"?>', "<index>", "\t<info>",
         "\t\t<name>World of Warcraft</name>",
         "\t\t<description>World of Warcraft by Andrey Kuzinskiy: classes, species, spells, feats, gear and renown for D&amp;D 2024. Requires the Aurora Legacy Player’s Handbook (2024).</description>",
         f'\t\t<author url="https://github.com/{REPO}">Andrey Kuzinskiy (book), converted by Kaya Acarbay</author>',
         f'\t\t<update version="{VERSION}">',
         f'\t\t\t<file name="world-of-warcraft.index" url="{BASE}/world-of-warcraft.index" />',
         "\t\t</update>", "\t</info>", "\t<files>"]
for f in files:
    rel = f.relative_to(root).as_posix()
    lines.append(f'\t\t<file name="{f.name}" url="{BASE}/{rel}" />')
lines += ["\t</files>", "</index>", ""]
(root / "world-of-warcraft.index").write_text("\n".join(lines))

names = [f.name for f in files]
dupe_names = {n for n in names if names.count(n) > 1}
for n in dupe_names:
    errors.append(f"DUPLICATE file name {n} (Aurora stores files flat by name)")

print(f"{len(files)} files, {len(ours)} elements")
print("\n".join(errors) if errors else "OK: no errors")
