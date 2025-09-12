import ctypes
import os
import secrets
import sys

_THIS_DIR = os.path.dirname(__file__)


def _default_lib_path():
    # ожидаем, что скомпиленная библиотека лежит в c_lib/
    base = os.path.join(os.path.dirname(_THIS_DIR), "c_lib")
    if sys.platform.startswith("linux"):
        return os.path.join(base, "libcrypto.so")
    if sys.platform == "darwin":
        return os.path.join(base, "libcrypto.dylib")
    if sys.platform == "win32":
        return os.path.join(base, "crypto.dll")
    return os.path.join(base, "libcrypto.so")


_USING_C = False
_lib = None

try:
    _libpath = _default_lib_path()
    if os.path.exists(_libpath):
        _lib = ctypes.CDLL(_libpath)
        _lib.generate_key.argtypes = [ctypes.c_int]
        _lib.generate_key.restype = ctypes.c_void_p  # pointer to char
        _lib.free_key.argtypes = [ctypes.c_void_p]
        _lib.free_key.restype = None
        _USING_C = True
    else:
        # если библиотеки нет, используем Python-резерв
        _USING_C = False
except Exception:
    _USING_C = False

_CHARSET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


def generate_key(length: int) -> str:
    """
    Возвращает строковый ключ длины `length`.
    Использует нативную библиотеку, если доступна; иначе — python fallback.
    """
    if length <= 0:
        return ""

    if _USING_C and _lib is not None:
        ptr = _lib.generate_key(length)
        if not ptr:
            raise RuntimeError("C generate_key failed")
        # скопируем содержимое и освободим нативную память
        s = ctypes.cast(ptr, ctypes.c_char_p).value.decode("utf-8")
        _lib.free_key(ptr)
        return s
    else:
        # безопасный вариант на Python
        return "".join(secrets.choice(_CHARSET) for _ in range(length))


def using_c() -> bool:
    # Вернёт True если используется нативная библиотека.
    return _USING_C
