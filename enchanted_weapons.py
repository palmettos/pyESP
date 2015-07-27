from Records import *
from FormID import *
import itertools
import random
import json

cols = {
    "Weight":           0,
    "Speed":            1,
    "Reach":            2,
    "Type":             3,
    "Value":            4,
    "Health":           5,
    "Damage":           6,
    "IgnoreResist":     7,
    "EnchantPoints":    8,
    "Enchantment":      9,
    "ItemName":         10,
    "Model":            11,
    "Icon":             12,
    "Script":           13,
    "ScriptID":         14,
    "EditorID":         15,
    "RecordType":       16,
    "Flags":            17,
    "UserData":         18,
    "QuestItem":        19,
    "Dangerous":        20,
    "Ignored":          21,
    "Deleted":          22
}

weap_types = {
    "Blade%20One%20Hand":   0,
    "Blade%20Two%20Hand":   1,
    "Blunt%20One%20Hand":   2,
    "Blunt%20Two%20Hand":   3,
    "Staff":                4,
    "Bow":                  5
}

max_meffs = 4
enchants = open('weapon_meffs.json', 'r')
enchants = json.load(enchants)
ench_type = 2
ench_cost = 10
ench_charge = 10
ench_autocalc = 0

weapons = open('weapons.json', 'r')
weapons = json.load(weapons)

form_ids = FormIDHandler()
h = Header('palmettos')
g_enchants = Group('ENCH', 0)
g_weapons = Group('WEAP', 0)
e = None
w = None

for n in range(1, max_meffs + 1):
    for meffs in itertools.combinations(enchants.keys(), n):
        meffs = list(meffs)
        random.shuffle(meffs)

        edid_suff = ''
        for s in meffs:
            edid_suff += s
        edid = 'OBXLEnch' + edid_suff

        ench_form_id = form_ids.new_form_id()
        e = Enchantment(
            ench_form_id,
            edid,
            [ench_type, ench_cost, ench_charge, ench_autocalc]
            )

        for effect_id in meffs:
            effect = [
                effect_id,
                random.randint(
                    enchants[effect_id]["magnitude"][0],
                    enchants[effect_id]["magnitude"][1]
                    ),
                random.randint(
                    enchants[effect_id]["area"][0],
                    enchants[effect_id]["area"][1]
                    ),
                random.randint(
                    enchants[effect_id]["duration"][0],
                    enchants[effect_id]["duration"][1]
                    ),
                1,
                enchants[effect_id]["actor_value"]
            ]
            e.add_effect(effect)

        e.finalize()
        g_enchants.add_record(e.record)

        rand_weapon = weapons[random.randint(0, len(weapons)-1)]
        edid = 'OBXLWeap' + edid_suff
        w = Weapon(form_ids.new_form_id())
        w.set_edid(edid)
        w.set_name('OBXLWeap' + edid_suff)
        w.set_model(rand_weapon[cols["Model"]])
        w.set_icon('Weapons\GlassLongsword.dds')
        w.set_script(0)
        w.set_enchantment_points(5000)
        w.set_enchantment(ench_form_id)
        w.set_type(int(weap_types[rand_weapon[cols["Type"]]]))
        w.set_speed(float(rand_weapon[cols["Speed"]]))
        w.set_reach(float(rand_weapon[cols["Reach"]]))
        w.set_flags(0)
        w.set_value(int(rand_weapon[cols["Value"]]))
        w.set_health(int(rand_weapon[cols["Health"]]))
        w.set_weight(float(rand_weapon[cols["Weight"]]))
        w.set_damage(int(rand_weapon[cols["Damage"]]))
        w.finalize()
        g_weapons.add_record(w.record)


g_enchants.finalize()
h.add_group(g_enchants)
g_weapons.finalize()
h.add_group(g_weapons)
h.finalize()

f = open('8.esp', 'wb')
f.write(h.packed)
for group in h.groups:
    f.write(group.header)
    for record in group.records:
        f.write(record)