import sys
from PyQt4.QtCore import Qt, pyqtSignal, QObject
from PyQt4 import QtGui

class Frame(QtGui.QWidget):
    # a custom QT class derived from a QWidget, consisting of a list of Windows and a minibuffer, displayed on a grid layout.

    def __init__(self):
        super(Frame, self).__init__()
        self._grid = QtGui.QGridLayout()
        self._other_grid = QtGui.QGridLayout()
        self.setLayout(self._grid)
        start_window = Window()
        other_window = Window()
        xtra_window = Window()
        self._grid.addWidget(start_window, 1, 1, 1, 1)
        self._other_grid.addWidget(other_window, 1, 1, 1, 1)
        self._other_grid.addWidget(xtra_window, 2, 1, 1, 1)
        self._grid.addLayout(self._other_grid, 1, 2)
        self._grid.setHorizontalSpacing(0)
        self._grid.setVerticalSpacing(0)
        self.show()

        # def split_window(self, name, direction):
    #     # the direction arg should be a string of either "v" or "h" for vertical or horizontal
    
class Window(QtGui.QFrame):
    # a custom QT class derived from a QFrame, consisting of a paired QTextEdit object and QLabel object.  together, they display the contents and name of a Buffer object.  constructor accepts a buffer object

    gorg_key_event_signal = pyqtSignal(str, int, int, QtGui.QWidget)

    def __init__(self):
        super(Window, self).__init__()
        # initialize layout
        self._doc = GorgTextEdit()
        self._statusbar = QtGui.QLabel()
        self._grid = QtGui.QGridLayout()
        self._grid.addWidget(self._doc, 1, 1)
        self._grid.addWidget(self._statusbar, 2, 1)
        self._grid.setSpacing(0)
        self.setLayout(self._grid)
        # connect slots
        self._doc.gorg_key_event_signal.connect(self._gorg_key_event)
        
    def _gorg_key_event(self, typ, key, pos, wdg):
        self.gorg_key_event_signal.emit(typ, key, pos, wdg)

class GorgLineEdit(QtGui.QLineEdit):
# the framing and content class for the minibuffer, which contains the GorgLineEdit object and the buffer that populates it.  constructor takes a buffer.

    gorg_key_event_signal = pyqtSignal(str, int, int, QtGui.QWidget)
    
    def __init__(self):
        super(GorgMiniBuffer, self).__init__()

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
        
    def update_view(self):
        self.clear()
        text_list = self._gate.get_text()
        for i in text_list:
            length = len(i[0])
            self.insertPlainText(i[0])
            self._select_text(self, self._cursor.position() - length, self._cursor.position())
            self._update_selected_text_properties(i[1])


    def keyPressEvent(self, e):
        self.gorg_key_event_signal.emit("p", e.key(), self._cursor.position(), self)
     
    def keyReleaseEvent(self, e):
        self.gorg_key_event_signal.emit("r", e.key(), self._cursor.position(), self)

class GorgTextEdit(QtGui.QTextEdit):
    # customized QTextEdit class, initialized with a Gate object

    gorg_key_event_signal = pyqtSignal(str, int, int, QtGui.QWidget)

    def __init__(self):
        super(GorgTextEdit, self).__init__()
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
        
    def update_view(self):
        self.clear()
        text_list = self._gate.get_text()
        for i in text_list:
            length = len(i[0])
            self.insertPlainText(i[0])
            self._select_text(self, self._cursor.position() - length, self._cursor.position())
            self._update_selected_text_properties(i[1])
        
    def keyPressEvent(self, e):
        self.gorg_key_event_signal.emit("p", e.key(), self._cursor.position(), self)
     
    def keyReleaseEvent(self, e):
        self.gorg_key_event_signal.emit("r", e.key(), self._cursor.position(), self)
        

app = QtGui.QApplication(sys.argv)
frame = Frame()
sys.exit(app.exec())
