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
  
  /* the 0.9em padding below counts INSIDE the 8.5in x 11in, so the page is exactly paper size */
  box-sizing: border-box;
  /* blank white background (overrides the theme's parchment image / theme color) */
  background: white;
  
  /* gap between content and the page edge, top */
  padding-top: 0.9em;
  /* gap between content and the page edge, right */
  padding-right: 0.9em;
  /* gap between content and the page edge, bottom */
  padding-bottom: 0.9em;
  /* gap between content and the page edge, left */
  padding-left: 0.9em;
  
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

/* ===== Tables ===== */

h3 {
  text-align: center;
}

.template {
  font-size: 8pt;
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

.compact p
{
  font-size: 8pt;
  line-height: 110%;
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

.center
{
  text-align: center;
}

.treasure table tbody tr td
{
  font-size: 8pt;
  line-height: 100%;
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
  /* fill the page's content area (the page minus its 0.9em padding) */
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

/* ===== Rows ===== */

/* four rows, each one quarter of the working area; each row is a 2-column grid.
   (Page 2 uses these rows; page 1 instead has two big half-page boxes — see
   the #p1 rule below.) */
.block.row1, .block.row2, .block.row3, .block.row4
{
  /* a quarter of the working area's height */
  height: 25%;
  /* make the row a grid with two equal-width columns for its two boxes */
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  /* 0.6em of space between the two boxes of a row */
  column-gap: 0.6em;
  /* no theme margins around rows (the vertical gap comes from the boxes, below) */
  margin: 0;
}

/* Page 1 (the front side of the paper) does NOT use the four rows: it holds two
   big boxes, 17 and 18, directly in the wide block — box 17 takes the top half
   of the page and box 18 the bottom half. Make page 1's wide a two-row grid so
   each big box gets exactly half of the page's height. */
#p1 .block.wide
{
  display: grid;
  grid-template-rows: repeat(2, 1fr);
}

/* ===== Octet boxes ===== */

/* every box: green planning border, content clipped to the box.
   The 8 octet boxes on page 2 all come out exactly the same size; the two
   boxes on page 1 each take a full half of that page (see the #p1 rule). */
.block.box
{
  /* the theme makes every .block an inline-block at 100% width;
     force a plain block that sits cleanly in its grid cell */
  display: block;
  width: auto;
  /* fill its row's height minus 0.6em: that 0.6em of slack at the bottom of
     every row is what makes the 0.6em vertical gap between rows (and, on
     page 1, between the two big boxes) */
  height: calc(100% - 0.6em);
  /* green border marking the octet's working area (remove when planning is done) */
  border: 1px solid green;
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

/* optional sideways: wrap a box's content in {{left ... }} to rotate the box 270 degrees.
   The block's top edge ends up at the box's LEFT edge: the heading (and its underline)
   runs vertically down the left side, and the lines of text fill in from left to right.
   Two things are both required, and missing either one breaks it:
   1. SWAP the block's dimensions — before the rotation it must be as wide as the box is
      tall and as tall as the box is wide, so that AFTER the rotation its shape matches
      the box. (A block that is not swapped keeps the box's own width and height, and
      rotated its shape no longer fits the box — most of it ends up clipped away.)
   2. CENTER the block in the box before rotating — a transform spins an element around
      its own center, so first move the element's center onto the box's center. */
.block.left
{
  /* park the element's center on the box's center (the box needs position: relative) */
  position: absolute;
  top: 50%;
  left: 50%;
  /* then shift the element so its center sits on that point, and rotate 270 degrees
     clockwise around its center */
  transform: translate(-50%, -50%) rotate(270deg);
  /* the swapped dimensions: before rotation, as wide as the box is tall and as tall as
     the box is wide, so that after the rotation the block fills the box exactly.
     Both are derived from the same page numbers the boxes above are built from
     (11in page, 0.9em padding, 4 rows, 0.6em gap, 1px border) */
  width: calc((11in - 1.8em) / 4 - 0.6em);
  height: calc((8.5in - 1.8em - 0.6em) / 2);
  /* plain block (the theme would otherwise make it an inline-block) */
  display: block;
}


.block.right
{
  /* park the element's center on the box's center (the box needs position: relative) */
  position: absolute;
  top: 50%;
  left: 50%;
  /* then shift the element so its center sits on that point, and rotate 270 degrees
     clockwise around its center */
  transform: translate(-50%, -50%) rotate(90deg);
  /* the swapped dimensions: before rotation, as wide as the box is tall and as tall as
     the box is wide, so that after the rotation the block fills the box exactly.
     Both are derived from the same page numbers the boxes above are built from
     (11in page, 0.9em padding, 4 rows, 0.6em gap, 1px border) */
  width: calc((11in - 1.8em) / 4 - 0.6em);
  height: calc((8.5in - 1.8em - 0.6em) / 2);
  /* plain block (the theme would otherwise make it an inline-block) */
  display: block;
}

/* \column markers between boxes are not needed (the grid places the boxes); hide any that exist */
.columnSplit
{
  display: none;
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

A [**Situation**] [**Person**], concerned about [**Motive**], asks you to  
[**Objective**] the [**Description**] [**Focus**] in the [**Dungeon**] of [**Adjective**] [**Noun**],  
[**Complication**].

}}

:

{{horizontal-compact

| # | Objective            | Description | Focus             | Complication                  |
|:-:|:--------------------:|:-----------:|:-----------------:|:-----------------------------:|
| 1 | Attain power from    | Abandoned   | Anomaly           | before time expires           |
| 2 | Destroy              | Astral      | Faction           | before the ritual completes   |
| 3 | Escape from          | Decayed     | Information       | before they escape            |
| 4 | Escort someone to    | Defended    | Monster           | while outmatched              |
| 5 | Infiltrate           | Hidden      | Seal              | while being hunted            |
| 6 | Investigate          | Elemental   | NPC               | against a rival faction       |
| 7 | Negotiate with       | Connected   | Object / Treasure | amid betrayal                 |
| 8 | Protect              | Strange     | Remains           | though nothing is as it seems |
| 9 | Rescue someone from  | Toxic       | Plant             | under false pretenses         |
| 0 | Steal something from | Artificial  | Villain           | while enemies converge        |

{{column-count:2

### Person

| # | Situation | Person      | Motive / Topic |
|:-:|:---------:|:-----------:|:--------------:|
| 1 | Deceiving | Criminal    | Equipment      |
| 2 | Guarding  | Entertainer | Experience     |
| 3 | Guiding   | Expert      | Family         |
| 4 | Hunting   | Mage        | Flaws          |
| 5 | Lost      | Mercenary   | History        |
| 6 | Spying    | Noble       | Quest          |
| 7 | Tasked    | Priest      | Reputation     |
| 8 | Trading   | Ranger      | Superiors      |
| 9 | Trapped   | Soldier     | Treasure       |
| 0 | Wounded   | Transporter | Wealth         |

\column

### Location

| # | Dungeon   | Adjective    | Noun     |
|:-:|:---------:|:------------:|:--------:|
| 1 | Catacombs | Bloodstained | Blades   |
| 2 | Cavern    | Chaotic      | Blight   |
| 3 | Crypt     | Endless      | Darkness |
| 4 | Fortress  | Fallen       | Fury     |
| 5 | Hideout   | Forbidden    | Lies     |
| 6 | Lair      | Forgotten    | Madness  |
| 7 | Mine      | Shattered    | Mist     |
| 8 | Depths    | Shrouded     | Prophecy |
| 9 | Sanctuary | Silent       | Runes    |
| 0 | Temple    | Unknown      | Terror   |

}}

}}

\column

### Settlement



{{horizontal-compact

| # | Settlement Name || Establishment | Artisan    | Symbol         | News             |
|:-:|:------:|:-------:|:-------------:|:----------:|:--------------:|:----------------:|
| 1 | Frost  | Crest   | Stable        | Artist     | Arrow          | War              |
| 2 | High   | Fall    | Tavern        | Baker      | Candle         | Sickness         |
| 3 | Lost   | Glen    | Inn           | Tailor     | Cauldron       | Natural Disaster |
| 4 | Moon   | Haven   | Entertainment | Tanner     | Chain          | Crime            |
| 5 | Raven  | Hollow  | General Store | Archer     | Claw           | Succession       |
| 6 | Shield | Ridge   | *Artisan*     | Blacksmith | Hook           | Remote Event     |
| 7 | Storm  | Rock    | Courier       | Carpenter  | Hourglass      | Arrival          |
| 8 | Sword  | Stead   | Temple        | Apothecary | Quill          | Mail             |
| 9 | Thorn  | Vale    | Guild Hall    | Jeweler    | Rose           | Sale             |
| 0 | Wolf   | Wood    | Magic Shop    | Scribe     | Skull          | Celebration      |

:::::

### Details

| # | Color                                                                                                        || Monster                || Trap                 ||
|:-:|:------------------------------------------------------------------------------------------:|:----------------:|:------------:|:--------:|:--------:|:----------:|
| 1 | <span style="background-color:Black;       color:Black;"> &nbsp;&nbsp;&nbsp;&nbsp; </span> | Shade Black      | Agile        | Climb    | Ambush   | Alarm      |
| 2 | <span style="background-color:Saddlebrown; color:Black;"> &nbsp;&nbsp;&nbsp;&nbsp; </span> | Leather Brown    | Beast        | Detect   | Collapse | Barrier    |
| 3 | <span style="background-color:Yellow;      color:Black;"> &nbsp;&nbsp;&nbsp;&nbsp; </span> | Highlight Yellow | Clothed      | Drain    | Divert   | Decay      |
| 4 | <span style="background-color:Forestgreen; color:Black;"> &nbsp;&nbsp;&nbsp;&nbsp; </span> | Forest Green     | Composite    | Entangle | Imitate  | Denizen    |
| 5 | <span style="background-color:Dodgerblue;  color:Black;"> &nbsp;&nbsp;&nbsp;&nbsp; </span> | Cobalt Blue      | Decayed      | Illusion | Lure     | Fall       |
| 6 | <span style="background-color:Crimson;     color:Black;"> &nbsp;&nbsp;&nbsp;&nbsp; </span> | Crimson Red      | Elemental    | Immune   | Obscure  | Fire       |
| 7 | <span style="background-color:Purple;      color:Black;"> &nbsp;&nbsp;&nbsp;&nbsp; </span> | Royal Violet     | Inscribed    | Magic    | Summon   | Light      |
| 8 | <span style="background-color:Silver;      color:Black;"> &nbsp;&nbsp;&nbsp;&nbsp; </span> | Metallic Silver  | Intimidating | Paralyze | Surprise | Path       |
| 9 | <span style="background-color:Goldenrod;   color:Black;"> &nbsp;&nbsp;&nbsp;&nbsp; </span> | Midas Gold       | Levitating   | Pierce   | Surround | Poison     |
| 0 | <span style="background-color:White;       color:Black;"> &nbsp;&nbsp;&nbsp;&nbsp; </span> | Holy White       | Nightmarish  | Ranged   | Trigger  | Projectile |

}}

}}

}}
<!-- END BOX 17 -->

<!-- START BOX 18 -->
{{box

{{column-count:2

### Wilderness Exploration

:

{{horizontal-compact

| # | Description | Environment         | Encounter               | Feature   |
|:-:|:-----------:|:-------------------:|:-----------------------:|:---------:|
| 1 | Exotic      | Arctic              | Natural Hazard          | Bones     |
| 2 | Haunted     | Mountains           | Weather                 | Bridge    |
| 3 | Luminous    | Cavern              | *Immersion*             | Cairn     |
| 4 | Pristine    | Hills               | Road / River            | Circle    |
| 5 | Sacred      | Grassland           | Monster                 | Monument  |
| 6 | Shadowed    | Forest              | *Challenge*             | Ruins     |
| 7 | Vast        | Swamp               | *Feature*               | Smoke     |
| 8 | Verdant     | Water Feature       | *Settlement* / Camp     | Spring    |
| 9 | Dying       | Coast               | Destination / *Dungeon* | Tracks    |
| 0 | Weathered   | Desert              | Advance Plot            | Well      |

}}

:

### Dungeon Exploration

{{horizontal-compact

| # | Next Area                   | Passage            | Encounter         | Feature   |
|:-:|:---------------------------:|:------------------:|:-----------------:|:---------:|
| 1 | *Passage*                   | 4-way Intersection | Natural Hazard    | Armory    |
| 2 | Small Chamber w/ 3 Doors    | T Intersection     | Safety            | Fountain  |
| 3 | Large Chamber w/ 3 Doors    | Side Passage       | *Immersion*       | Glyphs    |
| 4 | Small Chamber w/ 2 Doors    | Right Angle Turn   | Monster           | Known     |
| 5 | Circular Chamber w/ 2 Doors | Side Alcove        | Key*              | Library   |
| 6 | Locked Door                 | Long / Winding     | Trap              | Mural     |
| 7 | Small Chamber w/ 1 Door     | Narrow             | *Challenge*       | Prison    |
| 8 | Secret Exit / Stairs        | Sloped             | *Feature*         | Shrine    |
| 9 | Connection to Previous Area | Small Crawlspace   | *Treasure*        | Throne    |
| 0 | *Passage*                   | Bridge             | Objective* / Clue | Vault     |

}}

::

{{center
_Juice Pop! 10/19/26 - https://github.com/jrruethe/juice_
}}

\column

### Treasure

{{treasure

|       |               |             |               |               |
|:-----:|:-------------:|:-----------:|:-------------:|:-------------:|
| **1** | **Trinket**   | **Quality** | **Material**  | **Type**      |
|      ^| 1             | Broken      | Wood          | Toy/Game      |
|      ^| 2             | Damaged     | Bone          | Bottle        |
|      ^| 3             | Worn        | Leather       | Instrument    |
|      ^| 4             | Simple      | Silver        | Charm         |
|      ^| 5             | Exceptional | Gold          | Tool          |
|      ^| 6             | Magic       | Gem           | Key           |
| **2** | **Treasure**  | **Quality** | **Container** | **Contents**  |
|      ^| 1             | Dusty       | None          | Food          |
|      ^| 2             | Worn        | Pouch         | Art           |
|      ^| 3             | Sturdy      | Box           | Deed          |
|      ^| 4             | Fine        | Satchel       | Silver Coins  |
|      ^| 5             | New         | Crate         | Gold Coins    |
|      ^| 6             | Ornate      | Chest         | Gems          |
| **3** | **Document**  | **Type**    | **Content**   | **Subject**   |
|      ^| 1             | Song        | Lewd          | Religion      |
|      ^| 2             | Picture     | Common        | Art           |
|      ^| 3             | Letter/Note | Map           | Science       |
|      ^| 4             | Scroll      | Prophecy      | Creatures     |
|      ^| 5             | Journal     | Arcane        | History       |
|      ^| 6             | Book        | Forbidden     | Magic         |
| **4** | **Accessory** | **Quality** | **Material**  | **Type**      |
|      ^| 1             | Ruined      | Wood          | Headpiece     |
|      ^| 2             | Crude       | Bone          | Emblem        |
|      ^| 3             | Simple      | Leather       | Earring       |
|      ^| 4             | Fine        | Silver        | Bracelet      |
|      ^| 5             | Crafted     | Gold          | Necklace      |
|      ^| 6             | Magic       | Gem           | Ring          |
| **5** | **Weapon**    | **Quality** | **Material**  | **Type**      |
|      ^| 1             | Broken      | Wood          | Axe/Hammer    |
|      ^| 2             | Improvised  | Bone          | Halberd/Spear |
|      ^| 3             | Rough       | Steel         | Sword/Dagger  |
|      ^| 4             | Simple      | Silver        | Staff/Wand    |
|      ^| 5             | Martial     | Mithral       | Bow           |
|      ^| 6             | Masterwork  | Adamantine    | Exotic        |
| **6** | **Armor**     | **Quality** | **Material**  | **Type**      |
|      ^| 1             | Broken      | Cloth         | Headpiece     |
|      ^| 2             | Improvised  | Leather       | Bottom        |
|      ^| 3             | Tattered    | Bone/Fur      | Gloves        |
|      ^| 4             | Simple      | Steel         | Boots         |
|      ^| 5             | Fine        | Mithral       | Top           |
|      ^| 6             | Masterwork  | Adamantine    | Shield        |

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

### Box 4

}}
<!-- END BOX 4 -->

\column

<!-- START BOX 2 -->
{{box
{{right

### Name

:

| d20 | 1    | 2    | 3    |
|:---:|:----:|:----:|:----:|
| 1   |    A | hal  | an   |
| 2   |    E | ris  | ar   |
| 3   |    I | del  | er   |
| 4   |    O | mor  | ian  |
| 5   |    U | bar  | ic   |
| 6   |   De | net  | in   |
| 7   |   Ka | kel  | o    |
| 8   |   Li | lim  | on   |
| 9   |   Ma | tur  | or   |
| 10  |   Ro | pen  | us   |
| 11  |   Be | rond | a    |
| 12  |   Da | kay  | aea  |
| 13  |   Ki | jam  | aya  |
| 14  |   Le | vash | elle |
| 15  |   Mi | zab  | ene  |
| 16  |   Ne | yos  | ess  |
| 17  |   Ru | gran | ette |
| 18  |   Si | ched | ice  |
| 19  |   Ta | sark | id   |
| 20  |   To | kic  | osa  |

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

| # | Tone       | Response   | Subject          | Subtext       |
|:-:|:----------:|:----------:|:----------------:|:-------------:|
| 1 | Hostile    | Threat     | your weakness    | Malice        |
| 2 | Suspicious | Refusal    | a danger         | Distrust      |
| 3 | Guarded    | Deflection | the past         | Secrecy       |
| 4 | Distant    | Question   | an obstacle      | Uncertainty   |
| 5 | Calm       | Statement  | the situation    | Neutrality    |
| 6 | Curious    | Inquiry    | themselves       | Interest      |
| 7 | Open       | Discussion | your actions     | Consideration |
| 8 | Warm       | Offer      | the relationship | Goodwill      |
| 9 | Eager      | Agreement  | an opportunity   | Enthusiasm    |
| 0 | Trusting   | Revelation | your goal        | Alliance      |

}}
<!-- END BOX 5 -->

\column

<!-- START BOX 1 -->
{{box
{{right

### Yes/No Oracle

| Roll | Answer           |
|:----:|:----------------:|
| 6    | Yes, and ...     |
| 5    | Yes, because ... |
| 4    | Yes, but ...     |
| 3    | No, but ...      |
| 2    | No, because ...  |
| 1    | No, and ...      |

{{center
{{compact

Guidelines, not rules.  
There is no wrong way to play.  
Choose what is most fun.

:

Keep the flow moving:  
If something doesn't make sense, reroll.

:

Defer some questions for later;  
Answers may naturally come to you as you play.

:

Fail-forward:  
Every failure is a new opportunity  
and a challenge to overcome.

:

Be your character!  
Describe the situation, how you handle it, and why.

:

Your actions have consequences and   
change the world in a meaningful way.

}}
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

### Box 6

}}
<!-- END BOX 6 -->

\column


<!-- START BOX 8 -->
{{box
{{left

### Inspiration

:

| d20 | Inspiration                     |
|:---:|:-------------------------------:|
| 1   | Despair washes over you         |
| 2   | It fills you with fear          |
| 3   | This is only the beginning      |
| 4   | An enemy would want this        |
| 5   | You've been warned about this   |
| 6   | It feels out of place here      |
| 7   | It's not what it appears to be  |
| 8   | The timing seems deliberate     |
| 9   | That was too easy               |
| 10  | There's something hidden here   |
| 11  | It wasn't always this way       |
| 12  | This predates you               |
| 13  | Its size surprises you          |
| 14  | Deep down, you already know     |
| 15  | You've encountered this before  |
| 16  | It will matter later            |
| 17  | It's impossibly rare            |
| 18  | Someone trusted is connected    |
| 19  | It connects to your goal        |
| 20  | Your sidekick would know more   |

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

### Situation

| # | Situation                              |
|:-:|:--------------------------------------:|
| 1 |A chase begins.                         |
| 2 |A shorcut is offered, will you take it? |
| 3 |An assumption proves false.             |
| 4 |Are you being followed?                 |
| 5 |Backup will arrive soon.                |
| 6 |Can you pass without being noticed?     |
| 7 |Can you use this to your advantage?     |
| 8 |For the moment, it is safe to rest.     |
| 9 |Is this the way forward?                |
|10 |It's quiet. Too quiet...                |
|11 |Someone is exposed to danger.           |
|12 |Something calls to you, do you answer?  |
|13 |The enemy gains new allies.             |
|14 |The silence is suddenly broken.         |
|15 |The way forward becomes clear.          |
|16 |What are you willing to sacrifice?      |
|17 |Will you reveal yourself?               |
|18 |Your approach draws unwanted attention. |
|19 |Your fear is realized.                  |
|20 |Your past catches up to you.            |

}}
}}
<!-- END BOX 7 -->

\column

<!-- START BOX 3 -->
{{box
{{right

### Box 3

| # |                                                                                        | Color             |
|:-:|:--------------------------------------------------------------------------------------:|:-----------------:|
| 1 | <span style="background-color:#C700C7; color:Black;"> &nbsp;&nbsp;&nbsp;&nbsp; </span> | Ethereal Magenta  |
| 2 | <span style="background-color:#FFA1D0; color:Black;"> &nbsp;&nbsp;&nbsp;&nbsp; </span> | Shimmering Ruby   |
| 3 | <span style="background-color:#c41235; color:Black;"> &nbsp;&nbsp;&nbsp;&nbsp; </span> | Crimson Blood     |
| 4 | <span style="background-color:#FF8C00; color:Black;"> &nbsp;&nbsp;&nbsp;&nbsp; </span> | Warning Flame     |
| 5 | <span style="background-color:#FFFF00; color:Black;"> &nbsp;&nbsp;&nbsp;&nbsp; </span> | Highlight Sunbeam |
| 6 | <span style="background-color:#00FF7F; color:Black;"> &nbsp;&nbsp;&nbsp;&nbsp; </span> | Electric Lime     |
| 7 | <span style="background-color:#008000; color:Black;"> &nbsp;&nbsp;&nbsp;&nbsp; </span> | Forest Green      |
| 8 | <span style="background-color:#00CED1; color:Black;"> &nbsp;&nbsp;&nbsp;&nbsp; </span> | Luminescent Cyan  |
| 9 | <span style="background-color:#0000CD; color:Black;"> &nbsp;&nbsp;&nbsp;&nbsp; </span> | Sturdy Cobalt     |
|10 | <span style="background-color:#d6ecf3; color:Black;"> &nbsp;&nbsp;&nbsp;&nbsp; </span> | Clear Frost       |
|11 | <span style="background-color:#ae94e4; color:Black;"> &nbsp;&nbsp;&nbsp;&nbsp; </span> | Fragrant Lavender |
|12 | <span style="background-color:#4B0082; color:Black;"> &nbsp;&nbsp;&nbsp;&nbsp; </span> | Royal Violet      |
|13 | <span style="background-color:#000000; color:Black;"> &nbsp;&nbsp;&nbsp;&nbsp; </span> | Mirrored Obsidian |
|14 | <span style="background-color:#073642; color:Black;"> &nbsp;&nbsp;&nbsp;&nbsp; </span> | Midnight Shade    |
|15 | <span style="background-color:#657b83; color:Black;"> &nbsp;&nbsp;&nbsp;&nbsp; </span> | Hidden Slate      |
|16 | <span style="background-color:#C0C0C0; color:Black;"> &nbsp;&nbsp;&nbsp;&nbsp; </span> | Metallic Silver   |
|17 | <span style="background-color:#E3BF00; color:Black;"> &nbsp;&nbsp;&nbsp;&nbsp; </span> | Midas Gold        |
|18 | <span style="background-color:#8B4513; color:Black;"> &nbsp;&nbsp;&nbsp;&nbsp; </span> | Worn Leather      |
|19 | <span style="background-color:#D2B48C; color:Black;"> &nbsp;&nbsp;&nbsp;&nbsp; </span> | Weathered Sand    |
|20 | <span style="background-color:#FFFFFF; color:Black;"> &nbsp;&nbsp;&nbsp;&nbsp; </span> | Divine Pearl      |
}}
}}
<!-- END BOX 3 -->

}}
<!-- END ROW 4 -->

}}
<!-- END BACK PAGE -->

<!-- BEGIN BOX NUMBERS -->
<!-- Small floating number in the upper-right corner of each box, showing its
     physical box number (a planning aid).
     The numbers come ONLY from this one block at the end of the document —
     none of the boxes above mention them. To hide every number at once,
     delete this block (from the BEGIN comment to the END comment), or wrap
     the CSS rules inside the <style> tag in a single /* ... */ comment.
      Each rule below finds one box by position: on page 2, which row and
      left or right side of the row; on page 1, the two big boxes straight in
      the wide block. If you ever move boxes around, update the numbers here
      to match. -->
<style>

/* the number itself: small, floating in the upper-right corner of the box
   (the box is position: relative, so the number parks itself in its corner) */
.page .box::after
{
  position: absolute;
  top: 0.05em;
  right: 0.1em;
  /* small so it never competes with the table content */
  font-size: 8pt;
  font-weight: bold;
  /* green, to match the planning borders */
  color: green;
}

/* ---- page 1 (front side of the paper): two big boxes —
   17 = top half, 18 = bottom half (they sit directly in the wide block) ---- */
#p1 .block.wide > .box:nth-of-type(1)::after { content: "17"; }
#p1 .block.wide > .box:nth-of-type(2)::after { content: "18"; }

/* ---- page 2 (back side of the paper) ---- */
#p2 .block.row1 .box:first-child::after { content: "4"; }
#p2 .block.row1 .box:last-child::after  { content: "2"; }
#p2 .block.row2 .box:first-child::after { content: "5"; }
#p2 .block.row2 .box:last-child::after  { content: "1"; }
#p2 .block.row3 .box:first-child::after { content: "6"; }
#p2 .block.row3 .box:last-child::after  { content: "8"; }
#p2 .block.row4 .box:first-child::after { content: "7"; }
#p2 .block.row4 .box:last-child::after  { content: "3"; }

</style>
<!-- END BOX NUMBERS -->

