from antlr4.error.ErrorListener import ErrorListener

class CErrorListener(ErrorListener):

    class SyntaxError(Exception):
        
        def __init__(self, line, pos, message):
            super().__init__("\033[On line: {}:{} {}\033[0m".format(line, pos, message))

    def __init__(self):
        super().__init__()

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        raise self.SyntaxError(line, column, msg)