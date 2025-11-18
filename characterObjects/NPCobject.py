### Start of NPCobject

from characterObjects import BaseObject as base

class NPC(base):
    def __init__(self, npcJson):
        """NPC object extends the baseObject for a character, it
        contains some extras that the baseObject doesn't have."""
        super().__init__(self, npcJson)
        self.dialogue = npcJson.get("Dialogue")
        self.maxOption = len(self.dialogue)
        self.currentOption = 0

    def speak(self):
        """This function is for showing a dialogue from an NPC, it 
        will return the dialogue option from the list of dialogues."""
        if self.currentOption < self.maxOption:
            dialogue = self.dialogue[self.currentOption]
            self.currentOption += 1
            return dialogue
        else:
            self.currentOption = 0
            return self.dialogue[0]
        

### Test Area

