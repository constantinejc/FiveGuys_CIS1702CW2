### Start of  MainCharObject

from characterObjects.BaseObject import BaseCharacter as base

class MainChar(base):
    """Main Character object extends the baseObject for a character, it
        contains some extras that the baseObject doesn't have."""
    def __init__(self, mainCharJson):
        super().__init__(mainCharJson)
        self.experience = 0
        self.level = 1
        
    def equipItem(self, itemName, slot):
        """
        Docstring for equipItem
        
        :param self: This is the object its self
        :param itemName: The name of the item to be equipped
        :param slot: The slot to equip the item to
        """
        if slot in self.equipped:
            if itemName not in self.inventory["BackPack"]:
                print(f"Item {itemName} not in backpack.")
                return
            else:
                item = self.inventory["BackPack"][self.inventory["BackPack"].index(itemName)]
                self.inventory["BackPack"].remove(itemName)
            if self.equipped[slot]:
                self.unequipItem(slot)
            self.equipped[slot] = item
            self.checkDefense()
        else:
            print(f"Slot {slot} does not exist in equipped items.")
        
    def unequipItem(self, slot):
        """
        Docstring for unequipItem
        
        :param self: This is the object its self
        :param slot: The slot to unequip the item from
        """
        if slot in self.equipped:
            item = self.equipped[slot]
            self.inventory["BackPack"].append(item)
            self.equipped[slot] = {}
            self.checkDefense()
        else:
            print(f"Slot {slot} does not exist in equipped items.")

    def changeExperience(self, amount):
        """
        Docstring for changeExperience
        
        :param self: This is the object its self
        :param amount: The amount of experience to add or remove
        """
        self.experience += amount
        while self.experience >= self.experienceToLevelUp():
            self.levelUp()
        return
    
    def experienceToLevelUp(self):
        """
        Docstring for experienceToLevelUp
        
        :param self: This is the object its self
        :return: The experience needed to level up
        """
        currentExp = self.experience
        needed = 100 * self.level
        needed -= currentExp
        print (f"Experience needed to level up: {needed}")
        return needed

    def playerAttack(self, target):
        """
        Docstring for playerAttack
        
        :param self: This is the object its self
        :param target: This is the target object its self
        """
        try:
            addexp = self.attack(target)
            if addexp:
                if target.currentHealth == 0:
                    print(f"Defeated {target.name}! Gained 100 experience.")
                    self.changeExperience(100)  
                else:
                    print(f"Gained 10 experience for a successful hit.")
                    self.changeExperience(10)  
        except Exception as e:
            print(f"ERROR: {str(e)}")

    def levelUp(self):
        """
        Docstring for levelUp
        
        :param self: This is the object its self
        """
        self.level += 1
        self.maxHealth += 10
        self.currentHealth = self.maxHealth
        self.stats["StrengthModifier"] += 2
        self.stats["Defense"] += 2
        print(f"Leveled up to level {self.level}! Stats increased.")
    
### Test Area
