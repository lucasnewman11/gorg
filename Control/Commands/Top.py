import View.Frames

def _split_window(fie, ori):

    window = fie.gie.win
    parent = window.parent()
    loc = parent.loc_from_obj(window)
    path = window.path()
    name = parent.name_from_obj(window)
    frame = fie.gie.frame
    comm = fie.commander
    inter = comm.get_interface(window)

    print(window, loc, path, name)
    
    parent.remove_obj(window)

    new_lattice = View.Frames.Lattice()
    new_lattice.place_obj(window, name, (1, 1))
    lattice_name = frame._namer.newname()
    parent.place_obj(new_lattice, lattice_name, loc)

    new_name = frame._namer.newname()
    new_window = View.Frames.Window()
    if ori == "v":
        new_lattice.place_obj(new_window, new_name, (1, 2))
    elif ori == "h":
        new_lattice.place_obj(new_window, new_name, (2, 1))

    comm.add_window(new_name, new_window)
    comm.assign_window(new_window, inter)
    

def split_window_horizontal(fie):
    _split_window.__call__(fie, "h")

def split_window_vertical(fie):
    _split_window.__call__(fie, "v")

def change_window_focus(fie):
    window = fie.gie.win
    next_window = _get_next_window(window)
    print(next_window)
    next_window.setFocus()
    
def _get_next_window(widget):
    parent = widget.parent()
    if widget.path() == "TOP/MINI":
        result = _get_first_window(parent)
        print(result)
        return result
    next_widget = _get_next_widget(widget, parent)
    if next_widget:
        return _get_first_window(next_widget)
    else:
        return _get_next_window(parent)

def _get_next_widget(widget, parent):
    loc = parent.loc_from_obj(widget)
    hor_next_loc = (loc[0], loc[1] + 1)
    try:
        new_win = parent.obj_from_loc(hor_next_loc)
    except KeyError:
        new_win = False

    if new_win:
        return new_win
    else:
        ver_next_loc = (loc[0] + 1, 1)
        try:
            new_win = parent.obj_from_loc(ver_next_loc)
        except KeyError:
            new_win = False
        if new_win:
            return new_win
        else:
            return False

def _get_first_window(widget):
    print("wdg", widget, widget.path())
    if type(widget) == View.Frames.Lattice:
        new_widget = widget.obj_from_loc((1, 1))
        return _get_first_window(new_widget)
    else:
        return widget
                                         

    



    
