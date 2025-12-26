#Begginning of the Base Room Class

class BaseRoom:
    def __init__(self, name, description, position):
        self.name = name #Name of the room e.g. Kitchen, Hall etc
        self.description = description #Description of the room, maybe like what it looks like
        self.position = position # Positions of the room, north, east, south, west etc so the player can say things like go north
        