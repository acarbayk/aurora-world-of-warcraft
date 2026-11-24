"""Helpers for building Aurora race XML."""
import re, sys
sys.path.insert(0, "/home/claude/tools")
from textfmt import escape, slug, paragraphs, PAGES
from common import header, footer, SOURCE, idp, PREFIX, ROOT

ABIL = ["Intelligence", "Wisdom", "Charisma"]


def P(text, indent=True, label=None):
    cls = ' class="indent"' if indent else ""
    if label:
        return f"<p{cls}><strong><em>{escape(label)}.</em></strong> {escape(text)}</p>"
    return f"<p{cls}>{escape(text)}</p>"


def spell_id(name):
    """Our spells or PHB24 spells."""
    ours = {"Arcane Pulse", "Entropic Embrace"}
    if name in ours:
        return idp("SPELL", name)
    return "ID_WOTC_PHB24_SPELL_" + slug(name)


class Trait:
    def __init__(self, name, text, sheet=None, rules=(), usage=None, action=None,
                 tid=None, extra_desc=(), compendium=True, supports=None, req=None):
        self.name, self.text = name, text          # text: list of paragraphs
        self.sheet, self.rules = sheet, list(rules)
        self.usage, self.action, self.extra = usage, action, list(extra_desc)
        self.tid, self.compendium, self.supports, self.req = tid, compendium, supports, req

    def xml(self, race_slug):
        tid = self.tid or f"{PREFIX}_RACIAL_TRAIT_{race_slug}_{slug(self.name)}"
        self.tid = tid
        x = [f'\t<element name="{escape(self.name)}" type="Racial Trait" source="{SOURCE}" id="{tid}">']
        if self.supports:
            x.append(f"\t\t<supports>{escape(self.supports)}</supports>")
        if self.req:
            x.append(f"\t\t<requirements>{self.req}</requirements>")
        if not self.compendium:
            x.append('\t\t<compendium display="false" />')
        x.append("\t\t<description>")
        for i, t in enumerate(self.text):
            x.append("\t\t\t" + P(t, indent=i > 0))
        for e in self.extra:
            x.append("\t\t\t" + e)
        x.append("\t\t</description>")
        if self.sheet is False:
            x.append('\t\t<sheet display="false" />')
        else:
            attrs = ""
            if getattr(self, "alt", None):
                attrs += f' alt="{escape(self.alt)}"'
            if self.action:
                attrs += f' action="{self.action}"'
            if self.usage:
                attrs += f' usage="{self.usage}"'
            if isinstance(self.sheet, list):
                x.append(f"\t\t<sheet{attrs}>")
                for lvl, d in self.sheet:
                    la = f' level="{lvl}"' if lvl else ""
                    x.append(f"\t\t\t<description{la}>{escape(d)}</description>")
                x.append("\t\t</sheet>")
            else:
                d = self.sheet or " ".join(self.text)
                x.append(f"\t\t<sheet{attrs}>\n\t\t\t<description>{escape(d)}</description>\n\t\t</sheet>")
        if self.rules:
            x.append("\t\t<rules>")
            x += ["\t\t\t" + r for r in self.rules]
            x.append("\t\t</rules>")
        x.append("\t</element>")
        return "\n".join(x)


def spell_lineage(race_slug, owner, opt_name, l1_text, l1_rules, cantrip, l3, l5,
                  supports_tag, l1_sheet, abilities=ABIL, cantrip_select=None):
    """Lineage option + one element per spellcasting ability (PHB24 pattern).
    Returns list of Trait objects (option first)."""
    opt_id = f"{PREFIX}_RACIAL_TRAIT_{race_slug}_LINEAGE_{slug(opt_name)}"
    abil_ids = [f"{opt_id}_{a.upper()}" for a in abilities]
    opt = Trait(opt_name, [l1_text], sheet=False, tid=opt_id, supports=supports_tag,
                compendium=False,
                rules=l1_rules + [f'<select type="Racial Trait" name="Spellcasting Ability ({escape(owner)})" supports="{"|".join(abil_ids)}" />'])
    out = [opt]
    for a, aid in zip(abilities, abil_ids):
        spells = []
        if cantrip:
            spells.append(f"the {cantrip} cantrip")
        base = l1_sheet + (" " if l1_sheet else "")
        s3 = f"{base}You can cast {l3} once per Long Rest without a spell slot, or with a spell slot. {a} is your spellcasting ability for this trait."
        s5 = f"{base}You can cast {l3} and {l5} once each per Long Rest without a spell slot, or with spell slots. {a} is your spellcasting ability for this trait."
        s1 = f"{l1_sheet} {a} is your spellcasting ability for this trait.".strip()
        r = []
        if cantrip_select:
            r.append(cantrip_select)
        elif cantrip:
            r.append(f'<grant type="Spell" id="{spell_id(cantrip)}" />')
        r.append(f'<grant type="Spell" id="{spell_id(l3)}" level="3" />')
        r.append(f'<grant type="Spell" id="{spell_id(l5)}" level="5" />')
        out.append(Trait(a, [f"{a} is your spellcasting ability for the spells you cast with the {owner} trait."],
                         tid=aid, compendium=False,
                         sheet=[(None, s1), (3, s3), (5, s5)], rules=r))
        out[-1].alt = f"{owner} ({opt_name})"
    return out


def race_xml(fname, name, race_slug, lore, renown, info, traits_desc, rules, traits,
             extra_elements=(), desc_note=None):
    """info: (creature type, size text, speed) or None if using PHB traits text."""
    rid = idp("RACE", name)
    x = [f'\t<element name="{escape(name)}" type="Race" source="{SOURCE}" id="{rid}">', "\t\t<description>"]
    for i, t in enumerate(lore):
        x.append("\t\t\t" + P(t, indent=i > 0))
    if renown:
        x.append(f"\t\t\t<h5>{escape(name.upper())} RENOWN</h5>")
        for i, t in enumerate(renown):
            x.append("\t\t\t" + P(t, indent=i > 0))
    x.append(f"\t\t\t<h5>{escape(name.upper())} TRAITS</h5>")
    if info:
        ct, size, speed = info
        x.append('\t\t\t<ul class="unstyled" style="text-indent:-1em; margin-left:1em; margin-bottom:5px">')
        x.append(f"\t\t\t\t<li><strong>Creature Type:</strong> {escape(ct)}</li>")
        x.append(f"\t\t\t\t<li><strong>Size:</strong> {escape(size)}</li>")
        x.append(f"\t\t\t\t<li><strong>Speed:</strong> {escape(speed)}</li>")
        x.append("\t\t\t</ul>")
    for t in traits_desc:
        x.append("\t\t\t" + t)
    x.append("\t\t\t<h5>LANGUAGES</h5>")
    x.append("\t\t\t" + P("You know Common (Alliance) or Orcish (Horde), plus two languages from the Alliance Languages or Horde Languages tables. At least one of Common or Orcish is recommended.", indent=False))
    if desc_note:
        x.append("\t\t\t" + desc_note)
    x.append("\t\t</description>")
    x.append('\t\t<sheet display="false" />')
    x.append("\t\t<rules>")
    base = [
        f'<select type="Ability Score Improvement" name="Ability Score Improvement Option ({escape(name)})" supports="Custom Ability Score Improvement Option" requirements="!ID_INTERNAL_GRANTS_BACKGROUND_ASI" />',
        f'<select type="Language" name="Faction Language ({escape(name)})" supports="ID_LANGUAGE_COMMON|ID_LANGUAGE_ORC" />',
        f'<select type="Language" name="Language ({escape(name)})" supports="WoW Alliance Language||WoW Horde Language" number="2" />',
    ]
    x += ["\t\t\t" + r for r in base + rules]
    x.append("\t\t</rules>")
    x.append("\t</element>")
    body = ["\n".join(x)] + [t.xml(race_slug) for t in traits] + list(extra_elements)
    path = f"races/{fname}"
    open(f"{ROOT}/world-of-warcraft/{path}", "w").write(
        header(path, name, f"The {name} species from World of Warcraft (Andrey Kuzinskiy).") +
        "\n\n".join(body) + footer())
    return rid


def trait_desc(traits_spec):
    """[(label, text)] -> description paragraphs used in the race element."""
    return [P(t, label=l) for l, t in traits_spec]


def lore_from(page, start, end, drop=()):
    """Paragraphs between a start line and end line on the column-ordered page text."""
    lines = []
    pages = page if isinstance(page, list) else [page]
    for pg in pages:
        txt = (PAGES / f"p{pg:03d}.txt").read_text().split("=====RIGHT=====")
        for ci, c in enumerate(txt):
            for l in c.split("\n"):
                if re.search(r"CHAPTER \d+ •", l):
                    continue
                lines.append([f"p{pg:03d}.txt", ci, l])
    s = next(i for i, l in enumerate(lines) if l[2].strip() == start)
    e = next(i for i, l in enumerate(lines) if i > s and (l[2].strip() == end or (end.startswith("^") and l[2].strip().startswith(end[1:]))))
    sel = [l for l in lines[s + 1:e] if l[2].strip() not in drop]
    return paragraphs(sel)
