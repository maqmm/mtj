# MD to JSON
###### Pie-menus converter

_This is a small script thanks to which you can easily turn the branching dialogs you need into the pie-menu for interactive text insertion using tools [kando](https://github.com/kando-menu/kando) and [Fly-Pie](https://github.com/Schneegans/Fly-Pie)._

***

## Installation 

just:
```
git clone https://github.com/maqmm/mtj.git
```

...and go to usage

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

## Input structure

This script accepts .md or any text file as input. Each line in such a file is a menu element. Which element is nested in which is determined by the number of indents (`<\t>`), if there are 0 indents, you will see these elements when you open the menu, 1 indent will be nested in an element with 0 indentation higher in the file.

Let's examples:

#### Simplest

```
A
B
C
D
```
The simplest menu of four elements that have no indents, all of which will appear when the menu starts. Each line is a element,
![Example1](/img/ex1.png)

#### Nested and spaces&newlines

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
It is important that nesting of objects is done using tab indents, not spaces, because parsing occurs using `\t`. Children will be nested in the parent with the lower padding level shown above. The element without children will be the final element of the insert, the rest will be a menu with elements.

| Opening the menu we also see 4 elements A B C D. | ![Example2](/img/ex2.png) |
| ---         | ---         |
| A: All backslashes `\\` will be escaped due to the MD format, so use the `<enter>` tag for a new line. | ![Example2a](/img/ex2a.png) |
| B: Here you can see how the `<enter>` tag moved the text following it to a new line. But as you may have noticed, the text from the parent partners is included in the final insertion. This is a feature for printing dialogs. You can use the `<t>title<t>` tag and enter text into it, then it will be excluded from the final text and will be used only for the names of elements. | ![Example2b](/img/ex2b.png) |
| C: As you can see from this example, a new line in MD format will mean a new element. The parent is successfully escaped using the `<t>title</t>` tag and is not used in the resulting insertion. | ![Example2c](/img/ex2c.png) |
| D: Since the beginning and end of the line are used for parsing, I recommend using the `<space>` tag for spaces. | ![Example2d](/img/ex2d.png) |
