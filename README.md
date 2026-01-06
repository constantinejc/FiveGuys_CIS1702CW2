# TEXT-BASED ADVENTURE GAME ENGINE
- **Project Goal**
>  Create a reusable "engine" for a text-based adventure game. Instead of hard-coding the story, the engine should load the game's map, rooms, and interactions from a structured data file (e.g., game_map.json).
**The goal is to produce a single, functional, and well-documented software solution.**

## TASK SPECIFICATIONS
[...] you will **<ins>design, develop, test, and document</ins>** a complete
Python application [...]. 
The project will require you to combine your individual coding skills and manage your work collaboratively using a __shared GitHub repository__. Perchance 

## TECHNICAL SPECIFICATIONS
- **LANGUAGE**: Python 3.8 or newer
- **LIBRARIES**: Python Standard Library only. <ins>No third-party libraries.</ins>
Our engine has very few things hardcoded:
  - The .json files' filenames are static
  - The available actions are predefined (though the player input command is not)
  - As the project outline plans this as an **adventure** game engine, the way we handle characters falls in line with that descriptor's expectations (e.g. characters have current health, maximum health, they have defense attributes and their ability to damage is tracked, they also have inventories and can handle items, and they can speak and be spoken to)
  - The rooms follow a similar pattern, so they have a description, exits (connections between the rooms), and they can have items in them for the player to obtain

- **Key Functional Requirements:**
  - On startup, the program must load the entire game world from a JSON file.
    - This file will define:
      - Rooms
      - Descriptions
      - Items
      - Connections between rooms (e.g., "north" from the "Hall" leads to the "Kitchen")
  - The player must be able to navigate between rooms using commands like `go north`, `go east`, etc.
  - The player must have an inventory and be able to get item and drop item.
  - The program must parse user input to understand commands and arguments (e.g., verb: `go`, noun: `north`).
  - The game state (player's current location, inventory) must be tracked accurately.
  - The program must handle invalid commands and impossible actions gracefully (e.g., `"You can't go that way."`).
  - Include a `help` command that lists available actions.
  - The game must have a clear win or lose condition defined within the data file.

- **Possible Extensions:**
  - Implement "locked" doors that require a specific item from the inventory to open.
  - Add characters (NPCs) that the player can interact with using a `talk to` command.
  - Allow the player to save and load their game progress to a separate file.

- **Marking Focus Areas:** 
  - Strong separation of game logic ("engine") from game data ("JSON file")
  - Effective use of complex data structures (nested dictionaries/lists)
  - Robust input parser
  - Logical state management

# PREREQUISITES FOR A GAME TO BE LOADED
The engine looks for the following files in the same folder as `main.py`:
  - `actions.json`
  - `gameMap.json`
  - [jack's character object json(s?) for main char, enemies, npcs, etc]

# JSON FILE STRUCTURE
## ACTIONS.JSON
`actions.json` should have a table which maps verbs to a handler. The handlers are hardcoded and the full list is:
- `handlerMovement` which when called will take the direction argument (e.g. `north`) and update the player character's location;
- `handlerObservation` which when called will take the direction argument (e.g. `north`) OR item name argument (e.g. `lantern`) and print its description;
- `handlerInteraction` which when called will take the item name argument (e.g. `lantern`) and add it to the player's inventory;
- `handlerInventoryView` which when called does not take arguments and prints a list of items in the player's posession
- `handlerInventoryEquip` which when called will take the item name argument (e.g. `lantern`), check whether it is in the player's posession and then equip it in the player's hand
- `handlerHelp` which when called does not take arguments and prints a list of all currently available actions, filtering out unavailable ones
- `handlerSave` which when called will take a savefile name argument (e.g. `newestsave`) and will save the game's state to a .json file with the name stated in the argument. The attribute is not required and will default to `save.json`.
- `handlerQuit` which when called does not take arguments and will gracefully quit the program.

The verbs list can be infinitely long and contain any length of strings, fully definable by the game engine's user.

Example structure:
```
{
  "movement": {
    "verbs": ["go", "move", "walk", "run", "mv", "m"],
    "handler": "handlerMovement"
  },
  "observation": {
    "verbs": ["look", "examine", "inspect", "view", "v"],
    "handler": "handlerObservation"
  },
...
```

## GAMEMAP.JSON
`gameMap.json` should be an unordered list of rooms with attributes which define:
  - The room's ID (e.g. `kitchen1`)
  - `name`: The room's player-facing name (e.g. `Kitchen`)
  - `description`: The description of the room which the player can view by inspecting in its direction (e.g. `This is a kitchen. The oven has been left on and there is a gas leak. This is a dangerous place to be. perchance`)
  - `isStart`: Whether this room is the starting room for the player character. Only one room can have this value be set to `true`, the rest must be `false`.
  - `exits`: This defines whether the room has any exits, which cardinal directions they are in and which room is attached to that direction. (e.g. "south": "mainHall", "north": "bedroom1").
  - `death`: This defines whether this is a kill-room. The player dies upon entering and the game enters a failure state. (e.g. `true` as in our example, the kitchen has a gas leak)
  - `win`: This defines whether this is a win condition room. The game enters the win state upon the player entering it. (e.g. `false`)

*Note: the game engine's user must keep track that the exits of a room make sense to the player, unless they explicitly wish to create a non-Euclidean space with doors that change where they lead in one direction.*

Example structure:
```
{
    "rooms": {
        "kitchen1": {
            "name": "Kitchen",
            "description": "The smell of warm bread lingers in the air in the smaller cozy kitchen area",
            "isStart": true,
            "exits": {
                "north": "library1"
            },
            "death": false,
            "win": false
        },

        "library1": {
            "name": "Library",
            "description": "Dust floats in the air, cloating hundreds of old ancient looking books that cover the wall.",
            "isStart": false,
            "exits": {
                "south": "kitchen1",
                "east": "bedroom1"
            },
            "death": false,
            "win": false

        },
...
```

## CHARACTER .JSONS
- Base Character
```
{
    "Type": (NPC | Enemy | Player)
    "Name": CharacterName,
    "Descrtiption": description of character,
    "MaxHealth": Int value for health,
    "CurrentHealth": Int Value for value for health,
    "Inventory": {
        "Equipped": {
            "MainHand": ...ItemObject,
            "OffHand": ...ItemObject,
            "Armour": ...ItemObject,
        },
        "BackPack": [...ItemObjects]
    },
    "Location": RoomName,
    "Stats", {
        "StrengthModifier": Int value,
        "AttackModifier": Int value,
        "Defense": Int value
    }
}
```
- NPC Character
```
{
    ... BaseCharacter,
    "Dialog": [...Dialogues]
}
```

- Enemy Character
```
{
    ... BaseCharacter,
    "aggressionLevel": Int value,
    "LootTable": {
        Itemobjects: Int value drop rate,
        ...
    }
}
```
- Player Character
```
{
    ... BaseCharacter,
    "Experiance": Int value,
    "Level": Int value
}
```
The code does provide a default option for the creation of a base character, with int value filled in and the backpack and equiptment being set to empty.

# SETUP

Clone the repository to an empty folder, put prerequisite .json files next to `main.py` then run `main.py` in environment of choice with Python 3.8 or higher installed.

# USAGE 

Once `main.py` is run, the game should greet the player. The player can act upon the game by providing either a verb on its own, or a verb-noun combination. For a list of all available actions, the player may write `help`. Each command has guidance attached to it, so if the player is unsure about a command's usage they may write `help [command]` to view its guidance.

# LICENSE

This software is released under the GNU General Public License v3.0 (GPL-3.0).

A copy of the licence is included in this repository in the `LICENSE` file.  
Any redistribution or modification must comply with the terms of the GNU GPL.

![Licence: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)
