import re
import ply.lex as lex

texto = """
/* factorial.p
-- 2023-03-20 
-- by jcr
*/

int i;

// Função que calcula o factorial dum número n
function fact(n){
  int res = 1;
  while res > 1 {
    res = res * n;
    res = res - 1;
  }
}

// Programa principal
program myFact{
  for i in [1..10]{
    print(i, fact(i));
  }
}


/* max.p: calcula o maior inteiro duma lista desordenada
-- 2023-03-20 
-- by jcr
*/

int i = 10, a[10] = {1,2,3,4,5,6,7,8,9,10};

// Programa principal
program myMax{
  int max = a[0];
  for i in [1..9]{
    if max < a[i] {
      max = a[i];
    }
  }
  print(max);
}
"""

tokens = (
  'FUNCTIONKW',
  'PROGRAMKW',
  'FUNCTION',
  'PROGRAM',
  'DOT',
  'COLON',
  'AP',
  'FP',
  'APR',
  'FPR',
  'AC',
  'FC',
  'MOREEQUAL',
  'MORE',
  'LESSEQUAL',
  'LESS',
  'NUMBER',
  'WHILE',
  'IF',
  'ELSE',
  'FOR',
  'IN',
  'EQUALS',
  'MULTIPLY',
  'DIVIDE',
  'PLUS',
  'MINUS',
  'COMMA',
  'DCOMMA',
  'VARIABLE',
  'INT',
  'NEWLINE',
  'MLC_OPEN',
  'MLC_CLOSE',
  'SLC',
  'ALL'
)

states = (
    ('multilinecomment', 'exclusive'),
    ('singlelinecomment', 'exclusive'),
)


t_ignore = ' \t\n' # estes tokens apenas são ignorados no estado 'INITIAL' e em estados inclusivos
t_singlelinecomment_ignore = ' \t' # estes tokens são ignorados no estado 'singlelinecomment'
t_multilinecomment_ignore = ' \t' # estes tokens são ignorados no estado 'multilinecomment'


def t_COLON(t):
    r'\:'
    return t

def t_DOT(t):
    r'\.'
    return t

def t_AP(t):
    r'\('
    return t

def t_FP(t):
    r'\)'
    return t

def t_APR(t):
    r'\['
    return t

def t_FPR(t):
    r'\]'
    return t

def t_AC(t):
    r'\{'
    return t

def t_FC(t):
    r'\}'
    return t
  
def t_INT(t):
    r'int'
    return t
  
def t_MOREEQUAL(t):
    r'\>\='
    return t

def t_MORE(t):
    r'\>'
    return t

def t_LESSEQUAL(t):
    r'\<\='
    return t

def t_LESS(t):
    r'\<'
    return t
  
  
def t_SLC(t):
    r'\/\/'
    t.lexer.begin('singlelinecomment')
    pass

def t_MLC_OPEN(t):
    r'\/\*'
    t.lexer.begin('multilinecomment')
    pass
  
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_WHILE(t):
    r'while'
    return t

def t_IF(t):
    r'if'
    return t

def t_ELSE(t):
    r'else'
    return t

def t_FOR(t):
    r'for'
    return t

def t_IN(t):
    r'in'
    return t
  
def t_MULTIPLY(t):
    r'\*'
    return t

def t_DIVIDE(t):
    r'\/'
    return t
  
def t_PLUS(t):
    r'\+'
    return t

def t_MINUS(t):
    r'\-'
    return t

def t_EQUALS(t):
    r'\='
    return t
  
def t_COMMA(t):
    r','
    return t

def t_DCOMMA(t):
    r';'
    return t
  
def t_FUNCTIONKW(t):
    r'function'
    return t

def t_PROGRAMKW(t):
    r'program'
    return t

def t_FUNCTION(t):
    r'\w+(?=\()' # lookahead
    return t
  
def t_PROGRAM(t):
    r'\w+(?=\{)' # lookahead
    return t

def t_VARIABLE(t):
    r'\w+'
    return t

def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    return t
  
def t_singlelinecomment_NEWLINE(t):
    r'\n+'
    t.lexer.begin('INITIAL')
    t.lexer.lineno += len(t.value)
    pass

def t_multilinecomment_NEWLINE(t):
    r'\n+' 
    t.lexer.lineno += len(t.value)
    pass

def t_multilinecomment_MLC_CLOSE(t):
    r'\*\/'
    t.lexer.begin('INITIAL')
    pass
  
def t_singlelinecomment_ALL(t):
    r'.+'
    pass

def t_multilinecomment_ALL(t):
    r'.+'
    pass

def t_ANY_error(t):
    print(f"Carácter ilegal '{t.value[0]}' na linha {t.lineno}")
    t.lexer.skip(1)

lexer = lex.lex()
lexer.input(texto)
while tok:=lexer.token():
  print(tok)

