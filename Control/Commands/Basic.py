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

def hello(fie):
    _insert_text(fie.gate, fie.gate.cursor().point(), "hello")
    
def insert_character(fie):
    string = fie.string
    if string[0:4] == "Shft":
        _insert_text(fie.gate, fie.gate.cursor().point(), string[5:])
    else:
        _insert_text(fie.gate, fie.gate.cursor().point(), string.lower())

def insert_space(fie):
    _insert_text(fie.gate, fie.gate.cursor().point(), " ")

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
    
def delete(fie):
    gate = fie.gate
    cursor = gate.cursor()
    selection = cursor.selection()
    if len(selection) > 0:
        _delete_text(gate, gate.start(), gate.end())
    else:
        point = cursor.point()
        _delete_text(gate, point-1, point)
    cursor.deactive_mark()

def insert_new_line(fie):
    _insert_text(fie.gate, fie.gate.cursor().point(), "\n")

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
    _move_point(cursor, fme.gie.pos)

def move_mark_to_mouse_location(fme):
    cursor = fme.gate.cursor()
    cursor.activate_mark()
    _move_mark_only(cursor, fme.gie.pos)
    
def advance_point_by_char(fie):
    cursor = fie.gate.cursor()
    pos = cursor.point() + 1
    _move_point(cursor, pos)
            
def retreat_point_by_char(fie):
    cursor = fie.gate.cursor()
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

def advance_point_by_word(fie):
    gate = fie.gate
    _advance_point_to_match(gate, "\s")
    _advance_point_to_match(gate, "[^\s]")

def retreat_point_by_word(fie):
    gate = fie.gate
    _retreat_point_to_match(gate, "[^\s]")
    _retreat_point_to_match(gate, "\s")
    _advance_point_to_match(gate, "[^\s]")

def _start_of_line(fie):
    import pdb
    gte = fie.gie.win.doc
    cursor = fie.gate.cursor()
    point = cursor.point()
    layout = gte.document().firstBlock().layout()
    line = layout.lineForTextPosition(point)
    pos = line.textStart()
    # return pos

def _end_of_line(fie):
    gte = fie.gie.win.doc
    cursor = fie.gate.cursor()
    point = cursor.point()
    layout = gte.document().firstBlock().layout()
    line = layout.lineForTextPosition(point)
    pos = line.textStart() + line.textLength() - 1
    # return pos
    
def move_point_start_of_line(fie):
    cursor = fie.gate.cursor()
    pos = _start_of_line(fie)
    # _move_point(cursor, pos)    

def move_point_end_of_line(fie):
    cursor = fie.gate.cursor()
    pos = _end_of_line(fie)
    # _move_point(cursor, pos)

def move_point_next_line(fie):
    gte = fie.gie.win.doc
    cursor = fie.gate.cursor()
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
    
def move_point_previous_line(fie):
    gte = fie.gie.win.doc
    cursor = fie.gate.cursor()
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
    
def advance_point_by_sentence(fie):
    _advance_point_to_match(fie.gate, "\.\s")
    _advance_point_to_match(fie.gate, "[^\.\s]")

def retreat_point_by_sentence(fie):
    _retreat_point_to_match(fie.gate, "[^\.\s]")
    _retreat_point_to_match(fie.gate, "\.\s")
    _advance_point_to_match(fie.gate, "[^\.\s]")
      
def set_mark(fie):
    cursor = fie.gate.cursor()
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

def kill_region(fie):
    gate = fie.gate
    cursor = gate.cursor()
    ring = cursor.ring()
    selection = cursor.selection()
    start = cursor.start()
    end = cursor.end()
    ring.add(selection)
    _delete_text(gate, start, end)

def kill_line(fie):
    gate = fie.gate
    cursor = gate.cursor()
    point = cursor.point()
    ring = cursor.ring()
    end_of_line = _end_of_line(fie)
    substring = cursor.get_substring(point, end_of_line)
    ring.add(substring)
    _delete_text(gate, point, end_of_line)

def yank(fie):
    gate = fie.gate
    cursor = gate.cursor()
    point = cursor.point()
    ring = cursor.ring()
    attempt = ring.get()
    _insert_text(gate, point, attempt)
    gate.set_active_keymap(fie.commander.keymaps()["Yank"])
    
def yank_next(fie):
    gate = fie.gate
    cursor = gate.cursor()
    point = cursor.point()
    ring = cursor.ring()
    # deletes last yank attempt
    current = ring.get()
    start_of_current = point - len(current)
    _delete_text(gate, start_of_current, point)
    point = cursor.point()
    # updates ring
    ring.next_index()
    attempt = ring.get()
    _insert_text(gate, point, attempt)
        
def yank_previous(fie):
    gate = fie.gate
    cursor = gate.cursor()
    point = cursor.point()
    ring = cursor.ring()
    # deletes last yank attempt
    current = ring.get()
    start_of_current = point - len(current)
    _delete_text(gate, start_of_current, point)
    point = cursor.point()
    # updates ring
    ring.previous_index()
    attempt = ring.get()
    _insert_text(gate, point, attempt)

def yank_pop(fie):
    gate = fie.gate
    gate.set_active_keymap(gate.primary_keymap())
    ring = gate.cursor().ring()
    ring.remove(ring.index())

def yank_place(fie):
    gate = fie.gate
    gate.set_active_keymap(gate.primary_keymap())

def yank_cancel(fie):
    gate = fie.gate
    cursor = gate.cursor()
    point = cursor.point()
    ring = cursor.ring()
    # deletes last yank attempt
    current = ring.get()
    start_of_current = point - len(current)
    _delete_text(gate, start_of_current, point)
    # resets keymap
    gate.set_active_keymap(gate.primary_keymap())



    



    


    
        
    
