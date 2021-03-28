class EQLException(Exception):
    """A syntax error with the EQL match language"""
    message = ''
    offset = 0
    def __init__(self, equation, token):
        pointer = "^".rjust(token.location + self.offset + 1)
        message = self.message.rjust(len(self.message) // 2 + token.location)
        m = f"\n{equation}\n{pointer}\n{message}"
        super().__init__(m)

class MissingParen(Exception):
    def __init__(self, equation, token):
        msg = f"\n{equation}\n{'^'*token.location}\nThere should be a ( somewhere around here."
        super().__init__(msg)

class MissingValue(EQLException):
    message = 'There should be a value here.'
    offset = 1

class MissingValueAfterSpace(EQLException):
    message = 'There should be a value here, or you need to move the operator after the space.'

class MissingOp(EQLException):
    message = 'There should be an operator here.'
