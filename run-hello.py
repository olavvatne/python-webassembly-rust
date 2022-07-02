import os
from wasmtime import Engine, Store, Config, Module, Linker, WasiConfig
from hello import bindings
from util import timethis


path = os.path.join("hello", "target", "wasm32-wasi", "release", "hello.wasm")
name = "Wasm"


@timethis
def wasm_hello():
    config = Config()
    engine = Engine(config)
    store = Store(engine)
    store.set_wasi(WasiConfig())
    module = Module.from_file(engine, path)
    linker = Linker(engine)
    linker.define_wasi()
    say = bindings.Say(store, linker, module)
    res = say.hello(store, name)
    print(res)


@timethis
def hello():
    print("hello " + name)


print("\nTime hello wasm:")
wasm_hello()
print("\nTime hello python:")
hello()
