### Start of BaseCharacter objects

import datetime as dt
import os
import json

class BaseCharacter:
    """BaseCharacter class is the parent class for all character objects in the game.
    It contains the basic attributes and methods that all characters will have."""
    ### Contructor
    def __init__(self, characterJson): 
        """
        Docstring for __init__
        
        :param self: Description
        :param characterJson: Description
        """
        self.type = characterJson.get("Type", "Default Type")
        self.name = characterJson.get("Name", "Default Name")
        self.description = characterJson.get("Description","Default Description")
        self.maxHealth = characterJson.get("MaxHealth", 100)
        self.currentHealth = characterJson.get("CurrentHealth", self.maxHealth)
        self.alive = self.checkAlive()
        self.inventory = characterJson.get("Inventory", {
                                                "Equipped": {
                                                    "MainHand": {},
                                                    "OffHand": {},
                                                    "Armour": {}
                                                },
                                                "BackPack": []
                                        })
        self.equipped = self.inventory["Equipped"]
        self.location = characterJson.get("Location", "Starting Area")
        self.stats = characterJson.get("Stats", {
                                        "StrengthModifier": 5,
                                        "AttackModifier": 5,
                                        "Defense": 5
                                    })
        self.saveFile = f"{self.name}"

        if self.type not in ("NPC", "Player", "Enemy"):
            self.type = "NPC"
    
    ### Methods
    def checkAlive(self): 
        return (self.currentHealth > 0)

    def save(self):
        """
        Docstring for save
        
        :param self: Description
        """
        try:
            time = dt.datetime.now().strftime("%Y-%m-%d-%H%M")
            saveData = { 
                "Type": self.type,
                "Name": self.name,
                "Description": self.description,
                "MaxHealth": self.maxHealth,
                "CurrentHealth": self.currentHealth,
                "Inventory": self.inventory,
                "Location": self.location,
                "Stats": self.stats,
            }
            folder_path = f"SaveFile/{time}"
            os.makedirs(folder_path, exist_ok=True)

            with open (f"{folder_path}/{self.saveFile}.save", "w") as file:
                json.dump(saveData, file, indent=4)
                return
            
        except Exception as e:
            print(str(e))

    def checkDefense(self):
        """
        Docstring for checkDefense
        
        :param self: This is the object its self
        """
        armour = self.equipped.get("Armour",{}) or {}
        defense = armour.get("Defense", self.stats.get("Defense", 0))
        if defense != self.stats.get("Defense"):
            self.stats["Defense"] = defense

    def damage(self, value):
        """
        Docstring for damage
        
        :param self: This is the object its self
        :param value: How much damage is being delt to self
        """
        self.currentHealth = max(self.currentHealth - value, 0)
        self.alive = self.checkAlive() 
        if not self.alive:
            print(f"{self.name} has died.")
            return True
        return False
    
    def heal(self, value):
        """
        Docstring for heal
        
        :param self:  This is the object its self
        :param value: How much Health is being added to self capped at maxHealth
        """
        self.currentHealth = min(self.currentHealth + value, self.maxHealth)
        return

    def tryToHit(self, attack, damage):
        """
        Docstring for tryToHit
        
        :param self: This is the object its self
        :param attack: This is the value for attacking hit
        :param damage: The ammount of damage to be delt 
        """
        self.checkDefense()
        defense = self.stats.get("Defense", 0)
        if attack > defense:
            dead = self.damage(damage)
            print(f"Hit landed. {damage} damage dealt. {self.currentHealth} health left.")
            if dead:
                return True
        else:   
            print ("Hit missed.")
            return False

    def attack(self, target):
        """
        Docstring for attack
        
        :param self: This is the object its self
        :param target: This is the target object its self
        """
        try:
            attackValue = self.stats.get("AttackModifier")

            if "MainHand" not in self.equipped:
                return print("No main hand present in equipped")
        
            item = self.equipped["MainHand"]
            if not item:
                damage = self.stats.get("StrengthModifier")
            else:
                damage = item.get("Damage", 0) + self.stats.get("StrengthModifier", 0)
            return target.tryToHit(attackValue, damage)
            
        except Exception as e:
            print(f"ERROR: {str(e)}")
            return False
