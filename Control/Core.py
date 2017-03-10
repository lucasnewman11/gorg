import sys, types
from PyQt4.QtCore import Qt, QObject, pyqtSignal
from PyQt4 import QtGui
from Control.Keymaps import Keymap
import View
import Data

class FullInputEvent():

    def __init__(self, gie, string, commander, inter=False, gate=False):
        self.gie = gie
        self.string = string
        self.commander = commander
        self.inter = inter
        self.gate = gate

class Commander():
    # the top level controller class

    def __init__(self, keymaps_dict, blueprints_dict):
        super(Commander, self).__init__()

        # initialize basics
        self._keymaps = keymaps_dict
        self._blueprints = blueprints_dict
        self._handler = KeyEventHandler()
        self._windows = {}
        self._interfaces = {}
        self._window_assignments = {}
        self._initUI()
        # connect slot

    def _initUI(self):
        self.frame = View.Frames.Frame()
        self.frame.gorg_key_event_signal.connect(self._gorg_key_event)
        self.frame.gorg_mouse_event_signal.connect(self._gorg_mouse_event)

        start_interface = self._blueprints["Simple_Text"].interface(self._keymaps)
        mini_interface = self._blueprints["Simple_Text"].interface(self._keymaps)
        self.add_interface("start", start_interface)

        start_window = self.frame.obj_from_path("TOP/AAAAA")
        miniwindow = self.frame.obj_from_path("TOP/MINI")
        self.add_window("AAAAA", start_window)
        self.add_window("MINI", miniwindow)
        
        self.assign_window(start_window, start_interface)
        self.assign_window(miniwindow, mini_interface)

        self.frame.show()

    def keymaps(self):
        return self._keymaps

    def blueprints(self):
        return self._blueprints
    
    def add_window(self, name, window):
        self._windows[name] = window

    def add_interface(self, name, interface):
        self._interfaces[name] = interface

    def assign_window(self, window, interface):
        self._window_assignments[window] = interface

    def get_interface(self, window):
        return self._window_assignments[window]

    def _gorg_key_event(self, gke):
        fks = self._handler.process_gorg_key_event(gke)
        if gke.typ == "p":
            fie = FullInputEvent(gke, fks, self)
            self._process_full_input_event(fie)

    def _gorg_mouse_event(self, gme):
        fms = self._handler.process_gorg_mouse_event(gme)
        if gme.typ in ("p", "m"):
            fie = FullInputEvent(gme, fms, self)
            self._process_full_input_event(fie)

    def _process_full_input_event(self, fie):
        target_interface = self._window_assignments[fie.gie.win]
        target_interface.process_full_input_event(fie)
        self._update_views()

    def _update_views(self):
        for i in self._windows:
            window = self._windows[i]
            window.doc.update_view(self._window_assignments[window])

class KeyEventHandler():

    def __init__(self):
        self._currently_pressed_keys = []

    def _convert_key_to_gkey(self, key):
        if key == Qt.Key_Meta:
            return "Ctrl"
        elif key == Qt.Key_Alt:
            return "Meta"
        elif key == Qt.Key_Escape:
            return "Esc"
        elif key == Qt.Key_Return:
            return "Ret"
        elif key == Qt.Key_Delete:
            return "Del"
        elif key == Qt.Key_Backspace:
            return "Bkspc"
        elif key == Qt.Key_Tab:
            return "Tab"
        elif key == Qt.Key_Shift:
            return "Shft"
        elif key == Qt.Key_CapsLock:
            return "CpsL"
        elif key == Qt.Key_Control:
            return "Cmnd"
        elif key == Qt.Key_Space:
            return "Spc"
        else:
            return chr(key)

    def _convert_click_to_gclick(self, typ):
        if typ in ("p", "r"):
            return "MOUSE_P"
        elif typ == "m":
            return "MOUSE_M"

    def _get_full_key_string(self):
        event_string = False
        if self._currently_pressed_keys:
            if self._currently_pressed_keys[0] in ("Ctrl", "Meta", "Shft", "Cmnd"):
                event_string = "-".join(self._currently_pressed_keys)
            else:
                event_string = self._currently_pressed_keys[-1]

        return(event_string)

    def process_gorg_key_event(self, gke):
        key = gke.key
        typ = gke.typ
        gkey = self._convert_key_to_gkey(key)
        if typ == "p":
            if gkey not in self._currently_pressed_keys:
                self._currently_pressed_keys.append(gkey)
        elif typ == "r":
            self._currently_pressed_keys.remove(gkey)

        return self._get_full_key_string()

    def process_gorg_mouse_event(self, gme):
        typ = gme.typ
        pos = gme.pos
        gclick = self._convert_click_to_gclick(typ)
        if typ == "p":
            if gclick not in self._currently_pressed_keys:
                self._currently_pressed_keys.append(gclick)
        elif typ == "r":
                self._currently_pressed_keys.remove(gclick)
        elif typ == "m":
            return gclick
        return self._get_full_key_string()

        
        
