import sys
from PyQt4.QtCore import Qt, pyqtSignal
from PyQt4 import QtGui
import Data
import View
import Control

# creates a gorg directory object which points to an existing directory of JSON gorg data
gorg_directory = Data.Stores.JSONDir("/Users/amodeo/Dropbox/gorg-data/")

# calls the 'getlast' method on the gorg directory to return a live gorg network
gorg_network = gorg_directory.getlast()

# stores the current gorg network to the current gorg directory
# gorg_directory.store(gorg_network)

# current app 
Gorg = QtGui.QApplication(sys.argv)
frame1 = View.Frames.Frame()
keymaps = Control.Keymaps.make_keymap_dict_from_file(open("Control/keymaps.txt", "r"))
blueprints = Control.Blueprints.make_blueprints_dict_from_file(open("Control/blueprints.txt", "r"))
commander1 = Control.Core.Commander(keymaps, blueprints)

frame1.gorg_key_event_signal.connect(commander1._gorg_key_signal)
sys.exit(Gorg.exec_())


