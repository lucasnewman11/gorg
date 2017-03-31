import config
import Control.Commands
import re
        
class Keymap():
    def __init__(self, config):
        self._dict = {}
        self._config = config

    def add(self, key_string, dest):
        # Accepts as argument 1) a string containing an input event representation, and 2) a function object.
        self._dict[key_string] = dest

    def match(self, string):
        final_match = False
        for i in self._dict:
            if i.fullmatch(string): # method on the regex object
                final_match = i
        if final_match:
            return self._dict[final_match]
        else:
            return False

    def match_input_event(self, e):
        return self.match(e.string)

    def getdict(self):
        return self._dict

def make_keymaps_dict_from_file(fyl):
    keymaps = {}
    for line in fyl:
        token_list = line[1:-2].split()
        if len(token_list) > 1:
            fun = token_list[0]
            args = token_list[1:]
            if fun == "map":
                keymaps[args[0]] = Keymap(config)
            if fun == "bind":
                keymaps[args[0]].add(re.compile(args[1]), getattr(Control.Commands, args[2]))
            if fun == "add":
                pairings = keymaps[args[1]].getdict()
                for i in pairings:
                    keymaps[args[0]].add(i, pairings[i])
    return keymaps


            


                                 

        
        

    




    
    
