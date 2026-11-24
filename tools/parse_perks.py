"""Extract spell blocks from the per-page column text files.

Usage: python3 -I parse_spells.py PAGES_DIR OUT_JSON
"""
import json, re, sys, pathlib

pages_dir = pathlib.Path(sys.argv[1])
out = sys.argv[2]

HEADER = re.compile(r"^Prerequisite: (?P<pre>.*)$")
FIELD = re.compile(r"^(Casting Time|Range|Components|Duration):\s*(.*)$")
FOOTER = re.compile(r"(CHAPTER \d+ •|^\d+\s+CHAPTER|•\s+CHAPTER)")


def page_lines(path):
    """Left column then right column; strip footers and RIGHT marker."""
    raw = path.read_text().split("=====RIGHT=====")
    lines = []
    for ci, col in enumerate(raw):
        for ln in col.split("\n"):
            if FOOTER.search(ln):
                continue
            lines.append((path.name, ln.rstrip(), ci))
    return lines

all_lines = []
for p in sorted(pages_dir.glob("p*.txt")):
    if not (115 <= int(p.stem[1:]) <= 132): continue
    all_lines.extend(page_lines(p))

# find header indices
spells = []
idx = [i for i, (_, l, _c) in enumerate(all_lines) if HEADER.match(l.strip()) and _c >= 0]
for n, i in enumerate(idx):
    m = HEADER.match(all_lines[i][1].strip())
    # name = nearest non-empty line above
    j = i - 1
    while j >= 0 and (not all_lines[j][1].strip() or re.match(r"^[A-Z .’'-]+$", all_lines[j][1].strip())):
        j -= 1
    name = all_lines[j][1].strip()
    fields, k = {}, i + 1
    # header may wrap onto next line, e.g. "(Requires Attunement by a Paladin)"
    hdr = all_lines[i][1].strip()
    if hdr.count("(") > hdr.count(")"):
        hdr += " " + all_lines[k][1].strip(); k += 1
    # body until the line before the next spell's name line
    if n + 1 < len(idx):
        end = idx[n + 1] - 1
        while end > k and (not all_lines[end][1].strip() or re.match(r"^[A-Z .’'-]+$", all_lines[end][1].strip())):
            end -= 1
        # 'end' is now the next spell's name line; exclude it
    else:
        end = min(k + 80, len(all_lines))
    body = [[all_lines[x][0], all_lines[x][2], all_lines[x][1]] for x in range(k, end)]
    spells.append({
        "name": name,
        "header": hdr,
        "page": all_lines[i][0],
        **fields,
        "body": body,
    })

json.dump(spells, open(out, "w"), indent=1, ensure_ascii=False)
print(len(spells), "spells")
for s in spells:
    print(f"{s['page']} | {s['name']:<40} | {s['header']}")
