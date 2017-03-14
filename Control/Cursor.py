class GateCursor():

    def __init__(self, gate):
        self._gate = gate
        self._point = 0
        self._mark = 0
        self._start = 0
        self._end = 0
        self._selection = {}
        self._ring = KillRing()
        self._mark_active = False
        self._recent_points = []
        self._properties = {"color" : "black",
                            "bold" : False,
                            "italics": False,
                            "underline": False})

    def point(self):
        return self._point

    def mark(self):
        return self._mark

    def start(self):
        return self._start

    def end(self):
        return self._end

    def ring(self):
        return self._ring

    def setPoint(self, pos, record=True):
        raw_text = self._gate.get_raw_text()
        if pos < 0:
            self._point = 0
        elif pos > len(raw_text):
            self._point = len(raw_text)
        else:
            self._point = pos
        if record == True:
            self._recordPoint()            

    def _recordPoint(self):
        self._recent_points.append(self._point)
        if len(self._recent_points) > 10:
            self._recent_points.pop(0)
        
    def lastPoint(self, n=2):
        index = n*-1
        try:
            return self._recent_points[index]
        except IndexError:
            return False

    def setMark(self, pos):
        raw_text = self._gate.get_raw_text()
        if pos < 0:
            self._mark = 0
        elif pos > len(raw_text):
            self._mark = len(raw_text)
        else:
            self._mark = pos

    def isMarkActive(self):
        return self._mark_active

    def activateMark(self):
        self._mark_active = True

    def deactivateMark(self):
        self._mark_active = False

    def property(self, name):
        return self._properties[name]

    def setProperty(self, name, value):
        self._properties[name] = value

    def properties(self):
        return self._properties

    def setProperties(self, properties):
        self._properties = properties

    def insertFragments(self, fragments, pos):
        target = self._gate.frag_by_pos(pos)
        target_start = self._gate.pos_by_frag(target)
        adjusted_pos = pos - target_start
        if adjusted_pos > 0:
            new_fragments = target.split(adjusted_pos)
            fragments.insert(0, new_fragments[0])
            fragments.append(new_fragments[1])
            self._gate.removeFragment(target)
            self.insertFragments(new_fragments, target_start)
        else:
            self._gate.addFragments(fragments, target_start)
            self._gate.simplify()

    def killSelection(self, start, end, delete=False):
        

            

class KillRing():

    def __init__(self):
        self._members = []
        self._index = 0

    def add(self, new):
        self._members.append(new)

    def index(self):
        return self._index

    def get(self):
        return self._members[self._index]

    def next_index(self):
        if self._index > 0:
            self._index -= 1
        else:
            self._index = len(self._members)-1

    def previous_index(self):
        if self._index < len(self._members)-1:
            self._index += 1
        else:
            self._index = 0

    def remove(self, index):
        del self._members[index]
    
class Fragment():

    def __init__(self, text="", properties={"color" : "black",
                                            "bold" : False,
                                            "italics": False,
                                            "underline": False})
        self._text = text
        self._properties = properties

    def text(self):
        return self._text

    def setText(self, text):
        self._text = text

    def length(self):
        return len(self._text)

    def property(self, name):
        return self._properties[name]

    def setProperty(self, name, value):
        self._properties[name] = value

    def properties(self):
        return self._properties

    def setProperties(self, properties):
        self._properties = properties

    def split(self, pos):
        text1 = self._text[:pos]
        text2 = self._text[pos:]
        frag1 = Fragment(text1, self._properties)
        frag2 = Fragment(text2, self._properties)
        return (frag1, frag2)

    def absorb(self, fragment):
        if fragment.properties() != self._properties:
            print("Fragments can only absorb other fragments with identical properties.")
            raise ValueError
        self._text += fragment.text()

        


