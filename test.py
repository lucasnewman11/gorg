import sys
from PyQt4.QtCore import Qt, pyqtSignal
from PyQt4 import QtGui
import Data.Stores
import View.Frames
import Control.Core
import Control.Interfaces
import Control.Blueprints

# creates a gorg directory object which points to an existing directory of JSON gorg data
gorg_directory = Data.Stores.JSONDir("/Users/amodeo/Dropbox/gorg-data/")

# calls the 'getlast' method on the gorg directory to return a live gorg network
gorg_network = gorg_directory.getlast()

# stores the current gorg network to the current gorg directory
# gorg_directory.store(gorg_network)

# current app 
Gorg = QtGui.QApplication(sys.argv)

blueprints = Control.Blueprints.make_blueprint_dict_from_filepath("/Users/amodeo/Desktop/Stuff/Code/Python/gorg/Control/blueprints.txt")

commander1 = Control.Core.Commander(blueprints)
sys.exit(Gorg.exec_())



