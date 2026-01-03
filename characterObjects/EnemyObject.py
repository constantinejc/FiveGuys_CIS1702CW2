### Start of  MainCharObject
import random
from characterObjects.BaseObject import BaseCharacter as base

class Enemy(base):
    """Enemy Character object extends the baseObject for a character, it
        contains some extras that the baseObject doesn't have."""
    def __init__(self, enemyJson):
        super().__init__(enemyJson)
        self.aggressionLevel = enemyJson.get("aggressionLevel", 1)
        self.lootTable = enemyJson.get("lootTable", {})
    
    def dropLoot(self):
        """
        Docstring for dropLoot
        
        :param self: This is the object its self
        """
        droppedItems = []
        for item, dropChance in self.lootTable.items():
            if random.random() <= dropChance:
                droppedItems.append(item)
        return droppedItems

### Test Area
