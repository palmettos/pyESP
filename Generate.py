import random
import json
import itertools
from Records import *
from FormID import FormIDHandler

enchants = {
    #Burden
    "BRDN": {
        "area":       (0, 0, 0, 0),
        "duration":   (5, 10, 15, 20),
        "magnitude":  (25, 50, 75, 100),
        "actor_value": 11
    },
    #Turn Undead
    "TURN": {
        "area":       (0, 0, 0, 0),
        "duration":   (5, 10, 15, 20),
        "magnitude":  (15, 25, 35, 45),
        "actor_value": 34
    },
    #Damage Fatigue
    "DGFA": {
        "area":       (0, 0, 0, 0),
        "duration":   (0, 0, 0, 0),
        "magnitude":  (25, 30, 35, 40),
        "actor_value": 10
    },
    #Damage Health
    "DGHE": {
        "area":       (0, 0, 0, 0),
        "duration":   (0, 0, 0, 0),
        "magnitude":  (5, 7, 9, 11),
        "actor_value": 8
    },
    #Damage Magicka
    "DGSP": {
        "area":       (0, 0, 0, 0),
        "duration":   (0, 0, 0, 0),
        "magnitude":  (10, 15, 20, 25),
        "actor_value": 9
    },
    #Disintegrate Armor
    "DIAR": {
        "area":       (0, 0, 0, 0),
        "duration":   (0, 0, 0, 0),
        "magnitude":  (20, 30, 40, 50),
        "actor_value": 0
    },
    #Disintegrate Weapon
    "DIWE": {
        "area":       (0, 0, 0, 0),
        "duration":   (0, 0, 0, 0),
        "magnitude":  (20, 30, 40, 50),
        "actor_value": 0
    },
    #Drain Fatigue
    "DRFA": {
        "area":       (0, 0, 0, 0),
        "duration":   (0, 0, 0, 0),
        "magnitude":  (25, 30, 35, 40),
        "actor_value": 10
    },
    #Drain Health
    "DRHE": {
        "area":       (0, 0, 0, 0),
        "duration":   (0, 0, 0, 0),
        "magnitude":  (5, 10, 15, 20),
        "actor_value": 8
    },
    #Drain Magicka
    "DRSP": {
        "area":       (0, 0, 0, 0),
        "duration":   (0, 0, 0, 0),
        "magnitude":  (10, 15, 20, 25),
        "actor_value": 9
    },
    #Fire Damage
    "FIDG": {
        "area":       (0, 0, 0, 0),
        "duration":   (0, 0, 0, 0),
        "magnitude":  (5, 7, 9, 11),
        "actor_value": 8
    },
    #Frost Damage
    "FRDG": {
        "area":       (0, 0, 0, 0),
        "duration":   (0, 0, 0, 0),
        "magnitude":  (5, 7, 9, 11),
        "actor_value": 8
    },
    #Shock Damage
    "SHDG": {
        "area":       (0, 0, 0, 0),
        "duration":   (0, 0, 0, 0),
        "magnitude":  (5, 7, 9, 11),
        "actor_value": 8
    },
    #Weakness to Fire
    "WKFI": {
        "area":       (0, 0, 0, 0),
        "duration":   (5, 10, 15, 20),
        "magnitude":  (5, 10, 15, 20),
        "actor_value": 61
    },
    #Weakness to Frost
    "WKFR": {
        "area":       (0, 0, 0, 0),
        "duration":   (5, 10, 15, 20),
        "magnitude":  (5, 10, 15, 20),
        "actor_value": 62
    },
    #Weakness to Magic
    "WKMA": {
        "area":       (0, 0, 0, 0),
        "duration":   (5, 10, 15, 20),
        "magnitude":  (5, 10, 15, 20),
        "actor_value": 64
    },
    #Weakness to Normal Weapons
    "WKNW": {
        "area":       (0, 0, 0, 0),
        "duration":   (5, 10, 15, 20),
        "magnitude":  (5, 10, 15, 20),
        "actor_value": 65
    },
    #Weakness to Poison
    "WKPO": {
        "area":       (0, 0, 0, 0),
        "duration":   (5, 10, 15, 20),
        "magnitude":  (5, 10, 15, 20),
        "actor_value": 67
    },
    #Weakness to Shock
    "WKSH": {
        "area":       (0, 0, 0, 0),
        "duration":   (5, 10, 15, 20),
        "magnitude":  (5, 10, 15, 20),
        "actor_value": 68
    },
    #Calm
    "CALM": {
        "area":       (0, 0, 0, 0),
        "duration":   (5, 10, 15, 20),
        "magnitude":  (15, 25, 35, 45),
        "actor_value": 33
    },
    #Command Creature
    "COCR": {
        "area":       (0, 0, 0, 0),
        "duration":   (10, 20, 30, 40),
        "magnitude":  (15, 25, 35, 45),
        "actor_value": 0
    },
    #Command Humanoid
    "COHU": {
        "area":       (0, 0, 0, 0),
        "duration":   (10, 20, 30, 40),
        "magnitude":  (15, 25, 35, 45),
        "actor_value": 0
    },
    #Demoralize
    "DEMO": {
        "area":       (0, 0, 0, 0),
        "duration":   (10, 15, 20, 25),
        "magnitude":  (15, 25, 35, 45),
        "actor_value": 34
    },
    #Frenzy
    "FRNZ": {
        "area":       (0, 0, 0, 0),
        "duration":   (5, 10, 15, 20),
        "magnitude":  (15, 25, 35, 45),
        "actor_value": 33
    },
    #Rally
    "RALY": {
        "area":       (0, 0, 0, 0),
        "duration":   (5, 10, 15, 20),
        "magnitude":  (15, 25, 35, 45),
        "actor_value": 34
    },
    #Silence
    "SLNC": {
        "area":       (0, 0, 0, 0),
        "duration":   (5, 10, 15, 20),
        "magnitude":  (0, 0, 0, 0),
        "actor_value": 49
    },
    #Dispel
    "DSPL": {
        "area":       (0, 0, 0, 0),
        "duration":   (0, 0, 0, 0),
        "magnitude":  (15, 25, 35, 45),
        "actor_value": 0
    },
    #Soul Trap
    "STRP": {
        "area":       (0, 0, 0, 0),
        "duration":   (0, 0, 0, 0),
        "magnitude":  (5, 10, 15, 20),
        "actor_value": 0
    },
    #Absorb Health
    "ABHE": {
        "area":       (0, 0, 0, 0),
        "duration":   (0, 0, 0, 0),
        "magnitude":  (5, 7, 9, 11),
        "actor_value": 8
    },
    #Absorb Magicka
    "ABSP": {
        "area":       (0, 0, 0, 0),
        "duration":   (0, 0, 0, 0),
        "magnitude":  (10, 15, 20, 25),
        "actor_value": 9
    }
}

form_ids = FormIDHandler()
h = Header('palmettos')
g = Group('ENCH', 0)
e = None

for meffs in itertools.combinations(enchants.keys(), 4):
    meffs = list(meffs)
    random.shuffle(meffs)

    edid_suff = ''
    for s in meffs:
        edid_suff += s

    e = Enchantment(
        form_ids.new_form_id(),
        'OBXLEnchL0' + edid_suff,
        [2, 0, 0, 0] #weapon, autocalc
        )

    for effect_id in meffs:
        effect = [
            effect_id,
            enchants[effect_id]["magnitude"][0],
            enchants[effect_id]["area"][0],
            enchants[effect_id]["duration"][0],
            1,
            enchants[effect_id]["actor_value"]
        ]
        e.add_effect(effect)

    e.finalize()
    g.add_record(e.record)

g.finalize()
h.add_group(g)
h.finalize()

f = open('4.esp', 'wb')
f.write(h.packed)
for group in h.groups:
    f.write(group.header)
    for record in group.records:
        f.write(record)
