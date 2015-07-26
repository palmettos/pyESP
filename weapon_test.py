from Records import *
from FormID import *

form_ids = FormIDHandler()

h = Header('palmettos')
g = Group('WEAP', 0)
w = Weapon(form_ids.new_form_id())

w.set_edid('OBXLTestWeapon')
w.set_name('Test Glass LongSword')
w.set_model('Weapons\Glass\LongSword.NIF')
w.set_icon('Weapons\GlassLongsword.dds')
w.set_enchantment_points(5000)
w.set_enchantment(0)
w.set_type(0)
w.set_speed(1.5)
w.set_reach(1.0)
w.set_flags(0)
w.set_value(500)
w.set_health(500)
w.set_weight(10)
w.set_damage(22)
w.finalize()

g.add_record(w.record)
g.finalize()
h.add_group(g)
h.finalize()

f = open('testweapon.esp', 'wb')
f.write(h.packed)
for group in h.groups:
    f.write(group.header)
    for record in group.records:
        f.write(record)