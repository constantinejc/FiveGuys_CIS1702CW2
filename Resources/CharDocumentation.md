# Documentaion and reports for Character objects.
### Base object.

Base object imports json for the handling of json save files, it also imports os inorder to create save files and the datatime functionality to create a save file using the date.

Within the constructor of BaseCharcter, we initialise attributes:
- type, the type of charcter ( NPC | Enemy | Player )
- name, the name of the chacter
- description, a general description of the character
- maxHealth, the maximum amount of health the character can can have
- currentHealth, the current health of the character
- alive, weather the character is alive or dead
- inventory, the inventory and equipt items of the character
- equipped, just the equipped of the character
- location, where the character is located
- stats, what stats the char has such as strength and defense
- save file, location that the save fail will be located.

After that we continue to the methods:
- checkAlive, this is how we determain if the character is alive or dead based on if the current health is above 0.
- save, this is how we save the characters information using the current date and time in hours and minutes. we take all the attributes and place them into a dict then save that dict.
- checkDefense, this method gets the equiped armours defense status and updates the users defenses to match.
- damage, this is the method that is called when a character needs to take damage by passing in a value for the dameg and removing that value while not allowing ot to go below 0, it then checks to see if the character is alive.
- heal, this is the reverse of damage as it allows the charcter to gain health while not allowing the value to go above the maxHealth attribute.
- tryToHit, this is the method that needs to be called by other characters. It checks the defense of the character and checks the attack against this value to determain weather it hits, then damage is delt if the attack hits.
- attack, this calls the targets tryToHit and passes all the necisary values.

---

### NPC

The NPC object is a simplistic version of what an NPC should be able to do. It extends the baseCharacter object adding the ability to speak.

extra attributes:
- dialogue, this is a list of dialogue
- maxOption, this is the maximum number of dialogue options.
- currentOption, the current selected dialogue option

extra methods:
- speak, prints the current dialogue option and then moves to the next option.

---

### Enemy

The Enemy object is a basic version of how an enemy should work. Extending the baseCharacter object adding a loot table and agression level.

extra attributes:
- aggressionLevel, this currently has no relevance. Could be used to determain how likely they are to start combat with the player.
- lootTable, this is a dict of items that can be dropped each with a dropChance.

extra methods:
- dropLoot, simply a method for genorating a random number and seeing if a specific item is dropped.

---

### MainChar

This is the player.

extra attributes:
- experience, this is the current experiance ammount of the player.
- level, the current level of the player.

extra methods:
- equipItem, this checks first if the provided slot exists then checks that it is empty (if not it makes it empty) then places the item in the slot.
- unequipItem, removes an item from a slot and places it into the backpack
- changeExperience, this adds the ammount of experiance and then checks if the character should levelup
- experienceToLevelUp, this gets the number of experience needed to levelup.
- playerAttack, this is the specific way that a player attacks, it calls attack and checks how much exp to give for a hit or a kill of the target.
- levelUp, this levels up the plater and adds bonuses to stats.