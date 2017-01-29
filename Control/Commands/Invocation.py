def invoke_command(fke):
    gte.parent().parent().getminibuffer().insert("M-x")
    import inspect
    import Control.Commands
    list_of_commands = []
    for i in inspect.getmembers(Control.Commands):
        if inspect.isfunction(i[1]):
            list_of_commands.append(i[0])
    compl = Completor(list_of_commands)
    print(compl.get_remaining_string())
    compl.new_char("he")
    print(compl.get_remaining_string())

    
class Completor():

    def __init__(self, list_of_strings):

        self._list_of_strings = list_of_strings # the list of strings upon which completion is to run
        self._subm = "" # string of characters currently submitted so far
        self._subm_re = False # regular expression of current submission, used in matching, initialized as empty
        self._remaining_list = [] # the subset of the list of strings which can still be matched by the current submission

        self._create_subm_re()

    def _create_subm_re(self):
        import re
        # creates the regex object from the current submission
        self._subm_re = re.compile(self._subm)
        
    def new_char(self, char):
        # augments the current submission with a new character, to be used as more characters are typed and the search is narrowed
        self._subm += char
        self._create_subm_re()

    def _re_match(self, targ):
        # tries to match a specific target string with the regex of the current submission, returns a bool
        if self._subm_re.match(targ):
            return True
        else:
            return False

    def _update_remaining_list(self):
        self._remaining_list = []
        for i in self._list_of_strings:
            if self._re_match(i):
                self._remaining_list.append(i)
        return self._remaining_list

    def get_remaining_list(self):
        self._update_remaining_list()
        return self._remaining_list

    def get_remaining_string(self):
        self._update_remaining_list()
        return "|".join(self._remaining_list)
                
            
        

        

    
