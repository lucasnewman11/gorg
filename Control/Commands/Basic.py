def _insert_text(gate, pos, addition):
    print("POS", pos)
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
    _insert_text(fke.gate, fke.gate_adjusted_pos, "hello")
    
def insert_character(fke):
    string = fke.string
    if string[0:4] == "Shft":
        _insert_text(fke.gate, fke.gate.cursor().point(), string[5:])
    else:
        _insert_text(fke.gate, fke.gate.cursor().point(), string.lower())

def insert_space(fke):
    _insert_text(fke.gate, fke.gate.cursor().point(), " ")

def _delete_text(gate, start, end):
    point = gate.cursor().point()
    mark = gate.cursor().mark()
    text_list = list(gate.get_raw_text())
    new_text_list = text_list[:start] + text_list[end:]
    gate.set_raw_text("".join(new_text_list))
    if end < point:
        gate.cursor().setpoint(point - (end - start))
    elif end >= point and start < point:
        gate.cursor().setpoint(start)
    if end < mark:
        gate.cursor().setmark(mark - (end - start))
    elif end >= mark and start < mark:
        gate.cursor().setmark(start)
    
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

def _advance_point_only(cursor, num):
    cursor.setpoint(cursor.point() + num)

def _advance_mark_only(cursor, num):
    cursor.setmark(cursor.mark() + num)

def _advance_point(cursor, num):
    _advance_point_only(cursor, num)
    if not cursor.is_mark_active():
        _advance_mark_only(cursor, num)

def advance_point_by_char(fke):
    cursor = fke.gate.cursor()
    _advance_point(cursor, 1)
            
def retreat_point_by_char(fke):
    cursor = fke.gate.cursor()
    _advance_point(cursor, -1)

def _search_string_forwards(pattern, string, pos):
    import re
    test_string = string[pos:]
    match = re.search(pattern, test_string)
    relative_match_pos = match.start()
    match_pos = relative_match_pos + pos
    return match_pos

def _search_string_backwards(pattern, string, pos):
    import re
    test_string = string[:pos]
    match = list(re.finditer(pattern, test_string))[-1]
    match_pos = match.start()
    return match_pos

def advance_point_by_word(fke):
    cursor = fke.gate.cursor()
    point = cursor.point()
    text = fke.gate.get_raw_text()

    distance = 0
    space = False
    pos = point+1
    while not space:
        i = False

        try:
            i = text[pos]
        except IndexError:
            space = True
        if i == " ":
            space = True
        elif i == "\n":
            space = True
        else:
            pos += 1

        distance += 1            

    _advance_point(cursor, distance)

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

    


    
        
    
