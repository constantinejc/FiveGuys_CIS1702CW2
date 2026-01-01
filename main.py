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

        pass

    def handlerObservation(self, args):
        pass

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
        pass

    def handlerQuit(self, args):
        pass

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