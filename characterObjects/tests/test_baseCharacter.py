import BaseObject as base
import json

with open("characterObjects/TestCharacters.json", "r") as f:
    chars = json.load(f)
    mortJson = chars.get("Main")
    deathJson = chars.get("Enemy")
    Mort = base(mortJson)
    Death = base(deathJson)
    print(f"{Mort.alive}")
    Mort.attack(Death)
    Death.attack(Mort)
    print(f"{Mort.alive}")
    Mort.save()