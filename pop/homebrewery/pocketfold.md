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

/* four rows, each one quarter of the working area; each row is a 2-column grid */
.block.row1, .block.row2, .block.row3, .block.row4
{
  /* a quarter of the working area's height */
  height: 25%;
  /* make the row a grid with two equal-width columns for its two boxes */
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  /* 0.2em of space between the two boxes of a row */
  column-gap: 0.6em;
  /* no theme margins around rows (the vertical gap comes from the boxes, below) */
  margin: 0;
}

/* ===== Octet boxes ===== */

/* all 8 boxes: identical size, green planning border, content clipped to the box */
.block.box
{
  /* the theme makes every .block an inline-block at 100% width;
     force a plain block that sits cleanly in its grid cell */
  display: block;
  width: auto;
  /* fill the row's height minus 0.2em: that 0.2em of slack at the bottom of every
     row is what makes the 0.2em vertical gap between rows, and keeps all 8
     boxes exactly the same size */
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
     (11in page, 0.9em padding, 4 rows, 0.2em gap, 1px border) */
  width: calc((11in - 1.8em) / 4 - 0.2em);
  height: calc((8.5in - 1.8em - 0.2em) / 2);
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
     (11in page, 0.9em padding, 4 rows, 0.2em gap, 1px border) */
  width: calc((11in - 1.8em) / 4 - 0.2em);
  height: calc((8.5in - 1.8em - 0.2em) / 2);
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


<!-- START ROW 1 -->
{{row1

<!-- START BOX 9 -->
{{box

### Box 9
Upper left box on front page.
There is a horizontal cut between box 12 and box 14, from the right edge to the center of the paper.
Boxes 10 and 12 will be on the inside of flap that folds out to the right, revealing boxes 9 and 11. 
This means that we could have boxes 9,10,11,12 all be one large table.

}}
<!-- END BOX 9 -->

\column

<!-- START BOX 10 -->
{{box

### Box 10
Upper right on front page

}}
<!-- END BOX 10 -->

}}
<!-- END ROW 1 -->

<!-- START ROW 2 -->
{{row2

<!-- START BOX 11 -->
{{box

### Box 11

}}
<!-- END BOX 11 -->

\column

<!-- START BOX 12 -->
{{box

### Box 12

}}
<!-- END BOX 12 -->

}}
<!-- END ROW 2 -->

<!-- START ROW 3 -->
{{row3

<!-- START BOX 13 -->
{{box

### Box 13

}}
<!-- END BOX 13 -->

\column


<!-- START BOX 14 -->
{{box

### Box 14

}}
<!-- END BOX 14 -->

}}
<!-- END ROW 3 -->

<!-- START ROW 4 -->
{{row4

<!-- START BOX 15 -->
{{box

### Box 15

}}
<!-- END BOX 15 -->

\column

<!-- START BOX 16 -->
{{box

### Box 16

}}
<!-- END BOX 16 -->

}}
<!-- END ROW 4 -->

}}
<!-- END FRONT PAGE -->

\page

<!-- START BACK PAGE -->
{{wide


<!-- START ROW 1 -->
{{row1

<!-- START BOX 4 -->
{{box
{{left

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
<!-- END BOX 4 -->

\column

<!-- START BOX 2 -->
{{box
{{invert-

### What is your Quest?

{{template

A [**Situation**] [**Person**], concerned about [**Motive**], asks you to  
[**Objective**] the [**Description**] [**Focus**] in the [**Dungeon**] of [**Adjective**] [**Noun**],  
[**Complication**].

}}

{{horizontal-compact

| # | Objective            | Description | Focus             | Complication                  |
|:-:|:--------------------:|:-----------:|:-----------------:|:-----------------------------:|
| **1** | Attain power from    | Abandoned   | Anomaly           | before time expires           |
| **2** | Destroy              | Astral      | Faction           | before the ritual completes   |
| **3** | Escape from          | Decayed     | Information       | before they escape            |
| **4** | Escort someone to    | Defended    | Monster           | while outmatched              |
| **5** | Infiltrate           | Hidden      | Seal              | while being hunted            |
| **6** | Investigate          | Elemental   | NPC               | against a rival faction       |
| **7** | Negotiate with       | Connected   | Object / Treasure | amid betrayal                 |
| **8** | Protect              | Mystical    | Remains           | though nothing is as it seems |
| **9** | Rescue someone from  | Toxic       | Plant             | under false pretenses         |
| **0** | Steal something from | Artificial  | Villain           | while enemies converge        |

}}

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
{{invert-

### Yes/No Oracle

{{column-count:2

| Roll | Answer           |
|:----:|:----------------:|
| 6    | Yes, and ...     |
| 5    | Yes, because ... |
| 4    | Yes, but ...     |
| 3    | No, but ...      |
| 2    | No, because ...  |
| 1    | No, and ...      |

\column

:

- Roll _2d6_
- Equal Odds: Left Die
- Likely Odds: Highest Die
- Unlikely Odds: Lowest Die
- Doubles: **Random Event**
- Only 1 Random Event at a time

}}



- Guidelines, not rules. There is no wrong way to play. Choose what is most fun.
- Keep the flow moving. If something doesn't make sense, reroll.
- Defer some questions for later; Answers may naturally come to you as you play.
- Fail-forward: Every failure is a new opportunity and a challenge to overcome.
- Be your character. Describe the situation, how you handle it, and why.
- Your actions have consequences and change the world in a meaningful way.


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

}}

:

| # | Skill       | Obstacle       | Action     | Target        |
|:-:|:-----------:|:--------------:|:----------:|:-------------:|
| 1 | Arcana      | a barrier      | alter      | an advantage  |
| 2 | Examination | a cipher       | bypass     | the area      |
| 3 | Finesse     | a device       | destroy    | the artifact  |
| 4 | Influence   | a foe          | protect    | the captive   |
| 5 | Insight     | a guard        | redirect   | a resource    |
| 6 | Lore        | a hazard       | reveal     | a retreat     |
| 7 | Might       | a lever        | sabotage   | the ritual    |
| 8 | Naturecraft | the terrain    | secure     | a secret      |
| 9 | Perception  | a trap         | seize      | the source    |
| 0 | Stealth     | a vital link   | weaken     | the threat    |

}}
<!-- END BOX 6 -->

\column


<!-- START BOX 8 -->
{{box
{{left

### Random Event

:

{{horizontal-compact

| 1d20 | Random Event                                    |
|:----:|:-----------------------------------------------:|
| 1    | You see a monster.                              |
| 2    | You spot a trap.                                |
| 3    | You are too late.                               |
| 4    | An assumption you made is proven false.         |
| 5    | Time advances. Check torches, rations, etc.     |
| 6    | A periodic event occurs or advances.            |
| 7    | A remote event occurrs that will impact you.    |
| 8    | You sense something...                          |
| 9    | A new character appears.                        |
| 10   | Whatever difficulty you face is overcome.       |
| 11   | Your sidekick makes a mistake.                  |
| 12   | Your sidekick acts in their own self-interest.  |
| 13   | Your sidekick coughs or sneezes.                |
| 14   | Sidekick: "There are other things to do first." |
| 15   | Sidekick: "How do you plan on ...?"             |
| 16   | Your sidekick talks about their past.           |
| 17   | Your sidekick asks a question about you.        |
| 18   | Your sidekick acts in your interest.            |
| 19   | Your sidekick gives you something.              |
| 20   | Sidekick: "What's that?"                        |

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

### Immersion

{{template

You [**Sense**] something [**Description**] [**Location**]  
and it causes [**Emotion**] because [**Reason**].

}}

{{horizontal-compact
{{vertical-compact

| # | 1-3<br>See | 4-6<br>Hear | 7-8<br>Smell | 9-0<br>Feel |
|:-:|:----------:|:-----------:|:------------:|:-----------:|
| 1 | Broken     | Dripping    | Alcohol      | Cold        |
| 2 | Colorful   | Fire        | Blood        | Damp        |
| 3 | Discarded  | Footsteps   | Smoke        | Flexible    |
| 4 | Edible     | Growling    | Cooking      | Furry       |
| 5 | Liquid     | Laughter    | Decay        | Rough       |
| 6 | Natural    | Music       | Dust         | Sharp       |
| 7 | Odd        | Scratching  | Flowers      | Slippery    |
| 8 | Round      | Silence     | Leather      | Smooth      |
| 9 | Shiny      | Talking     | Oil          | Sticky      |
| 0 | Written    | Wind        | Soil         | Warm        |

:

| # | Location         | Emotion       | Reason                   |
|:-:|:----------------:|:-------------:|:------------------------:|
| 1 | Above            | Anger         | help is on the way       |
| 2 | Behind           | Clarity       | it is getting closer     |
| 3 | In Front         | Confusion     | it may be valuable       |
| 4 | In The Air       | Deja Vu       | of a childhood event     |
| 5 | In The Distance  | Desire        | of a recent memory       |
| 6 | In The Next Room | Fear          | the source is unknown    |
| 7 | In The Shadows   | Hope          | then it is suddenly gone |
| 8 | Next To You      | Joy           | you recognize it         |
| 9 | On The Ground    | Nostalgia     | you were warned about it |
| 0 | Under            | Panic         | you weren't expecting it |

}}
}}

}}
}}
<!-- END BOX 7 -->

\column

<!-- START BOX 3 -->
{{box
{{invert-

{{column-count:2

### Person

{{horizontal-compact



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

}}

\column

### Location

{{horizontal-compact

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

::

{{center
_Juice Pop! 10/19/2026 - https://github.com/jrruethe/juice_ 
}}

}}
}}
<!-- END BOX 3 -->

}}
<!-- END ROW 4 -->

}}
<!-- END BACK PAGE -->
