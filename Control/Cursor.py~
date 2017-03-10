class GateCursor():

    def __init__(self, gate):
        self._gate = gate
        self._point = 0
        self._mark = 0
        self._start = 0
        self._end = 0
        self._selection = {}
        self._ring = KillRing()
        self._mark_active = False

    def point(self):
        return self._point

    def mark(self):
        return self._mark

    def start(self):
        return self._start

    def end(self):
        return self._end

    def ring(self):
        return self._ring
        
    def setpoint(self, pos):
        raw_text = self._gate.get_raw_text()
        if pos < 0:
            self._point = 0
        elif pos > len(raw_text):
            self._point = len(raw_text)
        else:
            self._point = pos

    def setmark(self, pos):
        raw_text = self._gate.get_raw_text()
        if pos < 0:
            self._mark = 0
        elif pos > len(raw_text):
            self._mark = len(raw_text)
        else:
            self._mark = pos

    def is_mark_active(self):
        return self._mark_active

    def activate_mark(self):
        self._mark_active = True

    def deactivate_mark(self):
        self._mark_active = False

    def update_selection(self):
        self._start = min(self._point, self._mark)
        self._end = max(self._point, self._mark)

        raw_text = self._gate.get_raw_text()

        if self._point < self._mark and self.is_mark_active():
            self._selection = raw_text[self._point:self._mark]
        elif self._point > self._mark and self.is_mark_active():
            self._selection = raw_text[self._mark:self._point]
        else:
            self._selection = ''

    def selection(self):
        return self._selection

    def get_substring(self, start, end):
        raw_text = self._gate.get_raw_text()
        return raw_text[start:end]

class KillRing():

    def __init__(self):
        self._members = []
        self._index = 0

    def add(self, new):
        self._members.append(new)

    def index(self):
        return self._index

    def get(self):
        return self._members[self._index]

    def next_index(self):
        if self._index > 0:
            self._index -= 1
        else:
            self._index = len(self._members)-1

    def previous_index(self):
        if self._index < len(self._members)-1:
            self._index += 1
        else:
            self._index = 0

    def remove(self, index):
        del self._members[index]
    
