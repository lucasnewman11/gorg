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
        self._text_properties = {"color" : "black",
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

    def _update_text_properties(self):
        from copy import deepcopy
        fragment = self._gate.region().frag_by_pos(self._point, start=False)
        if fragment:
            self.set_text_properties(deepcopy(fragment.text_properties()))

    def set_point(self, pos, record=True, mark_also=True):
        length = self._gate.length()
        if pos < 0:
            self._point = 0
        elif pos > length:
            self._point = length
        else:
            self._point = pos
        if record == True:
            self._record_point()
        if mark_also == True:
            if not self.is_mark_active():
                self.set_mark(pos)
        self._update_text_properties()
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

    def text_property(self, name):
        return self._text_properties[name]

    def set_text_property(self, name, value):
        self._text_properties[name] = value

    def text_properties(self):
        return self._text_properties

    def set_text_properties(self, properties):
        self._text_properties = properties
                        
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

    def text(self):
        text = ""
        for i in self._fragments:
            text += i.text()
        return text

    def frag_by_pos(self, pos, start=True):
        "Returns the fragment which contains pos.  By default, will return the fragment which starts at pos, and false if position is at end of the region. With start set to False, will instead return the fragment which ends at pos, and False if position is at the start of the region."
        num = 0
        if start:
            for i in self._fragments:
                length = i.length()
                num += length
                if num > pos:
                    return i
            if pos == self.length():
                return False
            else:
                print("Position is outside of region.")
                raise ValueError
        else:
            for i in self._fragments:
                length = i.length()
                num += length
                if num >= pos:
                    return i
            if pos == 0:
                return False
            else:
                print("Position is outside of region.")
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

    def add_fragment(self, fragment, index="end",):
        if index == "end":
            self._fragments.append(fragment)
        else:
            self._fragments.insert(index, fragment)
            
    def add_fragments(self, fragments, index="end"):
        # accepts list of fragments
        if index == "end":
            self._fragments.extend(fragments)
        else:
            self._fragments[index:index] = fragments
        
    def remove_fragment(self, fragment):
        self._fragments.remove(fragment)

    def _split_frag(self, fragment, adjusted_pos, replace=True):
        new_fragments = fragment.split(adjusted_pos)
        if new_fragments and replace:
            frag_index = self.index_by_frag(fragment)
            self.remove_fragment(fragment)
            self.add_fragments(new_fragments, frag_index)
        
    def _split_frag_at_pos(self, pos, replace=True):
        target = self.frag_by_pos(pos)
        if target:
            target_start = self.pos_by_frag(target)
            adjusted_pos = pos - target_start
            if adjusted_pos > 0:
                self._split_frag(target, adjusted_pos, replace)
                                    
    def insert_region_at_pos(self, region, pos, simplify=True):
        self._split_frag_at_pos(pos)
        target = self.frag_by_pos(pos, start=True)
        if target:
            target_index = self.index_by_frag(target)
        else:
            target_index = "end"
        self.insert_region_at_index(region, target_index, simplify)

    def insert_region_at_index(self, region, index, simplify=True):
        self.add_fragments(region.fragments(), index)
        if simplify:
            self.simplify()
            
    def selection(self, start, end, remove=False):
        self._split_frag_at_pos(start)
        self._split_frag_at_pos(end)
        start_target = self.frag_by_pos(start)
        end_target = self.frag_by_pos(end)
        # assigns start index
        if start_target:
            start_index = self.index_by_frag(start_target)
        # assigns end index
        if end_target:
            end_index = self.index_by_frag(end_target)
        # creates sublist of fragments

        if start_target and end_target:
            fragments = self._fragments[start_index:end_index]
        elif start_target and not end_target:
            fragments = self._fragments[start_index:]
        else:
            fragments = []
        # removes fragments if necessary
        if remove:
            for i in fragments:
                self.remove_fragment(i)
            if self._fragments:
                self.simplify()
        # creates and returns Region
        selection_region = Region(fragments)

        return selection_region
        
    def simplify(self):
            index = 0
            frag = self._fragments[index]
            length = len(self._fragments)
            while index < length-1 and length >= 2:
                target = self.frag_by_index(index+1)
                if frag.text_properties() == target.text_properties():
                    frag.absorb(target)
                    self.remove_fragment(target)
                else:
                    index += 1
                    frag = self._fragments[index]
                length = len(self._fragments)
        
class Fragment():

    def __init__(self, text="", text_properties={"color" : "black",
                                            "bold" : False,
                                            "italics": False,
                                            "underline": False}):
        self._text = text
        self._text_properties = text_properties

    def text(self):
        return self._text

    def set_text(self, text):
        self._text = text

    def length(self):
        return len(self._text)

    def text_property(self, name):
        return self._text_properties[name]

    def set_text_property(self, name, value):
        self._text_properties[name] = value

    def text_properties(self):
        return self._text_properties

    def set_text_properties(self, properties):
        self._text_properties = properties

    def split(self, pos):
        from copy import deepcopy
        text1 = self._text[:pos]
        text2 = self._text[pos:]
        frag1 = Fragment(text1, deepcopy(self._text_properties))
        frag2 = Fragment(text2, deepcopy(self._text_properties))
        return (frag1, frag2)

    def absorb(self, fragment):
        if fragment.text_properties() != self._text_properties:
            print("Fragments can only absorb other fragments with identical text_properties.")
            raise ValueError
        self._text += fragment.text()

        


