import sys
from PyQt4.QtCore import Qt, pyqtSignal, QObject
from PyQt4 import QtGui

class GorgKeyEvent():

    def __init__(self, typ, key, pos, win=False, frame=False):
        self.typ = typ
        self.key = key
        self.win = win
        self.pos = pos
        self.frame = frame

class GorgMouseEvent():

    def __init__(self, typ, pos, win=False, frame=False):
        self.typ = typ
        self.pos = pos
        self.win = win
        self.frame = frame
        
class AlphaNamer():

    def __init__(self, length):
        self._length = length
        self._last_used = length * "A"

    def _increment_char(self, char):
        if char == "Z":
            return "A"
        else:
            return chr(ord(char) + 1)
    
    def _increment_string(self, string):
        char_list = (list(string))
        char_list.reverse()
        incr = True
        for i in range(len(char_list)):
            if incr == True:
                new_char = self._increment_char(char_list[i])
                if new_char != "A":
                    incr = False
                char_list[i] = new_char
        char_list.reverse()
        return  "".join(char_list)

    def newname(self):
        new = self._increment_string(self._last_used)
        self._last_used = new
        return new

class Frame(QtGui.QWidget):
    # a custom QT class derived from a QWidget, consisting of a list of Windows and a minibuffer, displayed on a grid layout.

    gorg_key_event_signal = pyqtSignal(GorgKeyEvent)
    gorg_mouse_event_signal = pyqtSignal(GorgMouseEvent)
    
    def __init__(self):
        super(Frame, self).__init__()
        self._grid = QtGui.QGridLayout()
        self.setLayout(self._grid)
        self._grid.setSpacing(0)
        self._grid.setContentsMargins(0, 0, 0, 0)

        self._loc_from_obj = {}
        self._obj_from_loc = {}
        self._name_from_obj = {}
        self._obj_from_name = {}

        top = Lattice()
        self.place_obj(top, "TOP", (1,1))

        self._namer = AlphaNamer(5)
        self._init_UI()

    def _init_UI(self):
        
        start_window = Window()
        self.place_obj(start_window, "TOP/AAAAA", (1,1))

        miniwindow = MiniWindow()
        self.place_obj(miniwindow, "TOP/MINI", (2,1))

        # set up presentation

        self.setGeometry(600, 600, 80, 600)
        self.setWindowTitle('Gorg')
        self.show()

        # accessing and placing objects at Frame level

    def obj_from_name(self, name):
        return self._obj_from_name[name]

    def name_from_obj(self, obj):
        return self._name_from_obj[obj]

    def loc_from_obj(self, obj):
        return self._loc_from_obj[obj]

    def obj_from_loc(self, loc):
        return self._obj_from_loc[loc]

    def _add_obj(self, obj, name, loc):
        self._obj_from_name[name] = obj
        self._name_from_obj[obj] = name
        self._loc_from_obj[obj] = loc
        self._obj_from_loc[loc] = obj
        self._grid.addWidget(obj, loc[0], loc[1])
        obj.gorg_key_event_signal.connect(self._gorg_key_event)
        obj.gorg_mouse_event_signal.connect(self._gorg_mouse_event)

    def remove_obj(self, obj):
        name = self._name_from_obj[obj]
        loc = self._loc_from_obj[obj]
        del self._obj_from_name[name]
        del self._name_from_obj[obj]
        del self._loc_from_obj[obj]
        del self._obj_from_loc[loc]
        self._grid.removeWidget(obj)
        obj.gorg_key_event_signal.disconnect()
        obj.gorg_mouse_event_signal.disconnect()

    def obj_from_path(self, path):
        path_list = path.split("/")
        if len(path_list) == 1:
            return self.obj_from_name(path_list[0])
        else:
            latt = self.obj_from_name(path_list[0])
            new_path = "/".join(path_list[1:])
            return latt.obj_from_path(new_path)
        
    def place_obj(self, obj, path, loc):
        path_list = path.split("/")
        if len(path_list) == 1:
            self._add_obj(obj, path_list[0], loc)
        else:
            latt = self.obj_from_name(path_list[0])
            new_path = "/".join(path_list[1:])
            latt.place_obj(obj, new_path, loc)

    def get_sub_paths(self):
        sub_paths = {}
        for i in self._obj_from_name:
            sub_paths[i] = self._obj_from_name[i].get_sub_paths()
        return sub_paths
            
    def path(self):
        return False

    def _gorg_key_event(self, gke):
        gke.frame = self
        self.gorg_key_event_signal.emit(gke)

    def _gorg_mouse_event(self, gme):
        gme.frame = self
        self.gorg_mouse_event_signal.emit(gme)        

class Lattice(QtGui.QWidget):

    gorg_key_event_signal = pyqtSignal(GorgKeyEvent)
    gorg_mouse_event_signal = pyqtSignal(GorgMouseEvent)

    def __init__(self):
        super(Lattice, self).__init__()
        self._grid = QtGui.QGridLayout()
        self._grid.setSpacing(0)
        self._grid.setContentsMargins(0, 0, 0, 0)
        policy = QtGui.QSizePolicy()
        policy.setVerticalPolicy(QtGui.QSizePolicy.Ignored)
        policy.setHorizontalPolicy(QtGui.QSizePolicy.Ignored)
        self.setSizePolicy(policy)

        self.setLayout(self._grid)

        self._obj_from_name = {}
        self._name_from_obj = {}
        self._obj_from_loc = {}
        self._loc_from_obj = {}

    def obj_from_name(self, name):
        return self._obj_from_name[name]

    def name_from_obj(self, obj):
        return self._name_from_obj[obj]

    def loc_from_obj(self, obj):
        return self._loc_from_obj[obj]

    def obj_from_loc(self, loc):
        return self._obj_from_loc[loc]

    def _add_obj(self, obj, name, loc):
        self._obj_from_name[name] = obj
        self._name_from_obj[obj] = name
        self._loc_from_obj[obj] = loc
        self._obj_from_loc[loc] = obj
        self._grid.addWidget(obj, loc[0], loc[1])
        obj.gorg_key_event_signal.connect(self._gorg_key_event)
        obj.gorg_mouse_event_signal.connect(self._gorg_mouse_event)

    def remove_obj(self, obj):
        name = self._name_from_obj[obj]
        loc = self._loc_from_obj[obj]
        del self._obj_from_name[name]
        del self._name_from_obj[obj]
        del self._loc_from_obj[obj]
        del self._obj_from_loc[loc]
        self._grid.removeWidget(obj)
        obj.gorg_key_event_signal.disconnect()
        obj.gorg_mouse_event_signal.disconnect()

    def obj_from_path(self, path):
        path_list = path.split("/")
        if len(path_list) == 1:
            return self.obj_from_name(path_list[0])
        else:
            latt = self.obj_from_name(path_list[0])
            new_path = "/".join(path_list[1:])
            return latt.obj_from_path(new_path)
        
    def place_obj(self, obj, path, loc):
        path_list = path.split("/")
        if len(path_list) == 1:
            self._add_obj(obj, path_list[0], loc)
        else:
            latt = self.obj_from_name(path_list[0])
            new_path = "/".join(path_list[1:])
            latt.place_obj(obj, new_path, loc)

    def path(self):
        myname = self.parent().name_from_obj(self)
        parent_path = self.parent().path()
        if parent_path:
            mypath = parent_path + "/" + myname
        else:
            mypath = myname
        return mypath

    def get_sub_paths(self):
        sub_paths = {}
        for i in self._obj_from_name:
            sub_paths[i] = self._obj_from_name[i].get_sub_paths()
        return sub_paths

    def _gorg_key_event(self, gke):
        self.gorg_key_event_signal.emit(gke)

    def _gorg_mouse_event(self, gme):
        self.gorg_mouse_event_signal.emit(gme)

class MiniWindow(QtGui.QWidget):
    # a custom QT class derived from a QFrame, consisting of a paired QTextEdit object and QLabel object.  Together, they display the contents and name of a Buffer object.  constructor accepts a buffer object

    gorg_key_event_signal = pyqtSignal(GorgKeyEvent)
    gorg_mouse_event_signal = pyqtSignal(GorgMouseEvent)

    def __init__(self):
        super(MiniWindow, self).__init__()
        # initialize layout
        self._gte = GorgTextEdit()
        self._gte.setMaximumHeight(16)
        self.setMaximumHeight(16)
        self._grid = QtGui.QGridLayout()
        self._grid.addWidget(self._gte, 1, 1)
        self._grid.setSpacing(0)
        self._grid.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self._grid)
        # connect slots
        self._gte.gorg_key_event_signal.connect(self._gorg_key_event)
        self._gte.gorg_mouse_event_signal.connect(self._gorg_mouse_event)
        
    def _gorg_key_event(self, gke):
        gke.win = self
        self.gorg_key_event_signal.emit(gke)

    def _gorg_mouse_event(self, gme):
        gme.win = self
        self.gorg_mouse_event_signal.emit(gme)

    def setFocus(self):
        self._gte.setFocus()

    def gte(self):
        return self._gte

    def path(self):
        myname = self.parent().name_from_obj(self)
        parent_path = self.parent().path()
        if parent_path:
            mypath = parent_path + "/" + myname
        else:
            mypath = myname
        return mypath

    def update_view(self, interface):
        self._gte.update_view(interface)
    
    def get_sub_paths(self):
        return False

class Window(QtGui.QWidget):
    # a custom QT class derived from a QFrame, consisting of a paired QTextEdit object and QLabel object.  Together, they display the contents and name of a Buffer object.  constructor accepts a buffer object

    gorg_key_event_signal = pyqtSignal(GorgKeyEvent)
    gorg_mouse_event_signal = pyqtSignal(GorgMouseEvent)

    def __init__(self):
        super(Window, self).__init__()
        # initialize layout
        self._gte = GorgTextEdit()
        policy = QtGui.QSizePolicy()
        policy.setVerticalPolicy(QtGui.QSizePolicy.Ignored)
        policy.setHorizontalPolicy(QtGui.QSizePolicy.Ignored)
        self.setSizePolicy(policy)
        self._label = GorgWindowLabel()
        self._grid = QtGui.QGridLayout()
        self._grid.addWidget(self._gte, 1, 1)
        self._grid.addWidget(self._label, 2, 1)
        self._grid.setSpacing(0)
        self._grid.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self._grid)
        # connect slots
        self._gte.gorg_key_event_signal.connect(self._gorg_key_event)
        self._gte.gorg_mouse_event_signal.connect(self._gorg_mouse_event)
    
    def _gorg_key_event(self, gke):
        gke.win = self
        self.gorg_key_event_signal.emit(gke)

    def _gorg_mouse_event(self, gme):
        gme.win = self
        self.gorg_mouse_event_signal.emit(gme)        

    def setFocus(self):
        self._gte.setFocus()

    def update_view(self, interface):
        self._gte.update_view(interface)
        self._label.update_view(interface)

    def gte(self):
        return self._gte
        
    def path(self):
        myname = self.parent().name_from_obj(self)
        parent_path = self.parent().path()
        if parent_path:
            mypath = parent_path + "/" + myname
        else:
            mypath = myname
        return mypath

    def get_sub_paths(self):
        return False

class GorgTextEdit(QtGui.QTextEdit):
    # customized QTextEdit class, initialized with a Gate object

    gorg_key_event_signal = pyqtSignal(GorgKeyEvent)
    gorg_mouse_event_signal = pyqtSignal(GorgMouseEvent)

    def __init__(self):
        super(GorgTextEdit, self).__init__()
        self._qtextcursor = self.textCursor()
        self._last_selection = {}
        
    def _select_text(self, start, end):
        self._qtextcursor.setPosition(start)
        self._qtextcursor.setPosition(end, mode = 1)
        
    def _update_selected_text_properties(self, prop_dict):
        print(prop_dict)
        # sets color
        colors = {"black": Qt.black,
                  "white": Qt.white,
                  "red": Qt.red,
                  "blue": Qt.blue,
                  "cyan": Qt.cyan,
                  "magenta": Qt.magenta,
                  "yellow": Qt.yellow,
                  "green": Qt.green}
        text_color = QtGui.QColor(colors[prop_dict["color"]])
        self.setTextColor(text_color)

        # sets bold
        if prop_dict["bold"] == True:
            self.setFontWeight(75)
        else:
            self.setFontWeight(50)

        # sets italic
        if prop_dict["italics"] == True:
            self.setFontItalic(True)
        else:
            self.setFontItalic(False)

        #sets underline
        if prop_dict["underline"] == True:
            self.setFontUnderline(True)
        else:
            self.setFontUnderline(False)
        
    def update_view(self, interface):
        self.clear()
        fragments = interface.fragments()
        print(fragments)
        for i in fragments:
            text = i.text()
            length = i.length()
            properties = i.properties()
            print("HERE", text, length, properties)
            self.insertPlainText(text)
            pos = self._qtextcursor.position()
            self._select_text(pos - length, pos)
            self._update_selected_text_properties(properties)
            self._qtextcursor.clearSelection()
        focus = interface.focus()
        print(focus, focus.cursor().point())
        if focus.cursor().is_mark_active():
            self._qtextcursor.setPosition(focus.cursor().mark())
            self._qtextcursor.setPosition(focus.cursor().point(), 1)
        else:
            self._qtextcursor.setPosition(focus.cursor().point())
        self.setTextCursor(self._qtextcursor)
                
    def keyPressEvent(self, e):
        gke = GorgKeyEvent("p", e.key(), self._qtextcursor.position())
        self.gorg_key_event_signal.emit(gke)
     
    def keyReleaseEvent(self, e):
        gke = GorgKeyEvent("r", e.key(), self._qtextcursor.position())
        self.gorg_key_event_signal.emit(gke)

    def mousePressEvent(self, e):
        pos = self.cursorForPosition(e.pos()).position()
        gme = GorgMouseEvent("p", pos)
        self.gorg_mouse_event_signal.emit(gme)

    def mouseReleaseEvent(self, e):
        pos = self.cursorForPosition(e.pos()).position()
        gme = GorgMouseEvent("r", pos)
        self.gorg_mouse_event_signal.emit(gme)

    def mouseMoveEvent(self, e):
        pos = self.cursorForPosition(e.pos()).position()
        gme = GorgMouseEvent("m", pos)
        self.gorg_mouse_event_signal.emit(gme)

class GorgWindowLabel(QtGui.QLabel):

    def __init__(self):
        super(GorgWindowLabel, self).__init__()
        self.setAutoFillBackground(True)
        self.setStyleSheet("QLabel { background-color : rgb(112, 128, 144); color : white; }")
        self.setTextFormat(1)

    def _setText(self, text):
        string = "<b>" + text + "<b>"
        self.setText(string)

    def update_view(self, interface):
        inter_name = interface.name()
        focus = interface.focus()
        focus_name = focus.name()
        point = focus.cursor().point()
        string = "::" + inter_name + "::" + focus_name + "::" + str(point)
        self._setText(string)
        
def main():
    
    app = QtGui.QApplication(sys.argv)
    frame = Frame()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()


    

    
