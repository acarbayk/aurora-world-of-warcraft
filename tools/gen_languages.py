import sys
sys.path.insert(0, "/home/claude/tools")
from common import header, footer, SOURCE, idp
from textfmt import escape

A, H, R = "WoW Alliance Language", "WoW Horde Language", "WoW Rare Language"
# name, speakers, tags, requirement (core duplicate to hide), note
LANGS = [
    ("Common Sign Language", "Humans", [A], "ID_WOTC_PHB24_LANGUAGE_COMMON_SIGN", ""),
    ("Darnassian", "Night elves", [A], "", ""),
    ("Draconic", "Dragons", [A, H], "ID_LANGUAGE_DRACONIC||ID_WOTC_PHB24_LANGUAGE_DRACONIC", ""),
    ("Draenei", "Draenei", [A], "", ""),
    ("Dwarven", "Dwarves", [A], "ID_LANGUAGE_DWARVISH", ""),
    ("Gnomish", "Gnomes", [A], "ID_LANGUAGE_GNOMISH", ""),
    ("Hara’ni", "Haranir", [A, H], "", ""),
    ("Pandaren", "Pandaren", [A, H], "", ""),
    ("Thalassian", "High elves", [A, H], "", ""),
    ("Orcish Sign Language", "Orcs", [H], "", ""),
    ("Goblin", "Goblins", [H], "ID_LANGUAGE_GOBLIN", ""),
    ("Forsaken", "Forsaken", [H], "", ""),
    ("Shalassian", "Nightborne", [H], "", ""),
    ("Taur-ahe", "Tauren", [H], "", ""),
    ("Vulpera", "Vulpera", [H], "", ""),
    ("Zandali", "Trolls", [H], "", ""),
    ("Cyphers of the First Ones", "First Ones", [R], "", "Fragments of language left by the First Ones, the enigmatic architects of the entire cosmos. They are akin to mathematics and largely incomprehensible to mortals."),
    ("Eredun", "Demons of the Burning Legion", [R], "", ""),
    ("Furbolg", "Furbolgs", [R], "", ""),
    ("Kalimag", "Elementals", [R], "", "Kalimag, the language of elementals, is equivalent to Primordial."),
    ("Nathrezim", "Nathrezim", [R], "", ""),
    ("Nazja", "Naga", [R], "", ""),
    ("Nerglish", "Murlocs", [R], "", ""),
    ("Nerubian", "Nerubians", [R], "", ""),
    ("Ogre", "Ogres", [R], "", ""),
    ("Qiraji", "Qiraji", [R], "", ""),
    ("Shath’Yar", "Old Gods", [R], "", "Shath’Yar, the language of the Old Gods, is equivalent to Deep Speech."),
    ("Titan", "Titans", [R], "", ""),
    ("Vrykul", "Vrykul", [R], "", ""),
]
out = []
for name, speakers, tags, req, note in LANGS:
    x = [f'\t<element name="{escape(name)}" type="Language" source="{SOURCE}" id="{idp("LANGUAGE", name)}">']
    if req:
        x.append(f"\t\t<requirements>!({req})</requirements>")
    x.append(f"\t\t<supports>{', '.join(tags)}</supports>")
    desc = note or f"Typically spoken by {speakers[0].lower() + speakers[1:] if speakers[0].isupper() and not speakers.startswith(('Draenei','Pandaren','Forsaken','Vulpera','Haranir','Nightborne','Tauren','Nathrezim','Qiraji','Titans','Vrykul','Ogres','Naga','Murlocs','Nerubians','Furbolgs','First','Demons','Old','Elementals','Gnomes','Goblins','Dwarves','Dragons','Orcs','Humans','Trolls')) else speakers}."
    x.append(f"\t\t<description>\n\t\t\t<p>{escape(desc)}</p>\n\t\t</description>")
    x.append("\t\t<setters>")
    x.append(f'\t\t\t<set name="speakers">{escape(speakers)}</set>')
    x.append(f'\t\t\t<set name="{"exotic" if R in tags else "standard"}">true</set>')
    x.append("\t\t</setters>\n\t</element>")
    out.append("\n".join(x))
open(sys.argv[1], "w").write(header("misc/wow-languages.xml", "Languages",
    "Languages of Azeroth from World of Warcraft (Andrey Kuzinskiy). Common and Orcish use the core Common and Orc languages.")
    + "\n\n".join(out) + footer())
print(len(out))
