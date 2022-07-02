from abc import abstractmethod
import ctypes
from typing import Any, Tuple
import wasmtime

try:
    from typing import Protocol
except ImportError:
    class Protocol: # type: ignore
        pass


def _encode_utf8(val: str, realloc: wasmtime.Func, mem: wasmtime.Memory, store: wasmtime.Storelike) -> Tuple[int, int]:
    bytes = val.encode('utf8')
    ptr = realloc(store, 0, 0, 1, len(bytes))
    assert(isinstance(ptr, int))
    ptr = ptr & 0xffffffff
    if ptr + len(bytes) > mem.data_len(store):
        raise IndexError('string out of bounds')
    base = mem.data_ptr(store)
    base = ctypes.POINTER(ctypes.c_ubyte)(
        ctypes.c_ubyte.from_address(ctypes.addressof(base.contents) + ptr)
    )
    ctypes.memmove(base, bytes, len(bytes))
    return (ptr, len(bytes))
class Rosetta:
    instance: wasmtime.Instance
    _canonical_abi_realloc: wasmtime.Func
    _memory: wasmtime.Memory
    _occurrences: wasmtime.Func
    def __init__(self, store: wasmtime.Store, linker: wasmtime.Linker, module: wasmtime.Module):
        self.instance = linker.instantiate(store, module)
        exports = self.instance.exports(store)
        
        canonical_abi_realloc = exports['canonical_abi_realloc']
        assert(isinstance(canonical_abi_realloc, wasmtime.Func))
        self._canonical_abi_realloc = canonical_abi_realloc
        
        memory = exports['memory']
        assert(isinstance(memory, wasmtime.Memory))
        self._memory = memory
        
        occurrences = exports['occurrences']
        assert(isinstance(occurrences, wasmtime.Func))
        self._occurrences = occurrences
    def occurrences(self, caller: wasmtime.Store, text: str, matching: str) -> int:
        memory = self._memory;
        realloc = self._canonical_abi_realloc
        ptr, len0 = _encode_utf8(text, realloc, memory, caller)
        ptr1, len2 = _encode_utf8(matching, realloc, memory, caller)
        ret = self._occurrences(caller, ptr, len0, ptr1, len2)
        assert(isinstance(ret, int))
        return ret & 0xffffffff
