import Control.Commands
import re

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


def make_keymap_from_file(fyl):
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
    return keymaps["Main"]
            


                                 

        
        

    




    
    
