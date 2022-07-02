import os
import markdown as mdpy
from wasmtime import Engine, Store, Config, Module, Linker, WasiConfig
from md import bindings
from util import timethis


path = os.path.join("md", "target", "wasm32-wasi", "release", "md.wasm")
with open("benchmark.md", "r") as f:
    markdown_raw = f.read()


@timethis
def wasm_markdown(text):
    config = Config()
    engine = Engine(config)
    store = Store(engine)
    store.set_wasi(WasiConfig())
    module = Module.from_file(engine, path)
    linker = Linker(engine)
    linker.define_wasi()
    say = bindings.Markdown(store, linker, module)
    res = say.render(store, text)
    # print(res)


@timethis
def python_markdown(text):
    html = mdpy.markdown(text)
    # print(html)


def wasm_overhead(text):
    config = Config()
    engine = Engine(config)
    store = Store(engine)
    store.set_wasi(WasiConfig())
    module = Module.from_file(engine, path)
    linker = Linker(engine)
    linker.define_wasi()
    say = bindings.Markdown(store, linker, module)
    res = say.overhead(store, text)
    print(str(res[1] / 1000000000) + "s")


def wasm_init():
    config = Config()
    engine = Engine(config)
    store = Store(engine)
    store.set_wasi(WasiConfig())
    module = Module.from_file(engine, path)
    linker = Linker(engine)
    linker.define_wasi()
    mdb = bindings.Markdown(store, linker, module)
    return mdb, store


@timethis
def wasm_markdown_call_only(mdb, store, text):
    mdb.render(store, text)


print("\nTime markdown wasm all:")
wasm_markdown(markdown_raw)

print("\nTime markdown python all:")
python_markdown(markdown_raw)

print("\nTime markdown wasm internal:")
wasm_overhead(markdown_raw)

print("\nTime markdown wasm calls only:")
mdb, store = wasm_init()
wasm_markdown_call_only(mdb, store, markdown_raw)

print("\nTime large markdown wasm call only:")
with open("benchmark.md", "r") as f:
    temp = f.read()
markdown_raw2 = temp
for i in range(5):
    markdown_raw2 += temp
wasm_markdown_call_only(mdb, store, markdown_raw2)

print("\nTime large markdown python call only:")
python_markdown(markdown_raw2)