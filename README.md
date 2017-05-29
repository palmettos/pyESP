# pyESP
A tool for programmatically generating ESP files for use in the TES4 Construction Set.
This library is primarily useful for overwriting large portions of TES4 game data with randomized records, and was created as a utility for use in the ongoing development of the TES4 modification, OblivionXL. Learn more about OblivionXL at www.oblivionxl.com.

The library currently only supports Enchantments, Weapons and Leveled Item lists. It is currently not very user friendly, but will be greatly improved upon as time permits.

# Tutorial
The TES4 ESP file format consists of its header and one or more groups consisting of records. There is one group for each set of records according to their type. For example, an ESP file that only modified armor objects would consist of a header and an 'ARMO' group. The 'ARMO' group would consist of 'ARMO' records. Each record would consist of subrecords specific to that object type. All record types follow this convention. For more information regarding type-specific subrecords, refer to this page: http://www.uesp.net/wiki/Tes4Mod:Mod_File_Format. Unfortunately, this page does only a mediocre job of explaining how the ESP file works and some reverse engineering may be necessary if you intend on expanding on this library.

As a basic example, let's create a weapon. We start by instantiating a FormIDHandler:

```python
from esp.form_ids import FormIDHandler

id_handler = FormIDHandler()
```

This will provide us with a way to give any objects we create unique FormIDs as the handler tracks dispensed FormIDs internally. Next, we create our header:

```python
from esp import records

header = records.Header('palmettos')
```

The argument provided is the author of the file which will be displayed in the TES4 launcher and Construction Set. Next, we create our weapon group:

```python
weapon_group = records.Group('WEAP', 0)
```

The second positional argument is the group type. For the purposes of most record types, this will always be 0. The exception to this is cell records, which you can read about on the wiki mentioned above. Next, we'll create our weapon:

```python
weapon = records.Weapon(id_handler.new_form_id()) # The FormID.
weapon.set_edid('pyESPExampleWeapon') # The EditorID of the record, for use in the Construction Set.
weapon.set_name('pyESP Example Weapon') # The name of the weapon, shown in-game.
weapon.set_model('Weapons\\GlassShortsword.dds') # The model to be used in-game.
weapon.set_bound_radius(28.748772) # The bound radius of the model.
weapon.set_icon('Weapons\\Glass\\ShortSword.NIF') # The icon to be used in the game's interface.
weapon.set_script(0) # The FormID of the script to be used for this weapon. If no script is desired, provide 0.
weapon.set_enchantment_points(100) # The enchantment points.
weapon.set_enchantment(0) # The FormID of the enchantment to be attached to the weapon. If no enchantment is desired, provide 0.
weapon.set_type('Blade%20One%20Hand') # The weapon type.
weapon.set_speed(0.8) # The speed of the weapon, in attacks per second.
weapon.set_reach(1.2) # The reach of the weapon
weapon.set_flags(0) # Any flags required. For more information, refer to the wiki provided above.
weapon.set_value(500) # The value of the weapon, in gold pieces.
weapon.set_health(100) # The health of the weapon. This is used in calculating disintegrate damage and durability.
weapon.set_weight(10) # The weight of the item in the inventory.
weapon.set_damage(15) # The base damage of the weapon.
```

Next, we must finalize each record to order its bytes correctly before writing them to the file. Then, we add them to the weapon group:

```python
weapon.finalize()
weapon_group.add_record(weapon.record) # The record attribute is the ordered and packed byte data after finalization.
```

Then, we finalize the group, add it to the header, and finalize the header:

```python
weapon_group.finalize()
header.add_group(weapon_group)
header.finalize()
```

Finally, we'll write the file to the hard drive starting from the header and looping through the groups record by record:

```python
f = open('Example.esp', 'wb')
f.write(header.packed)
for group in header.groups:
    f.write(group.header)
    for record in group.records:
        f.write(record)
f.close()
```

Now the file can be loaded into the Construction Set or loaded by the game for use. For a more complicated example which displays how useful the library can be for generating an arbitrary number of randomized records, see enchanted_weapons_and_leveled_lists.py in the root directory of this repository.
