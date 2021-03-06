import re
from copy import deepcopy
from Control.Interfaces import Fragment, Region

def markup_from_region(region):
    # returns a string of markup text
    fragments = region.fragments()
    fdl = Frag_Delta_List()
    last_frag = Fragment() # empty fragment, used here for the default properties
    for i in fragments:
        fd = Frag_Delta()
        fd.set_text(i.text())
        for j in ("bold", "italics", "underline", "color"):
            if last_frag.text_property(j) != i.text_property(j):
                fd.set_prop_d(j, i.text_property(j))
        last_frag = i
        fdl.add(fd)
    return fdl.markup()
    
def region_from_markup(markup):
    mi = Markup_Input(markup)
    fdl = Frag_Delta_List.parse(mi)
    return fdl.region()
    
class Markup_Input():
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
        try:
            return self._contents[self._index+x]
        except IndexError:
            return False

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
                try:
                    frag.set_text_property(j, i.prop_d(j))
                except KeyError:
                    pass
            last_frag = frag
            region.add_fragment(frag)
        return region

    def markup(self):
        # returns a string of markup text
        text = ""
        for i in self._frag_deltas:
            text += i.markup()
        return text

    @classmethod
    def parse(cls, mi):
        frag_deltas = []
        fd = Frag_Delta.parse(mi)
        while fd:
            frag_deltas.append(fd)
            fd = Frag_Delta.parse(mi)
        fdl = object.__new__(cls)
        cls.__init__(fdl)
        for i in frag_deltas:
            fdl.add(i)
        return fdl
                        
class Frag_Delta():

    def __init__(self):
        self._text = ""
        self._prop_deltas = {}

    def text(self):
        return self._text

    def set_text(self, text):
        self._text = text
        
    def prop_d(self, name):
        return self._prop_deltas[name]

    def set_prop_d(self, name, value):
        self._prop_deltas[name] = value

    def markup(self):
        text = ""
        termins = Termins()
        inits = Inits()
        string = Markup_String()
        for i in self._prop_deltas:
            if (((i == "color") and (self._prop_deltas[i] == "black")) or
                ((i != "color") and (self._prop_deltas[i] == False))):
                termin = Termin()
                termin.set_prop(i)
                termins.add_termin(termin)
            elif (((i == "color") and (self._prop_deltas[i] != "black")) or
                  ((i != "color") and (self._prop_deltas[i] == True))):
                init = Init()
                init.set_prop(i)
                init.set_value(self._prop_deltas[i])
                inits.add_init(init)
        string.set_string(self.text())
        for i in (termins, inits, string):
            text += i.markup()
        return text
            
        
    @classmethod
    def parse(cls, mi):
        termins = Termins.parse(mi)
        inits = Inits.parse(mi)
        ms = Markup_String.parse(mi)
        if ms:
            fd = object.__new__(cls)
            cls.__init__(fd)
            for i in termins.termins():
                prop = i.prop()
                if prop == "color":
                    value = "black"
                else:
                    value = False
                fd.set_prop_d(prop, value)
            for i in inits.inits():
                fd.set_prop_d(i.prop(), i.value())
            fd.set_text(ms.string())
            return fd
        else:
            return False

class Termins():
    # a sequence of text property opening indicators
    def __init__(self):
        self._termins = []

    def termins(self):
        return self._termins

    def add_termin(self, termin):
        self._termins.append(termin)

    def markup(self):
        text = ""
        for i in self._termins:
            text += i.markup()

    @classmethod
    def parse(cls, mi):
        termins = []
        termin = Termin.parse(mi)
        while termin:
            termins.append(termin)
            termin = Termin.parse(mi)
        trmns = object.__new__(cls)
        cls.__init__(trmns)
        for i in termins:
            trmns.add_termin(i)
        return trmns
        
class Termin():

    def __init__(self):
        self._prop = False

    def prop(self):
        return self._prop

    def set_prop(self, name):
        self._prop = name

    def markup(self):
        text = "</" + self.prop() + ">"
        return text
        
    @classmethod
    def parse(cls, mi):
        if (mi.check() == "<") and (mi.check(1) == "/"):
            mi.move(2)
            ms = Markup_String.parse(mi)
            if mi.check() != ">":
                print("Input markup not formatted properly.")
                raise ValueError
            mi.move(1)
            termin = object.__new__(cls)
            cls.__init__(termin)
            termin.set_prop(ms.string())
            return termin
        else:
            return False
                
class Inits():
    # a sequence of text property opening indicators
    def __init__(self):
        self._inits = []

    def inits(self):
        return self._inits

    def add_init(self, init):
        self._inits.append(init)

    def markup(self):
        text = ""
        for i in self._inits:
            text += i.markup()

    @classmethod
    def parse(cls, mi):
        inits = []
        init = Init.parse(mi)
        while init:
            inits.append(init)
            init = Init.parse(mi)
        ints = object.__new__(cls)
        cls.__init__(ints)
        for i in inits:
            ints.add_init(i)
        return ints

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

    def markup(self):
        text = "<" + self.prop() + ">"
        if not (self.value() is True):
            param = Param()
            param.set_contents(self.value())
            text += param.markup()
        return text

    @classmethod
    def parse(cls, mi):
        if (mi.check() == "<") and (mi.check(1) != "/"):
            mi.move(1)
            ms = Markup_String.parse(mi)
            mi.move(1)
            param = Param.parse(mi)
            init = object.__new__(cls)
            cls.__init__(init)
            init.set_prop(ms.string())
            if param:
                value = param.contents()
            else:
                value = True
            init.set_value(value)
            return init
        else:
            return False

class Param():
    def __init__(self):
        self._contents = False

    def contents(self):
        return self._contents

    def set_contents(self, contents):
        self._contents = contents

    def markup(self):
        text = "<param>" + self.contents() + "</param>"
        return text

    @classmethod
    def parse(cls, mi):
        checked = "".join([mi.check(i) for i in range(7)])
        if checked == "<param>":
            mi.move(7)
            ms = Markup_String.parse(mi)
            mi.move(8)
            param = object.__new__(cls)
            cls.__init__(param)
            param.set_contents(ms.string())
            return param
        else:
            return False

class Markup_String():
    def __init__(self):
        self._string = False

    def string(self):
        return self._string

    def set_string(self, string):
        self._string = string

    def markup(self):
        return self._string

    @classmethod
    def parse(cls, mi):
        string = ""
        char = mi.check()
        while char and (char not in ("<", ">")):
            string += char
            print(string)
            mi.move()
            char = mi.check()
        if string:
            mstring = object.__new__(cls)
            cls.__init__(mstring)
            mstring.set_string(string)
            return mstring
        else:
            return False

example = ""
mi = Markup_Input(example)

fdl = Frag_Delta_List.parse(mi)
print(fdl)
blah = fdl.region()
for i in blah.fragments():
    print(i, i.text(), i.text_properties())        
