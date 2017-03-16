import sys
from PyQt4.QtCore import Qt, pyqtSignal
from PyQt4 import QtGui
import Data.Stores
import View.Frames
import Control.Core
import Control.Keymaps
import Control.Interfaces

# creates a gorg directory object which points to an existing directory of JSON gorg data
gorg_directory = Data.Stores.JSONDir("/Users/amodeo/Dropbox/gorg-data/")

# calls the 'getlast' method on the gorg directory to return a live gorg network
gorg_network = gorg_directory.getlast()

# stores the current gorg network to the current gorg directory
# gorg_directory.store(gorg_network)

# current app 
Gorg = QtGui.QApplication(sys.argv)

keymaps = Control.Keymaps.make_keymaps_dict_from_file(open("Control/keymaps.txt", "r"))
gate_blueprints = Control.Interfaces.make_gate_blueprints_dict_from_file(open("Control/gates.txt", "r"))
interface_blueprints = Control.Interfaces.make_interface_blueprints_dict_from_file(open("Control/interfaces.txt", "r"), gate_blueprints)

commander1 = Control.Core.Commander(keymaps, interface_blueprints)
sys.exit(Gorg.exec_())



