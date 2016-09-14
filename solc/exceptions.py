import textwrap
import codecs


def force_text(maybe_bytes):
    if isinstance(maybe_bytes, bytes):
        return codecs.decode(maybe_bytes, 'utf8')
    return maybe_bytes


DEFAULT_MESSAGE = "An error occured during execution"


class SolcError(Exception):
    message = "An error occurred during execution"

    def __init__(self, command, return_code, stdout_data, stderr_data, message=None):
        if message is not None:
            self.message = message
        self.command = command
        self.return_code = return_code
        self.stderr_data = force_text(stderr_data)
        self.stdout_data = force_text(stdout_data)

    def __str__(self):
        return textwrap.dedent(("""
        {s.message}
        > command: `{command}`
        > return code: `{s.return_code}`
        > stderr:
        {s.stdout_data}
        > stdout:
        {s.stderr_data}
        """).format(
            s=self,
            command=' '.join(self.command),
        )).strip()


class ContractsNotFound(SolcError):
    message = "No contracts found during compilation"
