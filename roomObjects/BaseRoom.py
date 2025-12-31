#Begginning of the Base Room Class

class BaseRoom:
    def __init__(self, name, description):
        self.name = name #Name of the room e.g. Kitchen, Hall etc
        self.description = description #Description of the room, maybe like what it looks like
        self.exits = {} #Ive decided to change the posiitons variable to exits, this is so that instead of storing where the room is on the map
        #the program will now only store the positions of the exits so that the requirement in the brief that needs room connections is easier to code.
        #It might still be possible to have a position attribute, to show the position of the room on the map as a whole rahter than just its connections with other rooms.
        #Also by having the exits formatted like this it allows the program to not have hardcoded directions, makes it so that the user using the game engine
        #can add the placements of the exits in the json file with a dictionary.


        #The below code plays around with the idea that if the player enters a certain room then they can either win the game, or die. This means that the win room could 
        #be the outside, if the gmae is an escsape room game and a death room could be a pitfall that the user didnt look for before entering.
        self.inWinRoom = False
        self.inDeathRoom = False

    def addExit(self, direction, roomObject):
        #This function would link the room that the player is current in, to another room in a specific direction.
        self.exits[direction] = roomObject

    