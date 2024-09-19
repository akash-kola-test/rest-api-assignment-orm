class InvalidPageException(Exception):
    def __init__(self, msg):
        super().__init__(msg)
        self.msg = msg


class InvalidResourceIdException(Exception):
    def __init__(self, msg):
        super().__init__(msg)
        self.msg = msg


class ResourceNotFoundException(Exception):
    def __init__(self, msg):
        super().__init__(msg)
        self.msg = msg

class ValidationException(Exception):
    def __init__(self, msg):
        super().__init__(msg)
        self.msg = msg


class ResourceAlreadyExistsException(Exception):
    def __init__(self, msg):
        super().__init__(msg)
        self.msg = msg

