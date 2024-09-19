import attr

from typing import Any

from lexer import Lexer
from tokens import (
    PLUS, MINUS, NUMBER, LPAREN, RPAREN, IDENTIFIER, MUL, DIV,
    ASSIGN, COMMA, EOF, STRING, LBRACE, RBRACE, COLON, TRUE,
    FALSE, IF, ELIF, ELSE, AND, OR, NOT, EQUALS, NOT_EQUALS,
    LESS_THAN, GREATER_THAN, LESS_EQUAL, GREATER_EQUAL, LBRACKET,
    RBRACKET
)
from ast_nodes import (
    UnaryOp, Num, BinOp, FuncCall, Var, Assign, String,
    DictNode, Bool, IfNode, IndexAccess
)


@attr.s(auto_attribs=True)
class Parser:
    """Parser que convierte tokens en un AST."""
    lexer: Lexer

    def __attrs_post_init__(self):
        """Inicializa el parser obteniendo el primer token."""
        self.current_token = self.lexer.get_next_token()

    def error(self) -> None:
        """Lanza una excepción de análisis sintáctico."""
        raise Exception('Error de análisis sintáctico')

    def eat(self, token_type: str) -> None:
        """Consume el token actual si coincide con `token_type`."""
        if self.current_token[0] == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def expr(self) -> Any:
        """Analiza expresiones con operadores de baja precedencia (+, -)."""
        node = self.term()
        while self.current_token[0] in (PLUS, MINUS):
            token = self.current_token
            self.eat(token[0])
            node = BinOp(left=node, op=token, right=self.term())
        return node

    def term(self) -> Any:
        """Analiza términos con operadores de media precedencia (*, /)."""
        node = self.factor()
        while self.current_token[0] in (MUL, DIV):
            token = self.current_token
            self.eat(token[0])
            node = BinOp(left=node, op=token, right=self.factor())
        return node

    def factor(self) -> Any:
        """Analiza y devuelve un nodo de factor."""
        token = self.current_token
        token_type = token[0]
        dispatch_table = {
            NOT: self._parse_unary_op,
            PLUS: self._parse_unary_op,
            MINUS: self._parse_unary_op,
            NUMBER: self._parse_number,
            TRUE: self._parse_boolean,
            FALSE: self._parse_boolean,
            LBRACE: self.dict_literal,
            LPAREN: self._parse_grouped_expr,
            IDENTIFIER: self.variable_or_function,
            STRING: self._parse_string,
        }
        parse_method = dispatch_table.get(token_type)

        if not parse_method:
            self.error()

        node = parse_method()
        # Después de obtener el nodo, verificamos si hay un acceso a elemento
        while self.current_token[0] == LBRACKET:
            node = self._index_access(node)
        return node

    def _index_access(self, container_node: Any) -> Any:
        """Analiza el acceso a elementos de contenedores como diccionarios o listas."""
        self.eat(LBRACKET)
        index = self.logical_expr()
        self.eat(RBRACKET)
        return IndexAccess(container=container_node, index=index)

    def _parse_unary_op(self) -> UnaryOp:
        token = self.current_token
        self.eat(token[0])
        return UnaryOp(op=token, expr=self.factor())

    def _parse_number(self) -> Num:
        token = self.current_token
        self.eat(NUMBER)
        return Num(value=token[1])

    def _parse_boolean(self) -> Bool:
        token = self.current_token
        self.eat(token[0])
        return Bool(value=token[1])

    def _parse_grouped_expr(self) -> Any:
        self.eat(LPAREN)
        node = self.expr()
        self.eat(RPAREN)
        return node

    def _parse_string(self) -> String:
        token = self.current_token
        self.eat(STRING)
        return String(value=token[1])

    def logical_expr(self) -> Any:
        """Analiza expresiones lógicas con operadores AND, OR."""
        node = self.equality_expr()
        while self.current_token[0] in (AND, OR):
            token = self.current_token
            self.eat(token[0])
            node = BinOp(left=node, op=token, right=self.equality_expr())
        return node

    def equality_expr(self) -> Any:
        """Analiza expresiones de igualdad y relacionales."""
        node = self.expr()
        while self.current_token[0] in (EQUALS, NOT_EQUALS, LESS_THAN, GREATER_THAN, LESS_EQUAL, GREATER_EQUAL):
            token = self.current_token
            self.eat(token[0])
            node = BinOp(left=node, op=token, right=self.expr())
        return node

    def dict_literal(self) -> DictNode:
        """Analiza y devuelve un nodo de diccionario."""
        pairs = {}
        self.eat(LBRACE)
        while self.current_token[0] != RBRACE:
            key = self.expr()
            self.eat(COLON)
            value = self.expr()
            pairs[key] = value
            if self.current_token[0] == COMMA:
                self.eat(COMMA)
            else:
                break
        self.eat(RBRACE)
        return DictNode(pairs=pairs)

    def variable_or_function(self) -> Any:
        """Distingue entre variables y funciones."""
        token = self.current_token
        self.eat(IDENTIFIER)

        if self.current_token[0] == ASSIGN:
            self.eat(ASSIGN)
            node = Assign(left=Var(name=token[1]), right=self.logical_expr())
            return node
        elif self.current_token[0] == LPAREN:
            # Manejo de llamadas a funciones
            self.eat(LPAREN)
            args = []
            if self.current_token[0] != RPAREN:
                args.append(self.logical_expr())
                while self.current_token[0] == COMMA:
                    self.eat(COMMA)
                    args.append(self.logical_expr())
            self.eat(RPAREN)
            node = FuncCall(name=token[1], args=args)
            return node

        return Var(name=token[1])

    def statement(self) -> Any:
        """Analiza una sentencia, que puede ser una asignación, una estructura condicional o una expresión."""
        if self.current_token[0] == IF:
            return self.if_statement()

        return self.assignment()

    def assignment(self) -> Any:
        """Analiza una asignación o una expresión."""
        node = self.logical_expr()
        if self.current_token[0] == ASSIGN:
            if isinstance(node, Var):
                self.eat(ASSIGN)
                right = self.assignment()
                return Assign(left=node, right=right)
            self.error('Asignación inválida')
        return node

    def if_statement(self) -> Any:
        """Analiza una estructura condicional if-elif-else."""
        self.eat(IF)
        condition = self.logical_expr()
        self.eat(COLON)
        if_block = self.block()
        elif_blocks = []

        while self.current_token[0] == ELIF:
            self.eat(ELIF)
            elif_condition = self.logical_expr()
            self.eat(COLON)
            elif_block = self.block()
            elif_blocks.append((elif_condition, elif_block))
        else_block = None

        if self.current_token[0] == ELSE:
            self.eat(ELSE)
            self.eat(COLON)
            else_block = self.block()

        return IfNode(condition=condition, if_block=if_block, elif_blocks=elif_blocks, else_block=else_block)

    def block(self) -> list[Any]:
        """Analiza un bloque de código."""
        statements = []
        self.eat(LBRACE)

        while self.current_token[0] != RBRACE and self.current_token[0] != EOF:
            statements.append(self.statement())

        self.eat(RBRACE)
        return statements

    def parse(self) -> list[Any]:
        """Analiza todos los tokens y devuelve una lista de nodos."""
        statements = []
        while self.current_token[0] != EOF:
            node = self.statement()
            statements.append(node)
        return statements
