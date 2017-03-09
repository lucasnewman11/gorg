from PyQt4.QtCore import pyqtSignal
from Control.Cursor import GateCursor
import json

class Interface():
    # The controller class responsible for facilitating the manipulation of a specific chunk of data through a specific gate.

    def __init__(self):
        self._gates = {}
        self._order = []
        self._focus = False

    def setfocus(self, gate):
        self._focus = gate

    def getfocus(self):
        return self._focus
        
    def add_gate(self, name):
        self._gates[name] = Gate()
        self._order.append(name)
        
    def get_full_text(self):
        text_list = []
        for i in self._order:
            text_list.append(self._gates[i].get_full_text())
        return text_list

    def get_gate_by_name(self, name):
        return self._gates[name]

    def get_gate_by_pos(self, pos):
        num = 0
        for i in self._order:
            gate = self._gates[i]
            length = gate.get_len()
            num += length
            if num >= pos:
                return gate
        
    def process_full_input_event(self, fie):
        fie.inter = self
        point = fie.gie.pos
        gate = self.get_gate_by_pos(point)
        gate.process_full_input_event(fie)
        self.setfocus(gate)

class Gate():

    def __init__(self):
        self._active_keymap = False
        self._primary_keymap = False
        self._raw_text = ""
        self._properties = {"read-only" : False, "color" : "black", "bold" : False, "italics": False, "underline": False}
        self._cursor = GateCursor(self)

    def cursor(self):
        return self._cursor

    def active_keymap(self):
        return self._active_keymap

    def primary_keymap(self):
        return self._primary_keymap
                                
    def set_active_keymap(self, keymap):
        self._active_keymap = keymap

    def set_primary_keymap(self, keymap):
        self._primary_keymap = keymap
        
    def set_raw_text(self, text):
        self._raw_text = text

    def set_property(self, name, value):
        self._properties[name] = value

    def get_len(self):
        return len(self._raw_text)

    def get_raw_text(self):
        return self._raw_text

    def get_full_text(self):
        return (self._raw_text, self._properties)

    def process_full_input_event(self, fie):
        fie.gate = self
        self._active_keymap.match_input_event(fie)
        self.cursor().update_selection()

class Blueprint():

    def __init__(self):
        self._name = ""
        self._order = []
        self._gate_properties = {}

    def set_name(self, name):
        self._name = name

    def get_name(self):
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
        for i in self._order:
            interface.add_gate(i)
            keymap = keymaps_dict[self.get_gate_property(i, "keymap")]
            interface.get_gate_by_name(i).set_active_keymap(keymap)
            interface.get_gate_by_name(i).set_primary_keymap(keymap)
            interface.get_gate_by_name(i).set_raw_text(self.get_gate_property(i, "text"))
            for j in ("read-only", "color", "bold", "italics", "underline"):
                interface.get_gate_by_name(i).set_property(j, self.get_gate_property(i, j))
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
        
    

    
            

        














