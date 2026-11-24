"""Feats and Eldritch Invocations."""
import sys
sys.path.insert(0, "/home/claude/tools")
from sublib import html
from textfmt import escape, slug
from common import header, footer, SOURCE, PREFIX, ROOT

ASI = lambda *ab: "|".join(f"ID_INTERNAL_ABILITY_SCORE_IMPROVEMENT_FEAT_{a.upper()}" for a in ab)


def feat(name, kind, prereq_text, req, paras, sheet, rules=(), supports=None, usage=None, action=None, fid=None, etype="Feat", flavor=True):
    fid = fid or f"{PREFIX}_FEAT_{slug(name)}"
    x = [f'\t<element name="{escape(name)}" type="{etype}" source="{SOURCE}" id="{fid}">',
         f"\t\t<supports>{supports or kind}</supports>"]
    if req:
        x.append(f"\t\t<requirements>{req}</requirements>")
    if prereq_text:
        x.append(f"\t\t<prerequisite>{escape(prereq_text)}</prerequisite>")
    x.append("\t\t<description>")
    if flavor:
        fl = f"{kind} Feat" + (f" (Prerequisite: {prereq_text})" if prereq_text else "")
        x.append(f'\t\t\t<p class="flavor">{escape(fl)}</p>')
    elif prereq_text:
        x.append(f"\t\t\t<p><em>Prerequisite: {escape(prereq_text)}</em></p>")
    x += ["\t\t\t" + h for h in html(paras)]
    x.append("\t\t</description>")
    a = (f' action="{action}"' if action else "") + (f' usage="{usage}"' if usage else "")
    x.append(f"\t\t<sheet{a}>\n\t\t\t<description>{escape(sheet)}</description>\n\t\t</sheet>")
    if rules:
        x.append("\t\t<rules>")
        x += ["\t\t\t" + r for r in rules]
        x.append("\t\t</rules>")
    x.append("\t</element>")
    return "\n".join(x)


def write(path, name, desc, elements):
    open(f"{ROOT}/world-of-warcraft/{path}", "w").write(header(path, name, desc) + "\n\n".join(elements) + footer())


U = "||ID_WOTC_PHB24_GRANTS_FEAT_UNLOCKER"
G4 = f"[character:4]{U}"
G4DW = f"([character:4],[dex:13],[wis:13]){U}"
ints = f'<select type="Ability Score Improvement" name="Ability Score Increase ({{}})" supports="{ASI("Intelligence")}" />'
dexwis = '<select type="Ability Score Improvement" name="Ability Score Increase ({})" supports="' + ASI("Dexterity", "Wisdom") + '" />'

general = [
    feat("Clearcasting", "General", "Level 4+", G4,
         ["You gain the following benefits.", "Ability Score Increase. Increase your Intelligence score by 1, to a maximum of 20.",
          "Clearcasting. When you score a Critical Hit with a spell’s attack roll, you can take a Reaction to cast a cantrip with a casting time of an action.",
          "Force Adept. When you roll damage for a spell you cast that deals Force damage, you can treat any 1 on a damage die as a 2."],
         "When you score a Critical Hit with a spell attack, you can take a Reaction to cast a cantrip with a casting time of an action. You can treat any 1 on a Force damage die of your spells as a 2.",
         rules=[ints.replace("{}", "Clearcasting")]),
    feat("Fingers of Frost", "General", "Level 4+", G4,
         ["You gain the following benefits.", "Ability Score Increase. Increase your Intelligence score by 1, to a maximum of 20.",
          "Cold Mastery. Spells you cast ignore Resistance to Cold damage.",
          "Frostbite. When you deal Cold damage to a creature that has the Restrained condition, the creature takes extra Cold damage. To determine the extra damage, roll a number of d4s equal to your Proficiency Bonus and add them together."],
         "Your spells ignore Resistance to Cold damage. When you deal Cold damage to a Restrained creature, it takes an extra {{proficiency}}d4 Cold damage.",
         rules=[ints.replace("{}", "Fingers of Frost")]),
    feat("Hot Streak", "General", "Level 4+", G4,
         ["You gain the following benefits.", "Ability Score Increase. Increase your Intelligence score by 1, to a maximum of 20.",
          "Fire Mastery. Spells you cast ignore Resistance to Fire damage.",
          "Ignite. When a spell you cast deals Fire damage to a creature, the target starts burning. When you deal Fire damage to a creature that is already burning, the flames become more severe, increasing the burning damage by 1d4."],
         "Your spells ignore Resistance to Fire damage. When your spell deals Fire damage, the target starts burning; dealing Fire damage to a burning creature increases its burning damage by 1d4.",
         rules=[ints.replace("{}", "Hot Streak")]),
    feat("Elusive Brawler", "General", "Level 4+, Dexterity and Wisdom 13+", G4DW,
         ["You gain the following benefits.", "Ability Score Increase. Increase your Dexterity or Wisdom score by 1, to a maximum of 20.",
          "Reactive Dodge. When you take damage, you can take a Reaction to take the Dodge action."],
         "When you take damage, you can take a Reaction to take the Dodge action.", action="Reaction",
         rules=[dexwis.format("Elusive Brawler")]),
    feat("Enveloping Mist", "General", "Level 4+, Dexterity and Wisdom 13+", G4DW,
         ["You gain the following benefits.", "Ability Score Increase. Increase your Dexterity or Wisdom score by 1, to a maximum of 20.",
          "Enveloping Mist. When you cast a spell or use a feature to restore Hit Points to a creature, the creature is wrapped in a healing mist. Roll one of the dice from the feature that healed it, and note that number as the creature’s Life Cocoon value.",
          "If the creature is hit by an attack roll before the start of its next turn, you can take a Reaction to reduce the damage it takes from that attack by its Life Cocoon value. The mist then disappears.",
          "At the start of the creature’s next turn, if the mist persists, the creature gains Temporary Hit Points equal to its Life Cocoon value."],
         "When you heal a creature, roll one of the healing dice as its Life Cocoon value. If it’s hit before its next turn, Reaction: reduce the damage by that value; otherwise it gains that many Temporary Hit Points at the start of its turn.",
         rules=[dexwis.format("Enveloping Mist")]),
    feat("Fists of Fury", "General", "Level 4+, Dexterity and Wisdom 13+", G4DW,
         ["You gain the following benefits.", "Ability Score Increase. Increase your Dexterity or Wisdom score by 1, to a maximum of 20.",
          "Clean Hits. When you roll damage for an attack you make with an Unarmed Strike or a weapon that has the Light property, you can treat any 1 on a damage die as a 2.",
          "Combo Strikes. When you deal damage to a creature with an Unarmed Strike, you gain a +1 bonus to the damage roll for each time you previously hit that creature with a melee attack roll in the same turn."],
         "Treat 1s on damage dice of Unarmed Strikes and Light weapons as 2s. Unarmed Strike damage gains +1 for each earlier melee hit on the same creature this turn.",
         rules=[dexwis.format("Fists of Fury")]),
    feat("Stagger and Sway", "General", "Level 4+, Dexterity and Wisdom 13+", G4DW,
         ["You gain the following benefits.", "Ability Score Increase. Increase your Dexterity or Wisdom score by 1, to a maximum of 20.",
          "Defer Damage. When you take damage, reduce the damage you take by your Dexterity modifier (minimum of 1). Then add a d6 to your Delayed Reaction pool. At the end of your turn, remove all the dice from your Delayed Reaction pool and roll them. You take Force damage equal to the total rolled.",
          "Purify. As a Bonus Action, you can remove a number of dice equal to your Wisdom modifier from your Delayed Reaction pool."],
         "When you take damage, reduce it by {{dexterity:modifier}} (minimum 1) and add a d6 to your Delayed Reaction pool; at the end of your turn, take Force damage equal to the pool’s roll. Bonus Action: remove {{wisdom:modifier}} dice from the pool.",
         rules=[dexwis.format("Stagger and Sway")]),
    feat("Inscription Adept", "General", "Level 4+, Proficiency with Calligrapher’s Supplies, Cartographer’s Tools, or Painter’s Supplies",
         f"([character:4],(ID_PROFICIENCY_TOOL_PROFICIENCY_CALLIGRAPHERS_SUPPLIES||ID_PROFICIENCY_TOOL_PROFICIENCY_CARTOGRAPHERS_TOOLS||ID_PROFICIENCY_TOOL_PROFICIENCY_PAINTERS_SUPPLIES)){U}",
         ["Your mastery of inscription allows you to duplicate the effects of certain spells with your written magic. You gain the following benefits.",
          "Ability Score Increase. Increase your Intelligence, Wisdom, or Charisma score by 1, to a maximum of 20.",
          "Inscription Magic. You learn the Illusory Script spell and always have it prepared. You can cast it once without a spell slot, and you regain the ability to cast it in that way when you finish a Long Rest. You can also cast the spell using any spell slots you have of the appropriate level. You can use herbalism resources of the appropriate value in place of the Material component specified for that spell. The spell’s spellcasting ability is the ability increased by this feat.",
          "When you reach higher levels of proficiency in inscription, you learn higher-level spells and can cast them in the same way, as shown on the table.",
          '<table><thead><tr><td>Proficiency</td><td>Spell</td></tr></thead><tr><td>Journeyman (+3)</td><td><i>Glyph of Warding</i></td></tr><tr><td>Artisan (+5)</td><td><i>Symbol</i></td></tr></table>'],
         "You can cast Illusory Script (and Glyph of Warding at Proficiency Bonus +3, Symbol at +5) once each per Long Rest without a spell slot; herbalism resources can replace their Material components.",
         rules=[f'<select type="Ability Score Improvement" name="Ability Score Increase (Inscription Adept)" supports="{ASI("Intelligence", "Wisdom", "Charisma")}" />',
                '<grant type="Spell" id="ID_WOTC_PHB24_SPELL_ILLUSORY_SCRIPT" />',
                '<grant type="Spell" id="ID_WOTC_PHB24_SPELL_GLYPH_OF_WARDING" level="5" />',
                '<grant type="Spell" id="ID_WOTC_PHB24_SPELL_SYMBOL" level="13" />']),
]
write("feats/wow-feats-general.xml", "General Feats", "New General feats from World of Warcraft (Andrey Kuzinskiy): mage, monk and inscription feats.", general)

HUMAN = f"(ID_INTERNAL_GRANT_RACE_HUMAN||{PREFIX}_RACE_HUMAN_AZEROTH){U}"
origin = [
    feat("Arathi Heritage", "Origin", "World of Warcraft Campaign, Human Species", HUMAN,
         ["As a descendant of humans from Arathor and high elves from Quel’Thalas, you gain the following benefits.",
          "Fey Ancestry. You have Advantage on saving throws to avoid or end the Charmed condition.",
          "Lethargy Resilience. When you fail a saving throw to avoid or end the Unconscious condition, you can succeed instead. Once you use this trait, you can’t do so again until you finish 1d4 Long Rests."],
         "You have Advantage on saving throws to avoid or end the Charmed condition. Once per 1d4 Long Rests, when you fail a save to avoid or end the Unconscious condition, you can succeed instead."),
    feat("Child of the Sea", "Origin", "World of Warcraft Campaign, Human Species", HUMAN,
         ["As a Kul Tiran, you gain the following benefits.",
          "Lasting Breath. You can hold your breath for a number of minutes equal to 2 plus your Constitution modifier (minimum of 1 minute).",
          "Ocean Born. You have a Swim Speed equal to your Speed."],
         "You can hold your breath for 2 + {{constitution:modifier}} minutes (minimum 1). You have a Swim Speed equal to your Speed.",
         rules=['<stat name="innate speed:swim" value="innate speed" bonus="base" />']),
    feat("Will to Survive", "Origin", "World of Warcraft Campaign, Human Species", HUMAN,
         ["When you have the Incapacitated condition but not the Unconscious condition, you can draw on the proud heritage of Stormwind or Stromgarde to ignore the Incapacitated condition on your turn. If you do, you gain 1 Exhaustion level."],
         "When you are Incapacitated but not Unconscious, you can ignore the Incapacitated condition on your turn; if you do, you gain 1 Exhaustion level."),
]
write("feats/wow-feats-origin.xml", "Origin Feats", "Human Origin feats from World of Warcraft (Andrey Kuzinskiy).", origin)

# ---------------------------------------------------------------- Eldritch Invocations
INV = "PHB24 Eldritch Invocation"
LEGION = f"{PREFIX}_CLASS_FEATURE_ELDRITCH_INVOCATION_PACT_OF_THE_LEGION"
inv = lambda name, prereq, req, paras, sheet, rules=(), usage=None, action=None: feat(
    name, "Eldritch Invocation", prereq, req, paras, sheet, rules=rules, supports=INV, usage=usage, action=action,
    fid=f"{PREFIX}_CLASS_FEATURE_ELDRITCH_INVOCATION_{slug(name)}", etype="Class Feature", flavor=False)
invs = [
    inv("Pact of the Legion", "", "", [
        "You learn the Find Familiar spell and can cast it as a Magic action without expending a spell slot. When you cast the spell, you summon a Fel Imp familiar (see chapter 7).",
        "Additionally, when you take the Attack action, you can forgo one of your own attacks to allow your familiar to make one attack with its Reaction."],
        "You can cast Find Familiar without a spell slot, summoning a Fel Imp. You can forgo one of your attacks to let your familiar attack with its Reaction.",
        rules=['<grant type="Spell" id="ID_WOTC_PHB24_SPELL_FIND_FAMILIAR" />',
               '<select type="Companion" name="Pact of the Legion Familiar" supports="WoW Legion Familiar" />']),
    inv("Call of the Void", "Level 5+ Warlock, Pact of the Legion Invocation", f"[level:warlock:5],{LEGION}", [
        "When you cast Find Familiar using Pact of the Legion, you can choose to summon a Fel Imp familiar or a Voidwalker (see chapter 7 for both stat blocks). In addition, you gain the following benefits.",
        "Quick Attack. As a Bonus Action, you can command the familiar to take the Attack action.",
        "Your Spell Attack. The familiar uses your spell attack bonus for its attacks.",
        "Shadow Shield. When your Voidwalker familiar takes damage, you can take a Reaction to grant it Resistance against that damage."],
        "Your Pact of the Legion familiar can be a Fel Imp or a Voidwalker. Bonus Action: command the familiar to Attack; it uses your spell attack bonus. Reaction: give your Voidwalker Resistance to damage it takes."),
    inv("Curse of Corruption", "Level 2+ Warlock", "[level:warlock:2]", [
        "When an enemy starts its turn cursed by a Warlock spell you cast (such as Hex), it must succeed on a Charisma saving throw or take Necrotic damage equal to your Charisma modifier."],
        "When an enemy starts its turn cursed by your Warlock spell, it makes a Charisma save (DC {{warlock:spellcasting:dc}}) or takes {{charisma:modifier}} Necrotic damage."),
    inv("Expendable Minions", "Level 9+ Warlock", "[level:warlock:9]", [
        "When your familiar or a summoned creature you control dies, you or another creature within 60 feet of you regains Hit Points equal to your Warlock level plus your Charisma modifier."],
        "When your familiar or a summoned creature you control dies, you or a creature within 60 feet regains {{level:warlock}} + {{charisma:modifier}} HP."),
    inv("Health Funnel", "Level 2+ Warlock", "[level:warlock:2]", [
        "As a Bonus Action, you can expend any number of your unexpended Hit Dice to roll those dice, add your Charisma modifier to each die, and total the rolls. Your familiar or another Fiend you command gains that many Temporary Hit Points."],
        "Expend Hit Dice and roll them, adding {{charisma:modifier}} to each; your familiar or a Fiend you command gains that many Temporary Hit Points.", action="Bonus Action"),
    inv("Legion Summoning", "Level 9+ Warlock, Pact of the Legion Invocation", f"[level:warlock:9],{LEGION}", [
        "You can cast Planar Binding without expending a spell slot. When you do, you summon a Felguard, a Felhound, an Incubus, or a Succubus, and that Fiend becomes the target of the spell. (Felguards and felhounds are described in chapter 7.) Once you cast the spell in this way, you can’t do so again until you finish a Long Rest."],
        "Cast Planar Binding without a spell slot, summoning a Felguard, Felhound, Incubus, or Succubus as its target.", usage="1/Long Rest",
        rules=['<grant type="Spell" id="ID_WOTC_PHB24_SPELL_PLANAR_BINDING" />', '<select type="Companion" name="Legion Summoning" supports="WoW Legion Summon" optional="true" />']),
    inv("Master Demonologist", "Level 5+ Warlock", "[level:warlock:5]", [
        "Any Fiends you command also deal extra damage to the target of your Hex spell as if they were you."],
        "Fiends you command also deal Hex’s extra damage to its target."),
]
write("feats/wow-eldritch-invocations.xml", "Eldritch Invocations", "New Eldritch Invocations from World of Warcraft (Andrey Kuzinskiy).", invs)
print("feats written")
