"""Renown perks (chapter 4) as Items in a 'Renown Perks' category."""
import sys, json, re
sys.path.insert(0, "/home/claude/tools")
from textfmt import paragraphs, escape, slug
from sublib import html
from common import header, footer, SOURCE, PREFIX, ROOT

perks = json.load(open("/home/claude/wow/perks.json"))
PRE_FIX = {
    "Alliance: Honored": ("Renown 10+ with Any Alliance Subfaction", "Subfaction "),
    "Alliance: Revered": ("Renown 25+ with Any Alliance Subfaction", "Subfaction "),
    "Ambassador of the Alliance": ("Renown 50+ with Darnassus, the Exodar, Gilneas, Gnomeregan, Ironforge, and Stormwind", "Exodar, Gilneas, Gnomeregan, Ironforge, and Stormwind "),
    "Ambassador of the Horde": ("Renown 50+ with Bilgewater Cartel, Darkspear Tribe, Orgrimmar, Silvermoon City, Thunder Bluff, and Undercity", "Darkspear Tribe, Orgrimmar, Silvermoon City, Thunder Bluff, and Undercity "),
    "Steamwheedle Cartel: Honored": ("Renown 10+ with the Steamwheedle Cartel", "Cartel "),
    "Steamwheedle Cartel: Revered": ("Renown 25+ with the Steamwheedle Cartel", "Cartel "),
    "Steamwheedle Cartel: Exalted": ("Renown 50+ with the Steamwheedle Cartel", "Cartel "),
}
CUTS = [" Alliance Subfactions", " Darnassus Renown Perks", " Exodar Renown Perks", " Gilneas Renown Perks", " Gnomeregan Renown Perks",
        " Ironforge Renown Perks", " Obsidian Warders Renown Perks", " Stormwind Renown Perks", " Tushui Renown Perks", " The Horde The proud",
        " Horde Subfactions", " Bilgewater Cartel Renown Perks", " Dark Talons Renown Perks", " Darkspear Tribe Renown Perks", " Huojin Renown Perks",
        " Orgrimmar Renown Perks", " Silvermoon City Renown Perks", " Thunder Bluff Renown Perks", " Undercity Renown Perks", " Argent Dawn The knightly",
        "Malfurion Stormrage,", " Mutually Hostile Factions", " Kirin Tor The Kirin Tor", " Steamwheedle Cartel The Steamwheedle",
        " Valdrakken Accord The Valdrakken", " Earthen Ring The Earthen Ring", " Cenarion Circle Named"]
FIX = [("aBlack Dragonflight Whelp  (see", "a Black Dragonflight Whelp (see"), ("anApparatus of Kwalish )", "an Apparatus of Kwalish)"),
       ("Steamwheedle Apparatus  (which", "Steamwheedle Apparatus (which"), ("flasks of Elixir(see", "flasks of Noggenfogger Elixir (see"),
       (" Archmage Khadgar of the Kirin Tor", ""), (" ndris Feathermoon, Anduin Wrynn, Muradin katorque, Prophet Velen, and Tess Greymane", ""),
       (" all, Monte Gazlowe, Lor’themar", "")]
OVR = {
    "Darnassus: Exalted": "You can call on a Warden (Questing Knight), a leading Sentinel (Warrior Commander) with three Sentinel scouts (Scout Captains), or a leading priestess of Elune (Archpriest) to assist you for a single adventure. Once you request this assistance, you can’t do so again until your Renown Score with Darnassus increases.",
    "Exodar: Exalted": "You can call on fifty draenei soldiers (Warrior Infantry) led by three sergeants (Warrior Veterans) and one commander (Warrior Commander) to assist you for a single adventure. Once you request this assistance, you can’t do so again until your Renown Score with the Exodar increases.",
    "Ironforge: Exalted": "You can call on fifty dwarf soldiers (Warrior Infantry) led by three sergeants (Warrior Veterans) and one commander (Warrior Commander) to assist you for a single adventure. Once you request this assistance, you can’t do so again until your Renown Score with Ironforge increases.",
    "Bilgewater Cartel: Exalted": "You can call on a cartel captain (Pirate Admiral) with six crew members (Pirates) to assist you for a single adventure. The captain has a Sailing Ship, but you need to hire additional crew (at your own expense) to use the ship. Once you request this assistance, you can’t do so again until your Renown Score with the Bilgewater Cartel increases.",
    "Darkspear Tribe: Exalted": "You can call on a shadow hunter (Cultist Hierophant) and six hexxers (Cultist Fanatics) to assist you for a single adventure. Once you request this assistance, you can’t do so again until your Renown Score with the Darkspear tribe increases.",
    "Orgrimmar: Exalted": "You can call on a warband leader (Berserker Commander), a shaman (Elemental Cultist), and three experienced warriors (Berserkers), all mounted on Dire Wolves, to assist you for a single adventure. Once you request this assistance, you can’t do so again until your Renown Score with Orgrimmar increases.",
    "Silvermoon City: Exalted": "You can call on a single Magister (Archmage) or four Mages to assist you for a single adventure. Once you request this assistance, you can’t do so again until your Renown Score with Silvermoon City increases.",
    "Stormwind: Exalted": ["You can call on Stormwind forces to assist you for a single adventure. You receive your choice of one of the following groups:",
        "<ul><li>Fifty human soldiers (Warrior Infantry) led by three sergeants (Warrior Veterans) and one commander (Warrior Commander)</li><li>Three SI:7 agents (Scout Captains) and their leader (Spy Master)</li><li>A champion of the Holy Light (Questing Knight)</li><li>A Kul Tiran admiral (Pirate Admiral) with a Warship (you must hire the ship’s crew)</li></ul>",
        "Once you request this assistance, you can’t do so again until your Renown Score with Stormwind increases."],
    "Thunder Bluff: Exalted": "You can call on a tauren shaman (Elemental Cultist) and eight assistant shaman (Berserkers) to assist you for a single adventure. Once you request this assistance, you can’t do so again until your Renown Score with Thunder Bluff increases.",
}


def clean(name, paras):
    if name in OVR:
        return OVR[name] if isinstance(OVR[name], list) else [OVR[name]]
    if name in PRE_FIX and paras[0].startswith(PRE_FIX[name][1]):
        paras[0] = paras[0][len(PRE_FIX[name][1]):]
    out = []
    for p in paras:
        if p.strip() == "Training":
            break
        cut = None
        for c in CUTS:
            if c in p and (cut is None or p.index(c) < cut):
                cut = p.index(c)
        if cut is not None:
            if p[:cut].strip():
                out.append(p[:cut].strip())
            break
        out.append(p)
    text = "\n".join(out)
    for a, b in FIX:
        text = text.replace(a, b)
    ps = text.split("\n")
    merged = []
    for p in ps:
        if merged and not re.search(r"[.:!?”)]$", merged[-1]):
            merged[-1] += " " + p
        else:
            merged.append(p)
    return merged


def item(name, pre, paras, fid):
    x = [f'\t<element name="{escape(name)}" type="Item" source="{SOURCE}" id="{fid}">', "\t\t<description>"]
    if pre:
        x.append(f'\t\t\t<p class="flavor">Prerequisite: {escape(pre)}</p>')
    x += ["\t\t\t" + h for h in html(paras)]
    x += ["\t\t</description>", "\t\t<sheet>", f"\t\t\t<description>{escape(' '.join(p for p in paras if not p.startswith('<')))}</description>", "\t\t</sheet>",
          "\t\t<setters>", '\t\t\t<set name="category">Renown Perks</set>', '\t\t\t<set name="type">Renown Perk</set>',
          '\t\t\t<set name="weight" lb="0">—</set>', "\t\t</setters>", "\t</element>"]
    return "\n".join(x)


els = [
    item("General Renown Perks", "", [
        "The perks listed here apply to all the factions of Azeroth:",
        "Friendly (Renown 3+). Other members of the faction are Friendly to you by default.",
        "Honored (Renown 10+). You can purchase equipment found in the Player’s Handbook, as well as Common or Uncommon magic items, from merchants of the faction at a 10% discount.",
        "Revered (Renown 25+). Your discount increases to 15% and extends to Rare magic items.",
        "Exalted (Renown 50+). Your discount increases to 25% and extends to Very Rare magic items.",
        "Certain mounts and magic items are available only from merchants associated with a particular faction and might require a minimum Renown Score with that faction to purchase.",
        "Starting Renown. Most characters created using the World of Warcraft species have a starting Renown Score of 3 with one of the subfactions associated with either the Alliance or the Horde. A few species and class options give starting Renown Scores with other factions."],
        f"{PREFIX}_ITEM_RENOWN_GENERAL"),
    item("Renown Training", "", [
        "Several renown perks give you the opportunity to work with a trainer to learn a language or gain a proficiency. The days required needn’t be consecutive, but you must spend 8 consecutive hours with the trainer for a day to count. You can gain only one tool proficiency from each renown perk."],
        f"{PREFIX}_ITEM_RENOWN_TRAINING"),
    item("Subfaction Renown (Alliance and Horde)", "", [
        "If your species gives you a starting Renown Score with an Alliance or Horde subfaction, gaining renown with different subfactions of the same faction also increases your Renown Score with your starting faction:",
        "Friendly. The first time your Renown Score with each other subfaction reaches 3, increase your Renown Score with your starting faction by 1.",
        "Honored. The first time your Renown Score with each other subfaction reaches 10, increase your Renown Score with your starting faction by 2.",
        "Revered. The first time your Renown Score with each other subfaction reaches 25, increase your Renown Score with your starting faction by 3.",
        "Exalted. The first time your Renown Score with each other subfaction reaches 50, increase your Renown Score with your starting faction by 5.",
        "Alliance subfactions: Darnassus (night elves), Exodar (draenei), Gilneas (worgen), Gnomeregan (gnomes), Ironforge (dwarves), Obsidian Warders (dracthyr), Stormwind (humans), Tushui (pandaren).",
        "Horde subfactions: Bilgewater Cartel (goblins), Dark Talons (dracthyr), Darkspear Tribe (trolls), Huojin (pandaren), Orgrimmar (orcs and vulpera), Silvermoon City (blood elves), Thunder Bluff (tauren), Undercity (Forsaken)."],
        f"{PREFIX}_ITEM_RENOWN_SUBFACTIONS"),
]
for p in perks:
    name = p["name"]
    pre = PRE_FIX[name][0] if name in PRE_FIX else p["header"].replace("Prerequisite: ", "")
    paras = clean(name, paragraphs(p["body"]))
    els.append(item(name, pre, paras, f"{PREFIX}_ITEM_RENOWN_{slug(name)}"))
path = "items/wow-renown-perks.xml"
open(f"{ROOT}/world-of-warcraft/{path}", "w").write(header(path, "Renown Perks", "Faction renown perks from World of Warcraft (Andrey Kuzinskiy). Add earned perks to your character from the Equipment tab (category: Renown Perks).") + "\n\n".join(els) + footer())
print(len(els), "renown items")
