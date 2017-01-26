def _insert_text(gate, pos, addition):
    gate.set_raw_text("".join(list(gate.get_text()[0]).insert(pos, addition)))

def hello(fke):
    _insert_text(fke.gate, fke.pos, "hello")
    
def insert_character(fke):
    string = fke.string
    if string[0:4] == "Shft":
        _insert_text(fke.gate, fke.pos, string[5:])
    else:
        _insert_text(fke.gate, fke.pos, string.lower())

def insert_space(fke):
    _insert_text(fke.gate, fke.pos, " ")

def delete_character(fke):
    wdg = fke.gke.win
    if wdg.__class__.__name__ == 'MiniWindow':
        ge.backspace()
    else:
        if len(fke.gke.win.doc.textCursor().selectedText()) > 0:
            gte.textCursor().removeSelectedText()
        else:
            gte.textCursor().deletePreviousChar()

def insert_new_line(fke):
    gte.insertPlainText("\n")


    
        
    
