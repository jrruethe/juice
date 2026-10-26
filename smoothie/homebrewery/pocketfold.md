<!-- BEGIN Style -->
<style>

/* ===== Page ===== */

/* The page: US Letter portrait, blank, laid out by us (not by the theme) */
.page
{
  /* US Letter width (landscape: wider than tall) */
  width: 11in;
  /* US Letter height (landscape: shorter than wide, so boxes are wider than tall) */
  height: 8.5in;
  
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
  font-size: 11pt;
  text-align: center;
  font-style: italic;
}

.credits {
  font-size: 6pt;
  text-align: center;
  font-style: italic;
}

.page table
{
  line-height: 120%
}
  
.page table thead tr th
{
  vertical-align: middle;
  font-size: 12pt;
}
  
.page table tbody tr td
{
  vertical-align: middle;
  font-size: 11pt;
}

.invert table thead tr th
{
  line-height: 110%
}
  
.invert table tbody tr td
{
  line-height: 110%
}

div.block.center
{
  margin-top: 0.2em;
}
  
.center p
{
  text-align: center;
  font-size: 9pt;
  line-height: 85%;
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
   (In Smoothie neither page uses these rows: page 1 holds its two big boxes
   straight in the wide block and page 2 holds all of its boxes straight in the
   wide block too — see the #p1 and #p2 rules below. Kept so the standard D9
   block stays intact.) */
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

/* Page 1 does NOT use the four rows: it holds two big boxes directly in the
   wide block — box 1 takes the top half of the page and box 2 the bottom half.
   Make page 1's wide a two-row grid so each box gets exactly half of the page's
   height (both boxes come out the same size: full page width, half page height). */
#p1 .block.wide
{
  display: grid;
  grid-template-rows: repeat(2, 1fr);
}

/* Page 2 also does NOT use the four rows: all of its boxes sit directly in the
   wide block. The top row is split into four small boxes (3, 4, 5, 6); the
   bottom row is one single wide box (7) spanning all four columns. */
#p2 .block.wide
{
  /* make the wide block a grid so the boxes below are placed by grid
     (the theme leaves it a plain block) */
  display: grid;
  /* four equal columns for the four small boxes of the top row */
  grid-template-columns: repeat(4, 1fr);
  /* two rows: the small boxes (top) and box 7 (bottom), each a half-page */
  grid-template-rows: repeat(2, 1fr);
  /* 0.6em between the four columns */
  column-gap: 0.6em;
}

/* box 7 is the LAST box in page 2's wide block: let it span all four columns
   of the bottom row. The four small boxes before it are auto-placed into the
   top row, one per column, left to right. */
#p2 .block.wide > .box:last-child
{
  grid-column: 1 / -1;
}

/* ===== Octet boxes ===== */

/* every box: green planning border, content clipped to the box.
   Each box fills the grid cell it sits in, minus 0.6em: on page 1 that cell is
   a half of the page (see the #p1 rule); on page 2 the four small boxes get a
   quarter-width cell each and box 7 gets a full-width cell — so boxes 1, 2 and
   7 all come out exactly the same size: full page width, half page height
   (see the #p2 rule). */
.block.box
{
  /* the theme makes every .block an inline-block at 100% width;
     force a plain block that sits cleanly in its grid cell */
  display: block;
  width: auto;
  /* fill its cell's height minus 0.6em: that 0.6em of slack at the bottom of
     every cell is what makes the 0.6em vertical gaps (between the small boxes
     on page 2, between the two big boxes on page 1, and below the tall box) */
  height: calc(100% - 0.6em);
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
     Both are derived from the same page numbers the small boxes above are built from
     (11in x 8.5in landscape page, 0.9em padding, 2 rows, 0.6em gap, 1px border) */
  width: calc((8.5in - 1.8em) / 2 - 0.6em);
  height: calc((11in - 3.6em) / 4);
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
     Both are derived from the same page numbers the small boxes above are built from
     (11in x 8.5in landscape page, 0.9em padding, 2 rows, 0.6em gap, 1px border) */
  width: calc((8.5in - 1.8em) / 2 - 0.6em);
  height: calc((11in - 3.6em) / 4);
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


<!-- START BOX 9/10 -->
{{box

### What is your Quest?

{{template
You start your adventure in a [**Description**] [**Settlement**] [**Location**] [**Feature**]. [**Event**] [**Time**], causing [**Emotion**].
}}

:

| #     | Description | Settlement | Location       | Feature      | Event         | Time                     | Emotion   |
|:-----:|:-----------:|:----------:|:--------------:|:------------:|:-------------:|:------------------------:|:---------:|
| **1** | Deserted    | Campsite   | atop           | a deep pit   | A battle      | happened a long time ago | Anger     |
| **2** | Exotic      | Ruin       | near           | a great tree | A celebration | is anticipated           | Fear      |
| **3** | Fortified   | Outpost    | on the side of | a monument   | A death       | is happening tomorrow    | Hope      |
| **4** | Remote      | Village    | overlooking    | a tower      | A journey     | occurred today           | Joy       |
| **5** | Rustic      | Small Town | surrounding    | a waterfall  | A sickness    | recently ended           | Nostalgia |
| **6** | Well Known  | Large City | under          | the wall     | A theft       | recently started         | Panic     |

:

{{template

A [**Trait**] [**Person**], concerned about [**Motive**], asks you to [**Objective**] the [**Description**] [**Focus**] in the [**Dungeon**] of [**Adjective**] [**Noun**], [**Complication**].

}}

:

| #     | Trait     | Person      | Motive     | Objective            | Description | Focus             | Dungeon   | Adjective    | Noun     | Complication                  |
|:-----:|:---------:|:-----------:|:----------:|:--------------------:|:-----------:|:-----------------:|:---------:|:------------:|:--------:|:-----------------------------:|
| **1** | Deceiving | Criminal    | Equipment  | Attain power from    | Abandoned   | Anomaly           | Catacombs | Bloodstained | Blades   | before time expires           |
| **2** | Guarding  | Entertainer | Experience | Destroy              | Astral      | Faction           | Cavern    | Chaotic      | Blight   | before the ritual completes   |
| **3** | Guiding   | Expert      | Family     | Escape from          | Decayed     | Information       | Crypt     | Endless      | Darkness | before they escape            |
| **4** | Hunting   | Mage        | Flaws      | Escort someone to    | Defended    | Monster           | Fortress  | Fallen       | Fury     | while outmatched              |
| **5** | Lost      | Mercenary   | History    | Infiltrate           | Hidden      | Seal              | Hideout   | Forbidden    | Lies     | while being hunted            |
| **6** | Spying    | Noble       | Quest      | Investigate          | Elemental   | NPC               | Lair      | Forgotten    | Madness  | against a rival faction       |
| **7** | Tasked    | Priest      | Reputation | Negotiate with       | Connected   | Object / Treasure | Mine      | Shattered    | Mist     | amid betrayal                 |
| **8** | Trading   | Ranger      | Superiors  | Protect              | Strange     | Remains           | Depths    | Shrouded     | Prophecy | though nothing is as it seems |
| **9** | Trapped   | Soldier     | Treasure   | Rescue someone from  | Toxic       | Plant             | Sanctuary | Silent       | Runes    | under false pretenses         |
| **0** | Wounded   | Transporter | Wealth     | Steal something from | Artificial  | Villain           | Temple    | Unknown      | Terror   | while enemies converge        |

}}
<!-- END BOX 9/10 -->

<!-- START BOX 11/12 -->
{{box

{{column-count:3

### Exploring the Wilderness

{{template
You enter a [**Description**] [**Environment**].
}}

:

| #      | Description   | Environment          |
|:------:|:-------------:|:--------------------:|
| **1**  | a desolate    | frozen tundra        |
| **2**  | a familiar    | chilly expanse       |
| **3**  | a forgotten   | snowcapped ridge     |
| **4**  | a frozen      | rocky mountain range |
| **5**  | a haunted     | alpine meadow        |
| **6**  | a luminous    | deep valley          |
| **7**  | a misty       | rolling hillside     |
| **8**  | a rugged      | open plain           |
| **9**  | a sacred      | scattered woodlands  |
| **10** | a scorched    | dark forest          |
| **11** | a serene      | flooded woods        |
| **12** | a shadowed    | bubbling swamp       |
| **13** | a treacherous | misty grove          | 
| **14** | a vast        | tropical jungle      |
| **15** | a vibrant     | ashen wasteland      |
| **16** | a weathered   | volcanic field       |
| **17** | a wild        | rocky shore          |
| **18** | an exotic     | sandy beach          |
| **19** | an overgrown  | coastal scrubland    |
| **20** | an unexplored | arid desert          |

\column

### Exploring a Dungeon

{{template
You enter a [**Description**] [**Area**].
}}

:

| #      | Description      | Area                                 |
|:------:|:----------------:|:------------------------------------:|
| **1**  | a branching      | atrium with 3 exits                  |
| **2**  | a circular       | bridge                               |
| **3**  | a cluttered      | connection to a previous area        |
| **4**  | a cold           | chamber with 2 exits                 |
| **5**  | a cramped        | crawlspace                           |
| **6**  | a damaged        | dead end                             |
| **7**  | a dark           | exit from the dungeon                |
| **8**  | a decorated      | chamber with 2 exits                 |
| **9**  | a domed          | passage with a 4-way intersection    |
| **10** | a dusty          | passage with a locked side door      |
| **11** | a flooded        | passage with a right-angle turn      |
| **12** | a long           | chamber with 2 exits. One is locked  |
| **13** | a mossy          | passage with a T-shaped intersection |
| **14** | a narrow         | passage with an alcove               |
| **15** | a sealed         | room with a ladder                   |
| **16** | a sloped         | chamber with 3 exits                 |
| **17** | a torch-lit      | rotunda with 4 exits. One is locked  |
| **18** | a webbed         | staircase                            |
| **19** | an echoing       | vault with a larged, locked door     |
| **20** | an overgrown     | chamber with 3 exits. One is locked  |

\column

### What are they talking about?

{{template
They are talking about [**Information**] [**Subject**].
}}

:

| #      | Information                    | Subject              |
|:------:|:------------------------------:|:--------------------:|
| **1**  | a financial gain involving     | a dangerous place    |
| **2**  | a financial loss involving     | a distant location   |
| **3**  | a gain of influence involving  | a historical event   |
| **4**  | a link between an NPC and      | a PC                 |
| **5**  | a link between the PC and      | a safe location      |
| **6**  | a link between the villain and | a sidequest          |
| **7**  | a loss of influence involving  | a traitor            |
| **8**  | a material gain involving      | a world truth        |
| **9**  | a material loss involving      | an allied faction    |
| **10** | a negative change in           | an allied npc        | 
| **11** | a positive change in           | an artifact          |
| **12** | an ambush concerning           | an enemy hideout     |
| **13** | historical knowledge regarding | an enemy npc         |
| **14** | negative news regarding        | an important npc     |
| **15** | positive news regarding        | the current location |
| **16** | the family of                  | the current quest    |
| **17** | the identity of                | the destination      |
| **18** | the location of                | the enemy's plan     |
| **19** | the reputation of              | the party            |
| **20** | the weaknesses of              | the villain          |
}}
}}
<!-- END BOX 11/12 -->

}}
<!-- END FRONT PAGE -->

\page

<!-- START BACK PAGE -->
{{wide

<!-- START BOX 2 -->
{{box
{{invert

### Name

:

| #       | 1    | 2    | 3    |
|:-------:|:----:|:----:|:----:|
| **1**   |    A | hal  | an   |
| **2**   |    E | ris  | ar   |
| **3**   |    I | del  | er   |
| **4**   |    O | mor  | ian  |
| **5**   |    U | bar  | ic   |
| **6**   |   De | net  | in   |
| **7**   |   Ka | kel  | o    |
| **8**   |   Li | lim  | on   |
| **9**   |   Ma | tur  | or   |
| **10**  |   Ro | pen  | us   |
| **11**  |   Be | rond | a    |
| **12**  |   Da | kay  | aea  |
| **13**  |   Ki | jam  | aya  |
| **14**  |   Le | vash | elle |
| **15**  |   Mi | zab  | ene  |
| **16**  |   Ne | yos  | ess  |
| **17**  |   Ru | gran | ette |
| **18**  |   Si | ched | ice  |
| **19**  |   Ta | sark | id   |
| **20**  |   To | kic  | osa  |

}}
}}
<!-- END BOX 2 -->

\column

<!-- START BOX 1 -->
{{box
{{invert

### Yes/No Oracle

:

| #     | Answer           |
|:-----:|:----------------:|
| **6** | Yes, and ...     |
| **5** | Yes, because ... |
| **4** | Yes, but ...     |
| **3** | No, but ...      |
| **2** | No, because ...  |
| **1** | No, and ...      |

{{center

Guidelines, not rules.  
There is no wrong way to play.  
Choose what is most fun.

:

Keep the flow moving:  
If something doesn't make sense, reroll.

:

Defer some questions for later;  
Answers may come naturally as you play.

:

Fail-forward:  
Every failure is a new opportunity  
and a challenge to overcome.

:

Be your character!  
Describe the situation,  
how you handle it, and why.

:

Your actions have consequences and   
change the world in a meaningful way.

}}

{{credits
Juice Smoothie 10/26/26 github.com/jrruethe/juice CC BY-NC-SA 4.0
}}

}}
}}
<!-- END BOX 1 -->

\column

<!-- START BOX 8 -->
{{box
{{invert

### Inspiration

:

| #       | Inspiration                    |
|:-------:|:------------------------------:|
| **1**   | Despair washes over you        |
| **2**   | It fills you with fear         |
| **3**   | This is only the beginning     |
| **4**   | An enemy would want this       |
| **5**   | You've been warned about this  |
| **6**   | It feels out of place here     |
| **7**   | It's not what it appears to be |
| **8**   | The timing seems deliberate    |
| **9**   | That was too easy              |
| **10**  | There's something hidden here  |
| **11**  | It wasn't always this way      |
| **12**  | This predates you              |
| **13**  | Its size surprises you         |
| **14**  | Deep down, you already know    |
| **15**  | You've encountered this before |
| **16**  | It will matter later           |
| **17**  | It's impossibly rare           |
| **18**  | Someone trusted is connected   |
| **19**  | It connects to your goal       |
| **20**  | Your companion would know more |

}}
}}
<!-- END BOX 8 -->

\column

<!-- START BOX 3 -->
{{box
{{invert

### Color

:

| #      |                                                                                        | Color             |
|:------:|:--------------------------------------------------------------------------------------:|:-----------------:|
| **1**  | <span style="background-color:#C700C7; color:Black;"> &nbsp;&nbsp;&nbsp;&nbsp; </span> | Ethereal Magenta  |
| **2**  | <span style="background-color:#FFA1D0; color:Black;"> &nbsp;&nbsp;&nbsp;&nbsp; </span> | Shimmering Ruby   |
| **3**  | <span style="background-color:#c41235; color:Black;"> &nbsp;&nbsp;&nbsp;&nbsp; </span> | Crimson Blood     |
| **4**  | <span style="background-color:#FF8C00; color:Black;"> &nbsp;&nbsp;&nbsp;&nbsp; </span> | Warning Flame     |
| **5**  | <span style="background-color:#FFFF00; color:Black;"> &nbsp;&nbsp;&nbsp;&nbsp; </span> | Highlight Sunbeam |
| **6**  | <span style="background-color:#00FF7F; color:Black;"> &nbsp;&nbsp;&nbsp;&nbsp; </span> | Electric Lime     |
| **7**  | <span style="background-color:#008000; color:Black;"> &nbsp;&nbsp;&nbsp;&nbsp; </span> | Forest Green      |
| **8**  | <span style="background-color:#00CED1; color:Black;"> &nbsp;&nbsp;&nbsp;&nbsp; </span> | Luminescent Cyan  |
| **9**  | <span style="background-color:#0000CD; color:Black;"> &nbsp;&nbsp;&nbsp;&nbsp; </span> | Sturdy Cobalt     |
| **10** | <span style="background-color:#d6ecf3; color:Black;"> &nbsp;&nbsp;&nbsp;&nbsp; </span> | Clear Frost       |
| **11** | <span style="background-color:#ae94e4; color:Black;"> &nbsp;&nbsp;&nbsp;&nbsp; </span> | Fragrant Lavender |
| **12** | <span style="background-color:#4B0082; color:Black;"> &nbsp;&nbsp;&nbsp;&nbsp; </span> | Royal Violet      |
| **13** | <span style="background-color:#000000; color:Black;"> &nbsp;&nbsp;&nbsp;&nbsp; </span> | Mirrored Obsidian |
| **14** | <span style="background-color:#073642; color:Black;"> &nbsp;&nbsp;&nbsp;&nbsp; </span> | Midnight Shade    |
| **15** | <span style="background-color:#657b83; color:Black;"> &nbsp;&nbsp;&nbsp;&nbsp; </span> | Hidden Slate      |
| **16** | <span style="background-color:#C0C0C0; color:Black;"> &nbsp;&nbsp;&nbsp;&nbsp; </span> | Metallic Silver   |
| **17** | <span style="background-color:#E3BF00; color:Black;"> &nbsp;&nbsp;&nbsp;&nbsp; </span> | Midas Gold        |
| **18** | <span style="background-color:#8B4513; color:Black;"> &nbsp;&nbsp;&nbsp;&nbsp; </span> | Worn Leather      |
| **19** | <span style="background-color:#D2B48C; color:Black;"> &nbsp;&nbsp;&nbsp;&nbsp; </span> | Weathered Sand    |
| **20** | <span style="background-color:#FFFFFF; color:Black;"> &nbsp;&nbsp;&nbsp;&nbsp; </span> | Divine Pearl      |

}}
}}
<!-- END BOX 3 -->

<!-- START BOX 4/5/6/7 -->
{{box

### What is the current Situation?

{{template
[**Atmosphere**] [**Location**] [**Subject**] [**Action**]. [**Situation**]
}}
:
| #      | Atmosphere                        | Location            | Action               | Subject               | Situation                               |
|:------:|:---------------------------------:|:-------------------:|:--------------------:|:---------------------:|:---------------------------------------:|
| **1**  | A colorful glow pulses            | around the corner   | barring access to    | a beckoning passage.  | A chase begins.                         | 
| **2**  | A faint movement catches your eye | at the edge         | concealing           | a cairn.              | A shorcut is offered, will you take it? | 
| **3**  | A sticky film covers everything   | behind you          | disclosing           | a dark cave.          | An assumption proves false.             | 
| **4**  | Blood drips                       | below               | drawing attention to | a deep pit.           | Are you being followed?                 | 
| **5**  | Cold moisture beads on stone      | beside you          | encircling           | a glinting treasure.  | Backup will arrive soon.                | 
| **6**  | Creatures laugh                   | beyond reach        | guarding             | a grave.              | Can you pass without being noticed?     | 
| **7**  | Deafening noise fills the area    | everywhere          | hiding               | a large tree.         | Can you use this to your advantage?     | 
| **8**  | Embers crackle                    | far away            | highlighting         | a magical ward.       | For the moment, it is safe to rest.     | 
| **9**  | Flames flicker                    | high above          | hinting at           | a monument.           | Is this the way forward?                | 
| **10** | Fog hovers                        | in the air          | implying             | a stranger.           | It's quiet. Too quiet...                | 
| **11** | Insects buzz                      | in the area ahead   | leading to           | a territorial beast.  | Someone is exposed to danger.           | 
| **12** | Mushroom spores float             | in the distance     | masking              | a well.               | Something calls to you, do you answer?  | 
| **13** | Rouch scraping fills the air      | in the shadows      | obscuring            | creature tracks.      | The enemy gains new allies.             | 
| **14** | Scratching sounds echo            | just out of sight   | pointing toward      | fresh water.          | The silence is suddenly broken.         | 
| **15** | Smoke billows                     | near the walls      | protecting           | mushrooms.            | The way forward becomes clear.          | 
| **16** | The smell of decay rises          | nearby              | revealing            | ruins.                | What are you willing to sacrifice?      | 
| **17** | Thorns protrude                   | on the ground       | shrouding            | scavengers.           | Will you reveal yourself?               | 
| **18** | Water pools                       | to the side         | suggesting           | signs of pursuit.     | Your approach draws unwanted attention. | 
| **19** | Webs cling to every surface       | where you came from | uncovering           | smoke rising.         | Your fear is realized.                  | 
| **20** | Whispers are heard                | within arms reach   | warning of           | unstable ground.      | Your past catches up to you.            | 

}}

}}
<!-- END BOX 4/5/6/7 -->

<!-- END BACK PAGE -->
