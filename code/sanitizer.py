import re

class Sanitizer:
    white_list_re = re.compile("[\w]*")

    black_list = re.compile("(javascript|script|'|\")+", flags=re.IGNORECASE)

    html_escapes = {"<": "&lt;", ">": "&gt;"}    

    def __init__(self, replace=None, custom_black_list=None, custom_white_list=None):
        if not replace or not isinstance(replace, dict):
            self.replace = dict()
        else:
            self.replace = replace

        if custom_black_list:
            self.black_list_re = re.compile(custom_black_list, flags=re.IGNORECASE)
        else:
            self.black_list_re = Sanitizer.black_list

        if custom_white_list:
            self.white_list_re = re.compile(custom_white_list, flags=re.IGNORECASE)
        else:
            self.white_list_re = Sanitizer.white_list_re

        


    def only_white_list(self, string):
        if not string:
            return None
        if not self.white_list_re.fullmatch(string):
            return False
        return True
    
    def contains_black_list(self, string):
        if not string:
            return None
        if self.black_list_re.match(string):
            return True
        else:
            return False
    
    def sanitize(self, string, only_alpha_num=False):
        return string
        if not string:
            return None
        if self.contains_black_list(string):
            return None

        if only_alpha_num:
            if not self.only_white_list(string):
                return None

        for k in Sanitizer.html_escapes:
            string = string.replace(k, Sanitizer.html_escapes[k])

        for k in self.replace:
            string = string.replace(k, self.replace[k])

        return string


