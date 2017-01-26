import Control.Commands
import re

class Invoker():

    def __init__(self, keymap):
        self._default_keymap = keymap
        self._current_keymap = self._default_keymap

    def match_key_event(self, fke):
        match = self._current_keymap.match(fke.string)
        if match:
            if type(match) == Keymap:
                self._current_keymap = match
            else:
                self.invoke(match)
            return True
        else:
            return False

    def invoke(self, fun, fke):
        # I need to write a line of code here which goes and calculates the args to be passed into the function
        fun.__call__(fke)
        fke.gke.win.doc.update_view()
        
class Keymap():
    def __init__(self):
        self._dict = {}

    def add(self, key_string, dest):
        # Accepts as argument 1) a string containing a key press representation, and 2) either a keymap object or a function object.
        self._dict[key_string] = dest

    def match(self, string):
        print("String:" + string)
        final_match = False
        for i in self._dict:
            if i.fullmatch(string): # method on the regex object
                final_match = i
                print("final_match:", final_match)
        if final_match:
            return self._dict[final_match]
        else:
            print("No match for that key in this map.")
            return False

def make_keymaps_dict_from_file(fyl):
    keymaps = {}
    for line in fyl:
        token_list = line[1:-2].split()
        print("TOKEN LIST:", token_list)
        fun = token_list[0]
        args = token_list[1:]
        if fun == "map":
            keymaps[args[0]] = Keymap()
        if fun == "bindmap":
            keymaps[args[0]].add(re.compile(args[1]), keymaps[args[2]])
        if fun == "bindcom":
            keymaps[args[0]].add(re.compile(args[1]), getattr(Control.Commands, args[2]))
    return keymaps
            


                                 

        
        

    




    
    
