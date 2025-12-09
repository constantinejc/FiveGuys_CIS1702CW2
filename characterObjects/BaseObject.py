### Start of BaseCharacter objects

import datetime as dt
import os
import json

class BaseCharacter:
    ### Contructor
    def __init__(self, characterJson): 
        """Character object, this can be extended for players, enemies and NPCs. 
        All data is loaded from a JSON dict and provides core stats, combat and 
        inventory handling as well as save functionality""" 
        self.type = characterJson.get("Type", "")   # Is this specifiying between enemy, player and NPC? (im also just kinda testing pushing lol)
        self.name = characterJson.get("Name","")
        self.description = characterJson.get("Description","")
        self.maxHealth = characterJson.get("MaxHealth", int)
        self.currentHealth = characterJson.get("CurrentHealth", int)
        self.alive = self.checkAlive()
        self.inventory = characterJson.get("Inventory", "")
        self.equipped = self.inventory.get("Equipped","")
        self.location = characterJson.get("Location", "")
        self.stats = characterJson.get("Stats","")
        self.saveFile = f"{self.name}"
    
    ### Methods
    def checkAlive(self): 
        """Returns true if the character's health is above 0"""
        return (self.currentHealth > 0)

    def save(self):
        """Saves this object in the designated area under the correct filepath"""
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
                json.dump(saveData, file)
                return
            
        except Exception as e:
            print(str(e))

    def checkDefense(self):
        armour = self.equipped.get("Armour")
        defense = armour.get("Defense")
        if defense != self.stats.get("Defense"):
            self.stats["Defense"] = defense

    def damage(self, value): 
        """Function for taking damage and checking if the character is still alive."""
        self.currentHealth -= value
        self.alive = self.checkAlive() 
        if not self.alive: 
            self.currentHealth = 0
        return

    def tryToHit(self, attack, damage):
        """Check the opponent's attack against characters defense and take damage if they hit."""
        self.checkDefense()
        defense = self.stats.get("Defense")
        if attack > defense:
            self.damage(damage)
            return print(f"Hit landed. {damage} damage dealt. {self.currentHealth} health left.")
        return print ("Hit missed.")


    def attack(self, target):
        """Send attack and damage to the target's tryToHit function (use their fist if no weapon is in the hand)"""
        try:
            attack = self.stats.get("AttackModifier")

            if "MainHand" not in self.equipped:
                return print("No main hand present in equipped")
        
            item = self.equipped["MainHand"]
            if item == None:
                damage = self.stats.get("StrengthModifier")
            else:
                damage = item.get("Damage")
            target.tryToHit(attack, damage)
        
        except Exception as e:
            print(f"ERROR: {str(e)}")

### TEST AREA
with open("characterObjects/TestCharacters.json", "r") as f:
    chars = json.load(f)
    mortJson = chars.get("Main")
    deathJson = chars.get("Enemy")
    Mort = BaseCharacter(mortJson)
    Death = BaseCharacter(deathJson)
    print(f"{Mort.alive}")
    Mort.attack(Death)
    Death.attack(Mort)
    print(f"{Mort.alive}")