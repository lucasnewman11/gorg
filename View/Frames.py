import sys
from PyQt4.QtCore import Qt, pyqtSignal, QObject
from PyQt4 import QtGui

class Frame(QtGui.QWidget):
    # a custom QT class derived from a QWidget, consisting of a list of Windows and a minibuffer, displayed on a grid layout.

    gorg_key_event_signal = pyqtSignal(str, int, int, QtGui.QWidget)
    
    def __init__(self, start_inter, mini_inter):
        super(Frame, self).__init__()
        self._lattice = Lattice()
        self.setLayout(self._lattice)

        self._windows = {}
        self._last_name = "AAAA"

        start_window = Window()
        self._add_window(start_window, self._last_name, (1,1))

        self._miniwindow = GorgLineEdit()
        self._miniwindow.gorg_key_event_signal.connect(self._gorg_key_event)
        self._lattice.addWidget(self._miniwindow, 2, 1)

        # set up presentation
        self._grid.setHorizontalSpacing(0)
        self._grid.setVerticalSpacing(0)
        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('Gorg')
        self.show()

    def _increment_char(self, char):
        if char == "Z":
            return "A"
        else:
            return char(ord(char) + 1)
    
    def _new_name(self):
        r_char_list = reversed(list(self._last_name))
        incr = True
        for i in range(len(r_char_list)):
            if incr == True:
                new_char = self._increment_char(r_char_list[i])
                if new_char != "A":
                    incr = False
                r_char_list[i] = new_char
        new_name = "".join(reversed(r_char_list))
        self._last_name = new_name
        return new_name
                    
    def _add_window(self, window, name, loc, path=""):
        # A) str - name of new window, B) 2-tuple of int - location of window on frame grid
        self._windows[name] = {"obj" : window, "loc" : loc, "path": path}
        path_list = path.split("/")
        grid = self._lattice
        for i in path_list:
            grid = grid.obj_by_name(i)
        grid.addWindow(window, name, loc)
        window.gorg_key_event_signal.connect(self._gorg_key_event)

    def split_window(self, name, ori):
        # accepts the name and path of an existing window, and the orientation of the split.  ori should be a string of either "v" or "h" for vertical or horizontal
        target_window = self._windows[name]
        obj = target_window["obj"]
        loc = target_window["loc"]

        path = target_window["path"]
        path_list = path.split("/")
        grid = self._lattice
        for i in path_list:
            grid = grid.obj_by_name(i)
        grid.removeWidget(obj)            

        new_lattice = Lattice()
        new_lattice.addWindow(target_window, name, (1, 1))
        lattice_name = self._new_name()
        grid.addLattice(new_lattice, new_name, loc)
        
        new_window = Window()
        if ori == "v":
            self._add_window(new_window, self._new_name(), (1, 2), path + "/" + lattice_name)
        elif ori == "h":
            self._add_window(new_window, self._new_name(), (2, 1), path + "/" + lattice_name)
        else:
            print("Not a valid splitting orientation.")
            raise ValueError

    def get_window(self, name):
        return self._windows[name]
        
    def getminibuffer(self):
        return self._minibuffer

    def _gorg_key_event(self, gke):
        gke.frame = self
        self.gorg_key_event_signal.emit(gke)

class Lattice(QtGui.GridLayout):

    def __init__(self):
        super(Lattice, self).__init__()
        self._subordinates = {}

    def addWindow(self, obj, name, loc):
        self._subordinates[name] = {"obj": obj, "loc": loc}
        self.addWidget(obj, loc[0], loc[1])

    def addLattice(self, obj, name, loc):
        self._subordinates[name] = {"obj": obj, "loc": loc}
        self.addLayout(obj, loc[0], loc[1])

    def obj_by_name(self, name):
        return self._subordinates[name]

    def obj_by_loc(self, loc):
        # accepts 2-tuple of int corresponding to location in grid
        for i in self._subordinates:
            if self._subordinates[i]["loc"] == loc:
                return self._subordinates[i]

class Window(QtGui.QFrame):
    # a custom QT class derived from a QFrame, consisting of a paired QTextEdit object and QLabel object.  Together, they display the contents and name of a Buffer object.  constructor accepts a buffer object

    gorg_key_event_signal = pyqtSignal(GorgKeyEvent)

    def __init__(self):
        super(Window, self).__init__()
        # initialize layout
        self.doc = GorgTextEdit()
        self._statusbar = QtGui.QLabel()
        self._grid = QtGui.QGridLayout()
        self._grid.addWidget(self._doc, 1, 1)
        self._grid.addWidget(self._statusbar, 2, 1)
        self._grid.setSpacing(0)
        self.setLayout(self._grid)
        # connect slots
        self.doc.gorg_key_event_signal.connect(self._gorg_key_event)
        
    def _gorg_key_event(self, gke):
        gke.win = self
        self.gorg_key_event_signal.emit(gke)

class MiniWindow(QtGui.QLineEdit):
# the framing and content class for the minibuffer, which contains the GorgLineEdit object and the buffer that populates it.  constructor takes a buffer.

    gorg_key_event_signal = pyqtSignal(GorgKeyEvent)
    
    def __init__(self):
        super(MiniWindow, self).__init__()

    def insertPlainText(self, QString):
        self.insert(QString)

    def _select_text(self, start, end):
        self._cursor.setPosition(start)
        self._cursor.setPosition(end, mode = 1)
        
    def _update_selected_text_properties(self, prop_dict):
        # sets color
        colors = {"black": Qt.black,
                  "white": Qt.white,
                  "red": Qt.red,
                  "blue": Qt.blue,
                  "cyan": Qt.cyan,
                  "magenta": Qt.magenta,
                  "yellow": Qt.yellow
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
        
    def update_view(self):
        self.clear()
        text_list = self._gate.get_text()
        for i in text_list:
            length = len(i[0])
            self.insertPlainText(i[0])
            self._select_text(self, self._cursor.position() - length, self._cursor.position())
            self._update_selected_text_properties(i[1])

    def keyPressEvent(self, e):
        gke = GorgKeyEvent("p", e.key(), self._cursor.position()), self)
        self.gorg_key_event_signal.emit(gke)
     
    def keyReleaseEvent(self, e):
        gke = GorgKeyEvent("r", e.key(), self._cursor.position()), self)
        self.gorg_key_event_signal.emit(gke)


class GorgTextEdit(QtGui.QTextEdit):
    # customized QTextEdit class, initialized with a Gate object

    gorg_key_event_signal = pyqtSignal(GorgKeyEvent)

    def __init__(self, interface):
        super(GorgTextEdit, self).__init__()
        self._interface = interface
        self._cursor = self.textCursor

    def _select_text(self, start, end):
        self._cursor.setPosition(start)
        self._cursor.setPosition(end, mode = 1)
        
    def _update_selected_text_properties(self, prop_dict):
        # sets color
        colors = {"black": Qt.black,
                  "white": Qt.white,
                  "red": Qt.red,
                  "blue": Qt.blue,
                  "cyan": Qt.cyan,
                  "magenta": Qt.magenta,
                  "yellow": Qt.yellow
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
        
    def update_view(self):
        self.clear()
        text_list = self._gate.get_text()
        for i in text_list:
            length = len(i[0])
            self.insertPlainText(i[0])
            self._select_text(self, self._cursor.position() - length, self._cursor.position())
            self._update_selected_text_properties(i[1])
        
    def keyPressEvent(self, e):
        gke = GorgKeyEvent("p", e.key(), self._cursor.position())
        self.gorg_key_event_signal.emit(gke)
     
    def keyReleaseEvent(self, e):
        gke = GorgKeyEvent("r", e.key(), self._cursor.position())
        self.gorg_key_event_signal.emit(gke)

class GorgKeyEvent():

    def __init__(self, typ, key, pos, win=False, frame=False):
        self.typ = typ
        self.key = key
        self.pos = pos
        self.win = win
        self.frame = frame

def main():
    
    app = QtGui.QApplication(sys.argv)
    frame = Frame()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()


    

    
