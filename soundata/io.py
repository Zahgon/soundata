import functools
import io
from typing import BinaryIO, Callable, Optional, TextIO, TypeVar, Union
T = TypeVar('T')

def coerce_to_string_io(func: Callable[[TextIO], T]) -> Callable[[Optional[Union[str, TextIO]]], Optional[T]]:
    raise NotImplementedError()

def coerce_to_bytes_io(func: Callable[[BinaryIO], T]) -> Callable[[Optional[Union[str, BinaryIO]]], Optional[T]]:
    raise NotImplementedError()