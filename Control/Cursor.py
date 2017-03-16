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
                            "underline": False}

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

    def _update_selection_points(self):
        self._start = min(self._point, self._mark)
        self._end = max(self._point, self._mark)

    def set_point(self, pos, record=True):
        print("POSITION", pos, record)
        length = self._gate.length()
        if pos < 0:
            self._point = 0
        elif pos > length:
            self._point = length
        else:
            self._point = pos
        if record == True:
            self._record_point()
        self._update_selection_points()

    def _record_point(self):
        self._recent_points.append(self._point)
        if len(self._recent_points) > 10:
            self._recent_points.pop(0)
        
    def last_point(self, n=2):
        index = n*-1
        try:
            return self._recent_points[index]
        except IndexError:
            return False

    def set_mark(self, pos):
        length = self._gate.length()
        if pos < 0:
            self._mark = 0
        elif pos > length:
            self._mark = length
        else:
            self._mark = pos
        self._update_selection_points()

    def is_mark_active(self):
        return self._mark_active

    def activate_mark(self):
        self._mark_active = True

    def deactivate_mark(self):
        self._mark_active = False

    def property(self, name):
        return self._properties[name]

    def set_property(self, name, value):
        self._properties[name] = value

    def properties(self):
        return self._properties

    def set_properties(self, properties):
        self._properties = properties

    def _split_frag_at_pos(self, pos):
        # Returns the fragment index which begins at pos.  If pos lands in the middle of a fragment, splits the fragment and then returns.  With overwrite as True, will replace the fragment at position with the new fragments.  If pos is at the end of the gate, returns an index equal to the length of the fragments list.
        gate_region = self._gate.region()
        target = gate_region.frag_by_pos(pos)
        if target:
            target_index = gate_region.index_by_frag(target)
            target_start = gate_region.pos_by_frag(target)
            adjusted_pos = pos - target_start
            if adjusted_pos > 0:
                new_fragments = target.split(adjusted_pos)
                new_region = Region()
                new_region.add_fragments
                gate_region.remove_fragment(target)
                gate_region.add_fragments(new_fragments, target_index)
                target_index += 1
        else:
            target_index = len(gate_region.fragments())
        return target_index
        
    def insert_region(self, region, pos):
        gate_region = self._gate.region()
        following_index = self._split_frag_at_pos(pos)
        gate_region.absorb(region, following_index)

    def selection(self, start, end, remove=False):
        gate_region = self._gate.region()
        start_following_index = self._split_frag_at_pos(start)
        end_following_index = self._split_frag_at_pos(end)
        sequence = [gate_region.frag_by_index(i) for i in range(start_following_index,
                                                       end_following_index)]
        if remove:
            for i in sequence:
                gate_region.remove_fragment(i)
        gate_region.simplify()
        selection = Region(sequence)
        return selection
                        
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
    
class Region():

    def __init__(self, fragments=[]):
        self._fragments = fragments

    def fragments(self):
        return self._fragments

    def length(self):
        num = 0
        for i in self._fragments:
            num += i.length()
        return num

    def raw_text(self):
        text = ""
        for i in self._fragments:
            text += i.text()
        return text

    def frag_by_pos(self, pos):
        num = 0
        for i in self._fragments:
            length = i.length()
            num += length
            if num > pos:
                return i
        if num == self.length():
            print("Position is at end of region.")
            return False
        else:
            print("Position is too large for region.")
            raise ValueError
        
    def pos_by_frag(self, frag):
        num = 0
        for i in self._fragments:
            if i == frag:
                return num
            else:
                num += i.length()

    def frag_by_index(self, index):
        return self._fragments[index]

    def index_by_frag(self, frag):
        return self._fragments.index(frag)

    def add_fragment(self, fragment, index=False):
        if not index:
            self._fragments.append(fragment)
        else:
            try:
                self._fragments.insert(index, fragment)
            except IndexError:
                self._fragments.append(fragment)

    def add_fragments(self, fragments, index=False):
        # accepts list of fragments
        if not index:
            self._fragments.extend(fragments)
        try:
            self._fragments[index:index] = fragments
        except IndexError:
            self._fragments.extend(fragments)
        
    def remove_fragment(self, fragment):
        try:
            self._fragments.remove(fragment)
        except IndexError:
            print("Index number is too large for this gate.")
            return False

    def simplify(self):
        index = 0
        frag = self._fragments[index]
        length = len(self._fragments)
        while index < length-1:
            target = self._fragments[index+1]
            if frag.properties() == target.properties():
                frag.absorb(target)
                self.remove_fragment(target)
            else:
                index += 1
                frag = self._fragments[index]
            length = len(self._fragments)

    def absorb(self, region, index=False):
        self.add_fragments(region.fragments(), index)
        self.simplify()
        
class Fragment():

    def __init__(self, text="", properties={"color" : "black",
                                            "bold" : False,
                                            "italics": False,
                                            "underline": False}):
        self._text = text
        self._properties = properties

    def text(self):
        return self._text

    def set_text(self, text):
        self._text = text

    def length(self):
        return len(self._text)

    def property(self, name):
        return self._properties[name]

    def set_property(self, name, value):
        self._properties[name] = value

    def properties(self):
        return self._properties

    def set_properties(self, properties):
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

        


