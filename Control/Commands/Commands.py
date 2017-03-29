class Command():
    # Base interface for commands.  Commands are simply class definitions - they are not instantiated.

    @classmethod
    def name(cls):
        # Returns a string containing the name of the command.
        return cls.__name__

    @classmethod
    def doc(cls):
        # Returns a string containing the documentation of the command.
        return cls.__doc__

    def neutral():
        raise NotImplementedError
        
    def execute(fie, config):
        raise NotImplementedError

class WriteCommand(Command):
    # Base interface for commands that modify the fragments of their target gate.
    def neutral():
        return False

class NeutralCommand(Command):
    # Base interface for commands that do not modify the fragments of their target gate

    def neutral():
        return True
