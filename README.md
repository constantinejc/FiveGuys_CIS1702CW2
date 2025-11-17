# CW Requirements & Specifications
## THE TASK
[...] you will **<ins>design, develop, test, and document</ins>** a complete
Python application [...]. 
The project will require you to combine your individual coding skills and manage your work collaboratively using a __shared GitHub repository__. 

**The goal is to produce a single, functional, and well-documented software solution.**

## TECHNICAL SPECIFICATIONS
- **LANGUAGE**: Python 3.8 or newer
- **LIBRARIES**: Python Standard Library only. <ins>No third-party libraries.</ins>

## TEXT-BASED ADVENTURE GAME ENGINE
- **Project Goal**
>  Create a reusable "engine" for a text-based adventure game. Instead of hard-coding the story, the engine should load the game's map, rooms, and interactions from a structured data file (e.g., game_map.json).

- **Key Functional Requirements:**
  - On startup, the program must load the entire game world from a JSON file.
    - This file will define:
      - Rooms `branch:RoomObjects`
      - Descriptions `Part of each object, no need for separate object`
      - Items `branch:ItemObjects`
      - Connections between rooms (e.g., "north" from the "Hall" leads to the "Kitchen") `branch:MapObjects`
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

test thing
