import json
from characterObjects.MainCharObject import MainChar
import os

from roomObjects.BaseRoom import BaseRoom #This is importing in the class from the BaseRoom file so that I can reference it in 
#the main branch


class gameEngine: # primary class that will import the objects for the game
    def __init__(self, title: str = "Five Guys Game Engine"):
        self.title = title
        self.parser = playerCmdParser(self)
        self.currentRoom = None
        self.loadActions("actions.json")
        self.loadMap("gameMap.json") #I have added this function so that the user can enter the json file which has the data for the map 
        self.inventory = {
            "Equipped": {
                "MainHand": {},
                "OffHand": {},
                "Armour": {}
            },
            "Backpack": []
        }
        self.equipped = self.inventory["Equipped"]
        self.stats = {
            "StrengthModifier": 5,
            "AttackModifier": 5,
            "Defense": 5
        }
        self.running = True
        
        # welcome and call observation.
        if self.running and self.currentRoom:
            print("\n" + "="*50)
            print(self.title.center(50))
            print("="*50)
            print("\nType 'help' for a list of commands.\n")
            self.handlerObservation([])
    
    def loadActions(self, path):
        with open(path, "r") as f:
            data = json.load(f)
        for cmd in data.values():
            handler = getattr(self, cmd["handler"])
            desc = cmd.get("description", "")
            usage = cmd.get("usage", "")
            self.parser.addActions(cmd["verbs"], handler, desc, usage)

#This funciton will take a seperate file which holds all of the data about the map that the user has made, and turn it into a working map.

    def loadMap(self, path):
        #This block of code is the block that takes in the json file in read mode and then assigns all the data in it as a dictionary.
        try:
            with open(path, "r") as f:
                worldData = json.load(f)
        except FileNotFoundError:
            print(f"Map file '{path}' not found. Load a map.")
            return

        rooms = {}
        start_set = False
        #This for loop goes through each room in the json file and collects the data that the game engine needs from it.
        for roomID in worldData.get("rooms", {}):
            data = worldData["rooms"][roomID]
            newRoom = BaseRoom(
                data.get("name", roomID),
                data.get("description", ""),
                room_id=roomID,
                isWinRoom=data.get("win", False),
                isDeathRoom=data.get("death", False),
            )
            rooms[roomID] = newRoom
            #This block of code just assigns the player to the predefined starting room as specified in the json by the user.
            #It also handles the error if the user has not assigned a starting room for the player character.
            if data.get("isStart") and not start_set:
                self.currentRoom = newRoom
                start_set = True

        if not rooms:
            print("Warning, Map file has no rooms.")
            return

        if not start_set:
            first_id = next(iter(rooms))
            self.currentRoom = rooms[first_id]
            print(f"Warning, the player character has no starting point!! Defaulting to '{first_id}'.")

        # If the start room is already an end condition, end.
        if getattr(self.currentRoom, "isWinRoom", False):
            print("You win!")
            self.running = False
        if getattr(self.currentRoom, "isDeathRoom", False):
            print("You are dead! Womp Womp!")
            self.running = False

        #This for loop does the same thing as the last one, just going throught each room in the json file. Ive made two loops as
        #there would be clashes otherwise as the program would try and read through exits that dont actually exist yet.
        for roomID in worldData.get("rooms", {}):
            data = worldData["rooms"][roomID]
            for direction in data.get("exits", {}):
                targetID = data["exits"][direction]
                target_room = rooms.get(targetID)
                if target_room:
                    rooms[roomID].addExit(direction.lower(), target_room)
                else:
                    print(f"Warning, Exit '{direction}' from '{roomID}' targets missing room '{targetID}'.")

    

    def handlerMovement(self, args):
        #This checks whether the player has entered a valid direction into the program and if they havent, it just reprompts them so they can enter another command.
        if not self.currentRoom:
            print("No current room set. Load a world first.")
            return
        if not args:
            print("Where do you want to go?")
            return 
        
        direction = args[0].lower() #This gets the word that is after the first word, which for exmaple if the command said
        #"Go North" then the variable is going to store the lowercase version of the second word which is "north".
        #This if statement checks if the room that the player is currently in has an exit in that direction.
        if direction in self.currentRoom.exits:
            #This line then changes the room that the player is currently in, to the one that they are moving to.
            self.currentRoom = self.currentRoom.exits[direction]
            #The following lines arejust feedback to the player, depending on whether the direction they have entered
            #is valid or not.
            print(f"You moved to the {self.currentRoom.name}")
            # Auto-look after moving
            self.handlerObservation([])
            if getattr(self.currentRoom, "isWinRoom", False):
                print("You win!")
                self.running = False
            if getattr(self.currentRoom, "isDeathRoom", False):
                print("You are dead! Womp Womp!")
                self.running = False
        else:
            print("You cant go in that direction.")

    def handlerObservation(self, args):
        #This is just the reassignment of the varaible that stores the room that the user is currently in so its easier to 
        #type when coding.
        if not self.currentRoom:
            print("No current room set. Load a world first.")
            return
        room = self.currentRoom
        #These two lines just output the name of the room and its description to the player.
        print(f"\n {room.name}")
        print(room.description)
        #This following if statement checks whether there are exits in the room, if there are exits then it outputs their directions
        #to the player, and if there is not then it tells the player that they cantsee any exits.
        if room.exits:
            print("\nExits in the room:")
            for direction in room.exits:
                print(f"- {direction}")
        else:
            print("There are no visible exits")
        #The following if statement outputs the items that can be see in the room to the player if there is any.
        if room.items:
            print("\nYou see the following objects scattered around the room:")
            for item in room.items:
                item_name = getattr(item, "name", str(item))
                print(f"- {item_name}")
        else:
            print("\nNo items visible.")

    def handlerInteraction(self, args):
        if not self.currentRoom:
            print("No current room set.")
            return
            
        if not args:
            print("What do you want to do?")
            return

        #used to compare the users input with the items that match with data from the JSON file
        item_name = " ".join(args).lower()
        
        #Checking if the item is within the room
        target_item = None
        for item in self.currentRoom.items:
            if item.name.lower() == item_name:
                target_item = item
                break

        #If the item is within the room then it is removed and added to the inventory
        if target_item:
            self.currentRoom.items.remove(target_item)
            # Match this to your equipItem logic
            self.inventory["Backpack"].append(target_item) 
            print(f"{target_item.name} has been added to your inventory..")
            return

        #Searching for item in inventory and if it is within the inventory it is dropped
        if item_name in self.inventory["Backpack"]:
            self.inventory["Backpack"].remove(item_name)
            self.currentRoom.items.append(item_name)
            print(f"You have dropped {item_name}.")
            return

        #If there is not the item the user is searching for in the room then this message will pop up
        print(f"You don't see a '{item_name}' here.")

    def handlerInventoryView(self, args):
        print("8~~~~~~~8 Inventory 8~~~~~~~8")
        items = self.inventory.get("Backpack", [])
        if not items:
            #if there are no items in inventory then this will run
            print("Your inventory is empty.")
        else:
            #Outputs each item one by one
            print("You have these items:")
            for item in items:
                print(f"- {item}")

    def equipItem(self, itemName, slot):
        """
        Docstring for equipItem
        
        :param self: This is the object its self
        :param itemName: The name of the item to be equipped
        :param slot: The slot to equip the item to
        """
        if slot in self.equipped:
            if itemName not in self.inventory["Backpack"]:
                print(f"Item {itemName} not in backpack.")
                return
            else:
                item = self.inventory["Backpack"][self.inventory["Backpack"].index(itemName)]
                self.inventory["Backpack"].remove(itemName)
            if self.equipped[slot]:
                self.unequipItem(slot)
            self.equipped[slot] = item
            self.checkDefense()
        else:
            print(f"Slot {slot} does not exist in equipped items.")
        
    def unequipItem(self, slot):
        """
        Docstring for unequipItem
        
        :param self: This is the object its self
        :param slot: The slot to unequip the item from
        """
        if slot in self.equipped:
            item = self.equipped[slot]
            self.inventory["Backpack"].append(item)
            self.equipped[slot] = {}
            self.checkDefense()
        else:
            print(f"Slot {slot} does not exist in equipped items.")



    def handlerHelp(self, args):
        # formatting and menu layout
        print("\n" + "="*50)
        print(f"  {self.title} - Help")
        print("="*50 + "\n")
        print("Available Actions:")
        print("-" * 50)
        # pulls actions and handler names from json and lists
        if not self.parser.actions:
            print("No actions loaded. Check actions.json.")
        else:
            try:
                for cmd in self.parser.actions:
                    verbs = ", ".join(cmd.actions)
                    handlerName = cmd.handler.__name__.replace("handler", "").replace("Inventory", "") # removes either handler or Inventory from handle names
                    print(f"  [{handlerName}]")
                    if getattr(cmd, "description", None):
                        print(f"    {cmd.description}")
                    print(f"    Verbs: {verbs}")
                    if getattr(cmd, "usage", None):
                        print(f"    Usage: {cmd.usage}")
                    print()
            except Exception as e:
                print("Error reading the actions set. Check that the actions.json file is valid and contains all of the required fields.\n. Required fields are: verbs, handler, description, usage.")
        print("-" * 50)
        # can add tips or any other info here
        print("\nType any one of these actions to interact with this game.")
        print("\nUsage: <action> [arguments]")
        

    def handlerSave(self, args):
        #filename picker
        #if the user types a name it will take the name and attack it to the save file
        if args:
            base = args[0]
            filename = base if base.endswith(".json") else base + ".json"
        else:
            #if the user does not type a name it will save with this filename as a default
            filename = "save.json"
        
        
        #defining what is to be saved
        room_ref = None
        if self.currentRoom:
            room_ref = getattr(self.currentRoom, "id", None) or getattr(self.currentRoom, "name", None)
        
        # Save inventory (now a dict with Backpack and Equipped)
        backpack_items = self.inventory.get("Backpack", [])
        equipped_items_raw = self.inventory.get("Equipped", {})
        equipped_items = {slot: getattr(item, "name", str(item)) for slot, item in equipped_items_raw.items()}
        
        save_data = {
            "current_room": room_ref or "start",
            "inventory": {
                "Backpack": [getattr(item, "name", str(item)) for item in backpack_items],
                "Equipped": equipped_items
            },
            "stats": self.stats
        }

        #writing to a file with try except error handling
        try:
            with open(filename, "w") as file:
                json.dump(save_data, file)
                print(f"Game saved. File saved to: {filename} ")
        except OSError as e:
            print(f"Unable to save game: {e}")

    def handlerLoad(self, args):
        # pick filename
        if args:
            base = args[0]
            filename = base if base.endswith(".json") else base + ".json"
        else:
            filename = "save.json"
        
        # load save
        try:
            with open(filename, "r") as file:
                save_data = json.load(file)
                
            # get rooms
            room_id = save_data.get("current_room", "start")
            # reload map
            with open("gameMap.json", "r") as f:
                worldData = json.load(f)
            
            rooms = {}
            for roomID in worldData.get("rooms", {}):
                data = worldData["rooms"][roomID]
                newRoom = BaseRoom(
                    data.get("name", roomID),
                    data.get("description", ""),
                    room_id=roomID,
                    isWinRoom=data.get("win", False),
                    isDeathRoom=data.get("death", False),
                )
                rooms[roomID] = newRoom
            
            # room exits
            for roomID in worldData.get("rooms", {}):
                data = worldData["rooms"][roomID]
                for direction in data.get("exits", {}):
                    targetID = data["exits"][direction]
                    target_room = rooms.get(targetID)
                    if target_room:
                        rooms[roomID].addExit(direction.lower(), target_room)
            
            # set room
            if room_id in rooms:
                self.currentRoom = rooms[room_id]
            else:
                print(f"Warning: Saved room '{room_id}' not found. Starting at beginning.")
                self.currentRoom = rooms.get(next(iter(rooms)))
            
            # restore inventory
            inv_data = save_data.get("inventory", {})
            self.inventory["Backpack"] = inv_data.get("Backpack", [])
            self.inventory["Equipped"] = inv_data.get("Equipped", {"MainHand": {}, "OffHand": {}, "Armour": {}})
            
            # stats
            self.stats = save_data.get("stats", self.stats)
            
            print(f"Game loaded from {filename}")
            # show room
            self.handlerObservation([])
        
        #erorr handles for different cases
        except FileNotFoundError:
            print(f"Save file '{filename}' not found.")
        except json.JSONDecodeError:
            print(f"Error reading save file '{filename}'. File may be corrupted.")
        except Exception as e:
            print(f"Error loading game: {e}")
    
    def handlerQuit(self, args):
        self.handlerSave(args)
        print("Saving game...") #printed message to confirm that the game is saving
        self.running = False #stops the game from running

class playerCmd: # class that will handle player input
    def __init__(self, actions, handler, description="", usage=""):
        self.actions = actions # pulls a list of valid synonyms for all actions
        self.handler = handler # a handler is the executable instruction (actual result the player expects by writing an action)
        self.description = description
        self.usage = usage
class playerCmdParser: # the parser will read through the list of actions and match them to a handler, accounting for synonyms
    def __init__(self, engine):
        self.engine = engine # still gotta figure out why i would do this but some guy online doing the same thing did this, if i dont figure it out im deleting this :'D
        self.actions = [] # empty list of valid actions, to be populated by the following functions

    def addActions(self, actions, handler, description="", usage=""):
        self.actions.append(playerCmd(actions, handler, description, usage))

    def parse(self, line):
        words = line.lower().split() # grabs player input string (line), converts it to lowercase & splits for every space
        if not words: # handles the case where the player just presses enter without typing anything; returns the help menu
            return lambda: None  # do nothing on empty input
        userVerb = words[0] # words[0] grabs the first word in the split e.g. "go[0] up[1] later[2] now[3]" etc. and assigns it as the action

        for cmd in self.actions:
            if userVerb in cmd.actions:
                return lambda: cmd.handler(words[1:]) # run the function with the matching handler
        
        # If no matching action found, show an error message
        return lambda: print(f"'{userVerb}' is not a valid action. Type 'help' to see valid actions.")

if __name__ == "__main__":
    engine = gameEngine()
    while engine.running:
        line = input("> ")
        handler = engine.parser.parse(line)
        handler()  # run the selected action
