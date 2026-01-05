#Begginning of the Base Room Class

class BaseRoom:
    def __init__(self, name, description, room_id=None, isWinRoom=False, isDeathRoom=False):
        self.id = room_id or name
        self.name = name #Name of the room e.g. Kitchen, Hall etc
        self.description = description #Description of the room, maybe like what it looks like
        self.exits = {} #Ive decided to change the posiitons variable to exits, this is so that instead of storing where the room is on the map
        #the program will now only store the positions of the exits so that the requirement in the brief that needs room connections is easier to code.
        #It might still be possible to have a position attribute, to show the position of the room on the map as a whole rahter than just its connections with other rooms.
        #Also by having the exits formatted like this it allows the program to not have hardcoded directions, makes it so that the user using the game engine
        #can add the placements of the exits in the json file with a dictionary.
        self.items = []#Here is the list that will hold the items that are going to stored in the room. This means that the user can enter a list of items that they would want 
        #in that particular room, and then the player of the game could pick them up or use them in some way.


        #The below code plays around with the idea that if the player enters a certain room then they can either win the game, or die. This means that the win room could 
        #be the outside, if the gmae is an escsape room game and a death room could be a pitfall that the user didnt look for before entering.
        self.isWinRoom = isWinRoom
        self.isDeathRoom = isDeathRoom

    def addExit(self, direction, roomObject):
        #This function would link the room that the player is current in, to another room in a specific direction.
        self.exits[direction] = roomObject

    def addItem(self, itemObject):
        #This is the function that will put the item into the room, from the json file into the 
        self.items.append(itemObject)

    def removeItem(self, itemName):
        #This removes an item from the list, and would be called when a player picks an item up from a room so it can remove it form the list that holds all the items in that room.
        for item in self.items:
            if item.name.lower() == itemName.lower():    #This is checking whether the item that is to be removed is actually in the room.
                self.items.remove(item)    #This is the line that actually removes the item from the list.
                return item    #This is the linee that returns the item, which coudl then be added to the players inventory.
        return None #This will just return none to the system if the item cannot be found in the lsit.
    

    