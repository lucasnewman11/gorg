class InterfaceBlueprint():

    def __init__(self):
        self._name = ""
        self._order = []
        self._subordinates = {}
        self._focus_name = ""
        
    def name(self):
        return self._name
    
    def set_name(self, name):
        self._name = name

    def order(self):
        return self._order

    def set_order(self, order):
        self._order = order

    def focus_name(self):
        return self._focus_name

    def set_focus_name(self, focus_name):
        self._focus_name = focus_name

    def add(self, name, sub):
        self._subordinates[name] = sub
        self._order.append(name)
        
    def sub_by_name(self, name):
        return self._subordinates[name]

    def materialize(self, keymaps_dict):
        interface = Interface()
        interface.set_name(self.name())
        for i in self.order():
            blueprint = self.sub_by_name(i)
            subordinate = blueprint.materialize(keymaps_dict)
            interface.add(subordinate.name(), subordinate)
        interface.set_focus(interface.sub_by_name(self.focus_name()))
        return interface

    def data(self):
        # returns persistible Python data structure

class GateBlueprint():

    def __init__(self):
        self._name = False
        self._region_blueprint = False
        self._read_only = False
        self._crop = False
        self._keymap_blueprint = False

    def name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    def region_blueprint(self):
        return self._region_blueprint

    def set_region_blueprint(self, blue):
        self._region_blueprint = blue
    
    def read_only(self):
        return self._read_only

    def set_read_only(self, read_only):
        self._read_only = read_only

    def crop(self):
        return self._crop

    def set_crop(self, crop):
        self._crop = crop

    def keymap_blueprint(self):
        return self._keymap_blueprint

    def set_keymap_blueprint(self, blueprint):
        self._keymap_blueprint = blueprint

    def materialize(self, keymaps_dict):
        # from Control.Core import my_debug; my_debug()
        gate = Gate()
        gate.set_name(self.name())
        # initializes fragments
        for i in self.fragment_dicts():
            text = i["text"]
            properties = {k:v for k, v in i.items() if k != "text"}
            fragment = Fragment(text, properties)
            gate.region().add_fragment(fragment)
        # initializes gate properties
        gate.set_read_only(self.read_only())
        gate.set_crop(self.crop())
        # initializes gate keymaps
        keymap = keymaps_dict[self.keymap_name()]
        gate.set_active_map(keymap)
        gate.set_primary_map(keymap)
        return gate

    def data(self):
        # returns persistible Python data structure

class RegionBlueprint():

    def __init__(self):
        self._markup = ""

    def markup(self):
        return self._markup

    def set_markup(self, markup):
        self._markup = markup

    def materialize(self):
        # I need to specify the markup, and then write the parser

    def data(self):
        # returns persistible Python data structure

class KeymapBlueprint():

    
                           
def make_interface_blueprints_dict_from_file(fyl, gate_blueprints_dict):
    json_dict = json.load(fyl)
    interface_blueprints_dict = {}
    for i in json_dict:
        new_blue = InterfaceBlueprint()
        new_blue.set_name(i)
        properties = json_dict[i]
        order = properties["order"]
        for j in order:
            sub_name = j[0]
            sub_type = j[1]
            if sub_type == "interface":
                try:
                    sub = interface_blueprints_dict[sub_name]
                except ValueError:
                    print("The InterfaceBlueprint for", sub_name, "does not exist.  Check to see if it referenced in your json config file before it has been constructed.")
                    raise ValueError
            elif sub_type == "gate":
                try:
                    sub = gate_blueprints_dict[sub_name]
                except ValueError:
                    print("The GateBlueprint for", sub_name, "does not exist.")
                    raise ValueError
            new_blue.add(sub_name, sub)
        focus_name = properties["focus"]
        new_blue.set_focus_name(focus_name)
        interface_blueprints_dict[i] = new_blue
    return interface_blueprints_dict
        
def make_gate_blueprints_dict_from_file(fyl):
    json_dict = json.load(fyl)
    gate_blueprints_dict = {}
    for i in json_dict:
        new_blue = GateBlueprint()
        new_blue.set_name(i)
        properties = json_dict[i]
        # fragments
        fragments = properties["fragments"]
        for j in fragments:
            new_blue.add_fragment_dict(j)
        # read only
        read_only = properties["read_only"]
        new_blue.set_read_only(read_only)
        # crop
        crop = properties["crop"]
        new_blue.set_crop(crop)
        # keymap
        keymap_name = properties["keymap"]
        new_blue.set_keymap_name(keymap_name)
        # appends to main dict
        gate_blueprints_dict[i] = new_blue
    return gate_blueprints_dict


    



