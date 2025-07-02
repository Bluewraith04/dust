# Dust — A Minimal Interpreted Language

> *"Write fast, think clean, build small."*

Dust is a small interpreted programming language written in Python. It's designed to be understandable, hackable, and expressive with minimal syntax and maximum readability.

---

## Why Dust?

Dust is a toy language built for:

- Learning how interpreters and parsers work
- Experimenting with language design
- Creating small, readable programs without boilerplate
- Exploring implementation tradeoffs

---

## Features

- Easy-to-understand syntax
- Variables, functions, and conditionals
- While loops and scoping
- A working REPL with multiline support
- Simple interpreter backend in Python
- Easily extendable

---

## Installation

```bash
git clone https://github.com/Bluewraith04/dust.git
cd dust
pip install .
````
---

## Usage

Start the REPL:

```bash
dust
```

Run a script file:

```bash
dust path/to/file.dust
```

---

## Language Overview

```dust
// Hello world
print("Hello, Dust!");

// Variables
let x = 10;
let y = x + 5;

// Functions
fn add(a, b) {
    return a + b;
}

print(add(3, 4));

// Conditionals
if x > 5 {
    print("x is large");
} else {
    print("x is small");
}

// Loops
let i = 0;
while i < 5 {
    print(i);
    i = i + 1;
}
```

---

## Project Structure

```text
dust/
├── dust/             # Core interpreter code
│   ├── ast_nodes.py
│   ├── lexer.py
│   ├── parser.py
│   ├── env.py
│   ├── utils.py
│   ├── stdlib.py
│   ├── interpreter.py
│   ├── repl.py
│   └── main.py
├── README.md
└── pyproject.toml    # Build & packaging config
```


## Contributing

If you want to extend Dust, hack the parser, or build your own features, start by reading the code in the `dust/` directory. Contributions, forks, and experiments are all welcome.

---

## License

MIT License. Dust is free to use, learn from, or tear apart for your own language ideas.
