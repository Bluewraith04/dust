from env import Symbol, null
from typing import Any

def wrap(value, is_mutable=True) -> Symbol:
    return Symbol(value, '', is_mutable=is_mutable) if not isinstance(value, Symbol) else value

def unwrap(value):
    return value.value if isinstance(value, Symbol) else value

def to_symbol(*args: Symbol | Any) -> list[Symbol]:
    out = [Symbol(arg) if not isinstance(arg, Symbol) else arg for arg in args]
    return out

def binary_op(op, left, right):
    # Ensure that operands are raw values, not Symbols, for operations.
    # eval_Identifier already returns values, so this should be fine.
    left = unwrap(left)
    right = unwrap(right)
    
    # Using match case for clear operator handling
    match op:
        case '+': return left + right
        case '-': return left - right
        case '*': return left * right
        case '/':
            if right == 0:
                raise ZeroDivisionError("Division by zero")
            return left / right
        case '%': return left % right
        case '**': return left ** right
        case '==': return left == right
        case '!=': return left != right
        case '<': return left < right
        case '<=': return left <= right
        case '>': return left > right
        case '>=': return left >= right
        case '&&': return left and right
        case '||': return left or right
        case _: raise RuntimeError(f"Unknown binary operator '{op}'")