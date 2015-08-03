import struct

class Group:
    def __init__(self, label, group_type, stamp = 0):
        self.type = bytes('GRUP')
        self.group_size = 20
        self.label = bytes(label)
        self.group_type = struct.pack('<l', group_type)
        self.stamp = struct.pack('<L', stamp)
        self.records = []
        self.record_count = 1 #group itself counts as record

    def add_record(self, record):
        self.group_size += len(record)
        self.record_count += 1
        self.records.append(record)

    def finalize(self):
        self.header = bytes('')
        self.group_size = struct.pack('<L', self.group_size)
        self.header += (self.type + self.group_size + self.label +
            self.group_type + self.stamp)


class Record:
    def __init__(self, type, flags, formid, vci = 0):
        self.type = bytes(type)
        self.data_size = 0
        self.flags = struct.pack('<L', flags)
        self.formid = struct.pack('<L', formid)
        self.vci = struct.pack('<L', vci)
        self.data = bytes('')

    def add_subrecord(self, subrecord):
        self.data_size += len(subrecord)
        self.data += subrecord

    def finalize(self):
        self.record = bytes('')
        self.data_size = struct.pack('<L', self.data_size)
        self.record += (self.type + self.data_size +
            self.flags + self.formid + self.vci + self.data)


class Subrecord:
    def __init__(self, type):
        self.type = bytes(type)
        self.data_size = 0
        self.data = bytes('')

    def add_data(self, data):
        self.data_size += len(data)
        self.data += data

    def finalize(self):
        self.subrecord = bytes('')
        self.data_size = struct.pack('<H', self.data_size)
        self.subrecord += (self.type + self.data_size + self.data)


class Header:
    def __init__(self, author, master_file = 'Oblivion.esm'):
        self.tes4 = Record('TES4', 0, 0)

        self.hedr = Subrecord('HEDR')
        self.hedr.add_data(struct.pack('<L', 0x3F800000)) #version
        self.hedr.num_records = 0 #finalize

        self.cnam = Subrecord('CNAM')
        self.cnam.add_data(bytes(author) + '\x00')

        self.mast = Subrecord('MAST')
        self.mast.add_data(bytes(master_file) + '\x00') #master file

        self.data = Subrecord('DATA')
        self.data.add_data(struct.pack('<Q', 0))

        self.groups = []

    def add_group(self, group):
        self.hedr.num_records += group.record_count
        self.groups.append(group)

    def finalize(self):
        self.hedr.add_data(struct.pack('<L', self.hedr.num_records))
        self.hedr.add_data(struct.pack('<L', 0x00000800)) #next object id (meaningless?)
        self.hedr.finalize()
        self.cnam.finalize()
        self.mast.finalize()
        self.data.finalize()
        self.tes4.add_subrecord((
            self.hedr.subrecord +
            self.cnam.subrecord +
            self.mast.subrecord +
            self.data.subrecord
            ))
        self.tes4.finalize()
        self.packed = self.tes4.record


class Enchantment:
    def __init__(self, form_id, edid, enit):
        #enit = [type, charge_amount, enchant_cost, flags] & flags (autocalc off) = 0 or 1
        self.record = Record('ENCH', 0, form_id)

        self.edid = Subrecord('EDID')
        self.edid.add_data(bytes(edid) + '\x00')
        self.edid.finalize()

        self.record.add_subrecord(self.edid.subrecord)

        self.enit = Subrecord('ENIT')
        for item in enit:
            self.enit.add_data(struct.pack('<L', item))
        self.enit.finalize()
        self.record.add_subrecord(self.enit.subrecord)

    def add_effect(self, efit):
        #efit = [effect_id, magnitude, area, duration, type, av]
        self.efid = Subrecord('EFID')
        self.efid.add_data(bytes(efit[0])) #effect_id
        self.efid.finalize()

        self.record.add_subrecord(self.efid.subrecord)

        self.efit = Subrecord('EFIT')
        self.efit.add_data(bytes(efit[0]))
        for item in efit[1:]:
            self.efit.add_data(struct.pack('<L', item))
        self.efit.finalize()

        self.record.add_subrecord(self.efit.subrecord)

    def add_script_effect(self, scit):
        #scit = [script_form_id, school, visual_effect, flags] 
        #implement later
        pass

    def finalize(self):
        self.record.finalize()
        self.record = self.record.record


class Weapon:
    def __init__(self, form_id):
        self.weap = Record('WEAP', 0, form_id)
        self.data = Subrecord('DATA')

    def set_edid(self, edid):
        self.edid = Subrecord('EDID')
        self.edid.add_data(bytes(edid) + '\x00')
        self.edid.finalize()

    def set_name(self, name):
        self.full = Subrecord('FULL')
        self.full.add_data(bytes(name) + '\x00')
        self.full.finalize()

    def set_model(self, model):
        self.modl = Subrecord('MODL')
        self.modl.add_data(bytes(model) + '\x00')
        self.modl.finalize()

    def set_bound_radius(self, radius):
        self.modb = Subrecord('MODB')
        self.modb.add_data(struct.pack('<f', radius))
        self.modb.finalize()

    def set_icon(self0, icon):
        self.icon = Subrecord('ICON')
        self.icon.add_data(bytes(icon) + '\x00')
        self.icon.finalize()

    def set_script(self, form_id):
        self.scri = Subrecord('SCRI')
        self.scri.add_data(struct.pack('<L', form_id))
        self.scri.finalize()

    def set_enchantment(self, form_id):
        self.enam = Subrecord('ENAM')
        self.enam.add_data(struct.pack('<L', form_id))
        self.enam.finalize()

    def set_enchantment_points(self, points):
        self.anam = Subrecord('ANAM')
        self.anam.add_data(struct.pack('<H', points))
        self.anam.finalize()

    def set_type(self, type):
        self.type = struct.pack('<L', type)

    def set_speed(self, speed):
        self.speed = struct.pack('<f', speed)

    def set_reach(self, reach):
        self.reach = struct.pack('<f', reach)

    def set_flags(self, flags):
        self.flags = struct.pack('<L', flags)

    def set_value(self, value):
        self.value = struct.pack('<L', value)

    def set_health(self, health):
        self.health = struct.pack('<L', health)

    def set_weight(self, weight):
        self.weight = struct.pack('<f', weight)

    def set_damage(self, damage):
        self.damage = struct.pack('<H', damage)

    def finalize(self):
        self.data.add_data(
            self.type +
            self.speed +
            self.reach +
            self.flags +
            self.value +
            self.health +
            self.weight +
            self.damage
            )
        self.data.finalize()

        self.weap.add_subrecord(
            self.edid.subrecord +
            self.full.subrecord +
            self.modl.subrecord +
            self.modb.subrecord +
            self.icon.subrecord +
            self.scri.subrecord +
            self.enam.subrecord +
            self.anam.subrecord +
            self.data.subrecord
            )
        self.weap.finalize()
        self.record = self.weap.record


class LeveledItem:
    def __init__(self, form_id, edid, chance_none, flag):
        self.record = Record('LVLI', 0, form_id)

        self.edid = Subrecord('EDID')
        self.edid.add_data(bytes(edid) + '\x00')
        self.edid.finalize()
        self.record.add_subrecord(self.edid.subrecord)

        self.chance_none = Subrecord('LVLD')
        self.chance_none.add_data(struct.pack('<b', chance_none))
        self.chance_none.finalize()
        self.record.add_subrecord(self.chance_none.subrecord)

        self.flag = Subrecord('LVLF')
        self.flag.add_data(struct.pack('<b', flag))
        self.flag.finalize()
        self.record.add_subrecord(self.flag.subrecord)

    def add_item(self, level, form_id, count):
        self.lvlo = Subrecord('LVLO')
        self.lvlo.add_data(struct.pack('<H', level))
        self.lvlo.add_data(struct.pack('<H', 4667))
        self.lvlo.add_data(struct.pack('<L', form_id))
        self.lvlo.add_data(struct.pack('<H', count))
        self.lvlo.add_data(struct.pack('<H', 4667))
        self.lvlo.finalize()
        self.record.add_subrecord(self.lvlo.subrecord)

    def finalize(self):
        self.record.finalize()
        self.record = self.record.record
