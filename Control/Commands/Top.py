def _split_window(fke, ori):
    window = fke.gke.win
    parent = window.parent()
    loc = parent.loc_from_object(window)
    path = window.path()
    name = window.parent().name_from_obj(window)

    print(window, parent)

    parent.remove_obj(window)

    new_lattice = View.Frames.Lattice()
    new_lattice.place_obj(window, name, (1, 1))
    lattice_name = self._namer.newname()
    parent.place_obj(new_lattice, lattice_name, loc)

    new_name = self._namer.newname()
    new_window = View.Frames.Window()
    if ori == "v":
        new_lattice.place_obj(new_window, new_name, (1, 2))
    elif ori == "h":
        new_lattice.place_obj(new_window, new_name, (2, 1))

    fke.commander.add_window(new_name, new_window)
    fke.commander.assign_window(new_window, fke.inter)

def split_window_horizontal(fke):
    _split_window.__call__(fke, "h")

def split_window_vertical(fke):
    _split_window.__call__(fke, "v")




    
