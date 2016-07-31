class SolcError(Exception):
    pass


class CompileError(Exception):
    pass


class ContractsNotFound(Exception):
    """No contracts was found in the target folder."""
