"""Subclasses and class options for World of Warcraft."""
import sys, json
sys.path.insert(0, "/home/claude/tools")
import sublib
from sublib import *
from common import header, footer, SOURCE, PREFIX, ROOT

sublib.OUR_SPELLS.update(s["name"] for s in json.load(open("/home/claude/wow/spells.json")))
from common import ED, FP
E14 = ED == "2014"
R = lambda cls, feat: (f"ID_INTERNAL_FEATURE_REPLACEMENT_{cls}_{feat}" if E14 else f"ID_INTERNAL_PHB24_FEATURE_REPLACEMENT_{cls}_{feat}")
T14 = {"Paladin": "Sacred Oath", "Ranger": "Ranger Archetype", "Monk": "Monastic Tradition", "Cleric": "Divine Domain",
       "Rogue": "Roguish Archetype", "Barbarian": "Primal Path"}
TAG = lambda c: T14[c] if E14 else None
NOTE14 = "(2014 adaptation of a World of Warcraft 2024 subclass; see the README for how 2024 terms were converted.)"
F = Feature


def write(path, name, desc, elements):
    open(f"{ROOT}/world-of-warcraft/{path}", "w").write(spell14(header(path, name, desc) + "\n\n".join(elements) + footer()))


def option(fid, name, paras, supports, rules=(), sheet=None, usage=None, action=None, etype="Archetype Feature"):
    f = Feature(None, name, paras, sheet=sheet, rules=rules, usage=usage, action=action, etype=etype,
                fid=fid, supports=supports, compendium=False, grant=False)
    return f


# =====================================================================
# Oath of the Ebon Blade (Paladin) — Death Knight
# =====================================================================
base = f"{PREFIX}_ARCHETYPE_FEATURE_PALADIN_OATH_OF_THE_EBON_BLADE"
RUNE_TAG = "WoW Ebon Blade Rune"
rune_ids = {r: f"{base}_RUNE_{r.upper()}" for r in ("Blood", "Frost", "Unholy")}
dk_all = [(3, "Death Grip"), (5, "Death and Decay"), (9, "Summon Undead"), (13, "Freedom of Movement"), (17, "Circle of Power")]
dk_cols = {
    "Blood": [(3, "Vampiric Blood"), (5, "Spiritual Weapon"), (9, "Leeching Strike"), (13, "Evard’s Black Tentacles"), (17, "Bonestorm")],
    "Frost": [(3, "Chains of Ice"), (5, "Frostscythe"), (9, "Remorseless Winter"), (13, "Ice Storm"), (17, "Cone of Cold")],
    "Unholy": [(3, "Scourge Strike"), (5, "Ray of Enfeeblement"), (9, "Bestow Curse"), (13, "Blight"), (17, "Contagion")],
}
dk_table = spell_table("Oath of the Ebon Blade Spells", ["Paladin Level", "Spells (All)", "Spells (Blood)", "Spells (Frost)", "Spells (Unholy)"],
                       [[a[0], a[1], dk_cols["Blood"][i][1], dk_cols["Frost"][i][1], dk_cols["Unholy"][i][1]] for i, a in enumerate(dk_all)])
rune_text = {
    "Blood": "When you inscribe this rune on your weapon, and whenever you finish a Long Rest while the rune is inscribed on your weapon, you gain Temporary Hit Points equal to your Charisma modifier plus your Paladin level. While you are wielding your inscribed weapon, you gain these Temporary Hit Points whenever you reduce an enemy to 0 Hit Points.",
    "Frost": "While you are wielding your inscribed weapon, damage from your weapon attacks, Paladin spells, and Paladin features ignores Resistance to Cold damage. When you make the extra attack of the Light property and hit while wielding your inscribed weapon, you deal an extra 1d4 Cold damage.",
    "Unholy": "While you are wielding your inscribed weapon, damage from your weapon attacks, Paladin spells, and Paladin features ignores Resistance to Necrotic damage. If your inscribed weapon has the Heavy property, the first creature you hit with it each turn takes extra Necrotic damage equal to your Charisma modifier (minimum of 1).",
}
rune_opts = [option(rune_ids[r], f"{r} Rune", [rune_text[r]], RUNE_TAG,
                    rules=[grant_spell(n, l, "Paladin") for l, n in dk_cols[r]], sheet=rune_text[r]) for r in rune_ids]
dk_features = [
    F(1, "Death Coil", ["This feature replaces the Lay On Hands feature of the Paladin class.",
                        "Your creature type becomes Undead.",
                        "You also gain the ability to manipulate negative energy. You have a pool of d8s to fuel this ability. The number of dice in the pool equals one plus your Charisma modifier (minimum of one die).",
                        "As a Bonus Action, you can target a creature you can see within 60 feet of yourself and force it to make a Constitution saving throw, expending dice from the pool. The maximum number of dice you can expend at once equals your Charisma modifier (minimum of one die). Roll the dice you expend. The target takes Necrotic damage equal to the roll’s total on a failed save or half as much damage on a successful one. If the target is an Undead, you can choose to have it regain Hit Points equal to the roll’s total instead. Your pool regains all expended dice when you finish a Long Rest."],
      replaces=[R("PALADIN", "LAY_ON_HANDS")] + ([] if E14 else [R("PALADIN", "RESTORING_TOUCH")]), action="Bonus Action", usage="{{death coil:dice}}d8/Long Rest",
      sheet="Target a creature within 60 feet: Constitution save (DC {{paladin:spellcasting:dc}}), expending up to {{charisma:modifier}} dice from your pool of d8s. Necrotic damage equal to the roll on a failed save, half on success. An Undead target can instead regain that many Hit Points. Your creature type is Undead.",
      rules=['<stat name="death coil:dice" value="1" bonus="base" />', '<stat name="death coil:dice" value="charisma:modifier" />']),
    F(2, "Runic Smite", ["This feature replaces the Divine Smite feature of the Paladin class." if E14 else "This feature replaces the Paladin’s Smite feature of the Paladin class.",
                         "You always have the Rune Strike spell (see “Death Knight Spells”) prepared. You can cast it once without a spell slot, and you regain the ability to cast it in that way when you finish a Long Rest."],
      replaces=[R("PALADIN", "DIVINE_SMITE" if E14 else "PALADINS_SMITE")], usage="1/Long Rest",
      sheet="You always have Rune Strike prepared and can cast it once without a spell slot.",
      rules=[grant_spell("Rune Strike", 2, "Paladin")]),
    F(3, "Oath of the Ebon Blade Spells", ["The magic of your oath and your Runeforging feature (see below) ensure you always have certain spells ready; when you reach a Paladin level specified in the Oath of the Ebon Blade Spells table, you thereafter always have the spell in the Spells (All) column prepared. You also have the additional spells listed in the column matching the rune you have inscribed on your weapon, if any.", dk_table],
      sheet=False, rules=[grant_spell(n, l, "Paladin") for l, n in dk_all]),
    F(3, "Runeforging", ["When you finish a Long Rest, you can inscribe one of the following runes on a melee weapon you are holding, or you can transfer the rune to a different weapon. Whenever you gain a level, you can replace it with a different rune."] +
      [f"{r}. {rune_text[r]}" for r in rune_ids],
      sheet=False, rules=[f'<select type="Archetype Feature" name="Rune (Runeforging)" supports="{RUNE_TAG}" />']),
    F(3, "Runic Power", ["Immediately after you cast Rune Strike, you can expend one use of your Channel Divinity to gain one of the following benefits based on the rune inscribed on your weapon.",
                         "Blood. You regain a number of Hit Points equal to the Necrotic damage dealt with your Rune Strike.",
                         "Frost. Frost covers your weapon and shatters on impact. The target of your Rune Strike and each enemy in a 10-foot Emanation originating from the target take 2d6 Cold damage.",
                         "Unholy. The target of your Rune Strike is cursed until the end of your next turn. The next time the cursed target makes a saving throw, it subtracts 1d6 from the roll, and the curse ends."],
      usage="Channel Divinity", sheet="After you cast Rune Strike, expend a Channel Divinity: Blood—regain HP equal to its Necrotic damage; Frost—target and enemies within 10 feet take 2d6 Cold; Unholy—target subtracts 1d6 from its next saving throw."),
    F(5, "Faithful Steed", (["You always have the Find Steed spell prepared, and you can cast it once without expending a spell slot; you regain the ability to do so when you finish a Long Rest. When you cast Find Steed, the steed can be Undead (such as a skeletal warhorse). An Undead steed deals Necrotic damage with its attacks and has this Bonus Action:"] if E14 else
                            ["In addition to the benefits of the Paladin’s Faithful Steed feature, when you cast Find Steed, the Otherworldly Steed can be Undead. An Undead steed deals Necrotic damage with its Otherworldly Slam action and has this Bonus Action:"]) + [
                            "Ghostly Stride (Undead Only; Recharges After a Long Rest). The steed and its rider can move through other creatures and objects this turn as if they were Difficult Terrain. Both steed and rider take 5 (1d10) Force damage if they end their turn inside an object."],
      rules=['<grant type="Spell" id="ID_WOTC_PHB24_SPELL_FIND_STEED" spellcasting="Paladin" />'] if E14 else [], usage="1/Long Rest" if E14 else None),
    F(7, "Aura of Deathly Endurance", ["You and your allies have Resistance to Cold, Necrotic, and Psychic damage while in your Aura of Protection."]),
    F(11, "Runic Strikes", ["This feature replaces the Paladin’s Improved Divine Smite feature." if E14 else "This feature replaces the Paladin’s Radiant Strikes feature.",
                            "When you hit a target with an attack roll using a Melee weapon or an Unarmed Strike, the target takes an extra 1d8 Necrotic damage."],
      replaces=[R("PALADIN", "IMPROVED_DIVINE_SMITE" if E14 else "RADIANT_STRIKES")], sheet="When you hit a target with a Melee weapon or an Unarmed Strike, it takes an extra 1d8 Necrotic damage."),
    F(14, "Improved Death Coil", ["This feature replaces the Paladin’s Cleansing Touch feature." if E14 else "This feature replaces the Paladin’s Restoring Touch feature.",
                                  "When you use Death Coil to deal damage, the target takes extra Necrotic damage equal to your Charisma modifier (minimum of 1) whether or not it fails its saving throw. If the target is an Undead, and you have it regain Hit Points, it regains additional Hit Points equal to your Paladin level."],
      replaces=[R("PALADIN", "CLEANSING_TOUCH" if E14 else "RESTORING_TOUCH")]),
    F(15, "Runic Mastery", ["You can invoke the power of the rune inscribed on your weapon. Once you use this feature, you can’t do so again until you finish a Long Rest. The effect depends on the rune you have inscribed.",
                            "Blood. When a creature hits another creature you can see within 10 feet of you with an attack roll, you can take a Reaction to reduce the damage the target takes by your Paladin level. You then lose a number of Hit Points equal to your Paladin level.",
                            "Frost. When you take the Attack action on your turn, you can replace one attack with an exhalation of frost magic in a 30-foot Cone. Each creature in that area makes a Dexterity saving throw against your spell save DC. A creature takes 8d6 Cold damage on a failed save or half as much damage on a successful one.",
                            "Unholy. When you cast Summon Undead, you can modify it so that the spell doesn’t require Concentration. If you do so, the spell’s duration becomes 1 minute for that casting, and when summoned, the Undead Spirit has a number of Temporary Hit Points equal to your Paladin level plus your Charisma modifier. In addition, the first time each turn the spirit hits a creature, the spirit deals extra Necrotic damage equal to half your Paladin level (round up)."],
      usage="1/Long Rest", sheet="Blood—Reaction: reduce damage to a creature within 10 feet by your Paladin level, then lose that many HP. Frost—replace an attack with a 30-ft Cone, Dex save, 8d6 Cold. Unholy—cast Summon Undead without Concentration (1 minute), spirit gains THP and extra Necrotic damage."),
    F(20, "Aspect of the Horsemen", ["As a Bonus Action, you gain the benefits below for 10 minutes or until you end them (no action required). Once you use this feature, you can’t use it again until you finish a Long Rest. You can also restore your use of it by expending a level 5 spell slot (no action required).",
                                     "Generate Runic Power. You can restore a use of your Runic Mastery by expending a level 4 spell slot (no action required).",
                                     "Runeforging. When you use your Runic Power and Runic Mastery features, you can choose any effect, not just the one that corresponds to the rune inscribed on your weapon."],
      action="Bonus Action", usage="1/Long Rest"),
] + rune_opts
archetype(f"{FP}paladin-ebon-blade.xml", "Oath of the Ebon Blade", "Paladin", "Wield the Power of Death Against the Scourge",
          ["The Oath of the Ebon Blade unites the free death knights of Azeroth. No longer directly under the Lich King’s control, they still serve Bolvar Fordragon—first as agents of the new Lich King, and later, after the destruction of the Helm of Domination, as troops devoted to stopping the Scourge’s spread.",
           "Death knight is a hero class, which means you typically must start play at level 3 or higher. This subclass alters some of your core Paladin class features beginning at level 1. With your DM’s permission, you can start as a level 1 character of this class, but your subclass choice is fixed when you make the character. (In Aurora, the subclass’s level 1 and 2 features apply once you choose the subclass.)"],
          dk_features, tag=TAG("Paladin"), file_desc="Oath of the Ebon Blade (Death Knight) Paladin subclass from World of Warcraft (Andrey Kuzinskiy).")

# =====================================================================
# Demon Hunter (Ranger)
# =====================================================================
DH_ID = f"{PREFIX}_ARCHETYPE_RANGER_DEMON_HUNTER"
base = f"{PREFIX}_ARCHETYPE_FEATURE_RANGER_DEMON_HUNTER"
COL_TAG = "WoW Demon Hunter Specialization"
dh_all = [(3, "Throw Glaive"), (5, "Sigil of Flame"), (9, "Metamorphosis"), (13, "Chaos Nova"), (17, "Destructive Wave")]
dh_cols = {
    "Devourer": [(3, "Consume Soul"), (5, "Misty Step"), (9, "Soul Reap"), (13, "Collapsing Star"), (17, "Steel Wind Strike")],
    "Havoc": [(3, "Fel Rush"), (5, "Eye Beam"), (9, "Blink"), (13, "Fire Shield"), (17, "Conjure Volley")],
    "Vengeance": [(3, "Infernal Strike"), (5, "Fiery Brand"), (9, "Demon Spikes"), (13, "Banishment"), (17, "Sigil of Chains")],
}
dh_table = spell_table("Demon Hunter Spells", ["Ranger Level", "Spells (All)", "Spells (Devourer)", "Spells (Havoc)", "Spells (Vengeance)"],
                       [[a[0], a[1], dh_cols["Devourer"][i][1], dh_cols["Havoc"][i][1], dh_cols["Vengeance"][i][1]] for i, a in enumerate(dh_all)])
dh_opts = [option(f"{base}_SPELLS_{c.upper()}", f"{c} Spells", [f"You always have the spells in the Spells ({c}) column of the Demon Hunter Spells table prepared."], COL_TAG,
                  rules=[grant_spell(n, l, "Ranger") for l, n in dh_cols[c]], sheet=False) for c in dh_cols]
dh_features = [
    F(2 if E14 else 1, "Spellcasting", ["You can use an Arcane Focus as a Spellcasting Focus for your Ranger spells." if E14 else "You can use an Arcane Focus (not a Druidic Focus) as a Spellcasting Focus for your Ranger spells."]),
    (F(1, "Favored Enemy Languages", ["When you learn a language from the Favored Enemy (or Deft Explorer) class feature, choose from the language tables in chapter 2. Eredun and Nathrezim are recommended."], sheet=False) if E14 else
     F(2, "Deft Explorer", ["When you choose languages for the Deft Explorer class feature, choose from the language tables in chapter 2. Eredun and Nathrezim are recommended."], sheet=False)),
    F(2, "Fighting Style", ["As a Demon Hunter, you can choose a Fighting Style, or the Void Warrior option below." if E14 else "As a Demon Hunter, you can choose a Fighting Style feat, the Druidic Warrior option in the Player’s Handbook, or the Void Warrior option below.",
                            "Void Warrior. You learn two Warlock cantrips of your choice. Chill Touch and Mind Sliver are recommended. The chosen cantrips count as Ranger spells for you, and Wisdom is your spellcasting ability for them. Whenever you gain a Ranger level, you can replace one of these cantrips with another Warlock cantrip."], sheet=False),
    F(3, "Demon Hunter Spells", ["When you reach a Ranger level specified in the Demon Hunter Spells table, you thereafter always have the spell in the Spells (All) column prepared. You also have the additional spells listed in one other column of your choice.", dh_table],
      sheet=False, rules=[grant_spell(n, l, "Ranger") for l, n in dh_all] + [f'<select type="Archetype Feature" name="Demon Hunter Spells (Column)" supports="{COL_TAG}" />']),
    F(3, "Soul Fragments", ["You harvest the energy of souls to fuel some of your special powers. Whenever you finish a Long Rest, you gain a number of soul fragments equal to your Wisdom modifier (minimum of one fragment); each soul fragment is a Tiny object in the form of a crystal. These fragments last until you finish another Long Rest, at which point they disintegrate. If you ever move more than 30 feet from a fragment, the fragment immediately teleports to you, appearing somewhere on your person.",
                            "If a soul fragment effect requires a saving throw, the DC equals your Ranger spell save DC.",
                            "The number of soul fragments you gain when you finish a Long Rest increases when you reach Ranger levels 13 (Wisdom modifier plus one soul fragment) and 17 (Wisdom modifier plus two soul fragments).",
                            "Using Soul Fragments. You can use soul fragments in the following ways:",
                            "Double Jump. You can expend one soul fragment to cast Feather Fall or Jump without expending a spell slot.",
                            "Soul Cleave. Once on each of your turns, when you take the Attack action, you can expend one soul fragment and replace one of your attacks with a whirlwind of soul energy. Each creature in a 10-foot Emanation originating from you makes a Dexterity saving throw. On a failed save, a creature takes Psychic damage equal to 1d12 plus your Wisdom modifier, and you regain Hit Points equal to your Wisdom modifier.",
                            "Regaining Soul Fragments. When an enemy you can see within 30 feet of you dies, you can take a Reaction to regain one expended soul fragment."],
      usage="{{soul fragments}}/Long Rest",
      sheet=[(None, "Double Jump: 1 fragment to cast Feather Fall or Jump. Soul Cleave: once per turn, replace an attack; each creature within 10 feet makes a Dex save (DC {{ranger:spellcasting:dc}}) or takes 1d12 + {{wisdom:modifier}} Psychic; you regain {{wisdom:modifier}} HP. Reaction: regain 1 fragment when an enemy within 30 feet dies."),
             (11, "Double Jump: 1 fragment to cast Feather Fall or Jump. Soul Cleave: once per turn, replace an attack; each creature within 10 feet makes a Dex save (DC {{ranger:spellcasting:dc}}) or takes 1d12 + {{wisdom:modifier}} Psychic; you regain {{wisdom:modifier}} HP. Disrupt: 2 fragments to cast Counterspell. Warglaive Mastery: Bonus Action, 1 fragment to cast Throw Glaive. Reaction: regain 1 fragment when an enemy within 30 feet dies."),
             (15, "Double Jump: 1 fragment to cast Feather Fall or Jump. Soul Cleave: once per turn, replace an attack; each creature within 10 feet makes a Dex save (DC {{ranger:spellcasting:dc}}) or takes 2d12 + {{wisdom:modifier}} Psychic; you regain {{wisdom:modifier}} HP. Disrupt: 2 fragments to cast Counterspell. Warglaive Mastery: Bonus Action, 1 fragment to cast Throw Glaive. Regain 1 fragment on Initiative if you have none; Reaction: regain 1 when an enemy within 30 feet dies.")],
      rules=['<stat name="soul fragments" value="wisdom:modifier" />', '<stat name="soul fragments" value="1" level="13" />', '<stat name="soul fragments" value="1" level="17" />',
             '<grant type="Spell" id="ID_WOTC_PHB24_SPELL_FEATHER_FALL" level="3" spellcasting="Ranger" />', '<grant type="Spell" id="ID_WOTC_PHB24_SPELL_JUMP" level="3" spellcasting="Ranger" />']),
    F(3, "Spectral Sight", ["You have Blindsight with a range of 10 feet."], sheet=False,
      rules=['<grant type="Vision" id="ID_VISION_BLINDSIGHT" />', '<stat name="blindsight:range" value="10" bonus="base" />']),
    F(7, "Torment", ["A creature marked by your Hunter’s Mark spell has Disadvantage on attack rolls against targets other than you.",
                     "Additionally, once per turn when you hit a creature marked by your Hunter’s Mark with an attack roll with a weapon or a Ranger spell, you can impose one of the following effects on the target (your choice):",
                     "Aura of Pain. The target subtracts 1d4 from the next saving throw it makes before the end of your next turn.",
                     "Chaos Strike. The target takes an extra 1d8 Fire damage."]),
    F(11, "Illidari Knowledge", ["You gain new mastery over souls, granting you new ways to use soul fragments:",
                                 "Disrupt. You can expend two soul fragments to cast Counterspell in response to that spell’s trigger, using your spellcasting ability.",
                                 "Warglaive Mastery. As a Bonus Action, you can expend one soul fragment to cast Throw Glaive (see “Demon Hunter Spells”) without expending a spell slot."],
      sheet=False, rules=['<grant type="Spell" id="ID_WOTC_PHB24_SPELL_COUNTERSPELL" spellcasting="Ranger" />']),
    F(15, "Soul Shatter", ["Your mastery of fel magic reaches new heights. When you use the Soul Cleave option of Soul Fragments, the damage increases to 2d12 plus your Wisdom modifier.",
                           "In addition, when you roll Initiative, you regain one soul fragment if you have none."], sheet=False),
    F(18, "Improved Spectral Sight", ["This feature replaces the Ranger’s Feral Senses feature.", "You have Truesight with a range of 30 feet."],
      replaces=[R("RANGER", "FERAL_SENSES")], sheet=False,
      rules=['<grant type="Vision" id="ID_VISION_TRUESIGHT" />', '<stat name="truesight:range" value="30" bonus="base" />']),
] + dh_opts
void_warrior = f'''	<element name="Void Warrior" type="Feat" source="{SOURCE}" id="{PREFIX}_FEAT_VOID_WARRIOR">
		<supports>PHB24 Druidic Warrior Fighting Style</supports>
		<requirements>(ID_WOTC_PHB24_CLASS_FEATURE_RANGER_FIGHTING_STYLE,{DH_ID})||ID_WOTC_PHB24_GRANTS_FEAT_UNLOCKER</requirements>
		<prerequisite>Ranger Fighting Style Feature, Demon Hunter Subclass</prerequisite>
		<description>
			<p>You learn two Warlock cantrips of your choice. <i>Chill Touch</i> and <i>Mind Sliver</i> are recommended. The chosen cantrips count as Ranger spells for you, and Wisdom is your spellcasting ability for them. Whenever you gain a Ranger level, you can replace one of these cantrips with another Warlock cantrip.</p>
		</description>
		<sheet>
			<description>Whenever you gain a Ranger level, you can replace one of the chosen cantrips with another Warlock cantrip.</description>
		</sheet>
		<rules>
			<select type="Spell" name="Void Warrior" supports="0, Warlock" number="2" spellcasting="Ranger" />
		</rules>
	</element>'''
if E14:
    void_warrior = f'''	<element name="Void Warrior" type="Class Feature" source="{SOURCE}" id="{PREFIX}_CLASS_FEATURE_FIGHTING_STYLE_VOID_WARRIOR">
		<supports>Fighting Style, Ranger</supports>
		<requirements>{DH_ID}</requirements>
		<description>
			<p>You learn two Warlock cantrips of your choice. <i>Chill Touch</i> and <i>Mind Sliver</i> are recommended. The chosen cantrips count as Ranger spells for you, and Wisdom is your spellcasting ability for them. Whenever you gain a Ranger level, you can replace one of these cantrips with another Warlock cantrip. (Demon Hunter only; if you choose your Fighting Style before your subclass, you can switch to this option once you become a Demon Hunter.)</p>
		</description>
		<sheet>
			<description>Whenever you gain a Ranger level, you can replace one of the chosen cantrips with another Warlock cantrip.</description>
		</sheet>
		<rules>
			<select type="Spell" name="Void Warrior" supports="0, Warlock" number="2" spellcasting="Ranger" />
		</rules>
	</element>'''
archetype(f"{FP}ranger-demon-hunter.xml", "Demon Hunter", "Ranger", "Embrace the Magic of Demons to Fight Fire with Fire",
          ["Most Demon Hunters joined Illidan on Outland as he marshaled his forces to battle the Burning Legion. You might have followed a different path, inspired by Illidan rather than directly trained by him, but the result is the same: You have embraced the magic of the Burning Legion with the singular goal of defeating it on Azeroth and every other world.",
           "Demon hunter is a hero class, which means you typically must start play at level 3 or higher. All demon hunters in World of Warcraft lore are elves (blood elves, night elves, or void elves), so check with your DM before playing a demon hunter of another species. (In Aurora, the subclass’s level 1 and 2 features apply once you choose the subclass.)"],
          dh_features, extra=[void_warrior], tag=TAG("Ranger"))

# =====================================================================
# Evoker (Draconic Sorcery addition)
# =====================================================================
base = f"{PREFIX}_CLASS_FEATURE_SORCERER_EVOKER"
EV_TAG = "WoW Evoker Specialization"
ev_all = [(3, ["Chromatic Orb", "Dragon’s Breath"]), (5, ["Fly"]), (7, ["Arcane Eye"]), (9, ["Summon Dragon"])]
ev_cols = {
    "Augmentation": [(3, ["Ebon Might", "Eruption"]), (5, ["Blistering Scales"]), (7, ["Upheaval"]), (9, ["Breath of Eons"])],
    "Devastation": [(3, ["Azure Strike", "Scorching Ray"]), (5, ["Fireball"]), (7, ["Emberstorm"]), (9, ["Shattering Star"])],
    "Preservation": [(3, ["Dream Breath", "Living Flame"]), (5, ["Emerald Blossom"]), (7, ["Time Dilation"]), (9, ["Dream Flight"])],
}
ev_table = spell_table("Evoker Spells", ["Sorcerer Level", "Spells (All)", "Spells (Augmentation)", "Spells (Devastation)", "Spells (Preservation)"],
                       [[a[0], ", ".join(a[1])] + [", ".join(ev_cols[c][i][1]) for c in ev_cols] for i, a in enumerate(ev_all)])
gs = lambda rows: [grant_spell(n, l, "Sorcerer") for l, ns in rows for n in ns]
ev_opts = [option(f"{base}_SPELLS_{c.upper()}", f"{c} Spells", [f"You always have the spells in the Spells ({c}) column of the Evoker Spells table prepared."], EV_TAG,
                  rules=gs(ev_cols[c]), sheet=False) for c in ev_cols]
evoker = F(3, "Evoker Spells", ["Evokers wield the magic of the five ordered dragonflights—the chaotic flames of the red flight, the focused magic of the blue flight, the might of the black flight, the life-giving spirit of the green flight, and the time-bending magic of the bronze flight. To play an evoker, choose the Sorcerer class and the Draconic Sorcery subclass at level 3. Instead of the Draconic Spells subclass feature, you gain the Evoker Spells feature.",
                                "When you reach a Sorcerer level specified in the Evoker Spells table, you thereafter always have the spells in the Spells (All) column prepared. You also have the additional spells listed in one other column of your choice.", ev_table],
           sheet=False, etype="Archetype Feature", fid=f"{base}_EVOKER_SPELLS", supports="WoW Evoker 2014" if E14 else "WoW Evoker", grant=False,
           replaces=[] if E14 else [R("SORCERER", "DRACONIC_SORCERY_DRACONIC_SPELLS")],
           rules=gs(ev_all) + [f'<select type="Archetype Feature" name="Evoker Spells (Column)" supports="{EV_TAG}" />'])
evoker.alt = "Evoker Spells"
ev_append = f'''	<append id="{'ID_WOTC_PHB_ARCHETYPE_DRACONIC_BLOODLINE' if E14 else 'ID_WOTC_PHB24_ARCHETYPE_SORCERER_DRACONIC_SORCERY'}">
		<rules>
			<select type="Archetype Feature" name="Evoker (World of Warcraft, optional)" supports="WoW Evoker{' 2014' if E14 else ''}" level="{1 if E14 else 3}" optional="true" />
		</rules>
	</append>'''
write(f"archetypes/{FP}sorcerer-evoker.xml", "Evoker", "Evoker option for the Draconic Sorcery subclass from World of Warcraft (Andrey Kuzinskiy).",
      [evoker.xml(base)] + [o.xml(base) for o in ev_opts] + [ev_append])

# =====================================================================
# Hunter: Pet Specialization (Beast Master addition)
# =====================================================================
base = f"{PREFIX}_ARCHETYPE_FEATURE_RANGER_BEAST_MASTER"
pets = [("Basilisk", "Land", "C", "Slow"), ("Bat", "Sky", "F", "Vex"), ("Bear", "Land", "T", "Push"), ("Beetle", "Land", "T", "Sap"),
        ("Bird of Prey", "Sky", "C", "Slow"), ("Blood Beast* (stirge)", "Sky", "T", "Slow"), ("Boar", "Land", "C", "Sap"), ("Camel", "Land", "C", "Push"),
        ("Carrion Bird", "Sky", "F", "Cleave"), ("Cat", "Land", "F", "Graze"), ("Courser (horses)", "Land", "F", "Graze"), ("Crab", "Land", "T", "Slow"),
        ("Crocolisk", "Land", "F", "Slow"), ("Direhorn* (triceratops)", "Land", "T", "Cleave"), ("Dolphin", "Sea", "T", "Vex"), ("Dragonhawk", "Sky", "T", "Graze"),
        ("Feathermane* (gryphon)", "Sky", "T", "Graze"), ("Fox", "Land", "C", "Graze"), ("Frenzy (piranha-like fish)", "Sea", "F", "Cleave"), ("Gorilla", "Land", "F", "Push"),
        ("Gruffhorn (goats)", "Land", "C", "Push"), ("Hopper (frogs, toads)", "Land", "T", "Graze"), ("Hound", "Land", "C", "Slow"), ("Hydra", "Land", "T", "Cleave"),
        ("Hyena", "Land", "C", "Cleave"), ("Lizard", "Land", "T", "Cleave"), ("Mammoth", "Land", "T", "Slow"), ("Mechanized animal*", "Land", "C", "Sap"),
        ("Monkey", "Land", "C", "Graze"), ("Moth", "Sky", "C", "Vex"), ("Oxen", "Land", "T", "Push"), ("Raptor (allosaurus)", "Land", "C", "Cleave"),
        ("Ray", "Sky", "F", "Vex"), ("Riverbeast (hippo)", "Land", "T", "Cleave"), ("Rodent", "Land", "C", "Cleave"), ("Scalehide (ankylosaurus)", "Land", "F", "Sap"),
        ("Scorpid", "Land", "F", "Cleave"), ("Serpent", "Land or Sea", "C", "Graze"), ("Shark", "Sea", "C", "Graze"), ("Spider", "Land", "F", "Slow"),
        ("Stag", "Land", "T", "Vex"), ("Tallstrider (flightless bird)", "Land", "F", "Slow"), ("Threshadon* (plesiosaur)", "Sea", "T", "Sap"), ("Turtle", "Land", "T", "Sap"),
        ("Wasp", "Sky", "F", "Cleave"), ("Waterfowl", "Land", "T", "Vex"), ("Wolf", "Land", "F", "Slow")]
pet_table = spell_table("Pet Families", ["Family", "Stat Block", "Spec."] + ([] if E14 else ["Mastery"]), [list(p)[:3] if E14 else list(p) for p in pets])
pet_intro = ["As a Beast Master, when you use your Primal Companion feature to summon a primal beast, you choose the form it takes from among the pet families shown on the table below. Each family has three characteristics:",
             "Stat Block. Your primal beast’s family determines which one of the stat blocks in the Player’s Handbook it uses: Beast of the Land, Beast of the Sea, or Beast of the Sky.",
             "Specialization (Spec.). Each pet family has a specialization—Cunning (C), Ferocity (F), or Tenacity (T)—that comes into play only if you have the Pet Specialization feature.",
             ("Mastery Property (Mastery). When you gain the Primal Companion feature and whenever you finish a Long Rest, you can choose your pet’s family as one of the weapons for your Weapon Mastery feature. Then its mastery property applies to your primal companion’s Beast’s Strike attack." if not E14 else
              "The Mastery column of the book is left out of this version: the 2014 Ranger has no Weapon Mastery feature, so the table has only the Stat Block and Spec. columns."),
             pet_table, "*Unusual pet family; a hunter must acquire a special ability (typically by reading a magical tome) to tame an unusual pet."]
PET_TAG = "WoW Pet Specialization"
pet_specs = {
    "Cunning": ("Your Speed and all of your primal beast’s speeds increase by 10 feet. In addition, your primal beast can use its action to cast Freedom of Movement without any spell components, affecting itself and you (if you are within range). Once it does so, it can’t do so again until you finish a Long Rest.",
                ['<stat name="innate speed" value="10" />']),
    "Ferocity": ("When your primal beast is Bloodied and it hits with its Beast’s Strike attack, you and your primal beast each regain Hit Points equal to your Wisdom modifier. In addition, your primal beast can use its action to cast Haste without any spell components, affecting itself and you (if you are within range). Once it does so, it can’t do so again until you finish a Long Rest.", []),
    "Tenacity": ("Your Hit Point maximum increases by 6. Whenever you gain a Ranger level, your Hit Point maximum increases by an additional 1 Hit Point. Your primal beast’s Hit Point maximum also increases by your Ranger level. In addition, your primal beast can use its action to cast Stoneskin without any spell components, affecting itself and you (if you are within range). Once it does so, it can’t do so again until you finish a Long Rest.",
                 ['<stat name="hp" value="6" />', '<stat name="hp" value="level:ranger" />']),
}
spec_opts = [option(f"{base}_PET_SPECIALIZATION_{k.upper()}", f"Pet Specialization: {k}", [v[0]], f"{PET_TAG} Option", rules=v[1], sheet=v[0])
             for k, v in pet_specs.items()]
petspec = F(6, "Pet Specialization", [("This feature replaces the Ranger’s Roving feature. (Beast mastery and survival hunters.)" if not E14 else "This is an optional addition for hunters (beast mastery and survival). The 2014 Ranger has no Roving feature, so it replaces nothing."),
                                      "While the beast from your Primal Companion feature is within 60 feet of you, you gain one of the following benefits, depending on the beast’s pet family and its specialization (see “Hunter Pets”)."] +
            [f"{k}. {v[0]}" for k, v in pet_specs.items()] + ["<h5>Hunter Pets</h5>"] + pet_intro,
            sheet=False, fid=f"{base}_PET_SPECIALIZATION", supports=PET_TAG, grant=False, replaces=[] if E14 else [R("RANGER", "ROVING")],
            rules=[f'<select type="Archetype Feature" name="Pet Family Specialization" supports="{PET_TAG} Option" />'])
pet_append = f'''	<append id="{'ID_WOTC_ARCHETYPE_RANGER_BEAST_MASTER' if E14 else 'ID_WOTC_PHB24_ARCHETYPE_RANGER_BEAST_MASTER'}">
		<rules>
			<select type="Archetype Feature" name="Pet Specialization (World of Warcraft, optional)" supports="{PET_TAG}" level="6" optional="true" />
		</rules>
	</append>'''
write(f"archetypes/{FP}ranger-hunter-pets.xml", "Hunter Pets", "Hunter Pet Specialization option for the Beast Master subclass from World of Warcraft (Andrey Kuzinskiy).",
      [petspec.xml(base)] + [o.xml(base) for o in spec_opts] + [pet_append])

# =====================================================================
# Warrior of Mystic Brews (Monk)
# =====================================================================
BREW_TAG = "WoW Mystic Brew"
brews = [
    ("Cinnamon Dragon", "You can take a Magic action to exhale toxic flames in a 30-foot Cone. Each creature in the Cone makes a Dexterity saving throw (DC 8 plus your Wisdom modifier and Proficiency Bonus). On a failed save, a creature takes Fire damage equal to four rolls of your Martial Arts die and has the Poisoned condition until the end of its next turn. On a successful save, a creature takes half as much damage only."),
    ("Heavenly Spirit", "You gain Resistance to two of the following damage types of your choice: Cold, Necrotic, Psychic, or Radiant damage."),
    ("Refreshing Dip", "You have a pool of dice of the same type as your Martial Arts die. The maximum number of dice equals your Wisdom modifier plus half your Monk level (round down). Whenever you regain Hit Points, you can expend and roll one die from this pool to regain additional Hit Points equal to the number rolled."),
]
wise = [
    ("Blue Lightning", "Whenever you take a Reaction that isn’t making an Opportunity Attack or casting a spell, you can make one Unarmed Strike as part of that Reaction."),
    ("Drunkard’s Luck", "You gain Heroic Inspiration if you don’t already have it. In addition, you can give yourself Heroic Inspiration when you make an ability check or saving throw without it."),
    ("Stumbling Monk", "When you take a Bonus Action other than Patient Defense, you can also use Patient Defense immediately after that Bonus Action."),
]
mb = [
    F(3, "Bonus Proficiencies", ["You gain proficiency in the Performance skill, or if you already have it, you gain proficiency in one skill of your choice from the skills available to Monks at level 1. You also gain proficiency with Brewer’s Supplies if you don’t already have it."],
      sheet=False, rules=['<grant type="Proficiency" id="ID_PROFICIENCY_SKILL_PERFORMANCE" />', '<grant type="Proficiency" id="ID_PROFICIENCY_TOOL_PROFICIENCY_BREWERS_SUPPLIES" />']),
    F(3, "Drunken Technique", ["You twist and turn quickly as you move. Whenever you expend a Focus Point using Patient Defense, your Speed increases by 10 feet until the end of the current turn, and you can make one Unarmed Strike immediately after the Bonus Action."]),
    F(6, "Tipsy Sway", ["You can move in sudden, swaying ways. You gain the following benefits.",
                        "Leap to Your Feet. When you have the Prone condition, you can stand up by spending 5 feet of movement.",
                        "Redirect Attack. When an enemy misses you with a melee attack roll, you can take a Reaction and spend 1 Focus Point to cause that attack to hit one creature of your choice, other than the attacker, that you can see within 5 feet of yourself."]),
    F(6, "Mystic Brew", ["Whenever you finish a Short or Long Rest while holding Brewer’s Supplies, you can use that tool to magically produce one magical beverage, chosen from the following options: Cinnamon Dragon, Heavenly Spirit, or Refreshing Dip. A pint of the beverage appears in a bottle or flask you are holding or carrying; otherwise, the beverage spills out on the ground and then vanishes. If any beverage remains when you finish a Short or Long Rest, the beverage vanishes.",
                         "Drinking a Magical Beverage. Only you can gain the benefits of drinking the beverage. You must drink the full pint of the beverage before gaining its benefit. You can spend 1 minute drinking the beverage. You then gain the benefits of the beverage for 1 hour or until you drink another magical beverage, as described below:"] +
      [f"{n}. {t}" for n, t in brews] +
      ["Enhancing a Magical Beverage. When you create a magical beverage, you can expend 1 Focus Point to extend the benefits’ duration to 8 hours."],
      usage="1/Short Rest",
      sheet=[(None, "After a Short or Long Rest with Brewer’s Supplies, brew one beverage (1 hour; 1 Focus Point for 8 hours): Cinnamon Dragon (Magic action, 30-ft Cone, Dex save DC 8 + Wis + PB, 4 Martial Arts dice Fire and Poisoned), Heavenly Spirit (Resistance to two of Cold, Necrotic, Psychic, Radiant), or Refreshing Dip (pool of Martial Arts dice to boost healing)."),
             (11, "After a Short or Long Rest with Brewer’s Supplies, brew one beverage (1 hour; 1 Focus Point for 8 hours): Cinnamon Dragon, Heavenly Spirit, Refreshing Dip, Blue Lightning, Drunkard’s Luck, or Stumbling Monk."),
             (17, "After a Short or Long Rest with Brewer’s Supplies, brew one beverage combining two different options (1 hour; 1 Focus Point for 8 hours): Cinnamon Dragon, Heavenly Spirit, Refreshing Dip, Blue Lightning, Drunkard’s Luck, or Stumbling Monk.")]),
    F(11, "Wizened Brewer", ["You learn more complex flavors. The following beverages are added to your Mystic Brew options:"] + [f"{n}. {t}" for n, t in wise], sheet=False),
    F(17, "Master Brewer", ["When you create a magical beverage using your Mystic Brew feature, you can choose two different options and produce one magical beverage. Drinking the beverage provides the effects of both options for the duration."], sheet=False),
    F(17, "Intoxicated Frenzy", ["Immediately after you use your Patient Defense, you can move up to your Speed. During this movement, whenever you enter a space within 5 feet of a creature, you can make an Unarmed Strike targeting that creature. In addition, when you hit a creature with an Unarmed Strike granted by this feature, the creature must succeed on a Dexterity saving throw or have the Prone condition. A creature can be targeted by an Unarmed Strike granted by this feature only once per turn."]),
]
archetype(f"{FP}monk-mystic-brews.xml", "Warrior of Mystic Brews", "Monk", "Drink Mystic Brews to Overwhelm and Confound Foes",
          ["Warriors of Mystic Brews move with the jerky, unpredictable movements typical of someone who is intoxicated. Their apparently erratic stumbles conceal a carefully executed dance of blocks, parries, advances, attacks, and retreats. Warriors of Mystic Brews frequent bars and taverns to gather information or spy on potential threats. These warriors drink magical concoctions that enhance their martial arts.",
           "Warriors of Mystic Brews often enjoy playing the fool to bring gladness to the downtrodden or to teach humility to the arrogant, but these Monks are maddening, masterful foes in battle."], mb, tag=TAG("Monk"))

# =====================================================================
# Oath of the Holy (Paladin)
# =====================================================================
holy_sp = [(3, ["Cure Wounds", "Healing Word"]), (5, ["Lesser Restoration", "Prayer of Healing"]), (9, ["Dispel Magic", "Mass Healing Word"]),
           (13, ["Aura of Life", "Death Ward"]), (17, ["Greater Restoration", "Mass Cure Wounds"])]
holy = [
    F(3, "Oath of the Holy Spells", ["The magic of your oath ensures you always have certain spells ready; when you reach a Paladin level specified in the Oath of the Holy Spells table, you thereafter always have the listed spells prepared.",
                                     spell_table("Oath of the Holy Spells", ["Paladin Level", "Spells"], [[l, ", ".join(n)] for l, n in holy_sp])],
      sheet=False, rules=[grant_spell(n, l, "Paladin") for l, ns in holy_sp for n in ns]),
    F(3, "Beacon of Light", ["As a Magic action, you can expend one use of your Channel Divinity to wrap an ally within 60 feet in holy energy. For 1 minute, anytime you heal a creature other than the affected ally with a spell or your Lay On Hands, the chosen ally also regains half as many Hit Points."],
      action="Magic Action", usage="Channel Divinity"),
    F(7, "Lightbringer’s Aura", ["Whenever you cast a spell or use Lay On Hands to restore Hit Points to a Bloodied creature within your Aura of Protection, the creature regains an extra 1d6 Hit Points."]),
    F(15, "Infusion of Light", ["Whenever you cast a spell that deals Radiant damage, you refresh the pool of healing power that fuels your Lay On Hands feature. Your pool of healing power regains a number of Hit Points equal to the total number rolled for the spell’s Radiant damage, to a maximum of five times your Paladin level."]),
    F(20, "Holy Deliverance", ["As a Bonus Action, you can imbue your Aura of Protection with holy power, granting the benefits below for 10 minutes or until you end them (no action required). Once you use this feature, you can’t use it again until you finish a Long Rest. You can also restore your use of it by expending a level 5 spell slot (no action required).",
                               "Healing Power. Whenever an ally starts its turn Bloodied and in the aura, that creature regains Hit Points equal to your Charisma modifier plus your Proficiency Bonus.",
                               "Sunlight. The aura is filled with Bright Light that is sunlight."], action="Bonus Action", usage="1/Long Rest"),
]
archetype(f"{FP}paladin-holy.xml", "Oath of the Holy", "Paladin", "Serve as a Beacon of the Light",
          ["The Oath of the Holy unites Paladins who nurture life and use the power of the Light for healing and support. They combine great piety and virtue with martial skill, aspiring to the highest standards of morality, service to others, and self-sacrifice.",
           "These paladins share the following tenets:",
           '<ul><li>Live your life in service to others of goodwill.</li><li>Do all in your power to ease the suffering of the innocent.</li><li>Let the Light shine through you to banish the darkness.</li></ul>'], holy, tag=TAG("Paladin"))

# =====================================================================
# Discipline Domain / Shadow Domain (Cleric)
# =====================================================================

SPL_LV = {"Arcane Vigor": 2, "Guiding Bolt": 1, "Magic Weapon": 2, "Shield of Faith": 1, "Prayer of Mending": 3, "Protection from Energy": 3,
          "Guardian of Faith": 4, "Stoneskin": 4, "Circle of Power": 5, "Destructive Wave": 5, "Crown of Madness": 2, "Dissonant Whispers": 1,
          "Mind Spike": 2, "Shadow Word: Pain": 1, "Summon Undead": 3, "Vampiric Touch": 3, "Evard’s Black Tentacles": 4, "Psychic Horror": 4,
          "Dominate Person": 5, "Void Eruption": 5}


def dom14(rows):
    """2014 domain spells: 1st-level at Cleric 1, 2nd at 3, 3rd at 5, 4th at 7, 5th at 9."""
    if not E14:
        return rows
    out = {}
    for _, ns in rows:
        for n in ns:
            out.setdefault({1: 1, 2: 3, 3: 5, 4: 7, 5: 9}[SPL_LV[n]], []).append(n)
    return sorted(out.items())


CL1, CL2 = (1, 2) if E14 else (3, 3)
disc_sp = [(3, ["Arcane Vigor", "Guiding Bolt", "Magic Weapon", "Shield of Faith"]), (5, ["Prayer of Mending", "Protection from Energy"]),
           (7, ["Guardian of Faith", "Stoneskin"]), (9, ["Circle of Power", "Destructive Wave"])]
disc_sp = dom14(disc_sp)
disc = [
    F(CL1, "Discipline Spells", ["Your connection to this domain ensures you always have certain spells ready. When you reach a Cleric level specified in the Discipline Domain Spells table, you thereafter always have the listed spells prepared.",
                               spell_table("Discipline Domain Spells", ["Cleric Level", "Spells"], [[l, ", ".join(n)] for l, n in disc_sp])],
      sheet=False, rules=[grant_spell(n, l, "Cleric") for l, ns in disc_sp for n in ns]),
    F(CL2, "Holy Bolt", ["As a Bonus Action, you present your Holy Symbol and expend a use of your Channel Divinity to make a ranged spell attack, hurling a bolt of holy energy targeting one creature within 60 feet of yourself. On a hit, the target takes Radiant damage equal to 2d10 plus your Wisdom modifier, and you can choose a creature you can see within 60 feet of yourself to regain Hit Points equal to 1d10 plus your Wisdom modifier."],
      action="Bonus Action", usage="Channel Divinity",
      sheet="Ranged spell attack (+{{cleric:spellcasting:attack}}) against a creature within 60 feet: 2d10 + {{wisdom:modifier}} Radiant damage on a hit, and a creature you can see within 60 feet regains 1d10 + {{wisdom:modifier}} HP."),
    F(CL2, "Atonement", ["When a level 1+ spell you cast restores Hit Points to one or more creatures, each of those creatures gains a blessing that lasts until the end of your next turn. Whenever you cast a spell that deals damage to a creature using a spell slot, each blessed creature regains additional Hit Points equal to the level of the spell slot you used to cast the damaging spell."]),
    F(6, "Luminous Barrier", ["As a Bonus Action, you can expend a use of your Channel Divinity to place a magical ward of glowing light on each creature blessed by your Atonement. Each affected creature gains a number of Temporary Hit Points equal to your Cleric level plus your Wisdom modifier. While a creature has Temporary Hit Points gained from this feature, it has Resistance to all damage."],
      action="Bonus Action", usage="Channel Divinity"),
    F(17, "Ultimate Penitence", ["Your Holy Bolt grows more powerful as detailed below.",
                                 "Ascending Step. When you use Holy Bolt, you can teleport to an unoccupied space you can see within 30 feet before you make an attack roll.",
                                 "Ascending Volley. When you use Holy Bolt, you can expend a spell slot as part of the Bonus Action to hurl a number of additional bolts equal to the spell slot level expended. You can direct the bolts to hit one creature or several. Make a separate attack roll for each bolt."]),
]
archetype(f"{FP}cleric-discipline.xml", "Discipline Domain", "Cleric", "Cure Allies’ Wounds While Smiting Enemies",
          ["The Discipline Domain focuses on the balance between the Holy Light and its shadowy mirror, the Void. Wielding both powers at once, Clerics who embrace this domain aid their allies and harm their foes, often with a single spell."], disc, tag=TAG("Cleric"))
shad_sp = [(3, ["Crown of Madness", "Dissonant Whispers", "Mind Spike", "Shadow Word: Pain"]), (5, ["Summon Undead", "Vampiric Touch"]),
           (7, ["Evard’s Black Tentacles", "Psychic Horror"]), (9, ["Dominate Person", "Void Eruption"])]
shad_sp = dom14(shad_sp)
shad = [
    F(CL1, "Shadow Spells", ["Your connection to this domain ensures you always have certain spells ready. When you reach a Cleric level specified in the Shadow Domain Spells table, you thereafter always have the listed spells prepared.",
                           spell_table("Shadow Domain Spells", ["Cleric Level", "Spells"], [[l, ", ".join(n)] for l, n in shad_sp])],
      sheet=False, rules=[grant_spell(n, l, "Cleric") for l, ns in shad_sp for n in ns]),
    F(CL2, "Shadowform", ["As a Bonus Action, you can expend a use of your Channel Divinity to take on a shadowy form that grants you the following benefits:",
                        "Shadow Stealth. While you are in an area of Dim Light or Darkness, you can take the Hide action as a Bonus Action.",
                        "Void Empowerment. When you cast a spell using a spell slot that deals Psychic or Necrotic damage, you can add 1d6 to one damage roll of the spell.",
                        "The form lasts for 1 minute, but it ends early if you dismiss it (no action required), if you have the Incapacitated condition, or if you deal Radiant damage with a spell."],
      action="Bonus Action", usage="Channel Divinity"),
    F(CL2, "Devouring Plague", ["When a creature you can see within 30 feet of you fails a saving throw, you can cause that creature to take 1d10 Necrotic damage. If you do, you regain Hit Points equal to the Necrotic damage dealt.",
                              "You can use this feature a number of times equal to your Wisdom modifier (minimum of once), and you regain all expended uses when you finish a Long Rest."],
      usage="{{wisdom:modifier}}/Long Rest", sheet="When a creature you can see within 30 feet fails a saving throw, it takes 1d10 Necrotic damage and you regain that many HP."),
    F(6, "Dispersion", ["When you are hit by an attack roll, you can take a Reaction to disperse into shadowy energy. Until the end of your next turn, you have Resistance to all damage (including the damage from the triggering attack); you can’t take any action, Bonus Action, or Reaction; and you have a Fly Speed of 40 feet. When the effect ends, you can spend up to half of your total Hit Point Dice, regaining Hit Points as if you had finished a Short Rest.",
                        "Once you use this feature, you can’t use it again until you finish a Short or Long Rest."], action="Reaction", usage="1/Short Rest"),
    F(17, "Vampiric Embrace", ["While your Shadowform is active, whenever you roll 1d6 to add extra damage to a spell, one creature of your choice within 30 feet of you regains that many Hit Points."]),
]
archetype(f"{FP}cleric-shadow.xml", "Shadow Domain", "Cleric", "Draw on the Debilitating Power of the Void",
          ["The Shadow Domain deals with the powers of shadow and the Void—a sinister mirror of the life-giving powers of the Light. Clerics who embrace these powers can wither their enemies’ flesh and debilitate their minds."], shad, tag=TAG("Cleric"))

# =====================================================================
# Swashbuckler (Rogue)
# =====================================================================
swash = [
    F(3, "Fancy Footwork", ["You’ve learned how to land a strike and then slip away without reprisal. If you make a melee attack roll against a creature during your turn, that creature can’t make Opportunity Attacks against you for the rest of that turn."]),
    F(3, "Rakish Audacity", ["When you roll Initiative, you can give yourself a bonus to the roll equal to your Charisma modifier.",
                             "You also gain an additional way to use your Sneak Attack: You don’t need Advantage on the attack roll to use your Sneak Attack against a creature if you are within 5 feet of it, no other creatures are within 5 feet of you, and you don’t have Disadvantage on the attack roll. All the other rules for Sneak Attack still apply to you."],
      sheet="You can use Sneak Attack without Advantage against a creature within 5 feet of you if no other creatures are within 5 feet of you and you don’t have Disadvantage.",
      rules=['<stat name="initiative" value="charisma:modifier" />']),
    F(9, "Panache", ["You have practiced new ways to use your Sneak Attack. When you deal Sneak Attack damage, you can forgo a number of the Sneak Attack dice equal to an option’s cost to apply one of the following effects (only one per turn). A saving throw against these effects uses a DC equal to 8 plus your Dexterity modifier and Proficiency Bonus." if E14 else "You have practiced new ways to use your Sneak Attack. The following effects are now among your Cunning Strike options.",
                     "Goad (Cost: 1d6). The target must succeed on a Wisdom saving throw, or until the end of its next turn, the target has Disadvantage on attack rolls against targets other than you and can’t make Opportunity Attacks against targets other than you.",
                     "Awe (Cost: 3d6). Each creature of your choice within 30 feet of you must succeed on a Wisdom saving throw or have the Charmed condition until the end of your next turn."]),
    F(13, "Dashing Strikes", ["You have practiced new ways to use your Sneak Attack. The following effects are added to the options you can choose with your Panache feature." if E14 else "You have practiced new ways to use your Sneak Attack. The following effects are now among your Cunning Strike options.",
                              "Invigorate (Cost: 2d6). Choose a creature you can see within 30 feet of yourself. Until the end of that creature’s next turn, whenever it makes an attack roll or a saving throw, it can roll 1d6 and add the number rolled to the attack roll or saving throw.",
                              "Parrying Stance (Cost: 2d6). Roll 1d6. Until the start of your next turn, you gain a bonus to your AC equal to the number rolled."]),
    F(17, "Master Duelist", ["Immediately after you use your Sneak Attack, you can make another attack against the same target, provided you are within 5 feet of it and no other creatures are within 5 feet of you."]),
]
archetype(f"{FP}rogue-swashbuckler.xml", "Swashbuckler (World of Warcraft)", "Rogue", "Glide into Melee with Panache and Agility",
          ["As a Swashbuckler, you focus on the art of the blade, bringing speed, elegance, and charm to your combat style—topped off with an exquisite flourish of panache. You excel in single combat, and your methods make a duel look like a flamboyant performance."], swash, tag=TAG("Rogue"))

# =====================================================================
# Shaman: Totems (Barbarian addition), Path of the Elements, Spiritual Guardian
# =====================================================================
base = f"{PREFIX}_CLASS_FEATURE_BARBARIAN_SHAMAN"
totem_list = [
    ("Earthbind Totem", "Each enemy in the Emanation has its Speed reduced by 10 feet until the end of your next turn."),
    ("Primal Knowledge Totem", "Each ally in the Emanation is empowered with nature’s focus until the end of your next turn. While empowered in this way, whenever the creature makes an ability check using one of the following skills, the creature can make it as a Strength check even if it normally uses a different ability: Acrobatics, Intimidation, Perception, Stealth, or Survival. After you plant this totem, you can’t do so again until you finish a Long Rest. You can also restore your use of this totem by expending one use of your Rage (no action required)."),
    ("Tremor Totem", "Each ally in the Emanation has Immunity to the Charmed and Frightened conditions until the end of your next turn. If the creature was already Charmed or Frightened, those conditions are suppressed until the end of its next turn."),
    ("Wind Rush Totem", "Each ally in the Emanation has its Speed increased by 10 feet until the end of your next turn."),
]
totems = F(3, "Totems", [("This feature replaces the Barbarian’s Primal Knowledge feature. " if not E14 else "This is an optional addition for shaman; the 2014 Barbarian has no Primal Knowledge feature, so it replaces nothing. ")+"(Shaman are Barbarians in World of Warcraft; adopting the Barbarian class as a shaman increases a character’s Renown Score with the Earthen Ring by 3.)",
                         "You can coalesce elemental spirits into a totem that aids you and your allies. As a Bonus Action, you can plant one of the totems below into the ground in an unoccupied space you can see within 10 feet of yourself.",
                         "A totem is a Small object that has AC 10 and 1 Hit Point and lasts for 1 minute, until it drops to 0 Hit Points, or until you use this feature again. At the end of each of your turns, the totem pulses with elemental energy that fills a 30-foot Emanation."] +
           [f"{n}. {t}" for n, t in totem_list],
           etype="Class Feature", fid=f"{base}_TOTEMS", supports="WoW Shaman Totems 2014" if E14 else "WoW Shaman Totems", grant=False, action="Bonus Action",
           replaces=[] if E14 else [R("BARBARIAN", "PRIMAL_KNOWLEDGE")],
           sheet="Plant a totem (AC 10, 1 HP, 1 minute) within 10 feet; at the end of each of your turns it pulses in a 30-foot Emanation. Earthbind: enemies’ Speed −10 ft. Primal Knowledge (1/Long Rest or 1 Rage): allies use Strength for Acrobatics, Intimidation, Perception, Stealth, Survival checks. Tremor: allies immune to Charmed and Frightened. Wind Rush: allies’ Speed +10 ft.")
totems.alt = "Totems"
totem_append = f'''	<append id="{'ID_WOTC_PHB_CLASS_BARBARIAN' if E14 else 'ID_WOTC_PHB24_CLASS_BARBARIAN'}">
		<rules>
			<select type="Class Feature" name="Shaman Totems (World of Warcraft, optional)" supports="WoW Shaman Totems{' 2014' if E14 else ''}" level="3" optional="true" requirements="!{'ID_WOTC_PHB_MULTICLASS_BARBARIAN' if E14 else 'ID_WOTC_PHB24_MULTICLASS_BARBARIAN'}" />
		</rules>
	</append>'''
write(f"archetypes/{FP}barbarian-shaman-totems.xml", "Shaman Totems", "Shaman Totems option for Barbarians from World of Warcraft (Andrey Kuzinskiy).",
      [totems.xml(base), totem_append])

elem = [
    F(3, "Raging Elements", ["Whenever you activate your Rage, you can take one of the following Raging Elements options of your choice as part of that Bonus Action. While your rage is active, you can take a Bonus Action to use that option again or a different option.",
                             "If a Raging Elements option requires a saving throw, the DC equals 8 plus your Constitution modifier and Proficiency Bonus.",
                             "Icefury. When this effect is activated, roll a number of d8s equal to your Rage Damage bonus, and add them together. You hurl frigid ice at one creature within 30 feet of yourself. Make either a melee spell attack (if the target is within 5 feet) or a ranged spell attack, using Constitution as your spellcasting ability. On a hit, the attack deals Cold damage equal to the number rolled, and the next time the target takes Fire damage before the end of your next turn, it takes an extra 1d10 Fire damage.",
                             "Lava Burst. When this effect is activated, roll a number of d4s equal to your Rage Damage bonus, and add them together. You then hurl molten lava at one creature you can see within 30 feet. The target makes a Dexterity saving throw. On a failed save, the target takes Fire damage equal to the number rolled, and the next time the target takes Lightning damage until the end of your next turn, it takes an extra 1d8 Lightning damage. On a successful save, the target takes half as much damage only.",
                             "Lightning Bolt. When this effect is activated, roll a number of d6s equal to your Rage Damage bonus, and add them together. You can then hurl a bolt of lightning at one other creature you can see within 30 feet. The target makes a Dexterity saving throw. On a failed save, the target takes Lightning damage equal to the roll’s total, and the next time the target takes Cold damage until the end of your next turn, it takes an extra 1d6 Cold damage. On a successful save, the target takes half as much damage only."],
      action="Bonus Action", sheet="When you Rage (and as a Bonus Action while raging): Icefury (spell attack, Rage-bonus d8 Cold, 30 ft), Lava Burst (Dex save, Rage-bonus d4 Fire, 30 ft), or Lightning Bolt (Dex save, Rage-bonus d6 Lightning, 30 ft). Save DC 8 + Con modifier + {{proficiency}}."),
    F(6, "Echo of the Elements", ["You tap into the tranquility of the elements. You know the Elementalism cantrip. In addition, you can expend a use of your Rage to cast Daylight, Water Walk, or Wind Wall. Wisdom is your spellcasting ability for these spells."],
      usage="Rage", rules=['<grant type="Spell" id="ID_WOTC_PHB24_SPELL_ELEMENTALISM" />', '<grant type="Spell" id="ID_WOTC_PHB24_SPELL_DAYLIGHT" />',
                           '<grant type="Spell" id="ID_WOTC_PHB24_SPELL_WATER_WALK" />', '<grant type="Spell" id="ID_WOTC_PHB24_SPELL_WIND_WALL" />']),
    F(10, "Primordial Bond", ["While your Rage is active, you have Resistance to Cold, Fire, and Lightning damage."]),
    F(14, "Elemental Overload", ["The power of the storm you channel grows mightier, lashing out at your foes. Your Raging Elements options gain the following effects.",
                                 "Icefury. Whether or not you hit the target with this option, the target subtracts half the number rolled (round down) from the next damage roll it makes before the start of your next turn.",
                                 "Lava Burst. Whether or not the target fails its saving throw against this option, the target and each enemy within 10 feet of it start burning.",
                                 "Lightning Bolt. Whether or not the target fails its saving throw against this option, a bolt of lightning leaps from the target to another target of your choice that you can see within 30 feet of the first target. The new target makes a Dexterity saving throw, taking Lightning damage equal to the roll’s total on a failed save or half as much damage on a successful one."]),
]
archetype(f"{FP}barbarian-elements.xml", "Path of the Elements", "Barbarian", "Wield the Fury of the Elements",
          ["Barbarians who follow the Path of the Elements learn to harness their Rage into a storm of flames, frost, and lightning. When in their Rage, these Barbarians tap into the elemental forces of nature to create powerful magical effects."], elem, tag=TAG("Barbarian"))
spirit = [
    F(3, "Spiritual Protectors", ["Your Rage summons spectral warriors to your aid. While your Rage is active, when you hit a creature with a weapon or an Unarmed Strike, that creature becomes a target of the spirits, which cause one of the following effects of your choice.",
                                  "Distract. Until the start of your next turn, the target has Disadvantage on attack rolls against targets other than you or another Barbarian who has this feature.",
                                  ("Hinder. The target’s Speed is reduced by 10 feet until the start of your next turn." if E14 else "Hinder. You can activate the Slow mastery property in addition to a different mastery property you’re using with that weapon."),
                                  "Strike. The target takes an extra 1d4 damage, which can be Cold, Fire, or Lightning damage (your choice)."]),
    F(6, "Spirit Shield", ["Your guardian spirits can provide supernatural protection to those you defend. While your Rage is active, when another creature you can see within 30 feet of you takes damage, you can take a Reaction to reduce that damage. To determine the amount the damage is reduced by, roll a number of d6s equal to your Rage Damage bonus, and add them together."], action="Reaction"),
    F(10, "Consult the Spirits", ["You gain the ability to consult with your guardian spirits. When you do so, you cast the Augury or Clairvoyance spell without expending a spell slot or needing Material components. Rather than creating a spherical sensor, this use of Clairvoyance invisibly summons one of your guardian spirits to the chosen location. Wisdom is your spellcasting ability for these spells.",
                                  "After you cast either spell in this way, you can’t use this feature again until you finish a Short or Long Rest."],
      usage="1/Short Rest", rules=['<grant type="Spell" id="ID_WOTC_PHB24_SPELL_AUGURY" />', '<grant type="Spell" id="ID_WOTC_PHB24_SPELL_CLAIRVOYANCE" />']),
    F(14, "Spirits’ Fury", ["Your spirits hasten your attacks. When you make an attack roll with a Melee weapon as part of the Attack action and roll 18–20 on the d20, you can make one additional attack roll with the same weapon as part of that action. Once you use this feature, you can’t do so again until the start of your next turn."]),
]
archetype(f"{FP}barbarian-spiritual-guardian.xml", "Path of the Spiritual Guardian", "Barbarian", "Call on the Spirits for Combat Aid",
          ["Barbarians who walk the Path of the Spiritual Guardian call on spirits—whether bestial spirits of nature, spirits of departed ancestors, or spirits of raw elemental power—to guide and protect them. When these Barbarians rage, they contact the realm of the spirits and call on them for aid."], spirit, tag=TAG("Barbarian"))

if E14:
    LEG = f"{PREFIX}_CLASS_FEATURE_WARLOCK_PACT_BOON_PACT_OF_THE_LEGION"
    write(f"archetypes/{FP}warlock-pact-of-the-legion.xml", "Pact of the Legion", "Pact of the Legion as a 2014 Pact Boon, from World of Warcraft (Andrey Kuzinskiy).", [f'''	<element name="Pact of the Legion" type="Class Feature" source="{SOURCE}" id="{LEG}">
		<supports>Pact Boon</supports>
		<description>
			<p>You learn the <i>Find Familiar</i> spell and can cast it as an action without expending a spell slot. When you cast the spell, you summon a Fel Imp familiar (see chapter 7).</p>
			<p class="indent">Additionally, when you take the Attack action, you can forgo one of your own attacks to allow your familiar to make one attack with its reaction.</p>
			<p class="indent">(In 2014 rules, Pact of the Legion is a Pact Boon gained at Warlock level 3.)</p>
		</description>
		<sheet>
			<description>You can cast Find Familiar without a spell slot, summoning a Fel Imp. You can forgo one of your attacks to let your familiar attack with its reaction.</description>
		</sheet>
		<rules>
			<grant type="Spell" id="ID_WOTC_PHB24_SPELL_FIND_FAMILIAR" />
			<select type="Companion" name="Pact of the Legion Familiar" supports="WoW Legion Familiar" />
		</rules>
	</element>'''])
    print("2014 subclasses written")
    sys.exit(0)

# =====================================================================
# Warrior Maneuvers (Battle Master)
# =====================================================================
base = f"{PREFIX}_ARCHETYPE_FEATURE_MANEUVER"
mans = [
    ("Battle Shout", "As a Bonus Action, you can expend one Superiority Die to shout encouragement to allies within 30 feet of you that can hear you. Until the start of your next turn, each affected ally adds the Superiority Die to the damage roll the next time it hits with a melee attack.", "Bonus Action"),
    ("Demoralizing Shout", "As a Bonus Action, you can expend one Superiority Die to shout, demoralizing enemies within 30 feet of you that can hear you. Until the end of your next turn, each affected enemy subtracts the Superiority Die from the damage roll the next time it hits a target other than you with a melee attack.", "Bonus Action"),
    ("Heroic Leap", "As a Bonus Action, you can expend one Superiority Die to jump a number of feet up to your Strength score. Creatures within 5 feet of you when you land make a Strength saving throw, taking Bludgeoning damage equal to the Superiority Die roll on a failed save, or half as much damage on a successful one.", "Bonus Action"),
    ("Mortal Strike", "When you hit a creature with an attack roll, you can expend one Superiority Die to prevent the target from healing. Add the Superiority Die to the attack’s damage roll. The target can’t regain Hit Points until the end of your next turn.", None),
    ("Warding Maneuver", "When you or a creature you can see within 5 feet of you is hit by an attack roll, you can take a Reaction and expend one Superiority Die if you’re wielding a Melee weapon or a Shield. Add the Superiority Die to the target’s AC against the triggering attack. If the attack still hits, the target has Resistance against the attack’s damage.", "Reaction"),
]
man_el = [option(f"{base}_{slug(n)}", n, [t], "Maneuver, PHB24 Battle Master, Battle Master", sheet=t, usage="Superiority Die", action=a) for n, t, a in mans]
for m in man_el:
    m.compendium = True
write("archetypes/wow-fighter-warrior-maneuvers.xml", "Warrior Maneuvers", "Additional Battle Master maneuvers for World of Warcraft warriors (Andrey Kuzinskiy).",
      [m.xml(base) for m in man_el])

# =====================================================================
# Class spell list additions (Player's Handbook spells)
# =====================================================================
adds = {"Wizard": ["Create Food and Water", "Flame Strike", "Heroes’ Feast"],
        "Cleric": ["Mind Sliver", "Blur", "Levitate", "Haste", "Summon Undead", "Dominate Person", "Dominate Monster"]}
ap = []
for cls, names in adds.items():
    for n in names:
        ap.append(f'\t<append id="ID_WOTC_PHB24_SPELL_{slug(n)}">\n\t\t<supports>{cls}</supports>\n\t</append>')
write("spells/wow-spell-list-additions.xml", "Spell List Additions",
      "Player’s Handbook spells added to the Wizard (mage) and Cleric (priest) spell lists in World of Warcraft (Andrey Kuzinskiy).", ap)
print("subclasses written")
