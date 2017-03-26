from Control.Cursor import Fragment, Region
from copy import deepcopy

def basic_map(fie):
    fie.gate.set_active_map(fie.commander.keymaps()["Basic"])

def _insert_text(gate, pos, addition):
    properties = gate.cursor().text_properties()
    new_properties = deepcopy(gate.cursor().text_properties())
    # creates the Region object containing the text fragment
    fragments = [Fragment(addition, new_properties)]
    region = Region(fragments)
    # inserts the Region object into the target gate
    gate.insert_region(region, pos)
    
def insert_character(fie):
    string = fie.string
    if string[0:4] == "Shft":
        _insert_text(fie.gate, fie.gate.cursor().point(), string[5:])
    else:
        _insert_text(fie.gate, fie.gate.cursor().point(), string.lower())

def insert_space(fie):
    _insert_text(fie.gate, fie.gate.cursor().point(), " ")

def delete(fie):
    gate = fie.gate
    cursor = gate.cursor()
    start = cursor.start()
    end = cursor.end()
    if (end - start) > 1:
        gate.selection(start, end, remove=True)
    else:
        point = cursor.point()
        gate.selection(point-1, point, remove=True)

def insert_new_line(fie):
    _insert_text(fie.gate, fie.gate.cursor().point(), "\n")

def toggle_bold(fie):
    gate = fie.gate
    cursor = gate.cursor()
    start = cursor.start()
    end = cursor.end()
    is_bold = cursor.text_property("bold")
    if (end - start) > 0:
        selection = gate.selection(start, end, remove=True)
        for i in selection.fragments():
            i.set_text_property("bold", not is_bold)
        gate.insert_region(selection, start)
    cursor.set_text_property("bold", not is_bold)
    gate.set_active_map(gate.primary_map())                     
def toggle_italics(fie):
    gate = fie.gate
    cursor = gate.cursor()
    start = cursor.start()
    end = cursor.end()
    is_italics = cursor.text_property("italics")
    if (end - start) > 0:
        selection = gate.selection(start, end, remove=True)
        for i in selection.fragments():
            i.set_text_property("italics", not is_italics)
        gate.insert_region(selection, start)
    cursor.set_text_property("italics", not is_italics)
    gate.set_active_map(gate.primary_map())                                

def toggle_underline(fie):
    gate = fie.gate
    cursor = gate.cursor()
    start = cursor.start()
    end = cursor.end()
    is_underline = cursor.text_property("underline")
    if (end - start) > 0:
        selection = gate.selection(start, end, remove=True)
        for i in selection.fragments():
            i.set_text_property("underline", not is_underline)
        gate.insert_region(selection, start)
    cursor.set_text_property("underline", not is_underline)
    gate.set_active_map(gate.primary_map())                                

def move_point_to_click(fme):
    cursor = fme.gate.cursor()
    cursor.set_point(fme.gie.pos)

def move_mark_to_mouse_location(fme):
    cursor = fme.gate.cursor()
    cursor.activate_mark()
    cursor.set_mark(fme.gie.pos)
    
def advance_point_by_char(fie):
    cursor = fie.gate.cursor()
    pos = cursor.point() + 1
    cursor.set_point(pos)
            
def retreat_point_by_char(fie):
    cursor = fie.gate.cursor()
    pos = cursor.point() - 1
    cursor.set_point(pos)

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
    text = gate.region().text()
    cursor = gate.cursor()
    point = cursor.point()
    remaining = text[point:]
    relative_pos = _search_string_forwards(pattern, remaining)
    pos = point + relative_pos
    cursor.set_point(pos)

def _retreat_point_to_match(gate, pattern):
    text = gate.region().text()
    cursor = gate.cursor()
    point = cursor.point()
    remaining = text[:point]
    pos = _search_string_backwards(pattern, remaining)
    cursor.set_point(pos)

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
    text_length = gate.region().length()
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
    cursor.set_point(pos)
    
def move_point_end_of_line(fie):
    cursor = fie.gate.cursor()
    pos = _end_of_line(fie)
    cursor.set_point(pos)

def move_point_next_line(fie):
    # from Control.Core import my_debug; my_debug()
    gte = fie.gie.win.gte()
    cursor = fie.gate.cursor()
    point = cursor.point()
    document = gte.document()
    block = document.findBlock(point)
    sub_point = point - block.position()
    layout = block.layout()
    line = layout.lineForTextPosition(sub_point)
    layout_loc = (block.blockNumber(), line.lineNumber())
    column = gte._qtextcursor.columnNumber()
    # if column == 0:
    #     if cursor.last_point():
    #         cursor.set_point(cursor.last_point(), False)
    #         gte.update_view(fie.inter[0])
    #         column = gte._qtextcursor.columnNumber()
    #         cursor.set_point(point, False)
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
        
        cursor.set_point(target_line.textStart() + target_block.position(), False)
        if target_line.textLength() > column:
            cursor.set_point(cursor.point() + column)
        else:
            cursor.set_point(cursor.point() + target_line.textLength())
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
    column = gte._qtextcursor.columnNumber()
    if column == 0:
        if cursor.last_point():
            cursor.set_point(cursor.last_point(), False)
            gte.update_view(fie.inter[0])
            column = gte._qtextcursor.columnNumber()
            cursor.set_point(point, False)
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
        
        cursor.set_point(target_line.textStart() + target_block.position(), False)
        if target_line.textLength() > column:
            cursor.set_point(cursor.point() + column)
        else:
            cursor.set_point(cursor.point() + target_line.textLength())
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
        cursor.set_mark(point)
        cursor.activate_mark()
    elif point == mark and not cursor.is_mark_active():
        cursor.activate_mark()
    elif point == mark and cursor.is_mark_active():
        cursor.set_mark(point)
        cursor.deactivate_mark()

def kill_region(fie):
    gate = fie.gate
    cursor = gate.cursor()
    commander = fie.commander
    ring = commander.ring()
    start = cursor.start()
    end = cursor.end()
    selection = gate.selection(start, end, remove=True)
    ring.add(selection)

def kill_line(fie):
    gate = fie.gate
    cursor = gate.cursor()
    commander = fie.commander
    ring = commander.ring()
    point = cursor.point()
    end_of_line = _end_of_line(fie)
    selection = gate.selection(point, end_of_line, remove=True)
    ring.add(selection)
    _delete_text(gate, point, end_of_line)

def yank(fie):
    gate = fie.gate
    cursor = gate.cursor()
    commander = fie.commander
    ring = commander.ring()
    point = cursor.point()
    attempt = ring.get()
    gate.insert_region(attempt, point)
    gate.set_active_map(fie.commander.keymaps()["Yank"])
    
def yank_next(fie):
    gate = fie.gate
    cursor = gate.cursor()
    commander = fie.commander
    ring = commander.ring()
    point = cursor.point()
    # deletes last yank attempt
    current = ring.get()
    start_of_current = point - current.length()
    gate.selection(start_of_current, point, remove=True)
    point = cursor.point()
    # updates ring
    ring.next_index()
    # attempts next yank
    attempt = ring.get()
    gate.insert_region(attempt, point)

def yank_previous(fie):
    gate = fie.gate
    cursor = gate.cursor()
    commander = fie.commander
    ring = commander.ring()
    point = cursor.point()
    # deletes last yank attempt
    current = ring.get()
    start_of_current = point - current.length()
    gate.selection(start_of_current, point, remove=True)
    point = cursor.point()
    # updates ring
    ring.previous_index()
    attempt = ring.get()
    gate.insert_region(attempt, point)

def yank_pop(fie):
    gate = fie.gate
    gate.set_active_map(gate.primary_map())
    ring = fie.commander.ring()
    ring.remove(ring.index())

def yank_place(fie):
    gate = fie.gate
    gate.set_active_map(gate.primary_map())

def yank_cancel(fie):
    gate = fie.gate
    cursor = gate.cursor()
    commander = fie.commander
    ring = commander.ring()
    point = cursor.point()
    # deletes last yank attempt
    current = ring.get()
    start_of_current = point - len(current)
    gate.selection(start_of_current, point, remove=True)
    # resets keymap
    gate.set_active_map(gate.primary_map())

def basic_map(fie):
    fie.gate.set_active_map(fie.commander.keymaps()["Basic"])

def portal_map(fie): 
    fie.gate.set_active_map(fie.commander.keymaps()["Portal"])

def fonts_map(fie):
    fie.gate.set_active_map(fie.commander.keymaps()["Fonts"])



    



    


    
        
    
