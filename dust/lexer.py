import ply.lex as lex

# Reserved keywords
reserved = {
    'import': 'IMPORT',
    'fn': 'FN',
    'struct': 'STRUCT',
    'let': 'LET',
    'if': 'IF',
    'elif': 'ELIF',
    'else': 'ELSE',
    'while': 'WHILE',
    'for': 'FOR',
    'in': 'IN',
    'return': 'RETURN',
    'true': 'TRUE',
    'false': 'FALSE',
    'null': 'NIL'
}

# Token list (including reserved words)
tokens = [
    'ID', 'INTEGER', 'FLOAT', 'STRING',"POWER",
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MOD', 
    'EQ', 'NE', 'LT', 'GT', 'LE', 'GE',
    'AND', 'OR', 'NOT',
    'ASSIGN', 'DOT', 'COMMA', 'COLON',
    'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE',
    'LBRACKET', 'RBRACKET', 'SEMICOLON'
] + list(reserved.values())

# Operator symbols
t_POWER   = r'\*\*'
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_MOD     = r'%'
t_EQ      = r'=='
t_NE      = r'!='
t_LT      = r'<'
t_GT      = r'>'
t_LE      = r'<='
t_GE      = r'>='
t_AND     = r'&&'
t_OR      = r'\|\|'
t_NOT     = r'!'
t_ASSIGN  = r'='
t_DOT     = r'\.'
t_COMMA   = r','
t_COLON   = r':'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_LBRACE  = r'\{'
t_RBRACE  = r'\}'
t_LBRACKET= r'\['
t_RBRACKET= r'\]'
t_SEMICOLON = r';'

# Literal processing
def t_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_INTEGER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_STRING(t):
    r'\"([^\\\"]|\\.)*?\"'
    t.value = bytes(t.value[1:-1], 'utf-8').decode('unicode_escape')
    return t

# Identifier handling
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t

# Comment handling
def t_LINE_COMMENT(t):
    r'//.*'
    pass

def t_BLOCK_COMMENT(t):
    r'/\*(?s:.*?)\*/'
    pass

# Ignore whitespace (except newlines)
t_ignore = ' \t\r'

# Track newlines for error reporting
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Error handling
def t_error(t):
    print(f"Illegal character '{t.value[0]}' at line {t.lineno}")
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

# Test code
if __name__ == '__main__':
    data = '''
    let x = -3.14 + (10 * 2);
    if x > 5 {
        print("Result: ", x);
    }
    '''
    lexer.input(data)
    for tok in lexer:
        print(tok)