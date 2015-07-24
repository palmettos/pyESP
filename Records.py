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


class TES4(Record):
    def __init__(self):
        Record.__init__(self, 'TES4', 0, 0, 0)
        self.data_size = 0

    def finalize(self):
        self.record = bytes('')
        self.data_size = struct.pack('<L', self.data_size)
        self.record += (self.type + self.data_size +
            self.flags + self.formid + self.vci +
            self.data)


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
        self.tes4 = TES4()

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