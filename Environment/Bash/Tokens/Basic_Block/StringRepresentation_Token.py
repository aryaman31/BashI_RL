from Environment.Bash.Tokens.Token import Token

class StringRepresentation_Token(Token):
    def __init__(self, string):
        super().__init__()
        self.__string = string 
    
    def value(self):
        return self.__string
    
    def set_value(self, string):
        self.__string = string 

    def type(self):
        return f"String Representation Token"

    def category(self):
        return Token.Category.BASIC_BLOCK

    def __str__(self) -> str:
        return self.__string

    def is_string_rep(s:str):
        return True

    def parse(s:str):
        return StringRepresentation_Token()