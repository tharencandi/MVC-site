
class Sanitizer:
    def __init__(self, char_dict=None, replace=False):
        if not replace_char_dict:
            self.char_dict= {
                    "<": "&#x3C;", 
                    ">": "&#x3E;",
                    "/": ,
                    ";": ,
                    "\'": , 
                    "\"": ,
                    "\\": , 
                    "&": ,
                    "`": }
        else:
            self.char_black_list = char_black_list

        self.replace = replace

    def block(self, string):
        if not string:
            return None

        for char in string:
            if char in self.char_black_list:
                return None

        return string

    def replace_bad_chars(self, string):
        for 
