import json

from roomObjects.BaseRoom import BaseRoom #This is importing in the class from the BaseRoom file so that I can reference it in 
#the main branch


class gameEngine: # primary class that will import the objects for the game
    def __init__(self, title: str = "Five Guys Game Engine"):
        self.title = title
        self.parser = playerCmdParser(self)
        self.currentRoom = None
        self.loadActions("actions.json")
        self.loadMap("gameMap.json") #I have added this function so that the user can enter the json file which has the data for the map 
        self.inventory = []  # check inventory exists for saving
        self.running = True
    
    def loadActions(self, path):
        with open(path, "r") as f:
            data = json.load(f)
        for cmd in data.values():
            handler = getattr(self, cmd["handler"])
            self.parser.addActions(cmd["verbs"], handler)

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
        pass

    def handlerInventoryView(self, args):
        pass

    def handlerInventoryEquip(self, args):
        pass
    
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
            for cmd in self.parser.actions:
                verbs = ", ".join(cmd.actions)
                handlerName = cmd.handler.__name__.replace("handler", "") # removes "handler" from handle names
                print(f"  [{handlerName}]")
                print(f"    {verbs}")
                print()
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
        inv = getattr(self, "inventory", []) or []
        save_data = {
            "current_room": room_ref or "start",
            "inventory": [getattr(item, "name", str(item)) for item in inv]
        }

        #writing to a file with try except error handling
        try:
            with open(filename, "w") as file:
                json.dump(save_data, file)
                print(f"Game saved. File saved to: {filename} ")
        except OSError as e:
            print(f"Unable to save game: {e}")

    def handlerQuit(self, args):
        self.handlerSave(args)
        print("Saving game...") #printed message to confirm that the game is saving
        self.running = False #stops the game from running

class playerCmd: # class that will handle player input
    def __init__(self, actions, handler):
        self.actions = actions # pulls a list of valid synonyms for all actions
        self.handler = handler # a handler is the executable instruction (actual result the player expects by writing an action)
class playerCmdParser: # the parser will read through the list of actions and match them to a handler, accounting for synonyms
    def __init__(self, engine):
        self.engine = engine # still gotta figure out why i would do this but some guy online doing the same thing did this, if i dont figure it out im deleting this :'D
        self.actions = [] # empty list of valid actions, to be populated by the following functions

    def addActions(self, actions, handler):
        self.actions.append(playerCmd(actions, handler))

    def parse(self, line):
        words = line.lower().split() # grabs player input string (line), converts it to lowercase & splits for every space
        if not words: # handles the case where the player just presses enter without typing anything; returns the help menu
            return self.engine.handlerHelp  # return help
        userVerb = words[0] # words[0] grabs the first word in the split e.g. "go[0] up[1] later[2] now[3]" etc. and assigns it as the action

        for cmd in self.actions:
            if userVerb in cmd.actions:
                return lambda: cmd.handler(words[1:]) # run the function with the matching handler
        return self.engine.handlerHelp  # return help

if __name__ == "__main__":
    engine = gameEngine()
    while engine.running:
        line = input("> ")
        handler = engine.parser.parse(line)
        handler()  # run the selected action