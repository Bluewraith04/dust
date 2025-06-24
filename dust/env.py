# ======== Environment ========
# Handles values, and context specific behavior

from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class Symbol:
    value: Any
    kind: str
    is_mutable: bool = True
    
null = Symbol(
    None,
    'null',
    False
)

    

class Environment:
    def __init__(self, parent: Optional['Environment']) -> None:
        self.symbols: dict[str, Symbol] = {}
        self.parent = parent
        
    def define(self, name: str, symbol: Symbol, redefine=False) -> None:
        if name in self.symbols and not redefine:
            raise RuntimeError(f"Attempted double definition of variable '{name}'")
        self.symbols[name] = symbol
        
    def lookup(self, name: str) -> Optional['Environment']:
        if name in self.symbols:
            return self
        if self.parent:
            return self.parent.lookup(name)
        else:
            return None
        
    def has(self, name: str):
        return self.lookup(name) is not None
    
    def assign(self, name, value):
        env = self.lookup(name)
        if env:
            obj = env.symbols[name]
            if obj.is_mutable:
                obj.value = value
            else:
                raise RuntimeError(f"Attempted assignment to immutable object of kind '{obj.kind}'")
        else:
            raise RuntimeError(f"Attempted assignment to undefined variable '{name}'")
            
    def get(self, name):
        env = self.lookup(name)
        if env:
            obj = env.symbols[name]
            return obj.value
        else:
            raise RuntimeError(f"Undefined variable '{name}'")
    
    def ref(self, name):
        env = self.lookup(name)
        if env:
            obj = env.symbols[name]
            return obj
        else:
            raise RuntimeError(f"Undefined variable '{name}'")
    