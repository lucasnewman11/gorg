from PyQt4.QtCore import pyqtSignal
from Control.Keymaps import Invoker
import json

class Interface():
    # The controller class responsible for facilitating the manipulation of a specific chunk of data through a specific gate.

    def __init__(self):
        self._invoker = False
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
        
    def set_invoker(self, invoker):
        self._invoker = invoker

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
        
    def process_full_key_event(self, fke):
        fke.inter = self
        if not self._invoker.match_key_event(fke):
            point = fke.gke.pos
            gate = self.get_gate_by_pos(point)
            gate.process_full_key_event(fke)
            self.setfocus(gate)

    def process_full_mouse_event(self, fme):
        fme.inter = self
        if not self._invoker.match_mouse_event(fme):
            point = fme.gme.pos
            gate = self.get_gate_by_pos(point)
            gate.process_full_mouse_event(fme)
            self.setfocus(gate)
            
class Gate():

    def __init__(self):
        self._invoker = False
        self._raw_text = ""
        self._properties = {"read-only" : False, "color" : "black", "bold" : False, "italics": False, "underline": False}
        self._cursor = GateCursor(self)

    def cursor(self):
        return self._cursor
                                
    def set_invoker(self, invoker):
        self._invoker = invoker
        
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

    def process_full_key_event(self, fke):
        fke.gate = self
        self._invoker.match_key_event(fke)
        self.cursor().update_selection()

    def process_full_mouse_event(self, fme):
        fme.gate = self
        self._invoker.match_mouse_event(fme)
        self.cursor().update_selection()
        
class GateCursor():

    def __init__(self, gate):
        self._gate = gate
        self._point = 0
        self._mark = 0
        self._selection = {}
        self._mark_active = False

    def point(self):
        return self._point

    def mark(self):
        return self._mark

    def setpoint(self, pos):
        raw_text = self._gate.get_raw_text()
        if pos < 0:
            self._point = 0
        elif pos > len(raw_text):
            self._point = len(raw_text)
        else:
            self._point = pos

    def setmark(self, pos):
        raw_text = self._gate.get_raw_text()
        if pos < 0:
            self._mark = 0
        elif pos > len(raw_text):
            self._mark = len(raw_text)
        else:
            self._mark = pos

    def is_mark_active(self):
        return self._mark_active

    def activate_mark(self):
        self._mark_active = True

    def deactivate_mark(self):
        self._mark_active = False

    def update_selection(self):
        raw_text = self._gate.get_raw_text()
        if self._point < self._mark and self.is_mark_active():
            string = raw_text[self._point:self._mark]
        elif self._point > self._mark and self.is_mark_active():
            string = raw_text[self._mark:self._point]
        else:
            string = ''

        start = min(self._point, self._mark)
        end = max(self._point, self._mark)

        self._selection = {"string": string,
                           "start": start,
                           "end": end}

    def selection(self):
        return self._selection

    def get_selection(self, start, end):
        raw_text = self._gate.get_raw_text()
        return raw_text[start:end]

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

    def set_keymap_name(self, keymap_name):
        self._keymap_name = keymap_name

    def get_keymap_name(self):
        return self._keymap_name

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
        keymap = keymaps_dict[self.get_keymap_name()]
        interface.set_invoker(Invoker(keymap))
        for i in self._order:
            interface.add_gate(i)
            keymap = keymaps_dict[self.get_gate_property(i, "keymap")]
            interface.get_gate_by_name(i).set_invoker(Invoker(keymap))
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
        new_blue.set_keymap_name(json_dict[i]["keymap"])
        for j in new_blue.get_order():
            gate_name = j
            for k in json_dict[i][j]:
                prop_name = k
                new_blue.set_gate_property(j, k, json_dict[i][j][k])

        blue_dict[i] = new_blue
    return blue_dict
        
    

    
            

        














