import sys
from PyQt4.QtGui import QWidget
from PyQt4.QtCore import pyqtSignal

class Blah(QWidget):

    signal = pyqtSignal()
    
    def __init__(self):
        pass

    def emit(self):
        self.signal.emit()

class Blarg(QWidget):

    def __init__(self):
        pass

    def slot(self):
        print("I'm a slot!")

a = Blah()
b = Blarg()

a.emit()
        

