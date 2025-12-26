class gameEngine: # primary class that will import the objects for the game
    def __init__(self, title: str = "Five Guys Game Engine"):
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
        actions = words[0] # words[0] grabs the first word in the split e.g. "go[0] up[1] later[2] now[3]" etc. and assigns it as the action

        for action in self.actions:
            if action in playerCmd.actions:
                return lambda: action.handler(words[1:]) # run the function with the matching handler
        return None # placeholder for no valid handler being found by the parser