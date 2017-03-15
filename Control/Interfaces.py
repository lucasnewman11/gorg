from PyQt4.QtCore import pyqtSignal
from Control.Cursor import GateCursor, Region, Fragment
import sys
import json

class Interface():
    # The controller class responsible for facilitating the manipulation of a specific chunk of data through a specific gate.

    def __init__(self):
        self._name = ""
        self._parent = False
        self._subordinates = {}
        self._order = []
        self._focus = False

    def name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    def parent(self):
        return self._parent

    def set_parent(self, parent):
        self._parent = parent
        
    def add(self, name, sub):
        self._subordinates[name] = sub
        self._order.append(name)
        sub.setParent(self)

    def sub_by_name(self, name):
        return self._subordinates[name]

    def sub_by_pos(self, pos):
        num = 0
        for i in self._order:
            sub = self._subordinates[i]
            length = sub.length()
            num += length
            if num >= pos:
                return sub

    def focus(self):
        return self._focus

    def set_focus(self, sub):
        self._focus = sub

    def fragments(self):
        fragments = []
        for i in self._order:
            fragments.append(self._subordinates[i].fragments())
        return fragments
        
    def process_full_input_event(self, fie):
        fie.inter.append(self)
        point = fie.gie.pos
        sub = self.subByPos(point)
        sub.processFullInputEvent(fie)
        self.setFocus(sub)

class Gate():

    def __init__(self):
        self._name = ""
        self._parent = False
        self._region = Region()
        self._cursor = GateCursor(self)
        self._read_only = False
        self._crop = False
        self._active_keymap = False
        self._primary_keymap = False

    def name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    def parent(self):
        return self._parent

    def set_parent(self):
        self._parent = parent

    def region(self):
        return self._region

    def set_region(self):
        self._region = region

    def cursor(self):
        return self._cursor

    def read_only(self):
        return self._read_only

    def set_read_only(self, ro):
        self._read_only = ro

    def crop(self):
        return self._crop

    def set_crop(self, crop):
        self._crop = crop

    def active_map(self):
        return self._active_keymap

    def set_active_map(self, keymap):
        self._active_keymap = keymap

    def primary_map(self):
        return self._primary_keymap
                                
    def set_primary_map(self, keymap):
        self._primary_keymap = keymap

    def process_full_input_event(self, fie):
        fie.gate = self
        self._active_keymap.match_input_event(fie)
        self.cursor().update_selection()

class InterfaceBlueprint():

    def __init__(self):
        self._name = ""
        self._focus = ""
        self._order = []
        self._subordinates = {}
    
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

    def sub_by_name(self, name):
        return self._subordinates[name]

    def materialize(self, keymaps_dict):
        interface = Interface()
        interface.set_name(self.name())
        for i in self.order():
            blueprint = self.sub_by_name(i)
            subordinate = blueprint.materialize(keymaps_dict)
            interface.add(subordinate.name(), subordinate)
        interface.set_focus(interface.sub_by_name(self.focus()))
        return interface

class GateBlueprint():

    def __init__(self):
        self._name = False
        self._fragment_dicts = []
        self._read_only = False
        self._crop = False
        self._keymap_name = False


    def name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    def fragment_dicts(self):
        return self._fragment_dicts

    def add_fragment_dict(self, fragment_dict):
        self._fragment_dicts.append(fragment_dict)
    
    def read_only(self):
        return self._read_only

    def set_read_only(self, read_only):
        self._read_only = read_only

    def crop(self):
        return crop

    def set_crop(self, crop):
        self._crop = crop

    def keymap_name(self):
        return self._keymap_name

    def set_keymap_name(self, keymap_name):
        self._keymap_name = keymap_name

    def materialize(self, keymaps_dict):
        gate = Gate()
        gate.set_name(self.name())
        # initializes fragments
        for i in self.fragment_dicts():
            text = i["text"]
            properties = [v for k, v in i.items() if k != "text"]
            fragment = Fragment(text, properties)
            gate.region().add_fragment(fragment)
        # initializes gate properties
        gate.set_read_only(self.read_only())
        gate.set_crop(self.crop())
        # initializes gate keymaps
        keymap = keymaps_dict[self.keymaps_name()]
        gate.set_active_map(keymap)
        gate.set_primary_map(keymap)
        
def make_interface_blueprints_dict_from_file(fyl, gate_blueprints_dict):
    json_dict = json.load(fyl)
    interface_blueprints_dict = {}
    for i in json_dict:
        new_blue = InterfaceBlueprint()
        new_blue.set_name(i)
        properties = json_dict[i]
        order = properties["order"]
        for j in order:
            sub_name = j[0]
            sub_type = j[1]
            if sub_type == "interface":
                try:
                    sub = interface_blueprints_dict[sub_name]
                except ValueError:
                    print("The InterfaceBlueprint for", sub_name, "does not exist.  Check to see if it referenced in your json config file before it has been constructed.")
                    raise ValueError
            elif sub_type == "gate":
                try:
                    sub = gate_blueprints_dict[sub_name]
                except ValueError:
                    print("The GateBlueprint for", sub_name, "does not exist.")
                    raise ValueError
            new_blue.add(sub_name, sub)
        focus_name = properties["focus"]
        new_blue.set_focus_name(focus_name)
    return interface_blueprints_dict
        
def make_gate_blueprints_dict_from_file(fyl):
        
    

    
            

        














