# MD to JSON
###### Pie-menus converter

_This is a small script thanks to which you can easily turn the branching dialogs you need into the pie-menu for interactive text insertion using tools [kando](https://github.com/kando-menu/kando) or [Fly-Pie](https://github.com/Schneegans/Fly-Pie)._

***

## Installation 

just:
```
git clone https://github.com/maqmm/mtj.git
```

...and go to usage

***

## Usage

```
cd mtj
python3 MDTOJSON.py -i path/to/input/md -o path/to/output/json
```

| __Flag__ | __Description__ |
| ---         | ---         |
| _files settings_ |
| `-i`, `--input` | **(required)** Path to input .md file, details about structure this file [here](#input-structure). |
| `-o`, `--output` | **(required)** Path to output .json file. |
| `--flypie` | Generate JSON menu for [Fly-Pie](https://github.com/Schneegans/Fly-Pie), by default for [kando](https://github.com/kando-menu/kando). |
| `-p`, `--print` | Print output .json file with run cmd. |
| _menu settings_ |
| `-n`, `--name` | Name for output menu, by default `Converted menu`. |
| `-e`, `--emoji` | Emoji for menu, by default 🥝. |
| `-sc`, `--shortcut` | Menu execite shortcut, by default NUM3. |

***

## Output

| [kando](https://github.com/kando-menu/kando) | [Fly-Pie](https://github.com/Schneegans/Fly-Pie) |
| ---         | ---         |
| ![OutKando](/img/outk.png) | ![OutFP](/img/outfp.png) |
| In the case of kando, you need to find the menus.json configuration file. See the location for each OS [here](https://github.com/kando-menu/kando/blob/main/docs/config-files.md#the-config-files). Open it and add the converted menu separated by commas to the menus array, so your customized menus before will be saved. | In the case of Fly-Pie, we import the output file using the button on the screen, before doing this, do not forget to move the menu to stash so that they are saved, or upload them in advance using the export button (to the right of button 2). <br>__!!! BE SURE__ to use [the flag](#usage) `--flypie` to create a fly-pie menu|

***

## Input structure

This script accepts .md or any text file as input. Each line in such a file is a menu element. Which element is nested in which is determined by the number of indents (`<\t>`), if there are 0 indents, you will see these elements when you open the menu, X indent will be nested in an element with X-1 indentation higher in the file.

| __Tag__ | __Description__ |
| ---         | ---         |
| `<enter>` | Replaced with `\n` in the final text, it serves to bypass the condition that one line = one menu item. |
| `<space>` | Replaced with a simple space (` `) in the final text, used to bypass parsing restrictions at the edges of the element (line). |
| `<i>🗿</i>` | Must contain an emoji, if specified in a line, then the element that declares this line will have such an emoji installed. By default uses 📂 for submenus and 📄 for last insert elements. |
| `<a>-1-359</a>` | The angle [-1 - 359] of the menu item. (If you specify -1, the element will be positioned automatically. In cando too, but the parameter will not be inserted into the element, so as not to observe locks-icons in the editor.) |
| `<t>TITLE</t>` | When using a tag, the text inside it is not used to summarize the final text from the sum of the texts of all parents. But the text inside it will be used to name the element. More details in the [second example](#nested-and-spaces-and-newlines). |
| `<p>PERMANENT</p>` | The opposite of the `<t>TITLE</t>` tag. If this tag is present when summarizing the final text, ONLY its contents will be inserted (or the sum of their contents, if there are several of them). It is advisable to use it in finite elements, but no one limits it. |

__Let's examples:__

***

#### Simplest

```
A
B
C
D
```
The simplest menu of four elements that have no indents, all of which will appear when the menu starts. Each line is a element,
![Example1](/img/ex1.png)

***

#### Nested and spaces and newlines

```
A
	1\n1
B
	2<enter>2
<t>C</t>
	3
	3
<space><space><space><space>D
```
It is important that nesting of objects is done using tab indents, not spaces, because parsing occurs using `\t`. Children will be nested in the parent with the lower padding level shown above. The element without children will be the final element of the insert, the others will be a menu with elements.

| Opening the menu we also see 4 elements A B C D. | ![Example2](/img/ex2.png) |
| ---         | ---         |
| A: All backslashes `\\` will be escaped due to the MD format, so use the `<enter>` tag for a new line. | ![Example2a](/img/ex2a.png) |
| B: Here you can see how the `<enter>` tag moved the text following it to a new line. But as you may have noticed, the text from the parents is included in the final insertion. This is a feature for picking dialogs. You can use the `<t>title<t>` tag and enter text into it, then it will be excluded from the final summarized text and will be used only for the names of elements. | ![Example2b](/img/ex2b.png) |
| C: As you can see from this example, a new line in MD format will mean a new element. The parent text is successfully escaped using the `<t>title</t>` tag and is not used in the resulting insertion. | ![Example2c](/img/ex2c.png) |
| D: Since the beginning and end of the line are used for parsing, I recommend using the `<space>` tag for spaces. | ![Example2d](/img/ex2d.png) |

***

#### Autocopy feature

If you want to receive the same elements at each stage of selection, the easiest way is to copy copies of them under each parent element. But this script implements autocopying. The two examples below give the same result, but at what cost... =)

> [!TIP]
> An unspoken rule follows from this. If you do not want to use autocopy, then it makes sense to place elements of the same level and one parent higher if they have children and lower if they do not. Since with two or more elements of the same level in a row, if the next ones have children, they will be copied to all elements (brothers) above.

| ![Example3a](/img/ex3a.png) | ![Example3b](/img/ex3b.png) |
| ---         | ---         |
| <pre>A&#13;	1&#13;		X&#13;		Y&#13;		Z&#13;	2&#13;		X&#13;		Y&#13;		Z&#13;	3&#13;		X&#13;		Y&#13;		Z&#13;B&#13;	1&#13;		X&#13;		Y&#13;		Z&#13;	2&#13;		X&#13;		Y&#13;		Z&#13;	3&#13;		X&#13;		Y&#13;		Z&#13;C&#13;	1&#13;		X&#13;		Y&#13;		Z&#13;	2&#13;		X&#13;		Y&#13;		Z&#13;	3&#13;		X&#13;		Y&#13;		Z</pre> | <pre>a&#13;b&#13;c&#13;	1&#13;	2&#13;	3&#13;		x&#13;		y&#13;		z</pre> |

In such a simple example, we get 27 elements from 9 lines in the MD file, without having to repeat.

> [!WARNING]  
> Simplification of the example. Autocopy does NOT work with first-level elements that have 0 indents. To simplify the example above, in each case the root element was used to increase the number of indents by 1.