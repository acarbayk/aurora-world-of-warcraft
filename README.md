# World of Warcraft for Aurora Builder

Aurora Builder content for **World of Warcraft**, a fan-made D&D 5e (2024 rules) sourcebook by **Andrey Kuzinskiy**. This is an unofficial fan conversion. World of Warcraft is a trademark of Blizzard Entertainment.

## Requirements

- Aurora Builder with the **Aurora Legacy Player's Handbook (2024)** content loaded (`https://raw.githubusercontent.com/AuroraLegacy/elements/master/core.index`). The classes in this book are built on the 2024 classes and won't work without them.

## Installation

1. Open Aurora → **Start → Additional Content**.
2. Paste this URL into **Remote .index file URL** and click **Download**:
   ```
   https://raw.githubusercontent.com/acarbayk/aurora-world-of-warcraft/main/world-of-warcraft.index
   ```
3. Click **Update Content Files**, then restart Aurora.

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
