## Introduction

This document provides technical documentation for the Dust Interpreter, a barebones interpreter designed to execute a simplified programming language (referred to as "Dust"). It covers the core components, design principles, and current capabilities of the interpreter, aimed at developers who wish to understand, extend, or maintain the project.

## Language Overview (Dust)

Dust is a simple, dynamically-typed language with lexical scoping. Key features include:

- **Data Types:** Numbers (integers, floats), Strings, Booleans, `None` (represented by `null`).
- **Variables:** Declaration (`let`), assignment (`=`). Variables are mutable by default.
- **Control Flow:**
    - Conditional statements (`if-elif-else`).
    - Looping constructs (`while`, `for`).
    - Block scoping (`{ ... }`).
- **Functions:**
    - First-class functions with lexical scoping (closures).
    - Return statements (`return`).
- **Data Structures (Planned/Partial):**
    - Arrays (via `ArrayLiteral`, `IndexAccess`).
    - Structs (user-defined composite types via `StructDecl`, `StructLiteral`, `MemberAccess`).
- **Built-in Functions:** `print`.
- **Operators:** Standard arithmetic, comparison, and logical operators.
- **Modularity (Planned):** `import` statements.

## Architecture

The Dust Interpreter follows a classic interpreter design pattern, composed of distinct phases:

1. **Lexical Analysis**:  Converts source code into a stream of tokens.
2. **Syntactic Analysis (Parsing)**: (Future) Consumes tokens to build an Abstract Syntax Tree (AST).
3. **Semantic Analysis / Type Checking**: (Conceptual/Future) Analyzes the AST for meaning and type correctness. Currently, some basic runtime type checks exist, but a dedicated pass is planned.
4. **Interpretation (Execution)**: (Future) Traverses the AST and executes the program's instructions.

The core components are `AST Nodes`, `Symbol Table / Environment Management`, and the `Interpreter` itself.

### Abstract Syntax Tree (AST Nodes)

The AST is the intermediate representation of the Dust program after parsing. Each node in the AST represents a construct in the Dust language (e.g., a variable declaration, a binary operation, a function call).

- **Location:** Defined in `ast_.py`
- **Design:** Uses Python's `dataclass` for concise and readable node definitions. Each node has attributes corresponding to its syntactic components.
- **Key Categories:**
    - **Expressions (`Expr`):** Nodes that produce a value (e.g., `Literal`, `Identifier`, `BinaryOp`, `FunctionCall`).
    - **Statements (`Statement`):** Nodes that perform an action but don't necessarily produce a value (e.g., `VariableDecl`, `Assignment`, `IfStmt`).
    - **Declarations:** Top-level constructs that define entities (`FunctionDecl`, `StructDecl`).
    - **Top-Level (`Program`):** The root of the AST, containing all declarations and statements.

**Relevant AST Nodes (Current State):**

- `BinaryOp(op: str, left: Expr, right: Expr)`: Arithmetic, comparison, logical operations.
- `UnaryOp(op: str, expr: Expr)`: Unary minus, logical NOT.
- `Literal(value: int | float | str | bool | None)`: Represents constant values.
- `Identifier(name: str)`: Represents variable names or function names.
- `FunctionCall(func: Expr | None, args: List[Expr])`: Invokes a function.
- `MemberAccess(obj: Expr | None, field: str)`: Accesses fields of structs (e.g., `obj.field`).
- `IndexAccess(array: Expr | None, index: Expr)`: Accesses elements of arrays (e.g., `array[index]`).
- `StructLiteral(type_name: str, fields: List[FieldAssign])`: Creates an instance of a struct.
- `FieldAssign(name: str, value: Expr)`: Represents a field assignment within a `StructLiteral`.
- `ArrayLiteral(elements: List[Expr])`: Creates an array.
- `Import(path: str)`: (Planned) Imports modules.
- `FunctionDecl(name: str, parameters: List[str], body: Block)`: Defines a function.
- `StructDecl(name: str, fields: List[str])`: Defines a new struct type.
- `VariableDecl(name: str, expr: Expr)`: Declares and initializes a variable.
- `Assignment(target: AssignTarget, expr: Expr)`: Assigns a new value to a variable, struct field, or array element.
- `IfStmt(branches: List[tuple[Expr, Block]], else_block: Optional[Block])`: Conditional branching.
- `WhileStmt(condition: Expr, body: Block)`: While loop.
- `ForStmt(var: str, iterable: Expr, body: Block)`: For-each loop.
- `ReturnStmt(value: Optional[Expr])`: Returns a value from a function.
- `ExprStmt(expr: Expr)`: A statement consisting solely of an expression.
- `Block(statements: List[Statement])`: A sequence of statements, defining a new lexical scope.
- `Program(declarations: List[DeclarationOrStatement])`: The root AST node.

### Symbol Table and Environment Management

The interpreter uses a robust symbol table system to manage variables, functions, and other defined entities, along with their associated metadata and scope.

- **Location:** Defined in `symbol_table.py`.
- **Key Classes:**
    - `Symbol`: A `dataclass` representing an entry in the symbol table. It stores:
        - `name` (str): The identifier's name.
        - `kind` (str): What the symbol represents (e.g., 'variable', 'function', 'parameter', 'struct_type', 'builtin').
        - `type_info` (Optional[str]): Conceptual type information (e.g., 'number', 'string', 'callable'). This is currently a string and is targeted for enhancement into a formal `LangType` object.
        - `value` (Any): The actual runtime value associated with the symbol (e.g., `10`, a Python function object for interpreted functions).
        - `is_mutable` (bool): Indicates if the symbol's `value` can be reassigned.
    - `Scope`: Represents a single lexical scope. It uses a Python dictionary (`self.symbols`) as a hash table for efficient O(1) average-case lookup, definition, and resolution of `Symbol` objects within that specific scope. Each scope has a `parent` reference to its enclosing lexical scope.
    - `Environment`: Manages the runtime stack of active scopes.
        - Each `Environment` instance holds a reference to its `current_scope` (a `Scope` object) and a `parent_env` reference to the `Environment` that initiated the current context (e.g., the calling function's environment or the outer block's environment).
        - Methods:
            - `define(symbol: Symbol)`: Adds a new symbol to the `current_scope`.
            - `assign(name: str, value: Any)`: Finds the original defining `Scope` for a given `name` and updates the `value` of the `Symbol` object there, respecting `is_mutable`.
            - `lookup(name: str) -> Symbol`: Traverses the `parent_env` chain to find the `Symbol` for a given `name`, returning `null_symbol` if not found.
- **Lexical Scoping (Closures):** The `Environment` and `Scope` design implements lexical scoping. Functions capture the `Environment` they were defined in, allowing them to access variables from their enclosing lexical scopes even when called from a different context.

### Interpreter Core

The `Interpreter` class is responsible for traversing the AST and executing the program logic.

- **Location:** `interpreter.py`.
- **Main Method:** `eval(node)`: A generic method that dispatches to specific `eval_NodeType` methods based on the class of the AST node. This dynamic dispatch makes the interpreter highly extensible.
- **State:**
    - `global_env`: The root `Environment` for the program.
    - `env`: The currently active `Environment` (representing the top of the call stack). This is dynamically changed as the interpreter enters and exits blocks or function calls.
- **Scope Management in `eval_` methods:**
    - `eval_Block`: Creates a new `Environment` for the block, temporarily setting `self.env` to it, and restores the previous `self.env` upon exit (using `try...finally`).
    - `eval_FunctionDecl`: Captures the `self.env` at the time of definition (the "closure"). When the function is called, a _new_ `Environment` is created with the captured `self.env` as its `parent_env`.
- **Value Handling:**
    - `eval_Literal`: Returns the raw Python value directly.
    - `eval_Identifier`: Looks up the `Symbol` in the environment and returns its `value` attribute.
    - Other `eval_` methods (e.g., `BinaryOp`, `FunctionCall` arguments) expect raw Python values from their sub-expressions.
    - `eval_VariableDecl` and `eval_FunctionDecl` wrap values in `Symbol` objects when defining them.
- **Error Handling:** Uses `RuntimeError` for various semantic and execution errors (e.g., undefined variables, redefinition, type mismatches, out-of-bounds access). `ReturnException` is a special internal exception for function returns.

## Future Enhancements

Based on the current AST and planned features, the following enhancements are envisioned:

- **Formal Type System:**
    - Introduce `LangType` classes (e.g., `NumberType`, `StringType`, `ArrayType`, `StructType`) to represent Dust's types internally.
    - Update `Symbol.type_info` to `Symbol.type: LangType`.
    - Implement a separate **Semantic Analysis / Type Checker pass** before interpretation. This pass will:
        - Infer or validate types for all expressions and declarations.
        - Annotate AST nodes with their inferred types.
        - Perform static type checking, catching type errors before runtime.
        - This will reduce the number of `isinstance` checks in `eval_` methods and improve error messages.
- **Traits / Interfaces:** Define common behaviors (e.g., `Addable`, `Indexable`) that types can implement, enabling more robust operator overloading and polymorphism.
- **Module System:** Fully implement `eval_Import` to support loading and linking code from multiple files, including handling namespaces and exports.
- **Error Reporting:** Enhance error messages to include line numbers, column numbers, and more context for easier debugging.
- **Standard Library:** Expand built-in functions beyond `print`.
- **Debugging Tools:** Implement features like breakpoints or step-by-step execution.
- **Object-Oriented Features:** Classes, inheritance

##  Contributing

Contributions are welcome! If you're interested in helping extend the Dust Interpreter, please familiarize yourself with the current codebase and the planned enhancements. Feel free to open issues or pull requests.

---
