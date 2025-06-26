from ast_nodes import *
from typing import Any, List, Tuple, Callable
from env import Symbol, Environment, null, to_symbol

class ReturnException(Exception):
    """Exception raised for return statements in function evaluation."""
    def __init__(self, value: Any):
        self.value = value


class Interpreter:
    """
    The main interpreter class responsible for evaluating the Abstract Syntax Tree (AST).
    """
    def __init__(self):
        # Initialize the global environment
        self.global_env = Environment()
        self.env = self.global_env # The current active environment
        
    def eval(self, node: Any) -> Any:
        """
        Generic evaluation method that dispatches to specific eval_ methods
        based on the AST node's class name.
        """
        # Using hasattr and getattr for dynamic method dispatch is standard and maintainable
        # as it avoids long if/elif chains.
        method_name = 'eval_' + node.__class__.__name__
        if not hasattr(self, method_name):
            raise NotImplementedError(f"Evaluation method '{method_name}' not implemented for AST node type {node.__class__.__name__}")
        return getattr(self, method_name)(node)
    
    # Expressions
    def eval_BinaryOp(self, node: BinaryOp) -> Any:
        """Evaluates a binary operation (e.g., +, -, ==)."""
        left = self.eval(node.left)
        right = self.eval(node.right)
        # Ensure that operands are raw values, not Symbols, for operations.
        # eval_Identifier already returns values, so this should be fine.
        if isinstance(left, Symbol): left = left.value
        if isinstance(right, Symbol): right = right.value

        # Using match case for clear operator handling
        match node.op:
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
            case _: raise RuntimeError(f"Unknown binary operator '{node.op}'")

    def eval_UnaryOp(self, node: UnaryOp) -> Any:
        """Evaluates a unary operation (e.g., -, !)."""
        operand = self.eval(node.expr)
        if isinstance(operand, Symbol): operand = operand.value

        match node.op:
            case '-': 
                if not isinstance(operand, (int, float)):
                    raise RuntimeError(f"Unsupported unary operator '-' for type {type(operand).__name__}")
                return -operand
            case '!': return not bool(operand)
            case _: raise RuntimeError(f"Unknown unary operator '{node.op}'")
    
    def eval_Literal(self, node: Literal):
        return node.value
    
    def eval_Identifier(self, node: Any) -> Any:
        """
        Evaluates an identifier (variable reference).
        Looks up the symbol in the environment and returns its stored value.
        """
        symbol = self.env.ref(node.name)
        if symbol is null:
            raise RuntimeError(f"Undefined variable '{node.name}'")
        return symbol # Return the actual value stored within the Symbol
    
    def eval_FunctionCall(self, node: FunctionCall) -> Any:
        """Evaluates a function call."""
        # This evaluates the function expression; this should yield a callable (from a Symbol's value)
        func_callable: Callable = self.eval(node.func)
        
        if not callable(func_callable):
            # If the node.func was an identifier, it might have returned a non-callable symbol's value
            raise RuntimeError(f"'{node.func.name}' is not a callable function.")
        
        # This evaluates arguments, ensuring they are raw values not ast nodes
        args = [self.eval(arg) for arg in node.args]
        
        try:
            return func_callable(*args)
        except ReturnException as e:
            # This handles internal returns from interpreted functions
            return e.value
        except Exception as e:
            # This catches all other potential errors during function execution
            raise RuntimeError(f"Error during function call to '{getattr(node.func, 'name', 'anonymous_function')}': {e}")
        
    def eval_MemeberAccess(self, node: MemberAccess) -> Any:
        obj: Symbol | dict = self.eval(node.obj)
        if isinstance(obj, Symbol): return obj.value[node.field]
        return obj[node.field]
    
    def eval_IndexAccess(self, node: IndexAccess) -> Any:
        array = self.eval(node.array)
        index = self.eval(node.index)
        if isinstance(array, Symbol): return array.value[index]
        return array[index]
    
    def eval_ArrayLiteral(self, node: ArrayLiteral) -> Any:
        elements = [self.eval(expr) for expr in node.elements]
        return to_symbol(*elements)
    
    def eval_StructLiteral(self, node: Any) -> Any:
        struct_symbol = self.env.ref(node.type_name)
        if struct_symbol is null or struct_symbol.kind != "struct_type":
            raise RuntimeError(f"Undefined struct type '{node.type_name}'")
        fields = struct_symbol.value
        instance = {'type_name': node.type_name}

        assigned_fields = set()

        for field_assign in node.fields:
            if field_assign.name not in fields:
                raise RuntimeError(f"Struct type '{node.type_name}' has no field '{field_assign.name}'")
            elif field_assign.name in assigned_fields:
                raise RuntimeError(f"Attempted multiple assignments to field '{field_assign.name}'")
            field_name, field_val = self.eval(field_assign)
            instance[field_name] = field_val
            assigned_fields.add(field_assign.name)
            
        if len(assigned_fields) != len(fields):
            missing_fields = set(fields) - assigned_fields
            raise RuntimeError(f"Missing required fields for struct type '{node.type_name}': {', '.join(missing_fields)}")
        
        return Symbol(instance)
    
    def eval_FieldAssign(self, node: FieldAssign) -> Any:
        return node.name, Symbol(self.eval(node.value))
    