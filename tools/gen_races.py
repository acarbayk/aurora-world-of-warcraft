"""Generate all World of Warcraft species (except Vulpera, hand-written)."""
import sys
sys.path.insert(0, "/home/claude/tools")
from racelib import *

DV = lambda r: ['<grant type="Vision" id="ID_VISION_DARKVISION" />',
                f'<stat name="darkvision:range" value="{r}" bonus="base" />']
RES = lambda t: f'<grant type="Condition" id="ID_INTERNAL_CONDITION_DAMAGE_RESISTANCE_{t.upper()}" />'
SKILL = lambda s: f'<grant type="Proficiency" id="ID_PROFICIENCY_SKILL_{s.upper()}" />'
MED = '<grant type="Size" id="ID_SIZE_MEDIUM" />'
SMALL = '<grant type="Size" id="ID_SIZE_SMALL" />'
SPD = '<stat name="innate speed" value="30" bonus="base" />'
GT = lambda tid: f'<grant type="Racial Trait" id="{tid}" />'
SIZE_CHOICE = lambda n: f'<select type="Racial Trait" name="Size ({n})" supports="ID_INTERNAL_RACIAL_TRAIT_SMALL|ID_INTERNAL_RACIAL_TRAIT_MEDIUM" />'
PHB = "ID_WOTC_PHB24_RACIAL_TRAIT_"
LINEAGE_RULE = "Intelligence, Wisdom, or Charisma is your spellcasting ability for the spells you cast with this trait (choose the ability when you select the lineage)."


def tr(race_slug, name):
    return f"{PREFIX}_RACIAL_TRAIT_{race_slug}_{slug(name)}"


def simple(race, slug_, spec):
    """spec: list of (name, text, kwargs). Returns (traits, grant rules, desc)."""
    traits, rules, desc = [], [], []
    for name, text, kw in spec:
        t = Trait(name, [text] if isinstance(text, str) else text, **kw)
        traits.append(t)
        rules.append(GT(tr(slug_, name)))
        desc.append(P(" ".join([text] if isinstance(text, str) else text), label=name))
    return traits, rules, desc


# ---------------------------------------------------------------- Dracthyr
S = "DRACTHYR"
dr_lore = lore_from([71, 72], "Dracthyr", "^The Adamant Vigil")
dr_lore[-1] = dr_lore[-1].rstrip(":") + "."
dr_lore += [
    "The Adamant Vigil, intended as scouts and spies for the black dragonflight, were destroyed as they awakened from their stasis by the Primalists who freed Raszageth. Only their leader, Scalecommander Emberthal, survived, and she remains in the Forbidden Reach searching for slumbering dracthyr creches.",
    "The Dark Talons, trained to be an elite force of destruction feared by enemies of the black dragonflight, left the Dragon Isles and warned the Horde of the danger posed by Raszageth. They later allied with the Horde.",
    "The Ebon Scales, honed as a destructive force, rebelled against the dragons. The weyrn’s leader, Scalecommander Sarkareth, tried to reconstruct the Oathbinder and subjugate all dracthyr once more. After Sarkareth’s death, Scalecommander Emberthal took up the work of reawakening more creches of slumbering dracthyr.",
    "The Healing Wings, trained in the healing arts to give hope to the allies of the dragonflights, remained in the Dragon Isles.",
    "The Obsidian Warders, charged with defending the allies of the black dragonflight and protecting its strongholds, journeyed to Stormwind City to warn the Alliance and subsequently joined forces with that faction."]
traits, rules, desc = simple("Dracthyr", S, [
    ("Darkvision", "You have Darkvision with a range of 60 feet.", dict(sheet=False)),
    ("Gliding Wings", "While you’re in your natural form and don’t have the Incapacitated condition, when you fall, you subtract up to 100 feet from the distance fallen when calculating the fall’s damage, and you can move up to 2 feet horizontally for every 1 foot you descend.", {}),
    ("Natural Weaponry", "While you’re in your natural form, your wings and tail are powerful weapons. As a Bonus Action, you can use your wings or tail to make an Unarmed Strike to Shove a creature.", dict(action="Bonus Action")),
    ("Visage", "As a Magic action, you can shape-shift into a humanoid form called your visage, or back to your natural form. Your visage has a specific appearance that you choose when you select this species, including your coloration, height and weight, hair length, and sex. Changing shape with this trait doesn’t change your clothing, equipment, or game statistics.", dict(action="Magic Action")),
])
traits[0].rules = []  # darkvision handled on race
rules = [r for r in rules if "DARKVISION" not in r]
flight = Trait("Draconic Flight", ["When you reach character level 5, you can use your natural form’s wings to fly short distances. As a Bonus Action, you leap into the air and give yourself a Fly Speed equal to your Speed that lasts for 10 minutes. Once you use this trait, you can’t use it again until you finish a Long Rest."],
               sheet="As a Bonus Action, you gain a Fly Speed equal to your Speed for 10 minutes.", action="Bonus Action", usage="1/Long Rest")
traits.append(flight)
desc.append(P(flight.text[0], label="Draconic Flight"))
race_xml("wow-race-dracthyr.xml", "Dracthyr", S, dr_lore,
         ["Choose one of the following weyrns to align yourself with: the Dark Talons, the Ebon Scales, the Healing Wings, or the Obsidian Warders. If you choose the Dark Talons (Horde) or the Obsidian Warders (Alliance), your Renown Score with the chosen faction begins at 3. If you choose a different weyrn, your Renown Score with the Valdrakken Accord begins at 3."],
         ("Dragon", "Medium (about 7 feet tall)", "30 feet"),
         [P("As a Dracthyr, you have these special traits.", indent=False)] + desc,
         [MED, SPD] + DV(60) + rules + [f'<grant type="Racial Trait" id="{tr(S, "Draconic Flight")}" level="5" />'],
         traits[1:])

# ---------------------------------------------------------------- Draenei
S = "DRAENEI"
TAG = "WoW Eredar Lineage"
lin = []
for name, res, cantrip, l3, l5, txt in [
        ("Draenei", "Necrotic", "Spare the Dying", "Healing Word", "Prayer of Healing", "You have Resistance to Necrotic damage. You also know the Spare the Dying cantrip."),
        ("Krokul", "Poison", "Poison Spray", "Ray of Sickness", "Hold Person", "You have Resistance to Poison damage. You also know the Poison Spray cantrip."),
        ("Lightforged", "Radiant", "Sacred Flame", "Guiding Bolt", "Aid", "You have Resistance to Radiant damage. You also know the Sacred Flame cantrip."),
        ("Man’ari", "Fire", "Fire Bolt", "Hellish Rebuke", "Darkness", "You have Resistance to Fire damage. You also know the Fire Bolt cantrip.")]:
    lin += spell_lineage(S, "Eredar Lineage", name, txt + f" At character level 3 you learn {l3}, and at level 5 you learn {l5}.", [RES(res)],
                         cantrip, l3, l5, TAG, f"You have Resistance to {res} damage and know the {cantrip} cantrip.")
table = ('<table><thead><tr><td>Lineage</td><td class="col-50">Level 1</td><td>Level 3</td><td>Level 5</td></tr></thead>'
         '<tr><td>Draenei</td><td>You have Resistance to Necrotic damage. You also know the <i>Spare the Dying</i> cantrip.</td><td><i>Healing Word</i></td><td><i>Prayer of Healing</i></td></tr>'
         '<tr><td>Krokul</td><td>You have Resistance to Poison damage. You also know the <i>Poison Spray</i> cantrip.</td><td><i>Ray of Sickness</i></td><td><i>Hold Person</i></td></tr>'
         '<tr><td>Lightforged</td><td>You have Resistance to Radiant damage. You also know the <i>Sacred Flame</i> cantrip.</td><td><i>Guiding Bolt</i></td><td><i>Aid</i></td></tr>'
         '<tr><td>Man’ari</td><td>You have Resistance to Fire damage. You also know the <i>Fire Bolt</i> cantrip.</td><td><i>Hellish Rebuke</i></td><td><i>Darkness</i></td></tr></table>')
el_text = ["You are part of a lineage related to your ancestors’ embrace of the Light—or of the power of the Burning Legion. This lineage grants you supernatural abilities. Choose a lineage from the Eredar Lineages table: Draenei, Krokul, Lightforged, or Man’ari. You gain the level 1 benefit of that lineage.",
           "When you reach character levels 3 and 5, you learn a higher-level spell, as shown on the table. You always have that spell prepared. You can cast it once without a spell slot, and you regain the ability to cast it in that way when you finish a Long Rest. You can also cast it using any spell slots you have of the appropriate level.",
           LINEAGE_RULE]
eredar = Trait("Eredar Lineage", el_text, sheet=False, extra_desc=["<h5>Eredar Lineages</h5>", table],
               rules=[f'<select type="Racial Trait" name="Eredar Lineage" supports="{TAG}" />'])
heroic = Trait("Heroic Presence", ["When you cast a spell granted by your Eredar Lineage, if you don’t have Heroic Inspiration, you gain it. You can gain Heroic Inspiration in this way once, and you regain the ability to do so when you finish a Short or Long Rest."],
               usage="1/Short Rest")
race_xml("wow-race-draenei.xml", "Draenei", S, lore_from(73, "Draenei", "Krokul") + [
            "Krokul. The draenei known as Krokul (which means “Broken” in the Draenei language) are remnants of the original eredar who were neither preserved by the naaru, as the draenei were, nor transformed into demons, as the man’ari eredar were, but were corrupted by fel energies.",
            "Lightforged Draenei. The draenei most committed to the crusade against the Burning Legion underwent a ritual to become Lightforged, infusing their bodies with the essence of the Holy Light. Their eyes turned golden, and their bodies were marked with glowing golden tattoos.",
            "Man’ari Eredar. The man’ari eredar are those who followed Kil’jaeden and Archimonde and joined the Burning Legion, becoming demons. A group of these eredar, called the Penitents, now cooperate with their draenei kin in service to the Alliance."],
         ["If you choose the draenei or Lightforged draenei Eredar Lineage, your Renown Score with the Exodar (Alliance) begins at 3. Otherwise, you have no starting Renown Score."],
         ("Humanoid", "Medium (over 7 feet tall)", "30 feet"),
         [P("As a Draenei, you have these special traits.", indent=False), P("You have Darkvision with a range of 60 feet.", label="Darkvision"),
          P(" ".join(el_text), label="Eredar Lineage"), table, P(heroic.text[0], label="Heroic Presence")],
         [MED, SPD] + DV(60) + [GT(tr(S, "Eredar Lineage")), GT(tr(S, "Heroic Presence"))],
         [eredar, heroic] + lin)

# ---------------------------------------------------------------- PHB-based species
def phb_based(fname, name, S, lore, renown, phb_text, rules, traits=(), extra_desc=()):
    race_xml(fname, name, S, lore, renown, None,
             [P(phb_text, indent=False)] + list(extra_desc), rules, list(traits))


phb_based("wow-race-dwarf.xml", "Dwarf (Azeroth)", "DWARF",
          lore_from(75, "Dwarf", "Bronzebeard Dwarves") + [
              "Bronzebeard Dwarves. The Bronzebeard clan was the largest of Ironforge’s three factions and formed the bulk of its military and mercantile classes. Ironforge is now governed by the Council of Three Hammers, with representatives of all three clans.",
              "Dark Iron Dwarves. The Dark Iron clan inhabited the deepest and darkest corners of Ironforge. Enslaved for centuries by Ragnaros the Firelord, they rejoined Ironforge under Queen-Regent Moira Thaurissan and are now proud members of the Alliance.",
              "Frostborn. The Frostborn dwarves of Northrend descend directly from a different group of earthen who succumbed to the curse of flesh, and consider themselves friendly cousins of the other clans.",
              "Wildhammer Dwarves. The Wildhammers settled in the mountains of the Hinterlands, crafting the city of Aerie Peak, where they learned to train gryphons for use in war and travel."],
          ["Your Renown Score with Ironforge (Alliance) begins at 3."],
          "You have the Dwarf species traits from the Player’s Handbook: Darkvision (120 feet), Dwarven Resilience, Dwarven Toughness, and Stonecunning.",
          ['<grant type="Grants" id="ID_INTERNAL_GRANT_RACE_DWARF" />', MED, SPD,
           '<grant type="Vision" id="ID_VISION_DARKVISION" />', '<stat name="darkvision:range" value="120" bonus="base" />',
           GT(PHB + "DWARF_DWARVEN_RESILIENCE"), GT(PHB + "DWARF_DWARVEN_TOUGHNESS"), GT(PHB + "DWARF_STONECUNNING")])

phb_based("wow-race-orc.xml", "Orc (Azeroth)", "ORC",
          lore_from([87, 88], "Orc", "Mag’har Orcs") + [
              "Mag’har Orcs. A few orcs were never tainted by fel magic, remaining uncorrupted—in Orcish, “mag’har.” Retaining their original brown or gray skin, they also preserve the shamanistic traditions the orcs cherished before the Burning Legion’s intervention."],
          ["Your Renown Score with Orgrimmar (Horde) begins at 3."],
          "You have the Orc species traits from the Player’s Handbook: Adrenaline Rush, Darkvision (120 feet), and Relentless Endurance.",
          ['<grant type="Grants" id="ID_INTERNAL_GRANT_RACE_ORC" />', MED, SPD,
           '<grant type="Vision" id="ID_VISION_DARKVISION" />', '<stat name="darkvision:range" value="120" bonus="base" />',
           GT(PHB + "ORC_ADRENALINE_RUSH"), GT(PHB + "ORC_RELENTLESS_ENDURANCE")])

phb_based("wow-race-gnome.xml", "Gnome (Azeroth)", "GNOME",
          lore_from(81, "Gnome", "Mechagnome"),
          ["Your Renown Score with Gnomeregan (Alliance) begins at 3."],
          "You have the Gnome species traits from the Player’s Handbook, with the Rock Gnome lineage: Darkvision (60 feet), Gnomish Cunning, and Gnomish Lineage (Rock Gnome). If you are a Mechagnome, choose the Mechagnome species instead.",
          ['<grant type="Grants" id="ID_INTERNAL_GRANT_RACE_GNOME" />', SMALL, SPD,
           '<grant type="Vision" id="ID_VISION_DARKVISION" />', '<stat name="darkvision:range" value="60" bonus="base" />',
           GT(PHB + "GNOME_GNOMISH_CUNNING"), GT(PHB + "GNOME_GNOMISH_LINEAGE_ROCK_GNOME")])

human_lore = lore_from(85, "Human", "Stormwind")
phb_based("wow-race-human.xml", "Human (Azeroth)", "HUMAN", human_lore,
          ["Your starting Renown Score with Stormwind (Alliance) begins at 3, but if you hail from the Arathi Empire, you have no starting Renown Score."],
          "You have the Human species traits from the Player’s Handbook: Resourceful, Skillful, and Versatile. You also have access to Origin feats that reflect your national background: Arathi Heritage, Child of the Sea, and Will to Survive. Humans from Dalaran often choose Magic Initiate (Wizard) as their Origin feat.",
          ['<grant type="Grants" id="ID_INTERNAL_GRANT_RACE_HUMAN" />', SIZE_CHOICE("Human (Azeroth)"), SPD,
           GT(PHB + "HUMAN_RESOURCEFUL"), GT(PHB + "HUMAN_SKILLFUL"), GT(PHB + "HUMAN_VERSATILE")])

# ---------------------------------------------------------------- Elf
S = "ELF"
TAG = "WoW Azeroth Elven Lineage"
ELF_REQ = "!ID_INTERNAL_PHB24_RACIAL_TRAIT_REPLACEMENT_ELF_DARKVISION"
elin = []
elin += spell_lineage(S, "Elven Lineage", "Blood Elf",
    "You know the Prestidigitation cantrip. Whenever you finish a Long Rest, you can replace that cantrip with a different cantrip from the Wizard spell list. At character level 3 you learn Detect Magic, and at level 5 you learn Arcane Vigor.",
    [], "Prestidigitation", "Detect Magic", "Arcane Vigor", TAG,
    "You know a Wizard cantrip (Prestidigitation by default); you can replace it with another Wizard cantrip when you finish a Long Rest.",
    cantrip_select='<select type="Spell" name="Wizard Cantrip (Blood Elf)" supports="Wizard,0" default="ID_WOTC_PHB24_SPELL_PRESTIDIGITATION" />')
elin += spell_lineage(S, "Elven Lineage", "High Elf",
    "You know the Prestidigitation cantrip. Whenever you finish a Long Rest, you can replace that cantrip with a different cantrip from the Wizard spell list. At character level 3 you learn Detect Magic, and at level 5 you learn Misty Step. (This is the High Elf option from the Player’s Handbook.)",
    [], "Prestidigitation", "Detect Magic", "Misty Step", TAG,
    "You know a Wizard cantrip (Prestidigitation by default); you can replace it with another Wizard cantrip when you finish a Long Rest.",
    cantrip_select='<select type="Spell" name="Wizard Cantrip (High Elf)" supports="Wizard,0" default="ID_WOTC_PHB24_SPELL_PRESTIDIGITATION" />')
elin += spell_lineage(S, "Elven Lineage", "Night Elf",
    "You have proficiency in the Stealth skill, and while you are in Dim Light or Darkness, you can take the Hide action as a Bonus Action. At character level 3 you learn Longstrider, and at level 5 you learn Pass Without Trace.",
    [SKILL("Stealth")], None, "Longstrider", "Pass Without Trace", TAG,
    "While you are in Dim Light or Darkness, you can take the Hide action as a Bonus Action.")
elin += spell_lineage(S, "Elven Lineage", "Nightborne",
    "The range of your Darkvision increases to 120 feet. You also know the Arcane Pulse cantrip. At character level 3 you learn Faerie Fire, and at level 5 you learn Darkness.",
    ['<stat name="darkvision:range" value="120" bonus="base" />'], "Arcane Pulse", "Faerie Fire", "Darkness", TAG,
    "You know the Arcane Pulse cantrip.")
elin += spell_lineage(S, "Elven Lineage", "Void Elf",
    "The range of your Darkvision increases to 120 feet. You also know the Mind Sliver cantrip. At character level 3 you learn Entropic Embrace, and at level 5 you learn Misty Step.",
    ['<stat name="darkvision:range" value="120" bonus="base" />'], "Mind Sliver", "Entropic Embrace", "Misty Step", TAG,
    "You know the Mind Sliver cantrip.")
etable = ('<table><thead><tr><td>Lineage</td><td class="col-50">Level 1</td><td>Level 3</td><td>Level 5</td></tr></thead>'
          '<tr><td>Blood Elf</td><td>You know the <i>Prestidigitation</i> cantrip. Whenever you finish a Long Rest, you can replace that cantrip with a different cantrip from the Wizard spell list.</td><td><i>Detect Magic</i></td><td><i>Arcane Vigor</i></td></tr>'
          '<tr><td>Night Elf</td><td>You have proficiency in the Stealth skill, and while you are in Dim Light or Darkness, you can take the Hide action as a Bonus Action.</td><td><i>Longstrider</i></td><td><i>Pass Without Trace</i></td></tr>'
          '<tr><td>Nightborne</td><td>The range of your Darkvision increases to 120 feet. You also know the <i>Arcane Pulse</i> cantrip.</td><td><i>Faerie Fire</i></td><td><i>Darkness</i></td></tr>'
          '<tr><td>Void Elf</td><td>The range of your Darkvision increases to 120 feet. You also know the <i>Mind Sliver</i> cantrip.</td><td><i>Entropic Embrace</i></td><td><i>Misty Step</i></td></tr></table>')
elv_text = ["You are part of a lineage that grants you supernatural abilities. Choose one of the Elven Lineage options from the Azeroth Elven Lineages table or the High Elf option from the Player’s Handbook. You gain the level 1 benefit of that lineage.",
            "When you reach character levels 3 and 5, you learn a higher-level spell, as shown on the table. You always have that spell prepared. You can cast it once without a spell slot, and you regain the ability to cast it in that way when you finish a Long Rest. You can also cast it using any spell slots you have of the appropriate level.",
            LINEAGE_RULE]
elven = Trait("Elven Lineage", elv_text, sheet=False, extra_desc=["<h5>Azeroth Elven Lineages</h5>", etable],
              rules=[f'<select type="Racial Trait" name="Elven Lineage (Azeroth)" supports="{TAG}" />'])
elf_lore = lore_from(77, "Elf", "Night Elves (Kaldorei)", drop=("divided",))
elf_lore += [
    "Night Elves (Kaldorei). Forswearing the use of arcane magic, the night elves (or kaldorei, which means “children of the stars” in their own language, Darnassian) cultivated a druidic society in the shadowed recesses of Ashenvale Forest. Night elves average between 7 and 8 feet in height, with skin from pale lilac to dark violet and eyes that glow white, blue, or gold.",
    "Nightborne (Shal’dorei). Isolated for ten thousand years in Suramar and transformed by the energy of the Nightwell, the nightborne joined the ranks of the Horde after a rebellion toppled their corrupt leaders. They resemble night elves, though their skin is darker and grayer.",
    "High Elves (Quel’dorei). Descendants of the Highborne who founded Quel’Thalas around the Sunwell, the high elves who refused to adopt the blood elves’ parasitic techniques now live among the peoples of the Alliance with no nation of their own. Their eyes glow blue.",
    "Blood Elves (Sin’dorei). Most survivors of Quel’Thalas took on the name “blood elves” to honor their fallen kindred and joined the Horde. They resemble high elves, but their eyes glow green or gold.",
    "Void Elves (Ren’dorei). Exiled from Silvermoon for studying the Void and trained by Alleria Windrunner to control the shadows within themselves, the void elves pledged their support to the Alliance. Their eyes glow violet, and their hair is varying shades of purple and blue."]
race_xml("wow-race-elf.xml", "Elf (Azeroth)", S, elf_lore,
         ["Your starting Renown Score depends on your elven origin:",
          "Blood Elf or Nightborne. Your Renown Score with Silvermoon City (Horde) begins at 3.",
          "High Elf. You have no starting Renown Score.",
          "Night Elf or Void Elf. Your Renown Score with Darnassus (Alliance) begins at 3."],
         None,
         [P("You have the Elf species traits from the Player’s Handbook: Darkvision (60 feet), Fey Ancestry, Keen Senses, and Trance. Instead of the Player’s Handbook Elven Lineage options, choose one of the lineages below or the High Elf option. The general rules for Elven Lineage apply in any case.", indent=False),
          P(" ".join(elv_text), label="Elven Lineage"), etable],
         ['<grant type="Grants" id="ID_INTERNAL_GRANT_RACE_ELF" />', MED, SPD,
          '<grant type="Vision" id="ID_VISION_DARKVISION" />', '<stat name="darkvision:range" value="60" bonus="base" />',
          GT(tr(S, "Elven Lineage")), GT(PHB + "ELF_FEY_ANCESTRY"), GT(PHB + "ELF_KEEN_SENSES"), GT(PHB + "ELF_TRANCE")],
         [elven] + elin)

# ---------------------------------------------------------------- Earthen
S = "EARTHEN"
traits, rules, desc = simple("Earthen", S, [
    ("Azerite Surge", ["When you take the Attack action on your turn, you can replace one of the attacks with a blast of Azerite energy in a 15-foot Cone. Each creature of your choice in the Cone regains 1d10 Hit Points. Each other creature in the Cone makes a Dexterity saving throw (DC 8 plus your Constitution modifier and your Proficiency Bonus), taking 1d10 Radiant damage on a failed save or half as much damage on a successful one.",
                       "Both the damage and the healing increase by 1d10 when you reach character levels 5 (2d10), 11 (3d10), and 17 (4d10).",
                       "You can use this ability a number of times equal to your Proficiency Bonus, and you regain all expended uses when you finish a Long Rest."],
     dict(usage="{{proficiency}}/Long Rest",
          sheet=[(None, "Replace one attack with a 15-ft Cone: chosen creatures regain 1d10 HP; others make a DC {{azerite surge:dc}} Dex save or take 1d10 Radiant (half on success)."),
                 (5, "Replace one attack with a 15-ft Cone: chosen creatures regain 2d10 HP; others make a DC {{azerite surge:dc}} Dex save or take 2d10 Radiant (half on success)."),
                 (11, "Replace one attack with a 15-ft Cone: chosen creatures regain 3d10 HP; others make a DC {{azerite surge:dc}} Dex save or take 3d10 Radiant (half on success)."),
                 (17, "Replace one attack with a 15-ft Cone: chosen creatures regain 4d10 HP; others make a DC {{azerite surge:dc}} Dex save or take 4d10 Radiant (half on success).")],
          rules=['<stat name="azerite surge:dc" value="8" />', '<stat name="azerite surge:dc" value="constitution:modifier" />', '<stat name="azerite surge:dc" value="proficiency" />'])),
    ("Earthen Resilience", "You have Resistance to Poison damage. You also have Advantage on saving throws you make to avoid or end the Poisoned condition.",
     dict(sheet="You have Advantage on saving throws you make to avoid or end the Poisoned condition.", rules=[RES("Poison")])),
    ("Ingest Minerals", "You don’t gain Exhaustion levels from malnutrition.", {}),
    ("Quiet Contemplation", "When you spend Hit Point Dice when you finish a Short Rest, you regain 1 additional Hit Point per Hit Point Die you spend.", {}),
])
race_xml("wow-race-earthen.xml", "Earthen", S, lore_from(76, "Earthen", "Earthen Renown", drop=("SWATCHES STUDIO",)),
         ["You have no starting Renown Score."], ("Humanoid", "Medium (about 4–5 feet tall)", "30 feet"),
         [P("As an Earthen, you have these special traits.", indent=False), P("You have Darkvision with a range of 120 feet.", label="Darkvision")] + desc,
         [MED, SPD] + DV(120) + rules, traits)

# ---------------------------------------------------------------- Forsaken
S = "FORSAKEN"
traits, rules, desc = simple("Forsaken", S, [
    ("Deathly Endurance", "You have Resistance to Necrotic damage.", dict(sheet=False, rules=[RES("Necrotic")])),
    ("Everlasting", "You don’t gain Exhaustion levels from dehydration, malnutrition, or suffocation. You don’t need to sleep, and magic can’t put you to sleep. You can finish a Long Rest in 4 hours if you spend those hours in an inactive, motionless state, during which you retain consciousness.", {}),
    ("Touch of the Grave", ["When you deal damage to a creature, you can roll a number of d4s equal to your Proficiency Bonus. You deal extra Necrotic damage to the creature equal to the total rolled, and you regain a number of Hit Points equal to the extra damage dealt.",
                            "Once you use this benefit, you can’t use it again until you finish a Long Rest."],
     dict(usage="1/Long Rest", sheet="When you deal damage to a creature, deal an extra {{proficiency}}d4 Necrotic damage and regain Hit Points equal to that extra damage.")),
    ("Will of the Forsaken", "You have Advantage on saving throws to avoid or end the Charmed or Frightened condition.", {}),
])
race_xml("wow-race-forsaken.xml", "Forsaken", S,
         lore_from([79, 80], "Forsaken", "Forsaken Renown", drop=("For many of the Forsaken,", "life continues much as it did", "before their transformation.")),
         ["Your Renown Score with Undercity (Horde) begins at 3."],
         ("Undead", "Medium (about 4–7 feet tall) or Small (about 2–4 feet tall), chosen when you select this species", "30 feet"),
         [P("As a Forsaken, you have these special traits.", indent=False), P("You have Darkvision with a range of 60 feet.", label="Darkvision")] + desc,
         [SIZE_CHOICE("Forsaken"), SPD] + DV(60) + rules, traits)

# ---------------------------------------------------------------- Mechagnome
S = "MECHAGNOME"
traits, rules, desc = simple("Mechagnome", S, [
    ("Built for Success", "You can add 1d4 to one D20 Test you make, and you can do so after rolling the die but before resolving the effects of the roll. You can use this trait a number of times equal to your Proficiency Bonus, and you regain all expended uses when you finish a Long Rest.",
     dict(usage="{{proficiency}}/Long Rest", sheet="Add 1d4 to one D20 Test you make, after rolling but before resolving the roll.")),
    ("Emergency Fail-Safe", "When you become Bloodied, you can take a Reaction to spend one Hit Point Die, roll it, and regain a number of Hit Points equal to the roll plus your Constitution modifier (minimum of 1 Hit Point). Once you use this trait, you can’t use it again until you finish a Short or Long Rest.",
     dict(usage="1/Short Rest", action="Reaction", sheet="When you become Bloodied, spend one Hit Point Die and regain HP equal to the roll + {{constitution:modifier}} (minimum 1).")),
    ("Mechanical Nature", "You have Resistance to Poison damage, and you have Advantage on saving throws to avoid or end the Paralyzed or Poisoned condition. You don’t gain Exhaustion levels from dehydration, malnutrition, or suffocation.",
     dict(rules=[RES("Poison")], sheet="You have Advantage on saving throws to avoid or end the Paralyzed or Poisoned condition. You don’t gain Exhaustion levels from dehydration, malnutrition, or suffocation.")),
    ("Sentry’s Rest", "You don’t need to sleep. You can finish a Long Rest in 6 hours if you spend those hours in an inactive, motionless state, during which you retain consciousness.", {}),
    ("Specialized Design", "You gain proficiency with two tools of your choice.",
     dict(sheet=False, rules=['<select type="Proficiency" name="Tool Proficiency (Specialized Design)" supports="Tool" number="2" />'])),
])
race_xml("wow-race-mechagnome.xml", "Mechagnome", S,
         ["Many mechagnomes eluded the curse of flesh and remained mechanical. However, a new group of mechagnomes descends from gnomes who settled Mechagon Island in hopes of discovering useful titan technology. These gnomes performed extensive experiments to reverse the curse of flesh and become living machines. After facing the perils of full mechanization, they found the ideal balance between flesh and steel. Now reunited with their gnome cousins, these new mechagnomes bring both tenacity and ingenuity to the Alliance."],
         ["Your Renown Score with Gnomeregan (Alliance) begins at 3."],
         ("Construct", "Small (about 4 feet tall)", "30 feet"),
         [P("As a Mechagnome, you have these special traits.", indent=False)] + desc,
         ['<grant type="Grants" id="ID_INTERNAL_GRANT_RACE_GNOME" />', SMALL, SPD] + rules, traits)

# ---------------------------------------------------------------- Goblin
S = "GOBLIN"
traits, rules, desc = simple("Goblin", S, [
    ("Fey Ancestry", "You have Advantage on saving throws you make to avoid or end the Charmed condition.", {}),
    ("Fury of the Small", ["When you damage a creature with an attack or a spell and the creature’s size is larger than yours, you can cause the attack or spell to deal extra damage to the creature. The extra damage equals your Proficiency Bonus and is the same damage type as the other damage dealt.",
                           "You can use this trait a number of times equal to your Proficiency Bonus, regaining all expended uses when you finish a Long Rest, and you can use it no more than once per turn."],
     dict(usage="{{proficiency}}/Long Rest", sheet="When you damage a creature larger than you with an attack or spell, deal {{proficiency}} extra damage of the same type (once per turn).")),
    ("Nimble Escape", "You can take the Disengage or Hide action as a Bonus Action on each of your turns.", dict(action="Bonus Action")),
])
race_xml("wow-race-goblin.xml", "Goblin (Azeroth)", S,
         lore_from([82, 83], "Goblin", "Goblin Cartels") + [
             "Goblin Cartels. Besides the Bilgewater Cartel, three other cartels remain a significant mercantile force across Azeroth: the Blackwater Cartel, which runs the town of Booty Bay in Stranglethorn; the Steamwheedle Cartel, which remains carefully neutral and oversees operations from its capital, Gadgetzan in Tanaris; and the Venture Company, notorious for plundering natural resources across Azeroth without regard to the consequences.",
             "Though many believed all of Kezan was destroyed in the Cataclysm, the sprawling subterranean city of Undermine survived the volcanic eruption and still serves as the goblins’ capital."],
         ["Choose a cartel: Bilgewater Cartel, Blackwater Cartel, Steamwheedle Cartel, or Venture Company. If you are associated with the Bilgewater Cartel (Horde) or the Steamwheedle Cartel, your Renown Score with that faction begins at 3. Otherwise, you have no starting Renown Score."],
         ("Humanoid", "Small (about 4 feet tall)", "30 feet"),
         [P("As a Goblin, you have these special traits.", indent=False), P("You have Darkvision with a range of 60 feet.", label="Darkvision")] + desc,
         [SMALL, SPD] + DV(60) + rules, traits)

# ---------------------------------------------------------------- Haranir
S = "HARANIR"
hm_ids = [f"{tr(S, 'Haranir Magic')}_{a.upper()}" for a in ABIL]
hm_text = ["You know the Druidcraft and Thorn Whip cantrips.",
           "When you reach character level 3, you learn the Entangle spell. You always have it prepared. You can cast it once without a spell slot, and you regain the ability to cast it in that way when you finish a Long Rest. You can also cast the spell using any spell slots you have of the appropriate level.",
           "When you reach character level 5, you also always have the Spike Growth spell prepared and can cast it the same way.",
           "Intelligence, Wisdom, or Charisma is your spellcasting ability for the spells you cast with this trait (choose the ability when you select this species)."]
hm = Trait("Haranir Magic", hm_text, sheet=False,
           rules=[f'<select type="Racial Trait" name="Spellcasting Ability (Haranir Magic)" supports="{"|".join(hm_ids)}" />'])
hm_abil = []
for a, aid in zip(ABIL, hm_ids):
    t = Trait(a, [f"{a} is your spellcasting ability for the spells you cast with the Haranir Magic trait."], tid=aid, compendium=False,
              sheet=[(None, f"You know the Druidcraft and Thorn Whip cantrips. {a} is your spellcasting ability for this trait."),
                     (3, f"You know the Druidcraft and Thorn Whip cantrips, and you can cast Entangle once per Long Rest without a spell slot. {a} is your spellcasting ability for this trait."),
                     (5, f"You know the Druidcraft and Thorn Whip cantrips, and you can cast Entangle and Spike Growth once each per Long Rest without a spell slot. {a} is your spellcasting ability for this trait.")],
              rules=[f'<grant type="Spell" id="{spell_id("Druidcraft")}" />', f'<grant type="Spell" id="{spell_id("Thorn Whip")}" />',
                     f'<grant type="Spell" id="{spell_id("Entangle")}" level="3" />', f'<grant type="Spell" id="{spell_id("Spike Growth")}" level="5" />'])
    t.alt = "Haranir Magic"
    hm_abil.append(t)
gift = Trait("Gift of the World Trees", ["Because of your supernatural connection to the world trees, you have proficiency in the Nature and Survival skills."],
             sheet=False, rules=[SKILL("Nature"), SKILL("Survival")])
race_xml("wow-race-haranir.xml", "Haranir", S, lore_from(84, "Haranir", "Haranir Renown"),
         ["You have no starting Renown Score."], ("Humanoid", "Medium (about 7–8 feet tall)", "30 feet"),
         [P("As a Haranir, you have these special traits.", indent=False), P("You have Darkvision with a range of 120 feet.", label="Darkvision"),
          P(gift.text[0], label="Gift of the World Trees"), P(" ".join(hm_text), label="Haranir Magic")],
         [MED, SPD] + DV(120) + [GT(tr(S, "Gift of the World Trees")), GT(tr(S, "Haranir Magic"))],
         [gift, hm] + hm_abil)

# ---------------------------------------------------------------- Pandaren
S = "PANDAREN"
traits, rules, desc = simple("Pandaren", S, [
    ("Bouncy", "You have Resistance to Bludgeoning damage from falling.", {}),
    ("Inner Peace", "When you spend Hit Point Dice to regain Hit Points after a Short Rest, you regain 1 additional Hit Point per Hit Point Die you expend.", {}),
    ("Quaking Palm", "When you hit a creature with a melee attack on your turn, your movement doesn’t provoke Opportunity Attacks from that creature until the end of your turn.", {}),
])
race_xml("wow-race-pandaren.xml", "Pandaren", S,
         lore_from([88, 89], "Pandaren", "Pandaren Philosophies") + [
             "Pandaren Philosophies. When the mists that shrouded Pandaria vanished, the two philosophical sects of the Wandering Isle each aligned with one of the two global factions. The path of Huojin teaches direct action: injustice must be met with a swift and decisive response, and inaction is often worse than wrong action. Led by Ji Firepaw, the Huojin were drawn to the practical nature of the Horde.",
             "The path of Tushui, by contrast, emphasizes meditation and careful discernment in the context of constant training, meditation, and moral conviction. Its followers believe that living a principled life is the greatest good, a philosophy that attracted the Tushui—and their leader, Aysa Cloudsinger—to the cause of the Alliance."],
         ["Choose whether to align with the Huojin (Horde) or the Tushui (Alliance) philosophy. Your Renown Score with the chosen faction begins at 3."],
         ("Humanoid", "Medium (about 6–7 feet tall)", "30 feet"),
         [P("As a Pandaren, you have these special traits.", indent=False), P(traits[0].text[0], label="Bouncy"),
          P("You have Darkvision with a range of 60 feet.", label="Darkvision")] + desc[1:],
         [MED, SPD] + DV(60) + rules, traits)

# ---------------------------------------------------------------- Tauren
S = "TAUREN"
TAG = "WoW Tauren Lineage"
tl_text = ["You are part of a lineage that grants you supernatural qualities. If your lineage grants you an ability that allows a saving throw, the DC equals 8 plus your Strength, Constitution, or Wisdom modifier (choose when you select the lineage) and Proficiency Bonus. Choose one of the following options:"]
mul = Trait("Mulgore Tauren", ["When you take the Attack action on your turn, you can replace one of the attacks with a magically empowered stomp on the ground. You can’t use this feature if you have the Prone condition or if you are flying, climbing, or swimming. When you use your war stomp, each creature of your choice within a 5-foot Emanation originating from you makes a Constitution saving throw. On a failed save, a creature has the Stunned condition until the end of your current turn."],
            supports=TAG, sheet="War Stomp: replace one attack with a stomp; each chosen creature within 5 feet makes a Constitution save (DC 8 + Str, Con, or Wis modifier + {{proficiency}}) or is Stunned until the end of your turn.")
high = Trait("Highmountain Tauren", ["As an action, you can move up to your Speed without provoking Opportunity Attacks and can move through the spaces of other creatures. Each Medium or smaller creature whose space you enter makes a Strength saving throw. On a failed save, a creature takes Bludgeoning damage equal to your Proficiency Bonus plus your Strength modifier and has the Prone condition. A creature can take this damage only once per turn."],
             supports=TAG, action="Action", sheet="Move up to your Speed without provoking Opportunity Attacks, through other creatures’ spaces. Each Medium or smaller creature you enter makes a Strength save (DC 8 + Str, Con, or Wis modifier + {{proficiency}}) or takes {{proficiency}} + Str modifier Bludgeoning damage and is knocked Prone.")
tau = Trait("Taunka", ["Your shaggy hide gives you a +1 bonus to Armor Class and Resistance to Cold damage."], supports=TAG, sheet=False,
            rules=['<stat name="ac:misc" value="1" />', RES("Cold")])
for t in (mul, high, tau):
    t.compendium = False
tlin = Trait("Tauren Lineage", tl_text, sheet=False, rules=[f'<select type="Racial Trait" name="Tauren Lineage" supports="{TAG}" />'],
             extra_desc=[P(t.text[0], label=t.name) for t in (mul, high, tau)])
traits, rules, desc = simple("Tauren", S, [
    ("Horns", "Your horns are powerful natural weapons. When you hit with your Unarmed Strike and deal damage, you can deal Piercing damage equal to 1d6 plus your Strength modifier instead of the normal damage of an Unarmed Strike.", {}),
    ("Goring Rush", "Immediately after you take the Dash action on your turn and move at least 20 feet, you can make one Unarmed Strike as a Bonus Action.", dict(action="Bonus Action")),
    ("Hammering Horns", "Immediately after you hit a creature with a melee attack as part of the Attack action on your turn, you can use a Bonus Action to shove that target with an Unarmed Strike as long as the target is within 5 feet of you. When you shove a target in this way, you can push the target up to 10 feet away instead of 5 feet.", dict(action="Bonus Action")),
])
race_xml("wow-race-tauren.xml", "Tauren", S,
         lore_from([89, 90], "Tauren", "Highmountain Tauren") + [
             "Highmountain Tauren. The tauren of the Broken Isles are direct descendants of the tauren (led by Huln Highmountain) who fought alongside the night elves in the War of the Ancients. Cenarius blessed Huln and his followers with the Horns of Eche’ro, which manifest as antlers like those of a moose.",
             "Taunka. Taunka are the direct descendants of the ancient yaungol. Before the Great Sundering, they settled in the Storm Peaks (in what would become Northrend) and adapted to the harsh environment. In contrast to the peaceful shamanism of the Mulgore tauren, taunka shaman wrest power from the hostile elemental forces of Northrend."],
         ["Your Renown Score with Thunder Bluff (Horde) begins at 3."],
         ("Humanoid", "Medium (about 8–9 feet tall)", "30 feet"),
         [P("As a Tauren, you have these special traits.", indent=False)] + desc + [P(tl_text[0], label="Tauren Lineage")] + [P(t.text[0], label=t.name) for t in (mul, high, tau)],
         [MED, SPD] + rules + [GT(tr(S, "Tauren Lineage"))], traits + [tlin, mul, high, tau])

# ---------------------------------------------------------------- Troll
S = "TROLL"
TAG = "WoW Troll Lineage"
am = Trait("Amani Troll", ["Whenever you spend Heroic Inspiration, you regain 1 expended Hit Point Die."], supports=TAG)
ds = Trait("Darkspear Troll", ["When you take the Dash action, Difficult Terrain composed of ice, rubble, snow, or undergrowth doesn’t cost you extra movement until the end of your turn."], supports=TAG)
za = Trait("Zandalari Troll", ["If you roll a 1 on the d20 for a D20 Test, you gain Heroic Inspiration at the end of the current turn."], supports=TAG)
for t in (am, ds, za):
    t.compendium = False
trl = Trait("Troll Lineage", ["You are part of a lineage that grants you supernatural qualities. Choose one of the following options:"], sheet=False,
            rules=[f'<select type="Racial Trait" name="Troll Lineage" supports="{TAG}" />'], extra_desc=[P(t.text[0], label=t.name) for t in (am, ds, za)])
traits, rules, desc = simple("Troll", S, [
    ("Bloodied Frenzy", "While Bloodied, you have Advantage on attack rolls.", {}),
    ("Troll Healing", "When you expend Hit Point Dice to regain Hit Points after a Short Rest, you regain Hit Points equal to the maximum roll of the dice plus your Constitution modifier.", {}),
])
race_xml("wow-race-troll.xml", "Troll", S,
         lore_from([90, 91], "Troll", "Darkspear Trolls") + [
             "Darkspear Trolls. The first trolls to join the Horde were jungle trolls of the Darkspear tribe, driven out of Stranglethorn in fierce conflicts with other tribes of the Gurubashi Empire. When Thrall led the liberated orcs to Kalimdor, he offered the Darkspear tribe a place in the Horde’s new domain, and they settled on the Echo Isles, just off the coast of Durotar.",
             "Zandalari Trolls. Originally established by the first troll tribe, from which all other troll tribes descend, the ancient Zandalari Empire is steeped in ritual and spirituality. Its warriors ride mighty dinosaurs into battle. Under Queen Talanji’s rule, the Zandalari Empire has joined the Horde.",
             "Amani Trolls. The forest trolls of Zul’Aman, after centuries of war with the elves of Quel’Thalas, recently forged an uneasy alliance with the blood elves against common enemies serving the Void. These trolls remain suspicious of outsiders, but some have ventured out to learn more of the world."],
         ["If you choose the Darkspear troll or Zandalari troll Troll Lineage, your Renown Score with the Darkspear Tribe (Horde) begins at 3. Otherwise, you have no starting Renown Score."],
         ("Humanoid", "Medium (about 7 feet tall)", "30 feet"),
         [P("As a Troll, you have these special traits.", indent=False), desc[0], P("You have Darkvision with a range of 60 feet.", label="Darkvision"), desc[1],
          P(trl.text[0], label="Troll Lineage")] + [P(t.text[0], label=t.name) for t in (am, ds, za)],
         [MED, SPD] + DV(60) + rules + [GT(tr(S, "Troll Lineage"))], traits + [trl, am, ds, za])

# ---------------------------------------------------------------- Worgen
S = "WORGEN"
dark = ["As a Bonus Action, you can shape-shift to assume a more bestial appearance. This transformation lasts for 1 minute or until you revert to your normal appearance as a Bonus Action. When you enter your bestial form, you gain Temporary Hit Points equal to 2 times your Proficiency Bonus. You can enter this form a number of times equal to your Proficiency Bonus, and you regain all expended uses when you finish a Long Rest.",
        "In your bestial form, you gain the following benefits:"]
dark_ex = [P("Your Speed increases by 10 feet.", label="Increased Speed"),
           P("You can take a Reaction to move up to 10 feet when a creature ends its turn within 5 feet of you. This reactive movement doesn’t provoke Opportunity Attacks.", label="Reactive Movement"),
           P("You have Resistance to Necrotic damage.", label="Necrotic Resistance")]
darkflight = Trait("Darkflight", dark, extra_desc=dark_ex, action="Bonus Action", usage="{{proficiency}}/Long Rest",
                   sheet="Shape-shift into bestial form for 1 minute, gaining {{proficiency}}×2 Temporary Hit Points. While in this form: Speed +10 feet; you can take a Reaction to move up to 10 feet (without provoking Opportunity Attacks) when a creature ends its turn within 5 feet of you; and you have Resistance to Necrotic damage.")
inst = Trait("Instinctual Shift", ["When you roll Initiative while you have one or more uses of your Darkflight species trait remaining, you can immediately use that trait to shape-shift (no action required)."])
race_xml("wow-race-worgen.xml", "Worgen", S, lore_from(94, "Worgen", "Worgen Renown", drop=("CAIO MONTEIRO",)),
         ["Your Renown Score with Gilneas (Alliance) begins at 3."],
         ("Humanoid", "Medium (4–7 feet tall)", "30 feet"),
         [P("As a Worgen, you have these special traits.", indent=False), P(" ".join(dark), label="Darkflight")] + dark_ex +
         [P("You have Darkvision with a range of 60 feet.", label="Darkvision"), P(inst.text[0], label="Instinctual Shift")],
         [MED, SPD] + DV(60) + [GT(tr(S, "Darkflight")), GT(tr(S, "Instinctual Shift"))], [darkflight, inst])

print("races written")
