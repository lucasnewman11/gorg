import sys
from PyQt4.QtCore import Qt, pyqtSignal, QObject
from PyQt4 import QtGui

class Frame(QtGui.QWidget):
    # a custom QT class derived from a QWidget, consisting of a list of Windows and a minibuffer, displayed on a grid layout.

    gorg_key_press_signal = pyqtSignal(str, int, QtGui.QWidget)
    gorg_key_release_signal = pyqtSignal(str, int, QtGui.QWidget)
    
    def __init__(self):
        super(Frame, self).__init__()
        self._grid = QtGui.QGridLayout()
        self.setLayout(self._grid)

        self._windows = []
        self._minibuffer = GorgMiniBuffer(Buffer("minibuff", ""))
        self._initUI()
    
    def _initUI(self):
        # create starting window
        start_window = Window(Buffer("start-1", "hello!"))
        self._windows.append(start_window)

        # connect slots
        start_window.gorg_key_press_signal.connect(self._gorg_key_press)
        start_window.gorg_key_release_signal.connect(self._gorg_key_release)

        # set up grid and spacing
        self._grid.addWidget(start_window, 1, 1)
        self._grid.addWidget(self._minibuffer, 2, 1)
        self._grid.setHorizontalSpacing(0)
        self._grid.setVerticalSpacing(0)

        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('Gorg')
        self.show()

    def _gorg_key_press(self, typ, key, gte):
        self.gorg_key_press_signal.emit(typ, key, gte)

    def _gorg_key_release(self, typ, key, gte):
        self.gorg_key_release_signal.emit(typ, key, gte)


class Window(QtGui.QFrame):
    # a custom QT class derived from a QFrame, consisting of a paired QTextEdit object and QLabel object.  together, they display the contents and name of a Buffer object.  constructor accepts a buffer object

    gorg_key_press_signal = pyqtSignal(str, int, QtGui.QWidget)
    gorg_key_release_signal = pyqtSignal(str, int, QtGui.QWidget)
    
    def __init__(self, buff):
        super(Window, self).__init__()
        # initialize content
        self._buffer = buff
        # initialize layout
        self._doc = GorgTextEdit()
        self._statusbar = QtGui.QLabel()
        self._grid = QtGui.QGridLayout()
        self._grid.addWidget(self._doc, 1, 1)
        self._grid.addWidget(self._statusbar, 2, 1)
        self._grid.setSpacing(0)
        self.setLayout(self._grid)
        # populate layout
        self._updatetext()
        # connect slots
        self._doc.gorg_key_press_signal.connect(self._gorg_key_press)
        self._doc.gorg_key_release_signal.connect(self._gorg_key_release)
        
    def _updatetext(self):
        # reinitializes the displayed contents of the Window based on the current Buffer
        self._doc.clear()
        self._doc.setText(self._buffer.getcontents())

        self._statusbar.clear()
        self._statusbar.setText(self._buffer.getname())

    def _readtext(self):
        # updates the Buffer based on the displayed contents of the Window
        contents = self._doc.document().toPlainText()
        self._buffer.setcontents(contents)

    def setbuffer(self, buff):
        self._buffer = buff
        self._updatetext()

    def _gorg_key_press(self, typ, key, gte):
        self.gorg_key_press_signal.emit(typ, key, gte)

    def _gorg_key_release(self, typ, key, gte):
        self.gorg_key_release_signal.emit(typ, key, gte)

class GorgLineEdit(QtGui.QLineEdit):

    def __init__(self):
        super(GorgLineEdit, self).__init__()

class GorgMiniBuffer(QtGui.QLineEdit):
# the framing and content class for the minibuffer, which contains the GorgLineEdit object and the buffer that populates it.  constructor takes a buffer.
    def __init__(self, buff):
        super(GorgMiniBuffer, self).__init__()
        self._buffer = buff
        # populate 
        self._updatetext()
        
    def _updatetext(self):
        # reinitializes the displayed contents of the minibuffer based on the current Buffer
        self.clear()
        self.setText(self._buffer.getcontents())

    def _readtext(self):
        # updates the Buffer based on the displayed contents of the Window
        contents = self.document().toPlainText()
        self._buffer.setcontents(contents)

    def setbuffer(self, buff):
        self._buffer = buff
        self._updatetext()
        
class GorgTextEdit(QtGui.QTextEdit):
    # customized QTextEdit class with just a few extra methods and attributes

    gorg_key_press_signal = pyqtSignal(str, int, QtGui.QWidget)
    gorg_key_release_signal = pyqtSignal(str, int, QtGui.QWidget)
    
    def __init__(self):
        # specials is a list of special key events to which GorgTextEdit should respond by broadcasting an appropriate signal rather than by inserting text
        super(GorgTextEdit, self).__init__()
        
    def keyPressEvent(self, e):
        self.gorg_key_press_signal.emit("p", e.key(), self)
     
    #        super(GorgTextEdit, self).keyPressEvent(e)

    def keyReleaseEvent(self, e):
        self.gorg_key_release_signal.emit("r", e.key(), self)
        
        #    super(GorgTextEdit, self).keyReleaseEvent(e)


class Buffer:
    # container class, has a string attribute which corresponds to what's displayed in the buffer, and a name attribute which corresponds to the buffer label.  exposes methods for accessing those attributes.

    # constructor accepts as argument A) a string containing the intended name of the buffer object, and B) a string containing the intended contents of the buffer object
    
    def __init__(self, name, contents):
        self._name = name
        self._contents = contents

    def getname(self):
        return self._name

    def getcontents(self):
        return self._contents

    def setname(self, new_name):
        self._name = new_name

    def setcontents(self, new_contents):
        self._contents = new_contents

def main():
    
    app = QtGui.QApplication(sys.argv)
    frame = Frame()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()


    

    
