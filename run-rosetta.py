import os
from wasmtime import Engine, Store, Config, Module, Linker, WasiConfig
from rosetta import bindings
from util import timethis


path = os.path.join("rosetta", "target", "wasm32-wasi", "release", "rosetta.wasm")
text = "the three truths"
matching = "th"


# for i in range(2):
#     text += text


@timethis
def wasm_rosetta():
    config = Config()
    engine = Engine(config)
    store = Store(engine)
    store.set_wasi(WasiConfig())
    module = Module.from_file(engine, path)
    linker = Linker(engine)
    linker.define_wasi()
    say = bindings.Rosetta(store, linker, module)
    res = say.occurrences(store, text, matching)
    print(res)


def wasm_init():
    config = Config()
    engine = Engine(config)
    store = Store(engine)
    store.set_wasi(WasiConfig())
    module = Module.from_file(engine, path)
    linker = Linker(engine)
    linker.define_wasi()
    say = bindings.Rosetta(store, linker, module)
    return say, store


@timethis
def wasm_rosetta_call_only(mdb, store, text, matching):
    print(mdb.occurrences(store, text, matching))


@timethis
def python_rosetta():
    res = text.count(matching)
    print(res)


print("\nTime rosetta wasm all:")
wasm_rosetta()

print("\nTime rosetta python:")
python_rosetta()

print("\nTime rosetta wasm only calls:")
mdb, store = wasm_init()
wasm_rosetta_call_only(mdb, store, text, matching)