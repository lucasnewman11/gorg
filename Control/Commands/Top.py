def split_window_horizontal(fke):
    new_name = fke.gke.frame.split_window(fke.gke.win.name, "h")
    fke.commander.add_window(new_name, fke.gke.frame.get_window(new_name))
    fke.commander.assign_window(fke.gke.frame.get_window(new_name),
                                fke.gke.win.get_interface())

def split_window_vertical(fke):
    new_name = fke.gke.frame.split_window(fke.gke.win.name, "v")
    fke.commander.add_window(new_name, fke.gke.frame.get_window(new_name))
    fke.commander.assign_window(fke.gke.frame.get_window(new_name),
                                fke.gke.win.get_interface())


    
