import json

from roomObjects.BaseRoom import BaseRoom #This is importing in the class from the BaseRoom file so that I can reference it in 
#the main branch


class gameEngine: # primary class that will import the objects for the game
    def __init__(self, title: str = "Five Guys Game Engine"):
        self.title = title
        self.parser = playerCmdParser(self)
        self.loadActions("actions.json")
        self.loadMap("gameMap.json") #I have added this function so that the user can enter the json file which has the data for the map 
        self.currentRoom = None #I readded this because I think there was some issues with one of my commits and it didnt work so jsut ot be safe
        #ive readded this attribute.
    
    def loadActions(self, path):
        with open(path, "r") as f:
            data = json.load(f)
        for cmd in data.values():
            handler = getattr(self, cmd["handler"])
            self.parser.addActions(cmd["verbs"], handler)

#This funciton will take a seperate file which holds all of the data about the map that the user has made, and turn it into a working map.

    def loadMap(self, path):
        #This block of code is the block that takes in the json file in read mode and then assigns all the data in it as a dictionary.
        with open(path, "r") as f:
            worldData = json.load(f)
            #This is the dictionary that will hold all of the roomObjects in them.
            rooms = {}
            #This for loop goes through each room in the json file and collects the data that the game engine needs from it.
            for roomID in worldData["rooms"]:
                #This just assigns the data from the room that the for loop is currently on to a variable
                data = worldData["rooms"][roomID]
                #This line of code now actaully passes the data through the BaseRoom class and uses the correct data, in this instance
                #just the name and the description.
                newRoom = BaseRoom(data["name"], data["description"])
                #This then names the new object with its id that was taken from the json and stores it in the rooms dictionary.
                rooms[roomID] = newRoom
                #This block of code just assigns the player to the predefined starting room as specified in the json by the user.
                #It also handles the error if the user has not assigned a starting room for the player character.
                if data.get("isStart"):
                    self.currentRoom = newRoom
                else:
                    print("Warning, the player character has no starting point!!")
            #This for loop does the same thing as the last one, just going throught each room in the json file. Ive made two loops as
            #there would be clashes otherwise as the program would try and read through exits that dont actually exist yet.
            for roomID in worldData["rooms"]:
                #This assigns the data from the room that the for loop is currently on to a new variable
                data = worldData["rooms"][roomID]
                #This for loop goes through each exit that is in the room and takes its direction and assigns it to an exit accourding to the BaseRoom class.
                for direction in data["exits"]:

                    targetID = data["exits"][direction]

                    rooms[roomID].addExit(direction, rooms[targetID])

    def handlerMovement(self, args):
        #This checks whether the player has entered a valid direction into the program and if they havent, it just reprompts them so they can enter another command.
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
        else:
            print("You cant go in that direction.")

    def handlerObservation(self, args):
        #This is just the reassignment of the varaible that stores the room that the user is currently in so its easier to 
        #type when coding.
        room = self.currentRoom
        #These two lines just output the name of the room and its description to the player.
        print(f"\n {room.name}")
        print(room.description)
        #This following if statement checks whether there are exits in the room, if there are exits then it outputs their directions
        #to the player, and if there is not then it tells the player that they cantsee any exits.
        if room.exits:
            print("\nExits in the room:")
            for direction in room.exits:
                print({direction})
        else:
            print("There are no visibal exits")
        #The following if statement outputs the items that can be see in the room to the player if there is any.
        if room.items:
            print("\n You see the following objects scattered around the room:")
            for item in room.items:
                print({item.name})


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
            filename = args[0] + ".json"
        else:
            #if the user does not type a name it will save with this filename as a default
            filename = "save.json"
        
        
        #defining what is to be saved
        save_data = {
            "current_room": self.currentRoom.id if self.currentRoom else "start",
            "inventory": [item.name for item in self.inventory]
        }

        #writing to a file
        with open(filename, "w") as file:
            json.dump(save_data, file)
            print(f"Game saved. File saved to: {filename} ")

    def handlerQuit(self, args):
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

    def add_actions(self, actions, handler):
        self.actions.append(playerCmd(actions, handler))

    def parse(self, line):
        words = line.lower().split() # grabs player input string (line), converts it to lowercase & splits for every space
        if not words: # handles the case where the player just presses enter without typing anything; returns the help menu
            return help()
        userVerb = words[0] # words[0] grabs the first word in the split e.g. "go[0] up[1] later[2] now[3]" etc. and assigns it as the action

        for cmd in self.actions:
            if userVerb in cmd.actions:
                return lambda: cmd.handler(words[1:]) # run the function with the matching handler
        return help() # if no valid command is found based on player's input, show the help menu
