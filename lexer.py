import attr

from tokens import (
    PLUS, MINUS, NUMBER, LPAREN, RPAREN, IDENTIFIER, MUL, DIV,
    ASSIGN, COMMA, EOF, STRING, LBRACE, RBRACE, COLON, BOOLEAN,
    TRUE, FALSE, IF, ELIF, ELSE, AND, OR, NOT, NOT_EQUALS, GREATER_EQUAL,
    GREATER_THAN, LESS_EQUAL, LESS_THAN, EQUALS, LBRACKET, RBRACKET
)


CHAR_TOKENS_SWITCHER = {
    '+': (PLUS, '+'),
    '-': (MINUS, '-'),
    '*': (MUL, '*'),
    '/': (DIV, '/'),
    '(': (LPAREN, '('),
    ')': (RPAREN, ')'),
    '=': (ASSIGN, '='),
    ',': (COMMA, ','),
    '{': (LBRACE, '{'),
    '}': (RBRACE, '}'),
    ':': (COLON, ':'),
}

IDENTIFIER_SWITCHER = {
    'true': TRUE,
    'false': FALSE,
    'if': IF,
    'elif': ELIF,
    'else': ELSE,
    'and': AND,
    'or': OR,
    'not': NOT,
}


@attr.s(auto_attribs=True)
class Lexer:
    """Analizador léxico que convierte el código fuente en tokens."""
    text: str

    def __attrs_post_init__(self):
        """Inicializa el lexer estableciendo la posición y el carácter actual."""
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self) -> None:
        """Lanza una excepción de análisis léxico."""
        raise Exception('Error de análisis léxico')

    def advance(self) -> None:
        """Avanza al siguiente carácter en el texto."""
        self.pos += 1
        if self.pos >= len(self.text):
            self.current_char = None  # Indicador de fin de entrada
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self) -> None:
        """Salta los espacios en blanco."""
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def number(self) -> tuple:
        """Devuelve un token de tipo NUMBER."""
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return (NUMBER, int(result))

    def boolean(self) -> tuple:
        """Devuelve un token de tipo BOOLEAN."""
        result = ''
        while self.current_char is not None and isinstance(self.current_char, bool):
            result += self.current_char
            self.advance()
        return (BOOLEAN, bool(result))

    def identifier(self) -> tuple:
        """Devuelve un token de tipo IDENTIFIER o palabra clave."""
        result = ''
        while self.current_char is not None and (
            self.current_char.isalnum() or self.current_char == '_'
        ):
            result += self.current_char
            self.advance()
        result_lower = result.lower()
        token_type = IDENTIFIER_SWITCHER.get(result_lower, IDENTIFIER)
        if token_type != IDENTIFIER:
            return (token_type, result)
        else:
            return (IDENTIFIER, result)

    def string(self) -> tuple:
        """Devuelve un token de tipo STRING."""
        quote_char = self.current_char
        result = ''
        self.advance()  # Saltar la comilla inicial
        while self.current_char is not None and self.current_char != quote_char:
            if self.current_char == '\\':
                self.advance()
                if self.current_char in ['"', "'", '\\']:
                    result += self.current_char
                else:
                    result += '\\' + self.current_char
            else:
                result += self.current_char
            self.advance()
        self.advance()  # Saltar la comilla final
        return (STRING, result)

    def get_next_token(self) -> tuple:
        """Analiza y devuelve el siguiente token."""
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            elif self.current_char.isdigit():
                return self.number()
            elif self.current_char.isalpha() or self.current_char == '_':
                return self.identifier()

            token = CHAR_TOKENS_SWITCHER.get(self.current_char)

            if self.current_char == '=':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return (EQUALS, '==')
                return (ASSIGN, '=')

            if self.current_char == '!':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return (NOT_EQUALS, '!=')
                self.error()

            if self.current_char == '<':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return (LESS_EQUAL, '<=')
                return (LESS_THAN, '<')

            if self.current_char == '>':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return (GREATER_EQUAL, '>=')
                return (GREATER_THAN, '>')

            if self.current_char == '[':
                self.advance()
                return (LBRACKET, '[')

            if self.current_char == ']':
                self.advance()
                return (RBRACKET, ']')

            if token:
                self.advance()
                return token
            if self.current_char in ['"', "'"]:
                return self.string()
            self.error()
        return (EOF, None)
