import sys, types
from PyQt4.QtCore import Qt, QObject, pyqtSignal
from PyQt4 import QtGui
from Control.Keymaps import Keymap, Invoker
import View
import Data

class Commander():
    # the top level controller class

    def __init__(self, keymaps_dict, blueprints_dict):
        super(Commander, self).__init__()

        # initialize basics
        self._keymaps = keymaps_dict
        self._blueprints = blueprints_dict
        self._handler = KeyEventHandler()
        self._invoker = Invoker(self._keymaps["Top"])
        self._windows = {}
        self._interfaces = {}
        self._window_assignments = {}
        self._initUI()
        # connect slot

    def _initUI(self):
        self._frame = View.Frames.Frame()
        self._frame.gorg_key_event_signal.connect(self._gorg_key_event)

        start_interface = self._blueprints["Simple_Text"].interface(self._keymaps)
        self.add_interface("start", start_interface)

        start_window = self._frame.get_window("AAAA")["obj"]
        miniwindow = self._frame.get_window("mini")["obj"]
        self.add_window("AAAA", start_window)
        self.add_window("mini", miniwindow)
        
        self.assign_window(start_window, start_interface)
        self.assign_window(miniwindow, start_interface)

        self._frame.show()
    def add_window(self, name, window):
        self._windows[name] = window

    def add_interface(self, name, interface):
        self._interfaces[name] = interface

    def assign_window(self, window, interface):
        self._window_assignments[window] = interface

    def get_interface(self, window):
        return self._windows_assignments[window]

    def _gorg_key_event(self, gke):
        fks = self._handler.process_gorg_key_event(gke)
        if gke.typ == "p":
            fke = FullKeyEvent(gke, fks, self)
            self.process_full_key_event(fke)

    def process_full_key_event(self, fke):
        if not self._invoker.match_key_event(fke):
            target_interface = self._window_assignments[fke.gke.win]
            target_interface.process_full_key_event(fke)
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
            print("Removed:", key)
            self._currently_pressed_keys.remove(gkey)

        return self._get_full_key_string()


class FullKeyEvent():

    def __init__(self, gke, string, commander, inter=False, gate=False, start_pos=False, adjusted_pos=False):
        self.gke = gke
        self.string = string
        self.commander = commander
        self.inter = inter
        self.gate = gate
        self.gate_start_pos = start_pos
        self.gate_adjusted_pos = adjusted_pos
        
