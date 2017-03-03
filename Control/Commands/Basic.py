def _insert_text(gate, pos, addition):
    text_list = list(gate.get_raw_text())
    text_list.insert(pos, addition)
    point = gate.cursor().point()
    mark = gate.cursor().mark()
    new_string = "".join(text_list)
    gate.set_raw_text(new_string)
    if pos <= point:
        gate.cursor().setpoint(point + len(addition))
    if pos <= mark:
        gate.cursor().setmark(mark + len(addition))

def hello(fke):
    _insert_text(fke.gate, fke.gate.cursor().point(), "hello")
    
def insert_character(fke):
    string = fke.string
    if string[0:4] == "Shft":
        _insert_text(fke.gate, fke.gate.cursor().point(), string[5:])
    else:
        _insert_text(fke.gate, fke.gate.cursor().point(), string.lower())

def insert_space(fke):
    _insert_text(fke.gate, fke.gate.cursor().point(), " ")

def _delete_text(gate, start, end):
    cursor = gate.cursor()
    point = cursor.point()
    mark = cursor.mark()
    text_list = list(gate.get_raw_text())
    new_text_list = text_list[:start] + text_list[end:]
    gate.set_raw_text("".join(new_text_list))
    if end < point:
        cursor.setpoint(point - (end - start))
    elif end >= point and start < point:
        cursor.setpoint(start)
    if end < mark:
        cursor.setmark(mark - (end - start))
    elif end >= mark and start < mark:
        cursor.setmark(start)
    cursor.deactivate_mark()
    
def delete(fke):
    selection = fke.gate.cursor().selection()
    if len(selection["string"]) > 0:
        _delete_text(fke.gate, selection["start"], selection["end"])
    else:
        point = fke.gate.cursor().point()
        _delete_text(fke.gate, point-1, point)
    fke.gate.mark_active = False

def insert_new_line(fke):
    _insert_text(fke.gate, fke.gate.cursor().point(), "\n")

def _move_point_only(cursor, pos):
    cursor.setpoint(pos)

def _move_mark_only(cursor, pos):
    cursor.setmark(pos)

def _move_point(cursor, pos):
    _move_point_only(cursor, pos)
    if not cursor.is_mark_active():
        _move_mark_only(cursor, pos)

def move_point_to_click(fme):
    cursor = fme.gate.cursor()
    _move_point(cursor, fme.gme.pos)

def move_mark_to_mouse_location(fme):
    cursor = fme.gate.cursor()
    cursor.activate_mark()
    _move_mark_only(cursor, fme.gme.pos)
    
def advance_point_by_char(fke):
    cursor = fke.gate.cursor()
    pos = cursor.point() + 1
    _move_point(cursor, pos)
            
def retreat_point_by_char(fke):
    cursor = fke.gate.cursor()
    pos = cursor.point() - 1
    _move_point(cursor, pos)

def _search_string_forwards(pattern, string):
    import re
    match = re.search(pattern, string)
    if match:
        match_pos = match.start()
    else:
        match_pos = len(string)
    return match_pos

def _search_string_backwards(pattern, string):
    import re
    matches = list(re.finditer(pattern, string))
    if matches:
        match_pos = matches[-1].start()
    else:
        match_pos = 0
    return match_pos

def _advance_point_to_match(gate, pattern):
    text = gate.get_raw_text()
    cursor = gate.cursor()
    point = cursor.point()
    remaining = text[point:]
    relative_pos = _search_string_forwards(pattern, remaining)
    pos = point + relative_pos
    _move_point(cursor, pos)

def _retreat_point_to_match(gate, pattern):
    text = gate.get_raw_text()
    cursor = gate.cursor()
    point = cursor.point()
    remaining = text[:point]
    pos = _search_string_backwards(pattern, remaining)
    _move_point(cursor, pos)

def advance_point_by_word(fke):
    gate = fke.gate
    _advance_point_to_match(gate, "\s")
    _advance_point_to_match(gate, "[^\s]")

def retreat_point_by_word(fke):
    gate = fke.gate
    _retreat_point_to_match(gate, "[^\s]")
    _retreat_point_to_match(gate, "\s")
    _advance_point_to_match(gate, "[^\s]")

def move_point_start_of_line(fke):
    gte = fke.gke.win.doc
    cursor = fke.gate.cursor()
    point = cursor.point()
    layout = gte.document().firstBlock().layout()
    line = layout.lineForTextPosition(point)
    pos = line.textStart()
    _move_point(cursor, pos)

def move_point_end_of_line(fke):
    gte = fke.gke.win.doc
    cursor = fke.gate.cursor()
    point = cursor.point()
    layout = gte.document().firstBlock().layout()
    line = layout.lineForTextPosition(point)
    pos = line.textStart() + line.textLength() - 1
    _move_point(cursor, pos)

def move_point_next_line(fke):
    gte = fke.gke.win.doc
    cursor = fke.gate.cursor()
    point = cursor.point()
    layout = gte.document().firstBlock().layout()
    line = layout.lineForTextPosition(point)
    target_line = layout.lineAt(line.lineNumber()+1)
    column = gte._cursor.columnNumber()
    _move_point(cursor, target_line.textStart())
    if target_line.textLength() > column:
        _move_point(cursor, cursor.point() + column)
    else:
        _move_point(cursor, target_line.textStart() + target_line.textLength() - 1)
    
def move_point_previous_line(fke):
    move_point_start_of_line(fke)
    gte = fke.gke.win.doc
    cursor = fke.gate.cursor()
    point = cursor.point()
    layout = gte.document().firstBlock().layout()
    line = layout.lineForTextPosition(point)
    target_line = layout.lineAt(line.lineNumber()-1)
    column = gte._cursor.columnNumber()
    _move_point(cursor, target_line.textStart())
    if target_line.textLength() > column:
        _move_point(cursor, cursor.point() + column)
    else:
        _move_point(cursor, target_line.textStart() + target_line.textLength() - 1)
    
def advance_point_by_sentence(fke):
    _advance_point_to_match(fke.gate, "\.\s")
    _advance_point_to_match(fke.gate, "[^\.\s]")

def retreat_point_by_sentence(fke):
    _retreat_point_to_match(fke.gate, "[^\.\s]")
    _retreat_point_to_match(fke.gate, "\.\s")
    _advance_point_to_match(fke.gate, "[^\.\s]")
      
def set_mark(fke):
    cursor = fke.gate.cursor()
    point = cursor.point()
    mark = cursor.mark()
    if point != mark:
        cursor.setmark(point)
        cursor.activate_mark()
    elif point == mark and not cursor.is_mark_active():
        cursor.activate_mark()
    elif point == mark and cursor.is_mark_active():
        cursor.setmark(point)
        cursor.deactivate_mark()



    


    
        
    
