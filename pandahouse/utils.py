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
    from pytopickle import py_to_pickle as lib

    if isinstance(s, bytes):
        in_bytes = s
    else:
        in_bytes = s.encode("utf8")
    in_len = len(in_bytes)

    lib_result = lib(in_bytes, in_len)
    return lib_result.encode("utf8")

