import re
from copy import deepcopy

def markup_from_region(region):
    # returns a string of markup text
    
def region_from_markup(markup):
    # returns a region

class Markup_Text():
    # container class for the markup text requiring parsing
    # keeps track of an index number as well

    def __init__(self, markup):
        self._contents = markup
        self._index = 0

    def index(self):
        return self._index

    def length(self):
        return len(self._contents)

    def check(self, x=0):
        return self._contents[self._index+x]

    def move(self, x=1):
        self._index += x

class Frag_Delta_List():

    def __init__(self, fds=[]):
        self._frag_deltas = fds

    def add(self, frag_delta):
        self._frag_deltas.append(frag_delta)

    def region(self):
        # returns a region of fragments, created from the frag_delta list
        region = Region()
        last_frag = False
        for i in self._frag_deltas:
            frag = Fragment()
            frag.set_text(i.text())
            for j in ("bold", "underline", "italics", "color"):
                if last_frag:
                    frag.set_text_property(j, last_frag.text_property(j))
                frag.set_text_property(j, i.prop_d(j))
            last_frag = frag
            region.add_fragment(frag)
        return region

    @classmethod
    def parse(cls, mt):
        frag_deltas = []
        mtp = mt
        mtc = deepcopy(mtp)
        fd = Frag_Delta.parse(mtc)
        while fd:
            frag_delta.append(fd)
            mtp = mtc
            mtc = deepcopy(mtp)
            fd = Frag_Delta.parse(mtc)
        return cls.__init__(frag_deltas)
                        
class Frag_Delta():

    def __init__(self, text):
        self._text = text
        self._prop_deltas = {}

    def text(self):
        return text

    def set_text(self):
        self._text = text
        
    def prop_d(self, name):
        return self._prop_deltas[name]

    def set_prop_d(self, name, value):
        self._prop_deltas[name] = value

    @classmethod
    def parse(cls, mt):
        termins = Termins.parse(mt)
        inits = Inits.parse(mt)
        string = Markup_String.parse(mt)
        if string:
            fd = cls.__init__(string)
            for i in termins.prop_termins():
                fd.set_prop_d(i.prop(), False)
            for i in inits.prop_inits():
                fd.set_prop_d(i.prop(), i.value())
            return fd
        else:
            return False

class Termins():
    # a sequence of text property opening indicators
    def __init__(self):
        self._termins = []

    def termin(self):
        return self._termins

    def add_termin(self, termin):
        self._termins.append(termin)
        
class Termin():

    def __init__(self):
        self._prop = False

    def prop(self):
        return self._prop

    def set_prop(self, name):
        self._prop = name


class Inits():
    # a sequence of text property opening indicators
    def __init__(self):
        self._inits = []

    def init(self):
        return self._inits

    def add_init(self, init):
        self._inits.append(init)

class Init():
    def __init__(self):
        self._prop = False
        self._value = False

    def prop(self):
        return self._prop

    def set_prop(self, name):
        self._prop = name

    def value(self):
        return self._value

    def set_value(self, name):
        self._value = name
        
def parse_char(mt):
    checked = mt.check()
    if re.fullmatch("[^<>]", checked):
        return checked
    else:
        return False
        
def parse_string(mt):
    chars = []
    last_checked = parse_char(mt)
    while last_checked:
        chars.append(last_checked)
        mt.move()
        last_checked = parse_char(mt)
    return "".join(chars)

def parse_prop_init_start(mt):
    checked = mt.check()
    if checked == "<":
        mt.move()
        return checked
    else:
        return False

def parse_prop_term_start(mt):
    checked = mt.check()
    nxt = mt.check(1)
    if (checked, nxt) == ("<", "/"):
        mt.move(2)
        return "</"
    else:
        return False

def parse_prop_end(mt):
    checked = mt.check()
    if checked == ">":
        mt.move()
        return checked
    else:
        return False

def parse_param_start(mt):
    string = ""
    for i in range(7):
        string += mt.check(i)
    if string == "<param>":
        mt.move(7)
        return string
    else:
        return False

def parse_param_end(mt):
    string = ""
    for i in range(8):
        string += mt.check(i)
    if string == "</param>":
        mt.move(8)
        return string
    else:
        return False

def parse_param(mt):
    param_start = parse_param_start(mt)
    if param_start:
        string = parse_string(mt)
        param_end = parse_param_end(mt)
        return [param_start, string, param_end]
    else:
        return False

def parse_prop_init(mt):
    tokens = []
    parse_prop_init_start(mt)
    parse_string
    
    

    
        


    


    
        
        
