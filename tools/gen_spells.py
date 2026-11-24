"""Generate spells.xml from spells.json."""
import json, re, sys
sys.path.insert(0, "/home/claude/tools")
from textfmt import paragraphs, to_html, slug, escape, clean
from common import header, footer, SOURCE, idp

spells = json.load(open("/home/claude/wow/spells.json"))
FIX_NAMES = {}

TAIL = re.compile(r"^(Using a Higher-Level Spell Slot|Cantrip Upgrade)\.")
# manual fixes: name -> (number of paragraphs to keep | None, [substrings to drop])
OVR = json.load(open("/home/claude/tools/spell_overrides.json"))


def cut_fragment(p):
    """Drop trailing words after the last sentence end (column-bleed junk)."""
    m = re.match(r"^(.*[.)])\s+[A-Z][^.]{0,40}$", p, re.S)
    return m.group(1) if m else p


def trim(name, paras):
    o = OVR.get(name, {})
    if "paras" in o:
        return o["paras"]
    for d in o.get("drop", []):
        paras = [p.replace(d, "").strip() for p in paras]
        paras = [p for p in paras if p]
    if "keep" in o:
        paras = paras[:o["keep"]]
    else:
        for i, p in enumerate(paras):
            if TAIL.match(p):
                paras = paras[:i + 1]
                break
    if "cut" in o:
        paras[-1] = paras[-1].split(o["cut"])[0].rstrip()
    else:
        paras[-1] = cut_fragment(paras[-1])
    return paras


elements = []
for s in spells:
    name = FIX_NAMES.get(s["name"], s["name"])
    s["name"] = name
    paras = trim(name, paragraphs(s["body"]))
    text = " ".join(paras).lower()
    lists = []
    for part in s["lists"].split(","):
        part = part.strip()
        m = re.match(r"(\w+) \[(.+)\]", part)
        lists.append(m.group(2) if m else part)
    tags = list(lists)
    if re.search(r"\d+d\d+ \w+ damage", text):
        tags.append("Damaging Spell")
    if "spell attack" in text:
        tags.append("Spell Attack")
    if "saving throw" in text:
        tags.append("Spell Saving Throw")
    comp = clean(s.get("Components", ""))
    mat = re.search(r"M \((.*)\)", comp)
    dur = clean(s.get("Duration", ""))
    time = clean(s.get("Casting Time", ""))
    rng = clean(s.get("Range", "")).replace(" ft.", " feet")
    x = []
    x.append(f'\t<element name="{escape(name)}" type="Spell" source="{SOURCE}" id="{idp("SPELL", name)}">')
    x.append(f"\t\t<supports>{escape(', '.join(tags))}</supports>")
    x.append("\t\t<description>")
    x += ["\t\t\t" + h for h in to_html(paras)]
    x.append("\t\t</description>")
    x.append("\t\t<setters>")
    x.append(f'\t\t\t<set name="level">{s["level"]}</set>')
    x.append(f'\t\t\t<set name="school">{s["school"]}</set>')
    x.append(f'\t\t\t<set name="time">{escape(time)}</set>')
    x.append(f'\t\t\t<set name="range">{escape(rng)}</set>')
    if re.search(r"\bV\b", comp):
        x.append('\t\t\t<set name="hasVerbalComponent">true</set>')
    if re.search(r"\bS\b", comp):
        x.append('\t\t\t<set name="hasSomaticComponent">true</set>')
    if mat:
        x.append('\t\t\t<set name="hasMaterialComponent">true</set>')
        x.append(f'\t\t\t<set name="materialComponent">{escape(mat.group(1))}</set>')
    if dur.lower().startswith("concentration"):
        x.append('\t\t\t<set name="isConcentration">true</set>')
    if "ritual" in time.lower():
        x.append('\t\t\t<set name="isRitual">true</set>')
    x.append(f'\t\t\t<set name="duration">{escape(dur)}</set>')
    x.append("\t\t</setters>")
    x.append("\t</element>")
    elements.append((name, "\n".join(x)))

elements.sort()
body = "\n\n".join(e for _, e in elements)
open(sys.argv[1], "w").write(header("spells/wow-spells.xml", "Spells",
     "New spells from World of Warcraft (Andrey Kuzinskiy).") + body + footer())
print(len(elements), "spells written")
