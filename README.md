# Python -> WebAssembly -> Rust
Experiments with using code written in Rust run from Python via WebAssembly/WASI/Wasm.

Note that the wit-bindgen is very new and its api might change.

## Getting Started
Requires having Rust and Python installed on your system.

```bash
python -m venv .venv
. .venv/Script/activate
pip install -r requirements.txt

cargo install cargo-wasi
cargo wasi --version
cargo install --git https://github.com/bytecodealliance/wit-bindgen --rev  a4a138b wit-bindgen-cli
```

## Running experiments

### Hello experiment

```bash
cd hello
cargo wasi build --release
wit-bindgen host wasmtime-py --import wits/say.wit
cd ..
python run-hello.py
```

### Markdown experiment
```bash
cd md
cargo wasi build --release
wit-bindgen host wasmtime-py --import wits/markdown.wit
cd ..
python run-markdown.py
```

### Rosetta experiment
```bash
cd rosetta
cargo wasi build --release
wit-bindgen host wasmtime-py --import wits/rosetta.wit
cd ..
python run-rosetta.py
```

### Wasi-Alg experiment
```bash
cd wasi-alg
cargo wasi build --release
mv target/wasm32-wasi/release/wasi_alg.wasm ../wasi_alg.wasm
cd ..
python run-alg.py
```

## Create a wasi thingy with bindings

Create a new library with cargo
```
cargo new thingy --lib
cd thingy
```

Modify `Cargo.toml`:
```toml
[package]
name = "thingy"
version = "0.1.0"
edition = "2021"

[lib]
crate-type = ["cdylib"]

[dependencies]
wit-bindgen-guest-rust = { git = "https://github.com/bytecodealliance/wit-bindgen" }
```

Create an WebAssembly Interface Types file at `wits/thingy.wit`:
```
run: func(input: string) -> string
```

implement the run function in `src/lib.rs`:
```rust
wit_bindgen_guest_rust::export!("wits/thingy.wit");

struct Thingy;

impl thingy::Thingy for Thingy {
    fn run(input: String) -> String {
        input
    }
}
```
Create a release:
```
cargo wasi build --release
```
This produces a `thingy.wasm` file somewhere inside the target folder.

Then make the python bindings with the wit-bindgen CLI:
```
wit-bindgen host wasmtime-py --import wits/thingy.wit
```

This produces a bindings.py file. Add a `__init__.py` file in the root, so bindings.py can be imported. Or move it.


To use thingy.wasm from python first create a python file `run-thingy.py` and add the following:
```python
from wasmtime import Engine, Store, Config, Module, Linker, WasiConfig
from thingy import bindings

path = os.path.join("thingy", "target", "wasm32-wasi", "release", "thingy.wasm")
text = "some text"

config = Config()
engine = Engine(config)
store = Store(engine)
store.set_wasi(WasiConfig())
module = Module.from_file(engine, path)
linker = Linker(engine)
linker.define_wasi()
thingy = bindings.Thingy(store, linker, module)
return_string = thingy.run(store, text)
```

