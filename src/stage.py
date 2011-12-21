class Stage(object):
    # Private Variables:
    # These are the function names that are reserved by the runtime.
    _reservedFuns = ['input', 'type_error', 'create_class', 'create_object',
                     'is_class', 'get_function', 'get_receiver',
                     'is_bound_method', 'is_unbound_method']
    _stageInput = None

    # Public Methods:
    def setInput(self, stage_input):
        """Sets the input to the stage and prepares the class for the executing
           the do() method.
        """
        self._stageInput = stage_input

    def do(self):
        """Processes the stageInput. If the derived class is the parser, it
           should parse the input. If it's a flattener, it should flatten the
           input. The result is then returned.
        """
        # visit() is a method in the ASTVisitor class. Perhaps these classes
        # should be merged?
        return self.visit(self._stageInput)

    # Private Methods:
    def _genName(self, prefix):
        """Generate a name starting with prefix and a number from 0 to 1."""
        counter = 0
        while True:
            yield prefix + str(counter)
            counter += 1

class AbstractMethod(Exception):
    def __init__(self, msg):
        self.msg = msg
    def __str__(self):
        return repr(self.msg)
