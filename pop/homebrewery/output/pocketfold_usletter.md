<!-- BEGIN Style -->
<style>

/* ===== Page ===== */

/* The page: US Letter portrait, blank, laid out by us (not by the theme) */
.page
{
  /* US Letter width */
  width: 8.5in;
  /* US Letter height (portrait: taller than wide, so boxes are wider than tall) */
  height: 11in;
  
  /* the 1em padding below counts INSIDE the 8.5in x 11in, so the page is exactly paper size */
  box-sizing: border-box;
  /* blank white background (overrides the theme's parchment image / theme color) */
  background: white;
  
  /* gap between content and the page edge, top */
  padding-top: 1em;
  /* gap between content and the page edge, right */
  padding-right: 1em;
  /* gap between content and the page edge, bottom */
  padding-bottom: 1em;
  /* gap between content and the page edge, left */
  padding-left: 1em;
  
  /* the theme lays the page out as two PHB-style columns; force one so we control placement */
  column-count: 1;
  /* the theme pins the column width to 8cm and children inherit it; reset so it can't distort ours */
  column-width: auto;
}

/* the theme adds a 50px footer image bar along the page bottom; remove it */
.page::after
{
  content: none;
}

/* ===== Wrapper ===== */

/* Homebrewery wraps all content in this div; the theme turns it into a column container
   that inherits from the page. Make it a plain block that fills the page, so the
   percentage heights below have a definite size to measure against. */
.columnWrapper
{
  /* don't inherit the page's columns */
  column-count: 1;
  column-width: auto;
  /* fill the page's content area (the page minus its 1em padding) */
  height: 100%;
}

/* the {{wide}} block: the whole working area inside the page's padding */
.block.wide
{
  /* fill the wrapper (= the page's content area) */
  height: 100%;
  /* the theme adds margins around wide blocks; remove them */
  margin: 0;
  padding: 0;
}

/* ===== Page 1 (front side) ===== */

/* Page 1 (the front side of the paper) does NOT use the page-2 rows: it holds
   two big boxes directly in the wide block, one per half of the page. Make
   page 1's wide a two-row grid so each big box gets exactly half of the
   page's height (both boxes come out the same size: full page width, half
   page height). */
#p1 .block.wide
{
  display: grid;
  grid-template-rows: repeat(2, 1fr);
}

/* The single fold line on this side of the paper is the MIDDLE of the page;
   the two half-page boxes each give up 0.35em on that side, so the
   0.7em gap between them is centered exactly on the fold line. */
#p1 .block.wide > .box:first-child
{
  /* the top box ends 0.35em above the middle fold line */
  height: calc(100% - 0.35em);
}
#p1 .block.wide > .box:last-child
{
  /* the bottom box starts 0.35em below the middle fold line */
  margin-top: 0.35em;
  height: calc(100% - 0.35em);
}

/* ===== Octet boxes ===== */

/* every box: green planning border, content clipped to the box.
   (Each box's size is set by the version-specific fold-line rules above and
   in the version template — see the row/grid rules there.) */
.block.box
{
  /* the theme makes every .block an inline-block at 100% width;
     force a plain block that sits cleanly in its grid cell */
  display: block;
  width: auto;
  /* green border marking the octet's working area (remove when planning is done) */
  border: 0px solid green;
  /* content that overflows the box is clipped instead of spilling into its neighbor */
  overflow: hidden;
  /* anchor for the {{left block (positioned absolutely inside the box);
     does nothing for boxes that don't contain one */
  position: relative;
}

/* optional flip: wrap a box's content in {{invert ... }} to print the box upside-down.
   The content is anchored at the box's BOTTOM edge and flows UPWARD, and every line is
   rotated 180 degrees. So when the folded box is physically flipped, line one is at the
   top and everything reads normally. (A plain rotate of the whole content would leave
   it anchored at the top of the box — that is not a real flip.) */
.block.invert
{
  /* fill the box so that "bottom" below means the box's bottom edge */
  height: 100%;
  /* flexbox so the lines can be stacked from the bottom edge upward */
  display: flex;
  /* the first line sits at the bottom; each following line stacks above it */
  flex-direction: column-reverse;
}
/* rotate every line 180 degrees (upside-down on paper, right-side-up when flipped) */
.block.invert > *
{
  transform: rotate(180deg);
}
  
/* \column markers between boxes are not needed (the grid places the boxes); hide any that exist */
.columnSplit
{
  display: none;
}

/* ===== Tables ===== */

h3 {
  text-align: center;
}

.template {
  font-size: 8pt;
  text-align: center;
  font-style: italic;
}

.credits {
  font-size: 6pt;
  text-align: center;
  font-style: italic;
}

.page table thead tr th
{
  vertical-align: middle;
  font-size: 10pt;
}
  
.page table tbody tr td
{
  vertical-align: middle;
  font-size: 10pt;
}

.page li
{
  font-size: 8pt;
}

.horizontal-compact table thead tr th
{
  font-size: 8pt;
}
  
.horizontal-compact table tbody tr td
{
  font-size: 8pt;
}

.vertical-compact table thead tr th
{
  line-height: 130%;
}
  
.vertical-compact table tbody tr td
{
  line-height: 130%;
}

.treasure table tbody tr td
{
  font-size: 8pt;
  line-height: 100%;
}
  
/* ===== Page 2 (back side) ===== */

/* four rows; each row is a 2-column grid. (Page 2 uses these rows; page 1
   instead has two big half-page boxes — see the #p1 rules in the shared
   block.) The rows' heights are set just below, measured against the PAPER
   so that the gaps between the rows center on the fold lines (see the box
   rules under them). */
.block.row1, .block.row2, .block.row3, .block.row4
{
  /* make the row a grid with two equal-width columns for its two boxes */
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  /* 0.7em of space between the two boxes of a row; its center lands exactly
     on the paper's middle vertical fold line (the page is symmetric), so it
     needs no adjustment */
  column-gap: 0.7em;
  /* no theme margins around rows (the vertical gap comes from the boxes, below) */
  margin: 0;
}

/* The horizontal fold lines run at 1/4, 1/2 and 3/4 of the paper's FULL
   height — they do not know about the 1em margins — so the rows'
   boundaries are measured from the paper, not from the working area: row 1
   runs from the top margin to the 1/4 fold, rows 2 and 3 each run
   fold-to-fold, and row 4 runs from the 3/4 fold to the bottom margin. */
.block.row1, .block.row4
{
  /* a quarter of the paper's height (2.75in), minus the 1em margin at the outer edge */
  height: calc(2.75in - 1em);
}
.block.row2, .block.row3
{
  /* a full quarter of the paper's height (2.75in; they run between two fold lines) */
  height: 2.75in;
}

/* The 0.7em gap between two rows must be centered on the fold line
   between them: 0.35em of the gap on each side of the line. So a
   box that borders a fold line gives up 0.35em on that side — the
   row 1 and row 4 boxes on one side only, and the row 2 and row 3 boxes on
   BOTH sides. */
.block.row1 .block.box
{
  /* keeps the whole row except 0.35em at its bottom (the near half of the 1/4 gap) */
  height: calc(100% - 0.35em);
}
.block.row2 .block.box,
.block.row3 .block.box
{
  /* 0.35em of gap above the box; the box ends 0.35em short of the row's bottom */
  margin-top: 0.35em;
  height: calc(100% - 0.7em);
}
.block.row4 .block.box
{
  /* 0.35em of gap above the box; the box keeps the rest of the row */
  margin-top: 0.35em;
  height: calc(100% - 0.35em);
}

/* ===== Sideways boxes ===== */

/* optional sideways: wrap a box's content in {{left ... }} to rotate the box 270 degrees.
   The block's top edge ends up at the box's LEFT edge: the heading (and its underline)
   runs vertically down the left side, and the lines of text fill in from left to right.
   Two things are both required, and missing either one breaks it:
   1. SWAP the block's dimensions — before the rotation it must be as wide as the box is
      tall and as tall as the box is wide, so that AFTER the rotation its shape matches
      the box. (A block that is not swapped keeps the box's own width and height, and
      rotated its shape no longer fits the box — most of it ends up clipped away.)
   2. CENTER the block in the box before rotating — a transform spins an element around
       its own center, so first move the element's center onto the box's center.
   The swapped dimensions depend on which box the block sits in (the page 2 boxes
   come in two sizes after the fold-line rules above), so the width/height are set
   by the per-row size rules right below. */
.block.left
{
  /* park the element's center on the box's center (the box needs position: relative) */
  position: absolute;
  top: 50%;
  left: 50%;
  /* then shift the element so its center sits on that point, and rotate 270 degrees
     clockwise around its center */
  transform: translate(-50%, -50%) rotate(270deg);
  /* the width/height come from the per-row rules below (they swap the box's
     dimensions: before rotation the block is as wide as the box is tall and as
     tall as the box is wide, so that after the rotation it fills the box) */
  /* plain block (the theme would otherwise make it an inline-block) */
  display: block;
}

.block.right
{
  /* park the element's center on the box's center (the box needs position: relative) */
  position: absolute;
  top: 50%;
  left: 50%;
  /* then shift the element so its center sits on that point, and rotate 90 degrees
     clockwise around its center */
  transform: translate(-50%, -50%) rotate(90deg);
  /* the width/height come from the per-row rules below (they swap the box's
     dimensions: before rotation the block is as wide as the box is tall and as
     tall as the box is wide, so that after the rotation it fills the box) */
  /* plain block (the theme would otherwise make it an inline-block) */
  display: block;
}

/* the swapped dimensions, per row. Rows 1 and 4 hold the SHORTER boxes (a
   paper quarter (2.75in) minus the 1em outer margin and the
   0.35em fold-side slack: calc(2.75in - 1em) tall); rows 2 and 3 hold
   the full boxes (a paper quarter minus 0.35em on each side:
   2.75in tall). Before rotation the block is as wide as its box is
   TALL and as tall as its box is WIDE, so that after the 90-degree rotation
   it fills the box exactly. All the boxes are the same width (a half of the
   page's content area minus half the 0.7em gap). */
.block.row1 .block.left, .block.row1 .block.right,
.block.row4 .block.left, .block.row4 .block.right
{
  /* as wide as the short box is tall */
  width: calc(2.75in - 1.35em);
  /* as tall as the box is wide */
  height: calc(4.25in - 1.35em);
}
.block.row2 .block.left, .block.row2 .block.right,
.block.row3 .block.left, .block.row3 .block.right
{
  /* as wide as the full box is tall */
  width: calc(2.75in - 0.7em);
  /* as tall as the box is wide */
  height: calc(4.25in - 1.35em);
}
</style>
<!-- END Style -->

<!-- START FRONT PAGE -->
{{wide

<!-- START BOX 17 -->
{{box

{{column-count:2

### Quest

{{template

A [**Trait**] [**Person**], concerned about [**Motive**], asks you to  
[**Objective**] the [**Description**] [**Focus**] in the [**Dungeon**] of [**Adjective**] [**Noun**],  
[**Complication**].

}}

{{horizontal-compact

|   #   |      Objective       | Description |       Focus       |         Complication          |
|:-----:|:--------------------:|:-----------:|:-----------------:|:-----------------------------:|
| **1** |  Attain power from   |  Abandoned  |      Anomaly      |      before time expires      |
| **2** |       Destroy        | Artificial  |      Faction      |  before the ritual completes  |
| **3** |     Escape from      |   Astral    |    Information    |      before they escape       |
| **4** |  Escort someone to   |  Connected  |      Monster      |       while outmatched        |
| **5** |      Infiltrate      |   Decayed   |       Seal        |      while being hunted       |
| **6** |     Investigate      |  Defended   |        NPC        |    against a rival faction    |
| **7** |    Negotiate with    |  Elemental  | Object / Treasure |         amid betrayal         |
| **8** |       Protect        |   Hidden    |      Remains      | though nothing is as it seems |
| **9** | Rescue someone from  |   Strange   |       Plant       |     under false pretenses     |
| **0** | Steal something from |    Toxic    |      Villain      |    while enemies converge     |

{{column-count:2

:

### Person

|   #   |   Trait   |   Person    | Motive / Topic |
|:-----:|:---------:|:-----------:|:--------------:|
| **1** | Deceiving |  Criminal   |   Equipment    |
| **2** | Guarding  | Entertainer |   Experience   |
| **3** |  Guiding  |   Expert    |     Family     |
| **4** |  Hunting  |    Mage     |     Flaws      |
| **5** |   Lost    |  Mercenary  |    History     |
| **6** |  Spying   |    Noble    |     Quest      |
| **7** |  Tasked   |   Priest    |   Reputation   |
| **8** |  Trading  |   Ranger    |   Superiors    |
| **9** |  Trapped  |   Soldier   |    Treasure    |
| **0** |  Wounded  | Transporter |     Wealth     |

\column

:

### Location

|   #   |  Dungeon  |  Adjective   |   Noun   |
|:-----:|:---------:|:------------:|:--------:|
| **1** | Catacombs | Bloodstained |  Blades  |
| **2** |  Cavern   |   Chaotic    |  Blight  |
| **3** |   Crypt   |   Endless    | Darkness |
| **4** | Fortress  |    Fallen    |   Fury   |
| **5** |  Hideout  |  Forbidden   |   Lies   |
| **6** |   Lair    |  Forgotten   | Madness  |
| **7** |   Mine    |  Shattered   |   Mist   |
| **8** |  Depths   |   Shrouded   | Prophecy |
| **9** | Sanctuary |    Silent    |  Runes   |
| **0** |  Temple   |   Unknown    |  Terror  |

}}

}}

\column

### Settlement

{{template
Settlements have 1d6 **Establishments**.  
Use **Color** + **Symbol** to name an **Establishment**.  
Roll for **News** when entering a Settlement.
}}

{{horizontal-compact

|   #   | Settlement Name         || Establishment |  Artisan   |       News       |
|:-----:|:---------------:|:------:|:-------------:|:----------:|:----------------:|
| **1** |      Frost      | Crest  |    Stable     |   Artist   |       War        |
| **2** |      High       |  Fall  |    Tavern     |   Baker    |     Sickness     |
| **3** |      Lost       |  Glen  |      Inn      |   Tailor   | Natural Disaster |
| **4** |      Moon       | Haven  | Entertainment |   Tanner   |      Crime       |
| **5** |      Raven      | Hollow | General Store |   Archer   |    Succession    |
| **6** |     Shield      | Ridge  |   *Artisan*   | Blacksmith |   Remote Event   |
| **7** |      Storm      |  Rock  |    Courier    | Carpenter  |     Arrival      |
| **8** |      Sword      | Stead  |    Temple     | Apothecary |       Mail       |
| **9** |      Thorn      |  Vale  |  Guild Hall   |  Jeweler   |       Sale       |
| **0** |      Wolf       |  Wood  |  Magic Shop   |   Scribe   |   Celebration    |

::

### Color

|   #    |                                                                                        |       Color       |   #    |                                                                                        |       Color       |
|:------:|:--------------------------------------------------------------------------------------:|:-----------------:|:------:|:--------------------------------------------------------------------------------------:|:-----------------:|
| **1**  | <span style="background-color:#C700C7; color:Black;"> &nbsp;&nbsp;&nbsp;&nbsp; </span> | Ethereal Magenta  | **11** | <span style="background-color:#ae94e4; color:Black;"> &nbsp;&nbsp;&nbsp;&nbsp; </span> | Fragrant Lavender |
| **2**  | <span style="background-color:#FFA1D0; color:Black;"> &nbsp;&nbsp;&nbsp;&nbsp; </span> |  Shimmering Ruby  | **12** | <span style="background-color:#4B0082; color:Black;"> &nbsp;&nbsp;&nbsp;&nbsp; </span> |   Royal Violet    |
| **3**  | <span style="background-color:#c41235; color:Black;"> &nbsp;&nbsp;&nbsp;&nbsp; </span> |   Crimson Blood   | **13** | <span style="background-color:#000000; color:Black;"> &nbsp;&nbsp;&nbsp;&nbsp; </span> | Mirrored Obsidian |
| **4**  | <span style="background-color:#FF8C00; color:Black;"> &nbsp;&nbsp;&nbsp;&nbsp; </span> |   Warning Flame   | **14** | <span style="background-color:#073642; color:Black;"> &nbsp;&nbsp;&nbsp;&nbsp; </span> |  Midnight Shade   |
| **5**  | <span style="background-color:#FFFF00; color:Black;"> &nbsp;&nbsp;&nbsp;&nbsp; </span> | Highlight Sunbeam | **15** | <span style="background-color:#657b83; color:Black;"> &nbsp;&nbsp;&nbsp;&nbsp; </span> |   Hidden Slate    |
| **6**  | <span style="background-color:#00FF7F; color:Black;"> &nbsp;&nbsp;&nbsp;&nbsp; </span> |   Electric Lime   | **16** | <span style="background-color:#C0C0C0; color:Black;"> &nbsp;&nbsp;&nbsp;&nbsp; </span> |  Metallic Silver  |
| **7**  | <span style="background-color:#008000; color:Black;"> &nbsp;&nbsp;&nbsp;&nbsp; </span> |   Forest Green    | **17** | <span style="background-color:#E3BF00; color:Black;"> &nbsp;&nbsp;&nbsp;&nbsp; </span> |    Midas Gold     |
| **8**  | <span style="background-color:#00CED1; color:Black;"> &nbsp;&nbsp;&nbsp;&nbsp; </span> | Luminescent Cyan  | **18** | <span style="background-color:#8B4513; color:Black;"> &nbsp;&nbsp;&nbsp;&nbsp; </span> |   Worn Leather    |
| **9**  | <span style="background-color:#0000CD; color:Black;"> &nbsp;&nbsp;&nbsp;&nbsp; </span> |   Sturdy Cobalt   | **19** | <span style="background-color:#D2B48C; color:Black;"> &nbsp;&nbsp;&nbsp;&nbsp; </span> |  Weathered Sand   |
| **10** | <span style="background-color:#d6ecf3; color:Black;"> &nbsp;&nbsp;&nbsp;&nbsp; </span> |    Clear Frost    | **20** | <span style="background-color:#FFFFFF; color:Black;"> &nbsp;&nbsp;&nbsp;&nbsp; </span> |   Divine Pearl    |

}}

}}

}}
<!-- END BOX 17 -->

<!-- START BOX 18 -->
{{box

{{column-count:2

### Wilderness Exploration

{{template
Move Up/Down **Environment** Ladder when transitioning areas.  
Roll **Encounter** @ Disadvantage until Doubles, then @ Advantage.
}}

{{horizontal-compact

|   #   | Description |  Environment  |        Encounter        | Feature  |   *Ladder*    |
|:-----:|:-----------:|:-------------:|:-----------------------:|:--------:|:-------------:|
| **1** |   Exotic    |    Arctic     |     Natural Hazard      |  Bones   |  *Move Up 2*  |
| **2** |   Haunted   |   Mountains   |         Weather         |  Bridge  |  *Move Up 1*  |
| **3** |  Luminous   |    Cavern     |       *Immersion*       |  Cairn   |  *Move Up 1*  |
| **4** |  Pristine   |     Hills     |      Road / River       |  Circle  |  *Move Up 1*  |
| **5** |   Sacred    |   Grassland   |         Monster         | Monument |  *Same Env*   |
| **6** |  Shadowed   |    Forest     |       *Challenge*       |  Ruins   |  *Same Env*   |
| **7** |    Vast     |     Swamp     |        *Feature*        |  Smoke   | *Move Down 1* |
| **8** |   Verdant   | Water Feature |   *Settlement* / Camp   |  Spring  | *Move Down 1* |
| **9** |    Dying    |     Coast     | Destination / *Dungeon* |  Tracks  | *Move Down 1* |
| **0** |  Weathered  |    Desert     |      Advance Plot       |   Well   | *Move Down 2* |

}}

::

### Dungeon Exploration

{{template

**Early**: Roll **NA** & **Encounter** @ Disadv. | **Late**: Roll **NA** & **Encounter** @ Adv.  
Doubles on **NA**: **Early** ➜ **Late** | Doubles on **Encounter**: **Random Event**

}}

{{horizontal-compact

|   #   |          Next Area          |      Passage       |     Encounter     | Feature  |
|:-----:|:---------------------------:|:------------------:|:-----------------:|:--------:|
| **1** |          *Passage*          | 4-way Intersection |  Natural Hazard   |  Armory  |
| **2** |  Small Chamber w/ 3 Exits   |   T Intersection   |      Safety       | Fountain |
| **3** |  Large Chamber w/ 3 Exits   |    Side Passage    |    *Immersion*    |  Glyphs  |
| **4** |  Small Chamber w/ 2 Exits   |  Right Angle Turn  |      Monster      |  Known   |
| **5** | Circular Chamber w/ 2 Exits |    Side Alcove     |       Key*        | Library  |
| **6** |         Locked Door         |   Long / Winding   |       Trap        |  Mural   |
| **7** |   Small Chamber w/ 1 Exit   |       Narrow       |    *Challenge*    |  Prison  |
| **8** |    Secret Exit / Stairs     |       Sloped       |     *Feature*     |  Shrine  |
| **9** | Connection to Previous Area |  Small Crawlspace  |    *Treasure*     |  Throne  |
| **0** |          *Passage*          |       Bridge       | Objective* / Clue |  Vault   |

}}

\column

### Treasure

:

{{treasure

|       |               |             |               |               |
|:-----:|:-------------:|:-----------:|:-------------:|:-------------:|
| **1** |  **Trinket**  | **Quality** | **Material**  |   **Type**    |
|      ^|     **1**     |   Broken    |     Wood      |   Toy/Game    |
|      ^|     **2**     |   Damaged   |     Bone      |    Bottle     |
|      ^|     **3**     |    Worn     |    Leather    |  Instrument   |
|      ^|     **4**     |   Simple    |    Silver     |     Charm     |
|      ^|     **5**     | Exceptional |     Gold      |     Tool      |
|      ^|     **6**     |    Magic    |      Gem      |      Key      |
| **2** | **Treasure**  | **Quality** | **Container** | **Contents**  |
|      ^|     **1**     |    Dusty    |     None      |     Food      |
|      ^|     **2**     |    Worn     |     Pouch     |      Art      |
|      ^|     **3**     |   Sturdy    |      Box      |     Deed      |
|      ^|     **4**     |    Fine     |    Satchel    | Silver Coins  |
|      ^|     **5**     |     New     |     Crate     |  Gold Coins   |
|      ^|     **6**     |   Ornate    |     Chest     |     Gems      |
| **3** | **Document**  |  **Type**   |  **Content**  |  **Subject**  |
|      ^|     **1**     |    Song     |     Lewd      |   Religion    |
|      ^|     **2**     |   Picture   |    Common     |      Art      |
|      ^|     **3**     | Letter/Note |      Map      |    Science    |
|      ^|     **4**     |   Scroll    |   Prophecy    |   Creatures   |
|      ^|     **5**     |   Journal   |    Arcane     |    History    |
|      ^|     **6**     |    Book     |   Forbidden   |     Magic     |
| **4** | **Accessory** | **Quality** | **Material**  |   **Type**    |
|      ^|     **1**     |   Ruined    |     Wood      |   Headpiece   |
|      ^|     **2**     |    Crude    |     Bone      |    Emblem     |
|      ^|     **3**     |   Simple    |    Leather    |    Earring    |
|      ^|     **4**     |    Fine     |    Silver     |   Bracelet    |
|      ^|     **5**     |   Crafted   |     Gold      |   Necklace    |
|      ^|     **6**     |    Magic    |      Gem      |     Ring      |
| **5** |  **Weapon**   | **Quality** | **Material**  |   **Type**    |
|      ^|     **1**     |   Broken    |     Wood      |  Axe/Hammer   |
|      ^|     **2**     | Improvised  |     Bone      | Halberd/Spear |
|      ^|     **3**     |    Rough    |     Steel     | Sword/Dagger  |
|      ^|     **4**     |   Simple    |    Silver     |  Staff/Wand   |
|      ^|     **5**     |   Martial   |    Mithral    |      Bow      |
|      ^|     **6**     | Masterwork  |  Adamantine   |    Exotic     |
| **6** |   **Armor**   | **Quality** | **Material**  |   **Type**    |
|      ^|     **1**     |   Broken    |     Cloth     |   Headpiece   |
|      ^|     **2**     | Improvised  |    Leather    |    Bottom     |
|      ^|     **3**     |  Tattered   |   Bone/Fur    |    Gloves     |
|      ^|     **4**     |   Simple    |     Steel     |     Boots     |
|      ^|     **5**     |    Fine     |    Mithral    |      Top      |
|      ^|     **6**     | Masterwork  |  Adamantine   |    Shield     |

}}

}}

}}
<!-- END BOX 18 -->

}}
<!-- END FRONT PAGE -->

\page

<!-- START BACK PAGE -->
{{wide

<!-- START ROW 1 -->
{{row1

<!-- START BOX 4 -->
{{box
{{right

### Immersion

{{template
You [**Sense**] something [**Description**] [**Location**]  
and it causes [**Emotion**] because [**Reason**].
}}

{{horizontal-compact
{{vertical-compact

|   #   | 1-3<br>See | 4-6<br>Hear | 7-8<br>Smell | 9-0<br>Feel |
|:-----:|:----------:|:-----------:|:------------:|:-----------:|
| **1** |   Broken   |  Dripping   |   Alcohol    |    Cold     |
| **2** |  Colorful  |    Fire     |    Blood     |    Damp     |
| **3** | Discarded  |  Footsteps  |    Smoke     |  Flexible   |
| **4** |   Edible   |  Growling   |   Cooking    |    Furry    |
| **5** |   Liquid   |  Laughter   |    Decay     |    Rough    |
| **6** |  Natural   |    Music    |     Dust     |    Sharp    |
| **7** |    Odd     | Scratching  |   Flowers    |  Slippery   |
| **8** |   Round    |   Silence   |   Leather    |   Smooth    |
| **9** |   Shiny    |   Talking   |     Oil      |   Sticky    |
| **0** |  Written   |    Wind     |     Soil     |    Warm     |

:

|   #   |    Location     |  Emotion  |          Reason          |
|:-----:|:---------------:|:---------:|:------------------------:|
| **1** |      Above      |   Anger   |    help is on the way    |
| **2** |     Behind      |  Clarity  |   it is getting closer   |
| **3** |    In Front     | Confusion |    it may be valuable    |
| **4** |   In The Air    |  Deja Vu  |   of a childhood event   |
| **5** | In The Distance |  Desire   |    of a recent memory    |
| **6** |  In Next Room   |   Fear    |  the source is unknown   |
| **7** | In The Shadows  |   Hope    | then it is suddenly gone |
| **8** |   Next To You   |    Joy    |     you recognize it     |
| **9** |  On The Ground  | Nostalgia | you were warned about it |
| **0** |      Under      |   Panic   | you weren't expecting it |

}}
}}

}}
}}
<!-- END BOX 4 -->

\column

<!-- START BOX 2 -->
{{box
{{left

### Name

:

|   #    | Template |  1   |  2   |  3   |
|:------:|:--------:|:----:|:----:|:----:|
| **1**  | `12o  `  | (f)a | hal  |  an  |
| **2**  | `12   `  | (p)e | ris  |  ar  |
| **3**  | `12   `  | (v)i | del  |  er  |
| **4**  | `23-o `  | (n)o | mor  | ian  |
| **5**  | `23-  `  | (s)u | bar  |  ic  |
| **6**  | `23-  `  |  de  | net  |  in  |
| **7**  | `123-o`  |  ka  | kel  |  o   |
| **8**  | `123- `  |  li  | lim  |  on  |
| **9**  | `123- `  |  ma  | tur  |  or  |
| **10** | `111  `  |  ro  | pen  |  us  |
| **11** | `111  `  |  be  | rond |  a   |
| **12** | `123  `  |  da  | kay  | aea  |
| **13** | `12a  `  |  ki  | jam  | aya  |
| **14** | `12i  `  |  le  | vash | elle |
| **15** | `23-a `  |  mi  | zab  | ene  |
| **16** | `23-i `  |  ne  | yos  | ess  |
| **17** | `23+  `  |  ru  | gran | ette |
| **18** | `123-a`  |  si  | ched | ice  |
| **19** | `123-i`  |  ta  | sark |  id  |
| **20** | `123+ `  |  to  | kic  | osa  |

}}
}}
<!-- END BOX 2 -->

}}
<!-- END ROW 1 -->

<!-- START ROW 2 -->
{{row2

<!-- START BOX 5 -->
{{box

### What do they say?

{{template

Their [**Tone**] [**Response**] concerns [**Subject**] and suggests [**Subtext**].

}}

:

|   #   |    Tone    |  Response  |     Subject      |    Subtext    |
|:-----:|:----------:|:----------:|:----------------:|:-------------:|
| **1** |  Hostile   |   Threat   |  Your weakness   |    Malice     |
| **2** | Suspicious |  Refusal   |     A danger     |   Distrust    |
| **3** |  Guarded   | Deflection |     The past     |    Secrecy    |
| **4** |  Distant   |  Question  |   An obstacle    |  Uncertainty  |
| **5** |    Calm    | Statement  |  The situation   |  Neutrality   |
| **6** |  Curious   |  Inquiry   |    Themselves    |   Interest    |
| **7** |    Open    | Discussion |   Your actions   | Consideration |
| **8** |    Warm    |   Offer    | The relationship |   Goodwill    |
| **9** |   Eager    | Agreement  |  An opportunity  |  Enthusiasm   |
| **0** |  Trusting  | Revelation |    Your goal     |   Alliance    |

}}
<!-- END BOX 5 -->

\column

<!-- START BOX 1 -->
{{box
{{invert

### Yes/No Oracle / Next Scene

{{column-count:2

| Roll  |      Answer      |
|:-----:|:----------------:|
| **6** |   Yes, and ...   |
| **5** | Yes, because ... |
| **4** |   Yes, but ...   |
| **3** |   No, but ...    |
| **2** | No, because ...  |
| **1** |   No, and ...    |

\column

|       Next Scene        |
|:-----------------------:|
|       Alter (Add)       |
|    Normal (Expected)    |
|     Alter (Remove)      |
|   Next Most Expected    |
|  Interrupt (Favorable)  |
| Interrupt (Unfavorable) |

}}

{{column-count:2

:

- Roll _2d6_
- Equal Odds: Left Die
- Likely Odds: Highest Die
- Unlikely Odds: Lowest Die
- Doubles: **Random Event**
- Only 1 Random Event at a time

\column

:

- Determine the next Expected Scene
- Roll 1d6 on **Next Scene**
- Alter: Add or Remove a **Symbol**
- Interrupt: Roll **RE** + **Inspiration**
- Set up a **Challenge**, Play Out Scene
- Update Lists (Notecards)


}}

}}
}}
<!-- END BOX 1 -->

}}
<!-- END ROW 2 -->

<!-- START ROW 3 -->
{{row3

<!-- START BOX 6 -->
{{box

### Creating a Challenge

{{template

Use [**Skill**] to overcome [**Obstacle**] in order to [**Action**] [**Target**].  
If you fail [**Consequence**].

}}

:

|   #   | Physical Skill  |   #    | Mental Skill |   Obstacle   |  Action  |    Target    |
|:-----:|:---------------:|:------:|:------------:|:------------:|:--------:|:------------:|
| **1** |    Medicine     | **11** |     Tool     |  a barrier   |  alter   | an advantage |
| **2** |    Survival     | **12** |    Nature    |   a cipher   |  bypass  |   the area   |
| **3** | Animal Handling | **13** | Investigate  |   a device   | destroy  | the artifact |
| **4** |   Performance   | **14** |  Persuasion  |    a foe     | protect  | the captive  |
| **5** |  Intimidation   | **15** |  Deception   |   a guard    | redirect |  a resource  |
| **6** |   Perception    | **16** |   Language   |   a hazard   |  reveal  |  a retreat   |
| **7** | Sleight of Hand | **17** |   Religion   |   a lever    | sabotage |  the ritual  |
| **8** |     Stealth     | **18** |    Arcana    | the terrain  |  secure  |   a secret   |
| **9** |   Acrobatics    | **19** |   History    |    a trap    |  seize   |  the source  |
| **0** |    Athletics    | **20** |   Insight    | a vital link |  weaken  |  the threat  |
}}
<!-- END BOX 6 -->

\column

<!-- START BOX 8 -->
{{box
{{left

### Random Event

{{horizontal-compact

|   #    |                   Random Event                   |
|:------:|:------------------------------------------------:|
| **1**  |     An assumption you made is proven false.      |
| **2**  |        You are too late. (Thread Closes)         |
| **3**  |   A complication moves you away from a Thread.   |
| **4**  |  New information brings you closer to a Thread.  |
| **5**  |   Time advances. Check torches, rations, etc.    |
| **6**  |       A periodic event occurs or advances.       |
| **7**  |   A remote event occurs that will impact you.    |
| **8**  |        You sense something... (Immersion)        |
| **9**  |             A new character appears.             |
| **10** |    Whatever difficulty you face is overcome.     |
| **11** |         Your companion makes a mistake.          |
| **12** | Your companion acts in their own self-interest.  |
| **13** |         Your companion gestures subtly.          |
| **14** | Companion: "There are other things to do first." |
| **15** |       Companion: "How do you plan on ...?"       |
| **16** |      Your companion talks about their past.      |
| **17** |    Your companion asks a question about you.     |
| **18** |      Your companion acts in your interest.       |
| **19** |       Your companion gives you something.        |
| **20** |            Companion: "What's that?"             |

}}

{{credits
Juice Pop 11/04/26 github.com/jrruethe/juice CC BY-NC-SA 4.0
}}

}}
}}
<!-- END BOX 8 -->

}}
<!-- END ROW 3 -->

<!-- START ROW 4 -->
{{row4

<!-- START BOX 7 -->
{{box
{{right

### Consequence

{{horizontal-compact

:

|   #    |                  Consequence                  |
|:------:|:---------------------------------------------:|
| **1**  |        A critical resource is depleted        |
| **2**  |        A new danger or foe is revealed        |
| **3**  |             Escape routes narrow              |
| **4**  |  Something you relied upon proves unreliable  |
| **5**  |          The enemy gains new allies           |
| **6**  |    Two unrelated situations are connected     |
| **7**  | You are forced to act against your intentions |
| **8**  |   You are separated from a person or object   |
| **9**  |             You can only save one             |
| **10** |      You must accept help from an enemy       |
| **11** |     You must break a promise to continue      |
| **12** |        You must reveal yourself to act        |
| **13** |  You must rush forward at risk, or lose time  |
| **14** |    You must sacrifice something to proceed    |
| **15** |     Your action has an unintended effect      |
| **16** |    Your approach draws unwanted attention     |
| **17** |      Your information proves incomplete       |
| **18** |         Your past catches up with you         |
| **19** |            Your reputation shifts             |
| **20** |        Your surroundings turn hostile         |

}}

}}
}}
<!-- END BOX 7 -->

\column

<!-- START BOX 3 -->
{{box
{{left

### Inspiration

|   #    | Inspiration             ||  Symbol   |
|:------:|:-----------:|:----------:|:---------:|
| **1**  |   Ancient   | Assistance |   Arrow   |
| **2**  | Artificial  | Attention  |  Beetle   |
| **3**  | Communicate |   Blood    |   Blade   |
| **4**  |   Conceal   |  Comfort   |  Bottle   |
| **5**  |  Dangerous  |  Command   |  Candle   |
| **6**  |   Extreme   | Complexity | Cauldron  |
| **7**  |  Familiar   | Connection |   Chain   |
| **8**  |   Helpful   |  Control   |  Dragon   |
| **9**  |   Looming   |   Delay    |    Eye    |
| **10** |   Missing   | Direction  |   Fang    |
| **11** |   Mundane   |  Element   |  Hammer   |
| **12** | Mysterious  |    Home    |   Hook    |
| **13** |   Oppose    |   Memory   | Hourglass |
| **14** |  Peaceful   |  Resource  |    Key    |
| **15** | Persistent  |   Rumor    |  Lizard   |
| **16** |  Powerful   |   Secret   |   Quill   |
| **17** |   Reveal    |   Shadow   |   Rose    |
| **18** | Specialized | Threshold  |   Skull   |
| **19** |  Transform  |   Trust    |   Snake   |
| **20** |  Weakened   |    Vow     |  Spider   |

}}
}}
<!-- END BOX 3 -->

}}
<!-- END ROW 4 -->

}}
<!-- END BACK PAGE -->
