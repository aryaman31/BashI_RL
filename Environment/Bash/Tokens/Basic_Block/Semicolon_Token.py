from Environment.Bash.Tokens.Token import Token 

class Semicolon_Token(Token):
    def __init__(self):
        super().__init__()
    
    def value(self):
        return ';'

    def type(self):
        return f"Semi-colon Token"

    def category(self):
        return Token.Category.BASIC_BLOCK

    def __str__(self) -> str:
        return ";"

    def is_semicolon(s:str):
        return s == ';'

    def parse(s:str):
        assert(Semicolon_Token.is_semicolon(s))
        return Semicolon_Token()
