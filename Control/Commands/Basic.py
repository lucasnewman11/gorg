def hello(gte, fke):
    gte.insertPlainText("hello")

def insert_character(gte, fke):
    if fke[0:4] == "Shft":
        gte.insertPlainText(fke[5:])
    else:
        gte.insertPlainText(fke.lower())

def insert_space(gte, fke):
    gte.insertPlainText(" ")

def delete_character(gte, fke):
    if gte.__class__.__name__ == 'GorgMiniBuffer':
        gte.backspace()
    else:
        if len(gte.textCursor().selectedText()) > 0:
            gte.textCursor().removeSelectedText()
        else:
            gte.textCursor().deletePreviousChar()

def insert_new_line(gte, fke):
    gte.insertPlainText("\n")


    
        
    
