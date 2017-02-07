import sys
from PyQt4.QtCore import Qt, pyqtSignal, QObject
from PyQt4 import QtGui

class GorgKeyEvent():

    def __init__(self, typ, key, pos, win=False, frame=False):
        self.typ = typ
        self.key = key
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
    
    def __init__(self):
        super(Frame, self).__init__()
        self.grid = Lattice()
        self.grid.gorg_key_event_signal.connect(self._gorg_key_event)
        self.setLayout(self.grid)

        self._namer = AlphaNamer(5)
        self._init_UI()

    def _init_UI(self):
        
        start_window = Window()
        self.grid.place_obj(start_window, "AAAAA", (1,1))

        miniwindow = MiniWindow()
        self.grid.place_obj(miniwindow, "MINI", (2,1))

        # set up presentation
        self.grid.setHorizontalSpacing(0)
        self.grid.setVerticalSpacing(0)
        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('Gorg')
        self.show()

        # accessing and placing objects at Frame level

    def path(self):
        return False

    def _gorg_key_event(self, gke):
        gke.frame = self
        self.gorg_key_event_signal.emit(gke)

class Lattice(QtGui.QGridLayout):

    gorg_key_event_signal = pyqtSignal(GorgKeyEvent)

    def __init__(self):
        super(Lattice, self).__init__()
        self._loc_from_obj = {}
        self._obj_from_name = {}
        self._name_from_obj = {}

    def obj_from_name(self, name):
        return self._obj_from_name[name]

    def name_from_obj(self, obj):
        return self._name_from_obj[obj]

    def loc_from_object(self, obj):
        print(self._loc_from_obj)
        return self._loc_from_obj[obj]

    def _add_obj(self, obj, name, loc):
        self._obj_from_name[name] = obj
        self._name_from_obj[obj] = name
        self._loc_from_obj[obj] = loc
        print("OBJ", type(obj))
        print("CLASS", Window, MiniWindow, Lattice)
        if type(obj) in (Window, MiniWindow):
            self.addWidget(obj, loc[0], loc[1])
        elif type(obj) == Lattice:
            self.addLayout(obj, loc[0], loc[1])
        else:
            print("Object must be a Window or a Lattice.")
            raise TypeError
        obj.gorg_key_event_signal.connect(self._gorg_key_event)
        obj.setParent(self)

    def remove_obj(self, obj):
        name = self._name_from_obj[obj]
        del self._obj_from_name[name]
        del self._name_from_obj[obj]
        del self._loc_from_obj[obj]
        self._lattice.removeWidget(obj)
        if type(obj) == Window:
            self.removeWidget(obj)
        elif type(obj) == Lattice:
            self.removeItem(obj)

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
            mypath = "/".join(parent_path, myname)
        else:
            mypath = myname
        return mypath

    def _gorg_key_event(self, gke):
        print("YEAH") 
        self.gorg_key_event_signal.emit(gke)

class Window(QtGui.QFrame):
    # a custom QT class derived from a QFrame, consisting of a paired QTextEdit object and QLabel object.  Together, they display the contents and name of a Buffer object.  constructor accepts a buffer object

    gorg_key_event_signal = pyqtSignal(GorgKeyEvent)

    def __init__(self):
        super(Window, self).__init__()
        # initialize layout
        self.doc = GorgTextEdit()
        self.setContentsMargins(0, 0, 0, 0)
        self._statusbar = QtGui.QLabel()
        self._grid = QtGui.QGridLayout()
        self._grid.addWidget(self.doc, 1, 1)
        self._grid.addWidget(self._statusbar, 2, 1)
        self._grid.setSpacing(0)
        self.setLayout(self._grid)
        # connect slots
        self.doc.gorg_key_event_signal.connect(self._gorg_key_event)
        
    def _gorg_key_event(self, gke):
        gke.win = self
        self.gorg_key_event_signal.emit(gke)

    def path(self):
        myname = self.parent().name_from_obj(self)
        parent_path = self.parent().path()
        if parent_path:
            mypath = "/".join(parent_path, myname)
        else:
            mypath = myname
        return mypath

class MiniWindow(QtGui.QFrame):
    # a custom QT class derived from a QFrame, consisting of a paired QTextEdit object and QLabel object.  Together, they display the contents and name of a Buffer object.  constructor accepts a buffer object

    gorg_key_event_signal = pyqtSignal(GorgKeyEvent)

    def __init__(self):
        super(MiniWindow, self).__init__()
        # initialize layout
        self.doc = GorgTextEdit()
        self.doc.setMaximumHeight(16)
        self.setContentsMargins(0, 0, 0, 0)
        self._grid = QtGui.QGridLayout()
        self._grid.addWidget(self.doc, 1, 1)
        self._grid.setSpacing(0)
        self.setLayout(self._grid)
        # connect slots
        self.doc.gorg_key_event_signal.connect(self._gorg_key_event)
        
    def _gorg_key_event(self, gke):
        gke.win = self
        self.gorg_key_event_signal.emit(gke)

    def path(self):
        myname = self.parent().name_from_obj(self)
        parent_path = self.parent().path()
        if parent_path:
            mypath = "/".join(parent_path, myname)
        else:
            mypath = myname
        return mypath


# class GorgLineEdit(QtGui.QLineEdit):
# # the framing and content class for the minibuffer, which contains the GorgLineEdit object and the buffer that populates it.  constructor takes a buffer.

#     gorg_key_event_signal = pyqtSignal(GorgKeyEvent)
    
#     def __init__(self):
#         super(GorgLineEdit, self).__init__()

#     def insertPlainText(self, QString):
#         self.insert(QString)

#     def get_selection(self):
#         string = self.selectedText()
#         start = self.selectionStart()
#         end = start + len(string)
#         selection = {"string": string,
#                      "start": start,
#                      "end": end}
#         return selection

#     def _select_text(self, start, end):
#         length = end - start
#         self.setSelection(start, length)
        
#     def _update_selected_text_properties(self, prop_dict):
#         # sets color
#         colors = {"black": Qt.black,
#                   "white": Qt.white,
#                   "red": Qt.red,
#                   "blue": Qt.blue,
#                   "cyan": Qt.cyan,
#                   "magenta": Qt.magenta,
#                   "yellow": Qt.yellow,
#                   "green": Qt.green}
#         text_color = QtGui.QColor(colors[prop_dict["color"]])
#         self.setTextColor(text_color)

#         # sets bold
#         if prop_dict["bold"] == True:
#             self.setFontWeight(75)
#         else:
#             self.setFontWeight(50)

#         # sets italic
#         if prop_dict["italics"] == True:
#             self.setFontItalic(True)
#         else:
#             self.setFontItalic(False)

#         #sets underline
#         if prop_dict["underline"] == True:
#             self.setFontUnderline(True)
#         else:
#             self.setFontUnderline(False)
        
#     def update_view(self, interface):
#         self.clear()
#         text_list = interface.get_full_text()
#         for i in text_list:
#             length = len(i[0])
#             self.insertPlainText(i[0])
#             self._select_text(self.cursorPosition() - length, self.cursorPosition())
#             self._update_selected_text_properties(i[1])
#             self.deselect()

#     def keyPressEvent(self, e):
#         gke = GorgKeyEvent("p", e.key(), self.cursorPosition())
#         self.gorg_key_event_signal.emit(gke)
     
#     def keyReleaseEvent(self, e):
#         gke = GorgKeyEvent("r", e.key(), self.cursorPosition())
#         self.gorg_key_event_signal.emit(gke)


class GorgTextEdit(QtGui.QTextEdit):
    # customized QTextEdit class, initialized with a Gate object

    gorg_key_event_signal = pyqtSignal(GorgKeyEvent)

    def __init__(self):
        super(GorgTextEdit, self).__init__()
        self._cursor = self.textCursor()

    def get_selection(self):
        string = self._cursor.selectedText()
        start = self._cursor.selectionStart()
        end = self._cursor.selectionEnd()
        selection = {"string": string,
                     "start": start,
                     "end": end}
        return selection

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
        text_list = interface.get_full_text()
        print("TEXTS", text_list)
        for i in text_list:
            length = len(i[0])
            self.insertPlainText(i[0])
            pos = self._cursor.position()
            self._select_text(pos - length, pos)
            self._update_selected_text_properties(i[1])
            self._cursor.clearSelection()
        
    def keyPressEvent(self, e):
        gke = GorgKeyEvent("p", e.key(), self._cursor.position())
        self.gorg_key_event_signal.emit(gke)
     
    def keyReleaseEvent(self, e):
        gke = GorgKeyEvent("r", e.key(), self._cursor.position())
        self.gorg_key_event_signal.emit(gke)



def main():
    
    app = QtGui.QApplication(sys.argv)
    frame = Frame()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()


    

    
