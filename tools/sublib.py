"""Helpers for subclasses (Archetype + Archetype Feature elements)."""
import sys, re
sys.path.insert(0, "/home/claude/tools")
from racelib import lore_from, P, spell_id
from textfmt import escape, slug, to_html, is_label
from common import header, footer, SOURCE, PREFIX, ROOT, FP


def sec(pages, start, end, drop=()):
    return lore_from(pages, start, end, drop=drop)


import os
ED = os.environ.get("ED", "2024")
CONV14 = [
    ("Focus Points", "ki points"), ("Focus Point", "ki point"), ("Heroic Inspiration", "Inspiration"),
    ("starts its turn Bloodied", "starts its turn with half its Hit Points or fewer"),
    ("a Bloodied creature", "a creature that has half its Hit Points or fewer"),
    ("is Bloodied", "has half its Hit Points or fewer"), ("become Bloodied", "drop to half your Hit Points or fewer"),
    ("an Magic action", "an action"), ("a Magic action", "an action"), ("Magic action", "action"), ("Magic Action", "Action"),
    ("D20 Test", "attack roll, ability check, or saving throw"),
]


def conv(t):
    if ED != "2014" or not isinstance(t, str):
        return t
    for a, b in CONV14:
        t = t.replace(a, b)
    return t


def html(paras):
    """paragraph list -> html lines, with run-in labels bold and tables passed through."""
    paras = [conv(p) for p in paras]
    out = []
    for i, p in enumerate(paras):
        if p.startswith("<"):
            out.append(p)
            continue
        cls = ' class="indent"' if i > 0 else ""
        lab = is_label(p)
        if lab:
            out.append(f"<p{cls}><strong><em>{escape(lab[0])}.</em></strong> {escape(lab[1])}</p>")
        else:
            out.append(f"<p{cls}>{escape(p)}</p>")
    return out


class Feature:
    def __init__(self, level, name, paras, sheet=None, rules=(), usage=None, action=None,
                 replaces=(), etype="Archetype Feature", fid=None, supports=None, req=None,
                 compendium=True, alt=None, grant=True):
        self.level, self.name, self.paras = level, name, paras
        self.sheet, self.rules, self.usage, self.action = sheet, list(rules), usage, action
        self.replaces, self.etype, self.fid = replaces, etype, fid
        self.supports, self.req, self.compendium, self.alt = supports, req, compendium, alt
        self.grant = grant

    def title(self):
        return f"Level {self.level}: {self.name}" if self.level else self.name

    def xml(self, base):
        self.fid = self.fid or f"{base}_{slug(self.name)}"
        x = [f'\t<element name="{escape(self.title())}" type="{self.etype}" source="{SOURCE}" id="{self.fid}">']
        if self.supports:
            x.append(f"\t\t<supports>{escape(self.supports)}</supports>")
        if self.req:
            x.append(f"\t\t<requirements>{self.req}</requirements>")
        if not self.compendium:
            x.append('\t\t<compendium display="false" />')
        x.append("\t\t<description>")
        x += ["\t\t\t" + h for h in html(self.paras)]
        x.append("\t\t</description>")
        if self.sheet is False:
            x.append('\t\t<sheet display="false" />')
        else:
            a = ""
            if self.alt or self.level:
                a += f' alt="{escape(self.alt or self.name)}"'
            if self.action:
                a += f' action="{self.action}"'
            if self.usage:
                a += f' usage="{self.usage}"'
            if isinstance(self.sheet, list):
                x.append(f"\t\t<sheet{a}>")
                for lvl, d in [(l, conv(d)) for l, d in self.sheet]:
                    la = f' level="{lvl}"' if lvl else ""
                    x.append(f"\t\t\t<description{la}>{escape(d)}</description>")
                x.append("\t\t</sheet>")
            else:
                d = conv(self.sheet or " ".join(p for p in self.paras if not p.startswith("<")))
                x.append(f"\t\t<sheet{a}>\n\t\t\t<description>{escape(d)}</description>\n\t\t</sheet>")
        rules = [f'<grant type="Grants" id="{r}" />' for r in self.replaces] + self.rules
        if rules:
            x.append("\t\t<rules>")
            x += ["\t\t\t" + r for r in rules]
            x.append("\t\t</rules>")
        x.append("\t</element>")
        return "\n".join(x)


def archetype(fname, name, cls, flavor, intro, features, extra=(), spellcasting=None, file_desc=None,
              kind="ARCHETYPE", tag=None):
    """features: list of Feature (granted at their level) — options with grant=False are just emitted."""
    aid = f"{PREFIX}_{kind}_{slug(cls)}_{slug(name)}"
    base = f"{PREFIX}_{kind}_FEATURE_{slug(cls)}_{slug(name)}"
    body = [f.xml(base) for f in features] + list(extra)
    x = [f'\t<element name="{escape(name)}" type="Archetype" source="{SOURCE}" id="{aid}">',
         f"\t\t<supports>{tag or cls + ' Subclass'}</supports>", "\t\t<description>"]
    if flavor:
        x.append(f'\t\t\t<p class="flavor">{escape(flavor)}</p>')
    if ED == "2014":
        intro = list(intro) + ["This is a 2014 rules adaptation of a subclass from World of Warcraft (a 2024 rules book). Terms that exist only in the 2024 rules have been converted to their 2014 equivalents."]
    x += ["\t\t\t" + h for h in html(intro)]
    for f in features:
        if f.grant:
            x.append(f'\t\t\t<div element="{f.fid}" />')
    x.append("\t\t</description>")
    x.append('\t\t<sheet display="false" />')
    if spellcasting:
        x.append(spellcasting)
    x.append("\t\t<rules>")
    for f in features:
        if f.grant:
            lv = f' level="{f.level}"' if f.level else ""
            x.append(f'\t\t\t<grant type="Archetype Feature" id="{f.fid}"{lv} />')
    x.append("\t\t</rules>")
    x.append("\t</element>")
    path = f"archetypes/{fname}"
    open(f"{ROOT}/world-of-warcraft/{path}", "w").write(
        header(path, name, file_desc or f"The {name} {cls} subclass from World of Warcraft (Andrey Kuzinskiy).") +
        "\n\n".join(["\n".join(x)] + body) + footer())
    return aid, base


def spell_table(title, cols, rows):
    """rows: list of [level, cell, cell...]"""
    h = "".join(f"<td>{escape(c)}</td>" for c in cols)
    r = "".join("<tr>" + "".join(f"<td>{escape(str(c))}</td>" for c in row) + "</tr>" for row in rows)
    return f"<h5>{escape(title)}</h5><table class=\"class-features\"><thead><tr>{h}</tr></thead>{r}</table>"


def grant_spell(name, level, cls, req=None):
    rq = f' requirements="{req}"' if req else ""
    return f'<grant type="Spell" id="{spell_id_any(name)}" level="{level}" spellcasting="{cls}"{rq} />'


OUR_SPELLS = set()


def spell_id_any(name):
    n = name.rstrip("*")
    if n in OUR_SPELLS:
        return f"ID_KAYA_WOW_SPELL_{slug(n)}"
    return "ID_WOTC_PHB24_SPELL_" + slug(n)
