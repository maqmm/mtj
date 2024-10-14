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
| `--flypie` | Generate JSON menu for [Fly-Pie](https://github.com/Schneegans/Fly-Pie), by default for [kando](https://github.com/kando-menu/kando) |
| `-p`, `--print` | Print output .json file with run cmd. |
| _menu settings_ |
| `-n`, `--name` | Name for output menu, by default `Converted menu`. |
| `-e`, `--emoji` | Emoji for menu, by default 🥝. |
| `-sc`, `--shortcut` | Menu execite shortcut, by default NUM3. |

## Input structure

_soon..._