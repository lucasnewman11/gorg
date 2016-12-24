import sys, types
from PyQt4.QtCore import Qt, QObject, pyqtSignal
from PyQt4.QtGui import QKeySequence, QWidget
from Control.Keymaps import Keymap

class Commander(QWidget):
    # the top level controller class

    def __init__(self, keymap):
        super(Commander, self).__init__()
        self._default_keymap = keymap
        self._current_keymap = self._default_keymap
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
        
    def process_gorg_key_signal(self, typ, key, gte):
        gkey = self._convert_key_to_gkey(key)
        if typ == "p":
            if gkey not in self._currently_pressed_keys:
                self._currently_pressed_keys.append(gkey)
                print("Added:", key)
                self.invoke(gte)
            else:
                self.invoke(gte)
        elif typ == "r":
            print("Removed:", key)
            self._currently_pressed_keys.remove(gkey)

    def _process_full_key_event(self):
        print(self._currently_pressed_keys)
        if self._currently_pressed_keys[0] in ("Ctrl", "Meta", "Shft", "Cmnd"):
            event_string = "-".join(self._currently_pressed_keys)
        else:
            event_string = self._currently_pressed_keys[-1]
        return(event_string)
        
    def invoke(self, gte):
        full_key_event = self._process_full_key_event()
        match = self._current_keymap.match(full_key_event)
        if match:
            if type(match) == Keymap:
                self._current_keymap = match
            elif type(match) == types.FunctionType:
                match.__call__(gte, full_key_event)
                self._current_keymap = self._default_keymap
        
