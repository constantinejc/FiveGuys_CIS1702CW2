# Structer of json data for objects
#### This is the guide for how data should be saved for the objects in json format.
---
### Characters
- Base Character
```
{
    "Name": CharacterName,
    "Descrtiption": description of character,
    "MaxHealth": Int value for health,
    "CurrentHealth": Int Value for value for health,
    "Inventory": {
        "Equipped": {
            "MainHand": ...ItemObject,
            "OffHand": ...ItemObject,
            "Armour": ...ItemObject,
        },
        "BackPack": [...ItemObjects]
    },
    "Location": RoomName,
    "Stats": {
        ...Stats to be decided
    }
}
```

- NPCS
```
{
    ... SuperConstructor,
    "Dialog": [...DialogList],

}
```

- Enemy
```
{
    ... SuperConstructor,
    
}
```

- Main Character
```
{
    ... SuperConstructor,
    "Level": Int Value for level
    
}
```