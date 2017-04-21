class InterfaceBlueprint():

    def __init__(self):
        self._name = ""
        self._order = []
        self._subordinates = {}
        self._focus_name = ""
        
    def name(self):
        return self._name
    
    def set_name(self, name):
        self._name = name

    def order(self):
        return self._order

    def set_order(self, order):
        self._order = order

    def focus_name(self):
        return self._focus_name

    def set_focus_name(self, focus_name):
        self._focus_name = focus_name

    def add(self, name, sub):
        self._subordinates[name] = sub
        self._order.append(name)
        
    def sub_by_name(self, name):
        return self._subordinates[name]

    def materialize(self):
        interface = Interface()
        interface.set_name(self.name())
        for i in self.order():
            blueprint = self.sub_by_name(i)
            subordinate = blueprint.materialize()
            interface.add(subordinate.name(), subordinate)
        interface.set_focus(interface.sub_by_name(self.focus_name()))
        return interface

    def data(self):
        return {"name": self.name(),
         "order": [(i, self.sub_by_name(i)) for i in self.order()],
         "focus_name": self.focus_name()}

    def load(self, ind):
        self.set_name(ind["name"])
        self.set_focus_name(ind["focus_name"])
        for i in ind["order"]:
            gb = GateBlueprint()
            gb.load(i)
            self.add(i["name"], gb)
        
class GateBlueprint():

    def __init__(self):
        self._name = False
        self._keymap_blueprint = False
        self._region_blueprint = False
        self._read_only = False
        self._crop = False

    def name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    def region_blueprint(self):
        return self._region_blueprint

    def set_region_blueprint(self, blue):
        self._region_blueprint = blue
    
    def read_only(self):
        return self._read_only

    def set_read_only(self, read_only):
        self._read_only = read_only

    def crop(self):
        return self._crop

    def set_crop(self, crop):
        self._crop = crop

    def keymap_blueprint(self):
        return self._keymap_blueprint

    def set_keymap_blueprint(self, blueprint):
        self._keymap_blueprint = blueprint

    def materialize(self):
        # from Control.Core import my_debug; my_debug()
        gate = Gate()
        gate.set_name(self.name())
        gate.set_keymap(self.keymap_blueprint().materialize())
        gate.set_region(self.region_blueprint().materialize())
        gate.set_read_only(self.read_only())
        gate.set_crop(self.crop())
        return gate
 
    def data(self):
        return {"name": self.name(),
         "keymap": self.keymap_blueprint.data(),
         "region": self.region_blueprint.data(),
         "read_only": self.read_only(),
         "crop": self.crop()}

    def load(self, gd):
        self.set_name(gd["name"]) # name
        rb = RegionBlueprint()
        rb.load(gd["region"])
        self.set_region_blueprint(rb) # region
        kmb = KeymapBlueprint()
        kmb.load(gd["keymap"])
        self.set_keymap_blueprint(kmb) # keymap
        self.set_read_only(gd["read_only"]) # read_only
        self.set_crop(gd["crop"]) # crop

class RegionBlueprint():

    def __init__(self):
        self._markup = ""

    def markup(self):
        return self._markup

    def set_markup(self, markup):
        self._markup = markup

    def materialize(self):
        region = region_from_markup(self._markup)
        return region

    def data(self):
        return self._markup

    def load(self, rs):
        self.set_markup(rs)

class KeymapBlueprint():

    def __init__(self):
        self._name = ""
        self._items = {}

    def name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    def add(self, string, command_name):
        self._items[string] = command_name

    def items(self):
        return self._items

    def set_items(self, items):
        self._items = items

    def materialize(self):
        keymap = Keymap()
        for i in self._items:
            regex = re.compile(i)
            command = getattr(Control.Commands, self._items[i])
            keymap.add(regex, command)
            keymap.set_name(self._name)
        return keymap

    def data(self):
        return self._items

    def load(self, kmd):
        self.set_name(kmd["name"])
        self.set_items(kmd["bindings"])

def make_blueprint_dict_from_filepath(path):
    import sys
    this = sys.modules[__name__]
    fyl = open(path, 'r')
    string = fyl.read()
    yd = yaml.load(string)
    bd = {"Interfaces": {}, "Gates": {}, "Keymaps": {}}
    for i in bd:
        for j in yd[i]:
            attrname = i[:-1] + "Blueprint"
            blue_class = getattr(this, attrname)
            blue = object.__new__(blue_class)
            blue_class.__init__(blue)
            blue.load(yd[i][j])
            bd[i][blue.name()] = blue
    return bd

import re
import yaml
from Control.Markup import region_from_markup
import Control.Commands
from Control.Interfaces import Keymap, Region, Gate, Interface





        

    



