"""Companion stat blocks (Legion demons, mounts) and the Druid Circle Forms addition."""
import sys, re
sys.path.insert(0, "/home/claude/tools")
from textfmt import escape, slug
from common import header, footer, SOURCE, PREFIX, ROOT, ED, FP
E14 = ED == "2014"

SK = {"Athletics": "athletics", "Stealth": "stealth", "Perception": "perception"}


def comp(name, supports, size, ctype, align, ac, hp, speed, scores, skills="", resist="", immun="", cimmun="", senses="", langs="",
         cr="", pb=2, traits=(), actions=(), reactions=(), req=None, desc=None):
    cid = f"{PREFIX}_COMPANION_{slug(name)}"
    out, tids, aids, rids = [], [], [], []
    for kind, lst, ids in (("TRAIT", traits, tids), ("ACTION", actions, aids), ("REACTION", reactions, rids)):
        for n, t in lst:
            i = f"{PREFIX}_COMPANION_{kind}_{slug(name)}_{slug(n)}"
            ids.append(i)
            et = "Companion Trait" if kind == "TRAIT" else ("Companion Reaction" if kind == "REACTION" else "Companion Action")
            if kind == "REACTION":
                et = "Companion Action"
            out.append(f'''	<element name="{escape(n)}" type="{et}" source="{SOURCE}" id="{i}">
		<compendium display="false" />
		<description>
			<p>{escape(t)}</p>
		</description>
		<sheet>
			<description>{escape(t)}</description>
		</sheet>
	</element>''')
    hp_max = re.match(r"\d+", hp).group(0)
    spd = re.findall(r"(?:(Fly|Swim|Climb|Burrow) )?(\d+) ft\.", speed)
    rules = [f'<stat name="companion:ac" value="{ac}" bonus="base" />', f'<stat name="companion:hp:max" value="{hp_max}" bonus="base" />']
    for kind, v in spd:
        k = f"companion:speed:{kind.lower()}" if kind else "companion:speed"
        rules.append(f'<stat name="{k}" value="{v}" bonus="base" />')
    for s in re.findall(r"([A-Z][a-z]+) \+\d+", skills):
        if s.lower() in ("athletics", "stealth", "perception"):
            rules.append(f'<stat name="companion:{s.lower()}:proficiency" value="companion:proficiency" bonus="base" />')
    st = ["strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma"]
    x = [f'\t<element name="{escape(name)}" type="Companion" source="{SOURCE}" id="{cid}">', f"\t\t<supports>{supports}</supports>"]
    if req:
        x.append(f"\t\t<requirements>{req}</requirements>")
    if desc:
        x.append(f"\t\t<description>\n\t\t\t<p>{escape(desc)}</p>\n\t\t</description>")
    x.append("\t\t<setters>")
    for k, v in [("size", size), ("type", ctype), ("alignment", align), ("ac", str(ac)), ("hp", hp), ("speed", speed)] + list(zip(st, map(str, scores))) + \
            [("skills", skills), ("resistances", resist), ("immunities", immun), ("conditionImmunities", cimmun), ("senses", senses),
             ("languages", langs), ("challenge", cr), ("proficiency", str(pb))]:
        if v:
            x.append(f'\t\t\t<set name="{k}">{escape(v)}</set>')
    if tids:
        x.append(f'\t\t\t<set name="traits">{",".join(tids)}</set>')
    if aids:
        x.append(f'\t\t\t<set name="actions">{",".join(aids)}</set>')
    if rids:
        x.append(f'\t\t\t<set name="reactions">{",".join(rids)}</set>')
    x.append("\t\t</setters>\n\t\t<rules>")
    x += ["\t\t\t" + r for r in rules]
    x.append("\t\t</rules>\n\t</element>")
    return "\n\n".join(["\n".join(x)] + out)


DEM_RES = ("Demonic Restoration", "If the {n} dies outside the Twisting Nether, its body dissolves into ichor, and it gains a new body in 2d4 weeks, reviving with all its Hit Points somewhere in the Twisting Nether.")
CALL = f"{PREFIX}_CLASS_FEATURE_ELDRITCH_INVOCATION_CALL_OF_THE_VOID"
els = [
    comp("Fel Imp", "WoW Legion Familiar", "Tiny", "Fiend (Demon)", "Chaotic Evil", 13, "21 (6d4 + 6)", "20 ft.", [6, 17, 13, 11, 12, 14],
         skills="Stealth +5", resist="Cold", immun="Fire, Poison", cimmun="Poisoned", senses="Darkvision 120 ft.; Passive Perception 11",
         langs="Common, Eredun, Orcish", cr="1", traits=[("Magic Resistance", "The imp has Advantage on saving throws against spells and other magical effects.")],
         actions=[("Multiattack", "The imp makes two Fel Firebolt attacks."), ("Fel Firebolt", "Ranged Attack Roll: +4, range 30 ft. Hit: 7 (2d6) Fire damage.")],
         desc="Fel imps are mischievous demons that cackle with glee while immolating their foes in fel flames. They are the easiest demons for Warlocks to bind and control, making them common familiars for those who make pacts with the Burning Legion."),
    comp("Voidwalker", "WoW Legion Familiar", "Medium", "Fiend", "Neutral Evil", 16, "38 (7d8 + 7)", "40 ft.", [19, 11, 13, 8, 12, 14],
         resist="Poison", immun="Necrotic", cimmun="Exhaustion, Poisoned", senses="Darkvision 120 ft.; Passive Perception 11", langs="Common, Eredun, Orcish", cr="1",
         traits=[("Magic Resistance", "The voidwalker has Advantage on saving throws against spells and other magical effects."),
                 ("Threatening Presence", "An enemy that starts its turn within 5 feet of the voidwalker has Disadvantage on attack rolls against any creature other than a voidwalker.")],
         actions=[("Consuming Shadows", "Melee Attack Roll: +6 to hit, reach 5 ft. Hit: 6 (1d4 + 4) Necrotic damage, and the voidwalker regains 3 Hit Points.")],
         req=CALL, desc="Voidwalkers are creatures of the Void, hulking figures made of pure shadow. Warlocks highly prize ordinary voidwalkers as servants because of their ability to both attract and withstand enemy attacks."),
    comp("Felguard", "WoW Legion Summon", "Medium", "Fiend (Demon)", "Neutral Evil", 17, "60 (8d8 + 24)", "30 ft.", [16, 14, 17, 8, 10, 11],
         skills="Athletics +5", resist="Cold, Fire, Lightning", immun="Poison", cimmun="Poisoned", senses="Darkvision 60 ft.; Passive Perception 10",
         langs="Common, Eredun, Orcish", cr="4", traits=[(DEM_RES[0], DEM_RES[1].format(n="felguard")),
                                                         ("Fiendish Devotion", "The felguard has Advantage on saving throws against the Charmed and Frightened conditions."),
                                                         ("Pack Tactics", "The felguard has Advantage on an attack roll against a creature if at least one of the felguard’s allies is within 5 feet of the creature and the ally doesn’t have the Incapacitated condition.")],
         actions=[("Multiattack", "The felguard makes two attacks, using Fel Battleaxe or Fel Javelin in any combination."),
                  ("Fel Battleaxe", "Melee Attack Roll: +5 to hit, reach 5 ft. Hit: 12 (2d8 + 3) Slashing damage plus 7 (2d6) Fire damage."),
                  ("Fel Javelin", "Melee or Ranged Attack Roll: +5 to hit, reach 5 ft. or range 30/120 ft. Hit: 10 (2d6 + 3) Piercing damage plus 7 (2d6) Fire damage.")],
         desc="Conscripted from the demonic mo’arg species, felguard serve as the Burning Legion’s rank-and-file soldiers. They are fearless and unwaveringly loyal to Sargeras’s godlike will."),
    comp("Felhound", "WoW Legion Summon", "Medium", "Fiend (Demon)", "Neutral Evil", 15, "84 (13d8 + 26)", "50 ft.", [16, 17, 14, 4, 14, 8],
         skills="Perception +8", resist="Cold, Fire, Lightning", immun="Poison", cimmun="Poisoned", senses="Darkvision 60 ft.; Passive Perception 18",
         langs="Understands Eredun but can’t speak", cr="5", pb=3,
         traits=[(DEM_RES[0], DEM_RES[1].format(n="felhound")), ("Magic Resistance", "The felhound has Advantage on saving throws against spells and other magical effects."),
                 ("Smell Magic", "The felhound can sense the presence and location of magic within 120 feet of itself. It also has Advantage on attack rolls against creatures that have cast a spell or taken the Magic action since the end of the felhound’s last turn.")],
         actions=[("Multiattack", "The felhound makes one Bite attack and one Grappling Tentacles attack."),
                  ("Bite", "Melee Attack Roll: +6, reach 5 ft. Hit: 13 (3d6 + 3) Piercing damage. If the target is a Medium or smaller creature, it has the Prone condition."),
                  ("Grappling Tentacles", "Melee Attack Roll: +6, reach 5 ft. Hit: 12 (2d8 + 3) Bludgeoning damage. If the target is a Medium or smaller creature, it has the Grappled condition (escape DC 13) from both tentacles."),
                  ("Drink Magic (Bonus Action)", "Constitution Saving Throw: DC 13, one Medium or smaller creature Grappled by the felhound. Failure: 10 (3d6) Necrotic damage, and the target can’t take the Magic action until the start of the felhound’s next turn.")],
         desc="Felhounds are demonic canines used by pit lords to sniff out sources of magic. Unlike most demons, which are born of corrupted mortals, felhounds are shaped from raw fel energy."),
    comp("Mechanostrider", "WoW Mount", "Large", "Construct", "Unaligned", 13, "34 (4d10 + 12)", "60 ft.", [14, 15, 16, 2, 9, 6],
         immun="Poison", cimmun="Exhaustion, Poisoned", senses="Passive Perception 9", langs="None", cr="1/2",
         actions=[("Peck", "Melee Attack Roll: +4, reach 5 ft. Hit: 7 (2d4 + 2) Piercing damage.")],
         desc="A mechanical riding mount built by the gnomes of Gnomeregan (Renown 10+ with Gnomeregan, 450 GP)."),
    comp("Pandarian Dragon Turtle", "WoW Mount", "Large", "Beast", "Unaligned", 17, "30 (4d10 + 8)", "30 ft., Swim 60 ft.", [16, 12, 15, 2, 12, 9],
         senses="Darkvision 60 ft.; Passive Perception 11", langs="None", cr="1/2",
         traits=[("Amphibious", "The turtle can breathe air and water.")],
         actions=[("Bite", "Melee Attack Roll: +5, reach 5 ft. Hit: 7 (1d8 + 3) Piercing damage. If the target is a Large or smaller creature, it has the Grappled condition (escape DC 13).")],
         desc="A sturdy riding turtle of Pandaria (Renown 10+ with the Huojin or the Tushui, 500 GP)."),
]


def block(name, size, ac, hp, speed, skills, senses, actions, extra_title=None, extra=()):
    rows = [f"<p><em>{escape(size)}; Your Creature Type And Alignment Don’t Change. Requires Circle Forms.</em></p>",
            f"<p><strong>AC</strong> {escape(ac)}; <strong>{'Hit Points' if E14 else 'Temp HP'}</strong> {escape(hp)}; <strong>Speed</strong> {escape(speed)}</p>",
            "<p><strong>Str., Dex.</strong> Your Strength and Dexterity scores are equal to your Wisdom score. <strong>Con., Int., Wis., Cha.</strong> Your Constitution, Intelligence, Wisdom, and Charisma don’t change.</p>"]
    if skills:
        rows.append(f"<p><strong>Skills</strong> {escape(skills)}</p>")
    rows.append(f"<p><strong>Senses</strong> {escape(senses)}; <strong>Languages</strong> Your languages don’t change; <strong>CR</strong> – (Your Proficiency Bonus doesn’t change.)</p>")
    rows.append("<h6>Actions</h6>")
    rows += [f"<p><strong><em>{escape(n)}.</em></strong> {escape(t)}</p>" for n, t in actions]
    if extra_title:
        for title, lst in extra:
            rows.append(f"<h6>{title}</h6>")
            rows += [f"<p><strong><em>{escape(n)}.</em></strong> {escape(t)}</p>" for n, t in lst]
    return f"<h5>{escape(name)}</h5>" + "".join(rows)


cat = block("Cat Form", "Medium", "13 + your Wisdom modifier", "3 times your Druid level", "40 ft.", "You have proficiency in Stealth.", "Darkvision 60 ft.", [
    ("Multiattack", "You make one Pounce attack and use Prowl."),
    ("Pounce", "Melee Attack Roll: Bonus equals your spell attack modifier, reach 5 ft. Hit: 1d10 + your Wisdom modifier Slashing damage. This damage increases by 1d10 when you reach Druid levels 5 (2d10), 11 (3d10), and 17 (4d10). If you had Advantage on the attack roll, the target takes an extra 1d6 Slashing damage and, if it is Large or smaller, has the Prone condition. The extra damage increases by 1d6 when you reach Druid levels 6 (2d6), 9 (3d6), 12 (4d6), 15 (5d6), and 18 (6d6)."),
    ("Primal Wrath", "You expend a level 1+ spell slot and slash nearby enemies. Dexterity Saving Throw: DC equals your spell save DC, each creature of your choice within a 5-foot Emanation originating from you. Failure: 2d6 Slashing damage per spell slot level expended plus your Wisdom modifier."),
    ("Prowl", "You move up to half your Speed without provoking Opportunity Attacks. At the end of this movement, you can take the Hide action.")])
bear = block("Bear Form", "Large", "15 + your Wisdom modifier", "3 times your Druid level", "30 ft.", "", "Darkvision 60 ft.", [
    ("Multiattack", "You make two Mangle attacks."),
    ("Mangle", "Melee Attack Roll: Bonus equals your spell attack modifier, reach 5 ft. Hit: 1d8 + your Wisdom modifier Slashing damage. This damage increases by 1d8 when you reach Druid levels 5 (2d8), 11 (3d8), and 17 (4d8).")],
    extra_title=True, extra=[("Bonus Actions", [("Frenzied Regeneration", "You expend a level 1+ spell slot and gain Temporary Hit Points equal to five times the spell slot level.")]),
                             ("Reactions", [("Growl", "Trigger: A creature you can see attacks a target other than you that is within 5 feet of you. Response: You impose Disadvantage on the triggering attack roll and all other attack rolls against the target until the start of your next turn if you remain within 5 feet of the target.")])])
fid = f"{PREFIX}_ARCHETYPE_FEATURE_DRUID_CIRCLE_OF_THE_MOON_CLASSIC_FORMS"
forms = f'''	<element name="Level {2 if E14 else 3}: Cat Form and Bear Form" type="Archetype Feature" source="{SOURCE}" id="{fid}">
		<supports>WoW Druid Forms{' 2014' if E14 else ''}</supports>
		<description>
			<p>The beast forms that every druid in World of Warcraft learns are Cat Form, Bear Form, and Travel Form. If you have the Circle of the Moon subclass, when you use Wild Shape you can adopt the Cat Form (feral druids) or Bear Form (guardian druids) stat blocks below.</p>
			{'<p class="indent">2014 rules: when you take on one of these forms with Wild Shape, the form’s Hit Points equal 3 times your Druid level; when they drop to 0 you revert to your normal form, as with any Wild Shape form.</p>' if E14 else ''}
			<p class="indent">Without the Circle of the Moon, you can become a Panther at level 2 and a Tiger at level 8 (Cat Form), a Black Bear at level 4 and a Brown Bear at level 8 (Bear Form), and an Elk starting at level 2 (Travel Form). For fast swimming, consider a Giant Seahorse starting at level 4 (or level 3 for the Circle of the Moon). When you gain access to flying forms at level 8, you can become an Eagle, a Giant Bat, a Hawk, a Pteranodon, or a Raven.</p>
			{cat}
			{bear}
		</description>
		<sheet alt="Cat Form and Bear Form">
			<description>Wild Shape: Cat Form (Medium, AC 13 + {{{{wisdom:modifier}}}}, {'HP' if E14 else 'Temp HP'} 3 × Druid level, Speed 40 ft., Pounce + Prowl, Primal Wrath) or Bear Form (Large, AC 15 + {{{{wisdom:modifier}}}}, {'HP' if E14 else 'Temp HP'} 3 × Druid level, Speed 30 ft., two Mangle attacks, Frenzied Regeneration, Growl). Str and Dex equal your Wisdom.</description>
		</sheet>
	</element>

	<append id="{'ID_WOTC_PHB_ARCHETYPE_CIRCLEOFTHEMOON' if E14 else 'ID_WOTC_PHB24_ARCHETYPE_DRUID_CIRCLE_OF_THE_MOON'}">
		<rules>
			<select type="Archetype Feature" name="Cat Form and Bear Form (World of Warcraft, optional)" supports="WoW Druid Forms{' 2014' if E14 else ''}" level="{2 if E14 else 3}" optional="true" />
		</rules>
	</append>'''
if not E14:
  path = "companions/wow-companions.xml"
  open(f"{ROOT}/world-of-warcraft/{path}", "w").write(header(path, "Companions", "Companion stat blocks from World of Warcraft (Andrey Kuzinskiy): Legion demons and mounts.") + "\n\n".join(els) + footer())
path = f"archetypes/{FP}druid-forms.xml"
open(f"{ROOT}/world-of-warcraft/{path}", "w").write(header(path, "Druid Forms", "Cat Form and Bear Form for the Circle of the Moon from World of Warcraft (Andrey Kuzinskiy).") + forms + footer())
print("companions written")
