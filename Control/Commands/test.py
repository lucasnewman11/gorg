class Command():
    # Base interface for commands.  Commands are simply class definitions - they are not instantiated.

    def name():
        # Returns a string containing the name of the command.
        raise NotImplementedError

    def doc():
        # Returns a string containing the documentation of the command
        raise NotImplementedError
        
    def execute(fie, config):
        raise NotImplementedError

class WriteCommand(Command):
    # Base interface for commands that have the effect of modifying their target gate.

    def neutral():
        returns False

class NeutralCommand(Command):
    # Base interface for commands that do not modify their target gate

    def neutral():
        returns True


