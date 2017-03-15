from Control.Cursor import Fragment, Region

def _insert_text(gate, pos, addition):
    cursor = gate.cursor()
    properties = cursor.properties()
    # creates the Region object containing the text fragment
    fragments = [Fragment(addition, properties)]
    region = Region(fragments)
    # inserts the Region object into the target gate
    cursor.insert_region(region, pos)
    # adjusts the position of point if necessary
    point = cursor.point()
    if pos <= point:
        _move_point(cursor, len(addition))
    
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
    selection = cursor.selection(start, end, remove=True)
    if end < point:
        _move_point(cursor, (point - (end - start)))
    elif end >= point and start < point:
        _move_point(cursor, start)
    cursor.deactivate_mark()
    
def delete(fie):
    gate = fie.gate
    cursor = gate.cursor()
    selection = cursor.selection(cursor.start(), cursor.end())
    if len(selection) > 0:
        _delete_text(gate, cursor.start(), cursor.end())
    else:
        point = cursor.point()
        _delete_text(gate, point-1, point)

def insert_new_line(fie):
    _insert_text(fie.gate, fie.gate.cursor().point(), "\n")

def _move_point_only(cursor, pos, record):
    cursor.setpoint(pos, record)

def _move_mark_only(cursor, pos):
    cursor.setmark(pos)

def _move_point(cursor, pos, record=True):
    _move_point_only(cursor, pos, record)
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
    text = gate.region().raw_text()
    cursor = gate.cursor()
    point = cursor.point()
    remaining = text[point:]
    relative_pos = _search_string_forwards(pattern, remaining)
    pos = point + relative_pos
    _move_point(cursor, pos)

def _retreat_point_to_match(gate, pattern):
    text = gate.region().raw_text()
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
    gte = fie.gie.win.gte()
    cursor = fie.gate.cursor()
    point = cursor.point()
    document = gte.document()
    block = document.findBlock(point)
    sub_point = point - block.position()
    layout = block.layout()
    line = layout.lineForTextPosition(sub_point)
    this_layout_loc = (block.blockNumber(), line.lineNumber())
    current_layout_loc = this_layout_loc
    pos = point
    while (current_layout_loc == this_layout_loc) and (pos != 0):
        pos -= 1
        block = document.findBlock(pos)
        sub_pos = pos - block.position()
        layout = block.layout()
        line = layout.lineForTextPosition(sub_pos)
        current_layout_loc = (block.blockNumber(), line.lineNumber())
    return pos+1

def _end_of_line(fie):
    gte = fie.gie.win.gte()
    gate = fie.gate
    text = gate.get_raw_text()
    text_length = len(text)
    cursor = gate.cursor()
    point = cursor.point()
    document = gte.document()
    block = document.findBlock(point)
    sub_point = point - block.position()
    layout = block.layout()
    line = layout.lineForTextPosition(sub_point)
    this_layout_loc = (block.blockNumber(), line.lineNumber())
    current_layout_loc = this_layout_loc
    pos = point
    while (current_layout_loc == this_layout_loc) and (pos != text_length):
        pos += 1
        block = document.findBlock(pos)
        sub_pos = pos - block.position()
        layout = block.layout()
        line = layout.lineForTextPosition(sub_pos)
        current_layout_loc = (block.blockNumber(), line.lineNumber())
    return pos-1

def move_point_start_of_line(fie):
    cursor = fie.gate.cursor()
    pos = _start_of_line(fie)
    _move_point(cursor, pos)
    
def move_point_end_of_line(fie):
    cursor = fie.gate.cursor()
    pos = _end_of_line(fie)
    _move_point(cursor, pos)

def move_point_next_line(fie):
    gte = fie.gie.win.gte()
    cursor = fie.gate.cursor()
    point = cursor.point()
    document = gte.document()
    block = document.findBlock(point)
    sub_point = point - block.position()
    layout = block.layout()
    line = layout.lineForTextPosition(sub_point)
    layout_loc = (block.blockNumber(), line.lineNumber())
    column = gte._cursor.columnNumber()
    # if column == 0:
    #     if cursor.lastpoint():
    #         _move_point(cursor, cursor.lastpoint(), False)
    #         gte.update_view(fie.inter)
    #         column = gte._cursor.columnNumber()
    #         _move_point(cursor, point, False)
    block_length = block.length()
    last_line = layout.lineForTextPosition(block_length-1)
    last_line_number = last_line.lineNumber()
    blocks = document.blockCount()
    if layout_loc[1] == last_line_number:
        if layout_loc[0]+1 < blocks:
            target_layout_loc = (layout_loc[0]+1, 0)
        else:
            target_layout_loc = False
    else:
        target_layout_loc = (layout_loc[0], layout_loc[1]+1)
    if target_layout_loc:
        target_block = document.findBlockByNumber(target_layout_loc[0])
        target_block_layout = target_block.layout()
        target_line = target_block_layout.lineAt(target_layout_loc[1])
        
        _move_point(cursor, target_line.textStart() + target_block.position(), False)
        if target_line.textLength() > column:
            _move_point(cursor, cursor.point() + column)
        else:
            _move_point(cursor, cursor.point() + target_line.textLength())
    else:
        move_point_end_of_line(fie)

def print_shit(fie):
    True
    
def move_point_previous_line(fie):
    gte = fie.gie.win.gte()
    cursor = fie.gate.cursor()
    point = cursor.point()
    document = gte.document()
    block = document.findBlock(point)
    sub_point = point - block.position()
    layout = block.layout()
    line = layout.lineForTextPosition(sub_point)
    layout_loc = (block.blockNumber(), line.lineNumber())
    column = gte._cursor.columnNumber()
    if column == 0:
        if cursor.lastpoint():
            _move_point(cursor, cursor.lastpoint(), False)
            gte.update_view(fie.inter)
            column = gte._cursor.columnNumber()
            _move_point(cursor, point, False)
    block_length = block.length()
    blocks = document.blockCount()
    if layout_loc[1] == 0:
        if layout_loc[0] != 0:
            previous = block.previous()
            previous_last_line = previous.layout().lineForTextPosition(previous.length()-1)
            previous_last_line_number = previous_last_line.lineNumber()
            target_layout_loc = (layout_loc[0]-1, previous_last_line_number)
        else:
            target_layout_loc = False
    else:
        target_layout_loc = (layout_loc[0], layout_loc[1]-1)

    if target_layout_loc:
        target_block = document.findBlockByNumber(target_layout_loc[0])
        target_block_layout = target_block.layout()
        target_line = target_block_layout.lineAt(target_layout_loc[1])
        
        _move_point(cursor, target_line.textStart() + target_block.position(), False)
        if target_line.textLength() > column:
            _move_point(cursor, cursor.point() + column)
        else:
            _move_point(cursor, cursor.point() + target_line.textLength())
    else:
        move_point_start_of_line(fie)
    
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
    start = cursor.start()
    end = cursor.end()
    selection = cursor.selection(start, end, remove=True)
    ring.add(selection)

def kill_line(fie):
    gate = fie.gate
    cursor = gate.cursor()
    point = cursor.point()
    ring = cursor.ring()
    end_of_line = _end_of_line(fie)
    selection = cursor.selection(point, end_of_line, remove=True)
    ring.add(selection)
    _delete_text(gate, point, end_of_line)

def yank(fie):
    gate = fie.gate
    cursor = gate.cursor()
    point = cursor.point()
    ring = cursor.ring()
    attempt = ring.get()
    cursor.insert_region(attempt, point)
    gate.set_active_keymap(fie.commander.keymaps()["Yank"])
    
def yank_next(fie):
    gate = fie.gate
    cursor = gate.cursor()
    point = cursor.point()
    ring = cursor.ring()
    # deletes last yank attempt
    current = ring.get()
    start_of_current = point - current.length()
    _delete_text(gate, start_of_current, point)
    point = cursor.point()
    # updates ring
    ring.next_index()
    # attempts next yank
    attempt = ring.get()
    cursor.insert_region(attempt, point)

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
    cursor.insert_region(attempt, point)

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



    



    


    
        
    
