import json
import os

class gameEngine: # primary class that will import the objects for the game
    def __init__(self, title: str = "Five Guys Game Engine"):
        self.title = title
        self.parser = playerCmdParser(self)
        self.loadActions("actions.json")
    
    def loadActions(self, path):
        with open(path, "r") as f:
            data = json.load(f)
        for cmd in data.values():
            handler = getattr(self, cmd["handler"])
            self.parser.addActions(cmd["verbs"], handler)

    def handlerMovement(self, args):
        pass

    def handlerObservation(self, args):
        pass

    def handlerInteraction(self, args):
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
            self.inventory["Inventory"].append(target_item) 
            print(f"{target_item.name} has been added to your inventory..")
            return

        #Searching for item in inventory and if it is within the inventory it is dropped
        if item_name in self.inventory["Iventory"]:
            self.inventory["Inventry"].remove(item_name)
            self.currentRoom.items.append(item_name)
            print(f"You have dropped {item_name}.")
            return

        #If there is not the item the user is searching for in the room then this message will pop up
        print(f"You don't see a '{item_name}' here.")

    def handlerInventoryView(self, args):
        print("8~~~~~~~8 Inventory 8~~~~~~~8")
        items = self.inventory.get("Inventory", [])
        if not items:
            #if there are no items in inventory then this will run
            print("Your inventory is empty.")
        else:
            #Outputs each item one by one
            print("You have these items:")
            for item in items:
                print(f"- {item}")

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
        handlerSave()
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
