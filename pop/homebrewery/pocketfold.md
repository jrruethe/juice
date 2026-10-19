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

### Box 17
Top half of the front page — one large box combining the old boxes 9, 10, 11, 12.
There is a horizontal cut between this box and box 18, from the right edge to the center of the paper.
Opening this half to the right is what reveals it as one wide panel.

}}
<!-- END BOX 17 -->

<!-- START BOX 18 -->
{{box

### Box 18
Bottom half of the front page — one large box combining the old boxes 13, 14, 15, 16.

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

::

| # | Location         | Emotion       | Reason                   |
|:-:|:----------------:|:-------------:|:------------------------:|
| 1 | Above            | Anger         | help is on the way       |
| 2 | Behind           | Clarity       | it is getting closer     |
| 3 | In Front         | Confusion     | it may be valuable       |
| 4 | In The Air       | Deja Vu       | of a childhood event     |
| 5 | In The Distance  | Desire        | of a recent memory       |
| 6 | In Next Room | Fear          | the source is unknown    |
| 7 | In The Shadows   | Hope          | then it is suddenly gone |
| 8 | Next To You      | Joy           | you recognize it         |
| 9 | On The Ground    | Nostalgia     | you were warned about it |
| 0 | Under            | Panic         | you weren't expecting it |
}}
}}

}}
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
Failure leads to a [**Consequence**].

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

### Consequence

{{horizontal-compact

:

| 1d20 | Consequence                                   |
|:----:|:---------------------------------------------:|
| 1    | A critical resource is depleted               |
| 2    | The enemy gains new allies                    |
| 3    | You are separated from a person or object     |
| 4    | Your surroundings turn hostile                |
| 5    | Escape routes narrow                          |
| 6    | Your action has an unintended effect          |
| 7    | Your approach draws unwanted attention        |
| 8    | Your reputation shifts                        |
| 9    | Something you relied upon proves unreliable   |
| 10   | A new danger or foe is revealed               |
| 11   | Your past catches up with you                 |
| 12   | Two unrelated situations are connected        |
| 13   | Your information proves incomplete            |
| 14   | You can only save one                         |
| 15   | You are forced to act against your intentions |
| 16   | You must sacrifice something to proceed       |
| 17   | You must break a promise to continue          |
| 18   | You must accept help from an enemy            |
| 19   | You must reveal yourself to act               |
| 20   | Choose: Rush forward at risk, or lose time    |

}}

}}
}}
<!-- END BOX 7 -->

\column

<!-- START BOX 3 -->
{{box
{{right

### Inspiration

| d20 | Inspiration              ||
|:---:|:------------:|:----------:|
| 1   | Ancient      | Assist     |
| 2   | Artificial   | Break      |
| 3   | Betray       | Burden     |
| 4   | Burning      | Command    |
| 5   | Communicate  | Complexity |
| 6   | Conceal      | Conflict   |
| 7   | Dangerous    | Control    |
| 8   | Deceive      | Delay      |
| 9   | Dirty        | Direction  |
| 10  | Disagreeable | Duration   |
| 11  | Helpful      | Failure    |
| 12  | Loud         | Fight      |
| 13  | Oppose       | Happiness  |
| 14  | Peaceful     | Leave      |
| 15  | Powerful     | Memory     |
| 16  | Reassuring   | Move       |
| 17  | Reveal       | Sacrifice  |
| 18  | Specialized  | Shadow     |
| 19  | Transform    | Threshold  |
| 20  | Unexpected   | Trust      |

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

