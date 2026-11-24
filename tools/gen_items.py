"""Magic items, mounts, vehicles and companion creatures."""
import sys, json, re
sys.path.insert(0, "/home/claude/tools")
from textfmt import paragraphs, escape, slug
from sublib import html
from common import header, footer, SOURCE, PREFIX, ROOT

items = json.load(open("/home/claude/wow/items.json"))
NAME_FIX = {"Panther)": "Figurine of Wondrous Power (Jeweled Panther)"}
FIXES = [
    ("THOMAS TENERY, MATT GASER ", ""), (" Crown of the Ogre King", ""), ("Doomhammer Magic Weapon.  ", "\nMagic Weapon. "),
    (" Figurine of Wondrous Power (Jeweled", ""), ("AHearthstone", "A Hearthstone"),
    ("Sulfuras, Hand of Ragnaros Boiling Point.", "\nBoiling Point."), ("starts ots turn", "starts its turn"),
    ("As Anathema, the staff grants the   form following benefits:", "As Anathema, the staff grants the following benefits:"),
    ("Anathema.  As Anathema", "Anathema. As Anathema"), ("Sulfuras  is", "Sulfuras is"),
    ("Destroying the Helm of Domination.  ", "Destroying the Helm of Domination. "),
]
TABLES = {
    "Helm of Domination": ("Spell        Charge Cost", ["Spell", "Charge Cost"], [["Animate Dead", "1"], ["Clairvoyance", "2"], ["Dream", "4"], ["Speak with Dead", "1"], ["Telepathy", "5"], ["Word of Recall", "5"]]),
    "Potion of Mana": ("Potion        Level Rarity", ["Potion", "Level", "Rarity"], [["Potion of Mana", "1", "Common"], ["Potion of Mana (greater)", "1–3", "Uncommon"], ["Potion of Mana (superior)", "1–5", "Rare"]]),
    "Potion of Rejuvenation": ("Potion      Regained", ["Potion", "Regained", "Rarity"], [["Potion of Rejuvenation", "3d4 + 3 HP, slot level 1", "Uncommon"], ["Potion of Rejuvenation (greater)", "6d4 + 6 HP, slot level 1–3", "Rare"], ["Potion of Rejuvenation (superior)", "9d4 + 9 HP, slot level 1–5", "Very Rare"]]),
    "Troll’s Blood Elixir": ("Potion       HP Rarity", ["Potion", "HP", "Rarity"], [["Troll’s Blood Elixir", "2", "Uncommon"], ["Troll’s Blood Elixir (greater)", "4", "Rare"], ["Troll’s Blood Elixir (superior)", "6", "Very Rare"], ["Troll’s Blood Elixir (supreme)", "8", "Legendary"]]),
}
COST = {"Common": 50, "Uncommon": 400, "Rare": 4000, "Very Rare": 40000, "Legendary": 200000}


def table(cols, rows):
    h = "".join(f"<td>{escape(c)}</td>" for c in cols)
    return "<table><thead><tr>" + h + "</tr></thead>" + "".join("<tr>" + "".join(f"<td>{escape(c)}</td>" for c in r) + "</tr>" for r in rows) + "</table>"


def clean_paras(name, paras):
    text = "\n\n".join(paras)
    for a, b in FIXES:
        text = text.replace(a, b)
    text = re.sub(r"(propert(?:y|ies)) (Destroying [^.]+\.)", r"\1\n\n\2", text)
    ps = [p.strip() for p in re.split(r"\n+", text) if p.strip()]
    # merge hanging-indent continuation lines (previous paragraph not finished)
    out = []
    for p in ps:
        if out and not re.search(r"[.:!?”)]$", out[-1]) and not re.match(r"^\d+ (minor|major)", out[-1]) \
                and not re.match(r"^(Random Properties|Destroying [^.]+)\. ", p):
            out[-1] += ("" if out[-1].endswith("-") and not out[-1].endswith(" -") else " ") + p
        else:
            out.append(p)
    out = [o.replace("starts ots turn", "starts its turn") for o in out]
    # random property lines -> list
    res, buf = [], []
    for p in out:
        if re.match(r"^\d+ (minor|major) (beneficial|detrimental) propert", p):
            buf.append(p)
            continue
        if buf:
            res.append("<ul>" + "".join(f"<li>{escape(b)}</li>" for b in buf) + "</ul>")
            buf = []
        res.append(p)
    if buf:
        res.append("<ul>" + "".join(f"<li>{escape(b)}</li>" for b in buf) + "</ul>")
    if name in TABLES:
        marker, cols, rows = TABLES[name]
        for i, p in enumerate(res):
            if marker in p:
                res[i] = p.split(marker)[0].strip()
                res.insert(i + 1, table(cols, rows))
                break
    return res


els = []
for it in items:
    name = NAME_FIX.get(it["name"], it["name"])
    m = re.match(r"^(?P<kind>[A-Za-z ]+?)(?: \((?P<base>[^)]*)\))?, (?P<rarity>Common|Uncommon|Rare|Very Rare|Legendary|Artifact|Rarity Varies)(?: \((?P<att>Requires Attunement[^)]*)\))?", it["header"])
    kind, base, rarity, att = m.group("kind"), m.group("base"), m.group("rarity"), m.group("att")
    paras = clean_paras(name, paragraphs(it["body"]))
    x = [f'\t<element name="{escape(name)}" type="Magic Item" source="{SOURCE}" id="{PREFIX}_MAGIC_ITEM_{slug(name)}">',
         "\t\t<description>", f'\t\t\t<p class="flavor">{escape(it["header"])}</p>']
    x += ["\t\t\t" + h for h in html(paras)]
    x += ["\t\t</description>", "\t\t<setters>"]
    if kind == "Weapon":
        x += ['\t\t\t<set name="category">Magic Weapons</set>', f'\t\t\t<set name="type" addition="{base}">Weapon</set>', f'\t\t\t<set name="weapon">{base}</set>']
        enh = re.search(r"You gain a \+(\d) bonus to attack rolls and damage rolls", " ".join(paras))
        if enh:
            x.append(f'\t\t\t<set name="enhancement">{enh.group(1)}</set>')
    elif kind == "Armor":
        x += ['\t\t\t<set name="category">Magic Armor</set>', f'\t\t\t<set name="type" addition="{base}">Armor</set>', f'\t\t\t<set name="armor">{base}</set>', '\t\t\t<set name="slot">body</set>']
    elif kind == "Staff":
        x += ['\t\t\t<set name="category">Magic Weapons</set>', '\t\t\t<set name="type" addition="Staff">Weapon</set>', '\t\t\t<set name="weapon">Quarterstaff</set>']
    else:
        cat = {"Wondrous Item": "Wondrous Items", "Potion": "Potions", "Ring": "Rings", "Rod": "Rods"}[kind]
        x += [f'\t\t\t<set name="category">{cat}</set>', f'\t\t\t<set name="type">{kind}</set>']
        if kind == "Potion":
            x.append('\t\t\t<set name="stackable">true</set>')
        if kind == "Ring":
            x.append('\t\t\t<set name="slot">misc</set>')
    x.append(f'\t\t\t<set name="rarity">{rarity}</set>')
    if att:
        extra = att.replace("Requires Attunement", "").strip()
        a = f' addition="{escape(extra)}"' if extra else ""
        x.append(f'\t\t\t<set name="attunement"{a}>true</set>')
    if rarity in COST:
        x.append(f'\t\t\t<set name="cost" currency="gp">{COST[rarity]}</set>')
    ch = re.search(r"has (\d+) charges", " ".join(paras))
    if ch:
        x.append(f'\t\t\t<set name="charges">{ch.group(1)}</set>')
    x += ["\t\t</setters>", "\t</element>"]
    els.append("\n".join(x))

path = "items/wow-magic-items.xml"
open(f"{ROOT}/world-of-warcraft/{path}", "w").write(header(path, "Magic Items", "Magic items from World of Warcraft (Andrey Kuzinskiy).") + "\n\n".join(els) + footer())

# ---------------------------------------------------------------- mounts & vehicles
mounts = [("Camel", "None", "450 lb.", 50, None), ("Dire Wolf", "Renown 10+ with Orgrimmar", "510 lb.", 750, "Dire Wolf"),
          ("Draft Horse", "None", "540 lb.", 50, None), ("Elekk", "Renown 10+ with the Exodar", "510 lb.", 400, "Giant Goat"),
          ("Giant Goat", "Renown 10+ with Ironforge", "510 lb.", 400, "Giant Goat"), ("Giant Hyena", "Renown 10+ with Steamwheedle Cartel", "480 lb.", 750, "Giant Hyena"),
          ("Giant Seahorse", "None", "450 lb.", 1000, "Giant Seahorse"), ("Gryphon", "Renown 25+ with the Alliance", "540 lb.", 2000, "Griffon"),
          ("Hawkstrider", "Renown 10+ with Silvermoon City", "420 lb.", 150, "Axe Beak"), ("Kodo", "Renown 10+ with Thunder Bluff", "450 lb.", 100, "Giant Lizard"),
          ("Mechanostrider", "Renown 10+ with Gnomeregan", "420 lb.", 450, "Mechanostrider (see the Mechanostrider companion)"),
          ("Nightsaber", "Renown 10+ with Darnassus", "510 lb.", 750, "Tiger"),
          ("Pandarian Dragon Turtle", "Renown 10+ with the Huojin or the Tushui", "480 lb.", 500, "Pandarian Dragon Turtle (see the Pandarian Dragon Turtle companion)"),
          ("Raptor", "Renown 10+ with the Darkspear Tribe", "570 lb.", 1000, "Allosaurus"), ("Riding Horse", "None", "480 lb.", 75, None),
          ("Talbuk", "None", "480 lb.", 150, "Elk"), ("Warhorse", "Renown 10+ with Stormwind", "540 lb.", 400, None),
          ("Warhorse Skeleton", "Renown 10+ with Undercity", "540 lb.", 500, "Warhorse Skeleton"), ("Wind Rider", "Renown 25+ with the Horde", "450 lb.", 2000, "Giant Bat"),
          ("Zhevra", "None", "480 lb.", 200, "Elk")]
mels = []
for n, pre, cap, cost, block in mounts:
    nm = n if n in ("Mechanostrider", "Pandarian Dragon Turtle", "Elekk", "Gryphon", "Hawkstrider", "Kodo", "Nightsaber", "Raptor", "Talbuk", "Wind Rider", "Zhevra", "Dire Wolf", "Giant Hyena", "Giant Goat", "Giant Seahorse", "Warhorse Skeleton") else f"{n} (Azeroth)"
    lines = ['<p style="margin-bottom:5px"><i>Mount</i></p>',
             f"<p><strong>Prerequisite:</strong> {escape(pre)}</p>",
             f"<p><strong>Carrying Capacity:</strong> {escape(cap)}</p>"]
    if block:
        lines.append(f"<p><strong>Stat Block:</strong> {escape(block)}</p>")
    lines.append("<p>Many of these mounts can’t be purchased unless a character has achieved a certain level of renown with a particular faction (see chapter 4). They follow the mount rules in the Player’s Handbook.</p>")
    mels.append("\n".join([f'\t<element name="{escape(nm)}" type="Item" source="{SOURCE}" id="{PREFIX}_ITEM_MOUNT_{slug(n)}">', "\t\t<description>"] +
                          ["\t\t\t" + l for l in lines] + ["\t\t</description>", "\t\t<setters>",
                           '\t\t\t<set name="category">Mounts &amp; Vehicles</set>', f'\t\t\t<set name="cost" currency="gp">{cost}</set>',
                           '\t\t\t<set name="weight" lb="0">—</set>', '\t\t\t<set name="type">Mount</set>', "\t\t</setters>", "\t</element>"]))
vehicles = [("Flying Machine", "None (must be made with expert engineering; 2,000 GP of resources)", "4 mph", 1, 0, "300 lb.", 19, 27, None,
             "A small gyrocopter with a rotor on top, two side-mounted engines, and skis as landing gear."),
            ("Goblin Trike", "Renown 10+ with any goblin cartel", "3 mph", 1, 0, "600 lb.", 19, 27, 400, "A three-wheeled motor vehicle with luxurious wood paneling."),
            ("Mechano-Hog", "Renown 10+ with the Horde", "4 mph", 1, 1, "800 lb.", 19, 27, 4000, "A powerful motorcycle with an optional sidecar, made by the Horde."),
            ("Mekgineer’s Chopper", "Renown 10+ with the Alliance", "4 mph", 1, 1, "800 lb.", 19, 27, 4000, "A powerful motorcycle with an optional sidecar, made by the Alliance.")]
for n, pre, spd, crew, pas, cargo, ac, hp, cost, d in vehicles:
    lines = ['<p style="margin-bottom:5px"><i>Powered Vehicle</i></p>', f"<p>{escape(d)}</p>",
             f"<p><strong>Prerequisite:</strong> {escape(pre)}</p>",
             f"<p><strong>Speed</strong> {spd}; <strong>Crew</strong> {crew}; <strong>Passengers</strong> {pas}; <strong>Cargo</strong> {cargo}; <strong>AC</strong> {ac}; <strong>HP</strong> {hp}</p>",
             "<p>Characters traveling in these vehicles use the vehicle’s speed in miles per hour to determine their rate of travel, and they don’t choose a travel pace. These vehicles require Fuel, which weighs 10 pounds and costs 1 GP for each 8 hours of travel. (Characters can use the alchemy profession to craft Fuel.)</p>"]
    mels.append("\n".join([f'\t<element name="{escape(n)}" type="Item" source="{SOURCE}" id="{PREFIX}_ITEM_VEHICLE_{slug(n)}">', "\t\t<description>"] +
                          ["\t\t\t" + l for l in lines] + ["\t\t</description>", "\t\t<setters>",
                           '\t\t\t<set name="category">Mounts &amp; Vehicles</set>'] +
                          ([f'\t\t\t<set name="cost" currency="gp">{cost}</set>'] if cost else []) +
                          ['\t\t\t<set name="weight" lb="0">—</set>', '\t\t\t<set name="type">Vehicle</set>', "\t\t</setters>", "\t</element>"]))
mels.append(f'''	<element name="Fuel" type="Item" source="{SOURCE}" id="{PREFIX}_ITEM_FUEL">
		<description>
			<p>Powered vehicles require Fuel, which weighs 10 pounds and costs 1 GP for each 8 hours of travel. Characters can use the alchemy profession to craft Fuel.</p>
		</description>
		<setters>
			<set name="category">Adventuring Gear</set>
			<set name="type">Adventuring Gear</set>
			<set name="cost" currency="gp">1</set>
			<set name="weight" lb="10">10 lb.</set>
			<set name="stackable">true</set>
		</setters>
	</element>''')
path = "items/wow-mounts-vehicles.xml"
open(f"{ROOT}/world-of-warcraft/{path}", "w").write(header(path, "Mounts and Vehicles", "Mounts and powered vehicles from World of Warcraft (Andrey Kuzinskiy).") + "\n\n".join(mels) + footer())

# ---------------------------------------------------------------- companion creatures
comp_intro = ("Companion creatures are magically bound to a character. Summoning or dismissing a companion requires the Magic action, and a character can have only one companion summoned at a time. "
              "A companion creature can’t take actions and can’t be targeted by attacks; if it takes any damage, it is instantly dismissed or deactivated. "
              "When a character acquires a companion, its Loyalty Score equals the character’s Charisma modifier (minimum of 1) and can’t be higher than the character’s Charisma. "
              "It increases by 1d4 if the companion is treated particularly well, and decreases by 1 if it is dismissed or deactivated by taking damage. "
              "If a companion’s Loyalty Score reaches 10 or higher, it gives the character a small supernatural gift while present.")
comps = [("Aquatic", "fish, crabs, frogs, octopi, water birds, turtles, otters, and other water-dwelling creatures. Sometimes they float in a bubble of water near their owners.", "Blessing of the Aquatic Companion, which gives you a Swim Speed equal to your Speed."),
         ("Beast", "natural animals that neither fly nor swim, including Tiny and Small beasts, as well as the young of larger creatures. (These beasts don’t age while kept as a companion.)", "Blessing of the Beast Companion, which gives you proficiency and Expertise in Animal Handling and Survival."),
         ("Dragonkin", "dragon whelplings—younger and smaller than the whelps described in chapter 7—as well as draconic animals native to the Dragon Isles.", "Blessing of the Dragonkin Companion, which gives you Advantage on saving throws to avoid or end the Frightened condition."),
         ("Elemental", "animate plants and remnants of the Old Gods’ power as well as living motes of elemental energy.", "Blessing of the Elemental Companion, which gives you Advantage on saving throws to avoid or end the Exhaustion condition."),
         ("Flying", "flying creatures—ordinary birds, bats, moths, bumblebees, and flying snakes—and magical versions of these creatures.", "Blessing of the Flying Companion, which increases your Speed by 5 feet."),
         ("Humanoid", "imps, kobolds, baby murlocs, and a range of other beings that can help you in ways that don’t involve combat.", "Blessing of the Humanoid Companion, which gives you proficiency and Expertise in the Persuasion skill."),
         ("Magic", "a variety of beings that are fundamentally magical, including tiny fragments of Old Gods or other powers, stray eyes or tentacles of otherworldly origin, oozes, creatures of the Void, ghostly spirits, and animated magical tomes.", "Blessing of the Magic Companion, which gives you proficiency and Expertise in the Arcana skill."),
         ("Mechanical", "clockwork or otherwise engineered creatures, ranging from mechanical chickens to diminutive replicas of the Burning Legion’s terrifying fel reaver constructs.", "Blessing of the Mechanical Companion, which allows you to roll 1d4 whenever you take Psychic damage and reduce the damage taken by the number rolled."),
         ("Undead", "skeletal or ghostly animals and similar creatures.", "Blessing of the Undead Companion, which gives you Advantage on Death Saving Throws.")]
cels = []
for n, d, b in comps:
    cels.append(f'''	<element name="Companion Creature ({n})" type="Item" source="{SOURCE}" id="{PREFIX}_ITEM_COMPANION_CREATURE_{slug(n)}">
		<description>
			<p>{n} companion creatures include {escape(d)}</p>
			<p class="indent"><strong><em>Loyalty Gift.</em></strong> While you have a {n.lower()} companion whose Loyalty Score is 10 or higher, you have the {escape(b)}</p>
			<p class="indent">{escape(comp_intro)}</p>
		</description>
		<setters>
			<set name="category">Companion Creatures</set>
			<set name="type">Companion Creature</set>
			<set name="weight" lb="0">—</set>
		</setters>
	</element>''')
path = "items/wow-companion-creatures.xml"
open(f"{ROOT}/world-of-warcraft/{path}", "w").write(header(path, "Companion Creatures", "Companion creature types from World of Warcraft (Andrey Kuzinskiy).") + "\n\n".join(cels) + footer())
print(len(els), "magic items,", len(mels), "mounts/vehicles,", len(cels), "companion creatures")
