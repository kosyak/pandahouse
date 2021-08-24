import ctypes
import re
import json
import codecs
import ast
from typing import Union

SPECIAL_CHARS = {
    '\b': '\\b',
    '\f': '\\f',
    '\r': '\\r',
    '\n': '\\n',
    '\t': '\\t',
    '\0': '\\0',
    '\\': '\\\\',
    "'": "\\'"
}


def escape(value, quote='`'):
    if not isinstance(value, (str, bytes)):
        return value
    value = ''.join(SPECIAL_CHARS.get(c, c) for c in value)
    if quote == '`':
        return '`{}`'.format(value)
    elif quote == '\'':
        return '\'{}\''.format(value)
    else:
        return value


ESCAPE_SEQUENCE_RE = re.compile(r'''
    ( \\U........      # 8-digit hex escapes
    | \\u....          # 4-digit hex escapes
    | \\x..            # 2-digit hex escapes
    | \\[0-7]{1,3}     # Octal escapes
    | \\N\{[^}]+\}     # Unicode characters by name
    | \\[\\'"abfnrtv]  # Single-character escapes
    )''', re.UNICODE | re.VERBOSE)


def _decode_match(match):
    return codecs.decode(match.group(0), 'unicode-escape')


def decode_escapes(s):
    return ESCAPE_SEQUENCE_RE.sub(_decode_match, s)


def decode_array(clickhouse_array):
    return py_to_pickle(clickhouse_array)
    # return ast.literal_eval(clickhouse_array)


def py_to_pickle(s: Union[str, bytes]) -> bytes:
    if isinstance(s, bytes):
        in_bytes = s
    else:
        in_bytes = s.encode("utf8")
    in_ = ctypes.create_string_buffer(in_bytes)
    in_len = len(in_bytes)
    out_len = in_len + 1000  # should always be enough (some buffer len + len of literal Python code)
    out_ = ctypes.create_string_buffer(out_len)

    lib = ctypes.CDLL("pytopickle")
    lib.py_to_pickle.argtypes = (ctypes.c_char_p, ctypes.c_size_t, ctypes.c_char_p, ctypes.c_size_t)
    lib.py_to_pickle.restype = ctypes.c_int

    res = lib.py_to_pickle(in_, in_len, out_, out_len)
    assert res == 0, "there was some error in %r" % in_bytes
    return out_.raw
