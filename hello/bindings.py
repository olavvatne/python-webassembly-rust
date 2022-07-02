from abc import abstractmethod
import ctypes
from typing import Any, Tuple
import wasmtime

try:
    from typing import Protocol
except ImportError:
    class Protocol: # type: ignore
        pass


def _load(ty: Any, mem: wasmtime.Memory, store: wasmtime.Storelike, base: int, offset: int) -> Any:
    ptr = (base & 0xffffffff) + offset
    if ptr + ctypes.sizeof(ty) > mem.data_len(store):
        raise IndexError('out-of-bounds store')
    raw_base = mem.data_ptr(store)
    c_ptr = ctypes.POINTER(ty)(
        ty.from_address(ctypes.addressof(raw_base.contents) + ptr)
    )
    return c_ptr[0]

def _decode_utf8(mem: wasmtime.Memory, store: wasmtime.Storelike, ptr: int, len: int) -> str:
    ptr = ptr & 0xffffffff
    len = len & 0xffffffff
    if ptr + len > mem.data_len(store):
        raise IndexError('string out of bounds')
    base = mem.data_ptr(store)
    base = ctypes.POINTER(ctypes.c_ubyte)(
        ctypes.c_ubyte.from_address(ctypes.addressof(base.contents) + ptr)
    )
    return ctypes.string_at(base, len).decode('utf-8')

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
class Say:
    instance: wasmtime.Instance
    _canonical_abi_free: wasmtime.Func
    _canonical_abi_realloc: wasmtime.Func
    _hello: wasmtime.Func
    _memory: wasmtime.Memory
    _overhead: wasmtime.Func
    def __init__(self, store: wasmtime.Store, linker: wasmtime.Linker, module: wasmtime.Module):
        self.instance = linker.instantiate(store, module)
        exports = self.instance.exports(store)
        
        canonical_abi_free = exports['canonical_abi_free']
        assert(isinstance(canonical_abi_free, wasmtime.Func))
        self._canonical_abi_free = canonical_abi_free
        
        canonical_abi_realloc = exports['canonical_abi_realloc']
        assert(isinstance(canonical_abi_realloc, wasmtime.Func))
        self._canonical_abi_realloc = canonical_abi_realloc
        
        hello = exports['hello']
        assert(isinstance(hello, wasmtime.Func))
        self._hello = hello
        
        memory = exports['memory']
        assert(isinstance(memory, wasmtime.Memory))
        self._memory = memory
        
        overhead = exports['overhead']
        assert(isinstance(overhead, wasmtime.Func))
        self._overhead = overhead
    def hello(self, caller: wasmtime.Store, name: str) -> str:
        memory = self._memory;
        realloc = self._canonical_abi_realloc
        free = self._canonical_abi_free
        ptr, len0 = _encode_utf8(name, realloc, memory, caller)
        ret = self._hello(caller, ptr, len0)
        assert(isinstance(ret, int))
        load = _load(ctypes.c_int32, memory, caller, ret, 0)
        load1 = _load(ctypes.c_int32, memory, caller, ret, 4)
        ptr2 = load
        len3 = load1
        list = _decode_utf8(memory, caller, ptr2, len3)
        free(caller, ptr2, len3, 1)
        return list
    def overhead(self, caller: wasmtime.Store, name: str) -> Tuple[str, int]:
        memory = self._memory;
        realloc = self._canonical_abi_realloc
        free = self._canonical_abi_free
        ptr, len0 = _encode_utf8(name, realloc, memory, caller)
        ret = self._overhead(caller, ptr, len0)
        assert(isinstance(ret, int))
        load = _load(ctypes.c_int32, memory, caller, ret, 0)
        load1 = _load(ctypes.c_int32, memory, caller, ret, 4)
        ptr2 = load
        len3 = load1
        list = _decode_utf8(memory, caller, ptr2, len3)
        free(caller, ptr2, len3, 1)
        load4 = _load(ctypes.c_int64, memory, caller, ret, 8)
        return (list, load4 & 0xffffffffffffffff,)
