

class Bash:
    def __init__(self, bash_stmt, tokens=None):
        self.bash_stmt = bash_stmt

        if tokens == None:
            self.tokens = Bash.parse_string(self.bash_stmt)
        else:
            self.tokens = tokens 
        

    def parse_string(cmd):
        result = []
        