import View.Frames
from Control.Commands.Basic import NeutralCommand, WriteCommand

class SplitWindowCommand(NeutralCommand):
    "Base class of commands that split the window with focus."

    def _split_window(fie, ori):

        window = fie.gie.win
        parent = window.parent()
        loc = parent.loc_from_obj(window)
        path = window.path()
        name = parent.name_from_obj(window)
        frame = fie.gie.frame
        comm = fie.commander
        inter = comm.inter_by_window(window)
    
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
    

class Split_Window_Horizontal(SplitWindowCommand):
    "Splits the window with focus horizontally, assigning to the new window the same interface."

    @classmethod
    def execute(cls, fie, config):
        cls._split_window.__call__(fie, "h")

class Split_Window_Vertical(SplitWindowCommand):
    "Splits the window with focus veritcally, assigning to the new window the same interface."
    @classmethod
    def execute (cls, fie, config):
        cls._split_window.__call__(fie, "v")

class Change_Window_Focus(NeutralCommand):
    "Changes which window has focus according to a set rotation."

    @classmethod
    def _get_next_window(cls, widget):
        parent = widget.parent()
        if widget.path() == "TOP/MINI":
            result = cls._get_first_window(parent)
            return result
        next_widget = cls._get_next_widget(widget, parent)
        if next_widget:
            return cls._get_first_window(next_widget)
        else:
            print(parent.path())
            return cls._get_next_window(parent)

    def _get_next_widget(widget, parent):
        loc = parent.loc_from_obj(widget)
        hor_next_loc = (loc[0], loc[1]+1)
        try:
            new_win = parent.obj_from_loc(hor_next_loc)
        except KeyError:
            new_win = False
        if new_win:
            return new_win
        else:
            ver_next_loc = (loc[0]+1, 1)
            try:
                new_win = parent.obj_from_loc(ver_next_loc)
            except KeyError:
                new_win = False
            return new_win

    @classmethod
    def _get_first_window(cls, widget):
        if type(widget) == View.Frames.Lattice:
            new_widget = widget.obj_from_loc((1, 1))
            return cls._get_first_window(new_widget)
        else:
            return widget

    @classmethod
    def execute(cls, fie, config):
        window = fie.gie.win
        next_window = cls._get_next_window(window)
        next_window.setFocus()
    
    



    
