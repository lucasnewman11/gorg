from PyQt4.QtCore import pyqtSignal
from Control.Cursor import GateCursor
import json

class Interface():
    # The controller class responsible for facilitating the manipulation of a specific chunk of data through a specific gate.

    def __init__(self):
        self._subordinates = {}
        self._order = []
        self._focus = False
        self._name = ""
        self._parent = False

    def name(self):
        return self._name

    def setName(self, name):
        self._name = name

    def parent(self):
        return self._parent

    def setParent(self, parent):
        self._parent = parent

    def focus(self):
        return self._focus

    def setFocus(self, sub):
        self._focus = sub
        
    def add(self, name, sub):
        self._subordinates[name] = sub
        self._order.append(name)
        sub.setParent(self)
        
    def fragments(self):
        fragments = []
        for i in self._order:
            fragments.append(self._subordinates[i].fragments())
        return fragments

    def subByName(self, name):
        return self._subordinates[name]

    def subByPos(self, pos):
        num = 0
        for i in self._order:
            sub = self._subordinates[i]
            length = sub.length()
            num += length
            if num >= pos:
                return sub
        
    def processFullInputEvent(self, fie):
        fie.inter.append(self)
        point = fie.gie.pos
        sub = self.subByPos(point)
        sub.processFullInputEvent(fie)
        self.setFocus(sub)

class Gate():

    def __init__(self):
        self._name = ""
        self._parent = False
        self._cursor = GateCursor(self)
        self._read_only = False
        self._crop = False
        self._active_keymap = False
        self._primary_keymap = False
        self._text = ""
        self._text_properties = {"colors" : {"black": []}, "bold" : [], "italics": [], "underline": []}

    def name(self):
        return self._name

    def setName(self, name):
        self._name = name

    def parent(self):
        return self._parent

    def setParent(self):
        self._parent = parent

    def cursor(self):
        return self._cursor

    def readOnly(self):
        return self._read_only

    def setReadOnly(self, ro):
        self._read_only = ro

    def crop(self):
        return self._crop

    def setCrop(self, crop):
        self._crop = crop

    def activeMap(self):
        return self._active_keymap

    def setActiveMap(self, keymap):
        self._active_keymap = keymap

    def primaryMap(self):
        return self._primary_keymap
                                
    def setPrimaryMap(self, keymap):
        self._primary_keymap = keymap
        
    def setRaw_text(self, text):
        self._raw_text = text

    def set_property(self, name, value):
        self._properties[name] = value

    def length(self):
        return len(self._raw_text)

    def get_raw_text(self):
        return self._raw_text

    def get_full_text(self):
        return (self._raw_text, self._properties)

    def process_full_input_event(self, fie):
        fie.gate = self
        self._active_keymap.match_input_event(fie)
        self.cursor().update_selection()

class Fragment():

    def __init__(self)
        self._text = ""
        self._properties = {"color" : "black", "bold" : False, "italics": False, "underline": False}

    def text(self):
        return self._text

    def setText(self, text):
        self._text = text

    def properties(self):
        return self._properties

    def setProperty(self, name, value):
        self._properties[name] = value

class Blueprint():

    def __init__(self):
        self._name = ""
        self._order = []
        self._gate_properties = {}

    def set_name(self, name):
        self._name = name

    def name(self):
        return self._name

    def set_order(self, order):
        self._order = order

    def get_order(self):
        return self._order

    def _add_gate(self, gate_name):
        self._gate_properties[gate_name] = {}
        
    def set_gate_property(self, gate_name, prop_name, prop_value):
        if gate_name in self._gate_properties:
            self._gate_properties[gate_name][prop_name] = prop_value
        else:
            self._add_gate(gate_name)
            self._gate_properties[gate_name][prop_name] = prop_value

    def get_gate_property(self, gate_name, prop_name):
        return self._gate_properties[gate_name][prop_name]

    def interface(self, keymaps_dict):
        interface = Interface()
        interface.setname(self.name())
        for i in self._order:
            interface.add_gate(i)
            keymap = keymaps_dict[self.get_gate_property(i, "keymap")]
            interface.get_gate_by_name(i).setname(i)
            interface.get_gate_by_name(i).set_active_keymap(keymap)
            interface.get_gate_by_name(i).set_primary_keymap(keymap)
            interface.get_gate_by_name(i).set_raw_text(self.get_gate_property(i, "text"))
            for j in ("read-only", "color", "bold", "italics", "underline"):
                interface.get_gate_by_name(i).set_property(j, self.get_gate_property(i, j))
            interface.setfocus(i)        
        return interface
        
def make_blueprints_dict_from_file(fyl):
    json_dict = json.load(fyl)
    blue_dict = {}
    for i in json_dict:
        new_blue = Blueprint()
        new_blue.set_name(i)
        new_blue.set_order(json_dict[i]["order"])
        for j in new_blue.get_order():
            gate_name = j
            for k in json_dict[i][j]:
                prop_name = k
                new_blue.set_gate_property(j, k, json_dict[i][j][k])
        blue_dict[i] = new_blue
    return blue_dict
        
    

    
            

        














