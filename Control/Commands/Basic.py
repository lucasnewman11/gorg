def _insert_text(gate, pos, addition):
    text_list = list(gate.get_raw_text())
    text_list.insert(pos, addition)
    new_string = "".join(text_list)
    gate.set_raw_text(new_string)

def hello(fke):
    _insert_text(fke.gate, fke.gate_adjusted_pos, "hello")
    
def insert_character(fke):
    string = fke.string
    if string[0:4] == "Shft":
        _insert_text(fke.gate, fke.gate_adjusted_pos, string[5:])
    else:
        _insert_text(fke.gate, fke.gate_adjusted_pos, string.lower())

def insert_space(fke):
    _insert_text(fke.gate, fke.gate_adjusted_pos, " ")

def _delete_selection(fke, selection_dict):
    adjusted_start = selection_dict["start"] - fke.gate_start_pos
    adjusted_end = selection_dict["end"] - fke.gate_start_pos
    text_list = list(fke.gate.get_raw_text())
    text_list = text_list[:adjusted_start] + text_list[adjusted_end:]
    fke.gate.set_raw_text("".join(text_list))

def _delete_char(fke):
    text_list = list(fke.gate.get_raw_text())
    text_list.pop()
    fke.gate.set_raw_text("".join(text_list))
    
def delete(fke):
    selection_dict = fke.gke.win.doc.get_selection()
    if len(selection_dict["string"]) > 0:
        _delete_selection(fke, selection_dict)
    else:
        _delete_char(fke)

def insert_new_line(fke):
    _insert_text(fke.gate, fke.gate_adjusted_pos, "\n")


    
        
    
