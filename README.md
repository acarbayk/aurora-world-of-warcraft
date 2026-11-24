# World of Warcraft for Aurora Builder

Aurora Builder content for **World of Warcraft**, a fan-made D&D 5e (2024 rules) sourcebook by **Andrey Kuzinskiy**. This is an unofficial fan conversion. World of Warcraft is a trademark of Blizzard Entertainment.

## Requirements

- Aurora Builder with the **Aurora Legacy Player's Handbook (2024)** content loaded (`https://raw.githubusercontent.com/AuroraLegacy/elements/master/core.index`). The classes in this book are built on the 2024 classes and won't work without them.

## Installation

1. Open Aurora → **Start → Additional Content**.
2. Paste one of these URLs into **Remote .index file URL** and click **Download**:
   - 2024 rules (as written in the book):
     ```
     https://raw.githubusercontent.com/acarbayk/aurora-world-of-warcraft/main/world-of-warcraft.index
     ```
   - 2014 rules (subclasses and class options adapted to the 2014 Player's Handbook classes):
     ```
     https://raw.githubusercontent.com/acarbayk/aurora-world-of-warcraft/main/world-of-warcraft-2014.index
     ```
3. Click **Update Content Files**, then restart Aurora.

You can load both. The 2014 subclasses use the source "World of Warcraft (2014)", so you can switch either set on or off in **Start → Sources**. Species, spells, feats, items and renown are shared by both versions.

### 2014 adaptation notes

The book is written for the 2024 rules. The 2014 version is an unofficial adaptation:
- Death Knight replaces Lay on Hands, Divine Smite, Improved Divine Smite and Cleansing Touch; Demon Hunter replaces Feral Senses; Void Warrior is a Ranger Fighting Style option.
- Evoker Spells (Draconic Bloodline, level 1), Pet Specialization (Beast Master, level 6), Shaman Totems (Barbarian, level 3) and Cat/Bear Form (Circle of the Moon, level 2) are optional additions; in 2014 they don't replace anything.
- Swashbuckler's Panache options are paid for by giving up Sneak Attack dice. Spiritual Guardian's Hinder reduces Speed by 10 feet instead of using Weapon Mastery.
- Pact of the Legion is a Pact Boon. The other new invocations work with both warlocks.
- Focus Points become ki points, Bloodied becomes "half Hit Points or fewer", Heroic Inspiration becomes Inspiration and the Magic action becomes an action, Emanations become radii or "within X feet" and Hit Point Dice become Hit Dice.
- The Hunter pet table has no Mastery column in 2014 (the 2014 Ranger has no Weapon Mastery). Pet Specialization and Shaman Totems replace nothing in 2014, because the 2014 Ranger and Barbarian have no Roving or Primal Knowledge.
- 2014 subclasses use the 2014 spell IDs (Player's Handbook, Xanathar's, Tasha's) wherever one exists. Arcane Vigor, Elementalism and Summon Dragon only exist in the 2024 Player's Handbook, so the 2014 version still needs it for those three.
- Discipline and Shadow Domain follow the 2014 domain pattern: domain spells at Cleric levels 1, 3, 5, 7 and 9 (by spell level), the Channel Divinity features (Holy Bolt, Shadowform) and Atonement / Devouring Plague at level 2, then levels 6 and 17 as in the book.

## What's included

| Part | Contents |
|---|---|
| Species | Dracthyr, Draenei, Dwarf, Earthen, Elf (Blood, High, Night, Nightborne, Void), Forsaken, Gnome, Mechagnome, Goblin, Haranir, Human, Orc, Pandaren, Tauren, Troll, Vulpera, Worgen |
| Languages | All Alliance, Horde and rare languages of Azeroth |
| Subclasses | Oath of the Ebon Blade (Death Knight), Demon Hunter, Oath of the Holy, Discipline Domain, Shadow Domain, Warrior of Mystic Brews, Swashbuckler, Path of the Elements, Path of the Spiritual Guardian |
| Class options | Evoker (optional for Draconic Sorcery), Hunter Pet Specialization (optional for Beast Master), Shaman Totems (optional for Barbarian), Cat Form and Bear Form (optional for Circle of the Moon), warrior maneuvers for Battle Master |
| Spells | 69 new spells, plus Player's Handbook spells added to the Wizard and Cleric lists |
| Feats | Mage, monk and inscription General feats; human Origin feats; Void Warrior fighting style option |
| Eldritch Invocations | Pact of the Legion, Call of the Void, Curse of Corruption, Expendable Minions, Health Funnel, Legion Summoning, Master Demonologist |
| Equipment | 26 magic items, mounts, powered vehicles, companion creature types |
| Renown | General rules and all faction renown perks (Equipment tab, category "Renown Perks") |
| Companions | Fel Imp, Voidwalker, Felguard, Felhound, Mechanostrider, Pandarian Dragon Turtle |

Optional class options (Evoker, Pet Specialization, Shaman Totems, Cat/Bear Form) appear as optional selections at the right level in the class or subclass they modify.

Not included: the specialization guides (they are advice, not rules), profession crafting rules, and chapters 5–7 (lore, adventures, bestiary). Aurora is a character builder.

## Known limitations

- Hero classes (Death Knight, Demon Hunter) change level 1–2 features. In Aurora those features apply once the subclass is chosen at level 3, which matches the book's default of starting hero classes at level 3.
- Resource pools such as Runic Power or Soul Fragments are shown on the sheet with usage counts; Aurora doesn't track them automatically.

## Maintenance

`tools/` holds the Python scripts that generated the XML from the book text and `tools/build.py`, which rebuilds the index and validates every file (well-formed XML, unique ids, every referenced id exists in this content or in Aurora Legacy).

## Credits

- Book: Andrey Kuzinskiy
- Aurora conversion: Kaya Acarbay
