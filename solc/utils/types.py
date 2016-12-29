import sys


if sys.version_info.major == 2:
    bytes_types = (bytes, bytearray)
    text_types = (unicode,)  # NOQA
    string_types = (basestring, bytearray)  # NOQA
else:
    bytes_types = (bytes, bytearray)
    text_types = (str,)
    string_types = (bytes, str, bytearray)


def is_bytes(value):
    return isinstance(value, bytes_types)


def is_text(value):
    return isinstance(value, text_types)


def is_string(value):
    return isinstance(value, string_types)
