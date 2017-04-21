from copy import deepcopy

class Interface():
    # The controller class responsible for facilitating the manipulation of a specific chunk of data through a specific gate.

    def __init__(self):
        self._name = ""
        self._parent = False
        self._subordinates = {}
        self._order = []
        self._focus = False
        
    def name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    def order(self):
        return self._order

    def set_order(self, order):
        self._order = order

    def parent(self):
        return self._parent

    def set_parent(self, parent):
        self._parent = parent
        
    def add(self, name, sub):
        self._subordinates[name] = sub
        self._order.append(name)
        sub.set_parent(self)

    def sub_by_name(self, name):
        return self._subordinates[name]

    def sub_by_pos(self, pos):
        num = 0
        for i in self._order:
            sub = self._subordinates[i]
            length = sub.length()
            num += length
            if num >= pos:
                return sub

    def focus(self):
        return self._focus

    def set_focus(self, sub):
        self._focus = sub

    def fragments(self):
        fragments = []
        for i in self._order:
            fragments.extend(self._subordinates[i].fragments())
        return fragments
        
    def process_full_input_event(self, fie):
        fie.inter.append(self)
        point = fie.gie.pos
        sub = self.sub_by_pos(point)
        sub.process_full_input_event(fie)
        self.set_focus(sub)

    def blueprint(self):
        # returns a blueprint object of this interface with all of its contents
        blueprint = InterfaceBlueprint()
        blueprint.set_name(self.name())
        blueprint.set_focus_name(self.focus().name())
        for i in self.order():
            blueprint.add(i.name(), i.blueprint())
        return blueprint

class Gate():

    def __init__(self,
                 name="",
                 parent=False,
                 region=False,
                 read_only=False,
                 crop=False,
                 keymap=False):
        self._name = name
        self._parent = parent
        self._region = region
        self._cursor = GateCursor(self)
        self._read_only = read_only
        self._crop = crop
        self._keymap = keymap
        self._excursion = {}

    def name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    def parent(self):
        return self._parent

    def set_parent(self, parent):
        self._parent = parent

    def region(self):
        return self._region

    def set_region(self, region):
        self._region = region

    def cursor(self):
        return self._cursor
    
    def read_only(self):
        return self._read_only

    def set_read_only(self, ro):
        self._read_only = ro

    def crop(self):
        return self._crop

    def set_crop(self, crop):
        self._crop = crop

    def keymap(self):
        return self._keymap

    def set_keymap(self, keymap):
        self._keymap = keymap

    def length(self):
        return self._region.length()

    def fragments(self):
        return self._region.fragments()

    def insert_region(self, region, pos):
        length = region.length()
        point = self._cursor.point()
        self._region.insert_region_at_pos(region, pos)
        if point >= pos:
            self._cursor.set_point(point + length)

    def selection(self, start, end, remove=False, deactivate=True):
        selection = self._region.selection(start, end, remove)
        length = selection.length()
        point = self._cursor.point()
        if remove:
            if deactivate:
                self._cursor.deactivate_mark()
            if point > end:
                self._cursor.set_point(point-length)
            elif point >= start:
                self._cursor.set_point(start)
                
        return selection
            
    def process_full_input_event(self, fie):
        fie.gate = self
        command = self._keymap.match_input_event(fie)
        if command:
            if self.read_only() and not command.neutral():
                print("Target gate is read only.")
            else:
                command.execute(fie, config)

    def excursion(self):
        self._excursion["keymap"] = self._keymap

    def resume(self):
        self._keymap = self._excursion["keymap"]

    def blueprint(self):
        # returns a blueprint version of this gate
        blueprint = GateBlueprint()
        blueprint.set_name(self.name())
        blueprint.set_region_blueprint(self.region().blueprint())
        blueprint.set_read_only(self.read_only())
        blueprint.set_crop(self.crop())
        blueprint.set_keymap_blueprint(self.keymap().blueprint())
        return blueprint
        
class GateCursor():

    def __init__(self, gate):
        self._gate = gate
        self._point = 0
        self._mark = 0
        self._start = 0
        self._end = 0
        self._selection = {}
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
                        
class Region():

    def __init__(self, fragments=[]):
        self._fragments = deepcopy(fragments)

    def fragments(self):
        return self._fragments

    def length(self):
        num = 0
        for i in self._fragments:
            num += i.length()
        return num

    def __len__(self):
        return self.length()

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

    def blueprint(self):
        blueprint = RegionBlueprint()
        blueprint.set_markup(markup_from_region(self))
        return blueprint
                
class Fragment():

    def __init__(self, text="", text_properties={"color" : "black",
                                            "bold" : False,
                                            "italics": False,
                                            "underline": False}):
        self._text = text
        self._text_properties = deepcopy(text_properties)

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

class Keymap():
    def __init__(self):
        self._dict = {}
        self._config = False
        self._name = ""

    def name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    def config(self):
        return self._config

    def set_config(self, config):
        self._config = config

    def add(self, regex, command):
        # Accepts as argument 1) a regex object, and 2) a command class.
        self._dict[regex] = command

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

    def blueprint(self):
        kmb = KeymapBlueprint()
        for i in self._dict:
            kmb.add(i.pattern, self._dict[i].name())
        return kmb
        
import config
from Control.Blueprints import InterfaceBlueprint, GateBlueprint, RegionBlueprint
from Control.Markup import markup_from_region


