import attr
import sqlite3
import threading
import uvicorn
from rich.console import Console
from typing import Any, Optional
from tokens import (
    PLUS, MINUS, MUL, DIV, AND, OR, EQUALS, NOT_EQUALS, LESS_THAN, LESS_EQUAL,
    GREATER_EQUAL, GREATER_THAN, NOT
)
from ast_nodes import (
    Num, BinOp, UnaryOp, Assign, Var, FuncCall, String, DictNode, Bool, IfNode,
    IndexAccess
)
from apiapp import APIApp
import json


console = Console()


@attr.s(auto_attribs=True)
class Context:
    """Contexto que almacena variables y conexiones de base de datos."""
    variables: dict[str, Any] = attr.ib(factory=dict)
    database: Optional[Any] = None
    app: Optional[APIApp] = None


@attr.s(auto_attribs=True)
class Interpreter:
    """Intérprete que ejecuta el AST."""
    tree: list[Any]
    context: Context = attr.ib(factory=Context)

    def visit(self, node: Any) -> Any:
        """Despacha el método de visita adecuado para el nodo dado."""
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node: Any) -> None:
        """Lanza una excepción si no se encuentra el método de visita."""
        raise Exception(f'No visit_{type(node).__name__} method')

    def visit_Num(self, node: Num) -> int:
        """Devuelve el valor numérico."""
        return node.value

    def visit_Bool(self, node: Bool) -> int:
        """Devuelve el valor booleano."""
        return node.value

    def visit_String(self, node: String) -> Any:
        """Devuelve el valor de una cadena de texto o un objeto si es JSON."""
        value = node.value
        try:
            # Intentar parsear como JSON
            return json.loads(value)
        except json.JSONDecodeError:
            # Si falla, devolver la cadena como está
            return value

    def visit_DictNode(self, node: DictNode) -> dict[Any, Any]:
        """Devuelve el valor de un diccionario."""
        result = {}
        for key_node, value_node in node.pairs.items():
            key = self.visit(key_node)
            value = self.visit(value_node)
            if not isinstance(key, (str, int, float, bool, tuple)):
                raise TypeError(f'Las claves del diccionario deben ser tipos hashables, pero se recibió: {type(key).__name__}')
            result[key] = value
        return result

    def visit_BinOp(self, node: BinOp) -> Any:
        """Realiza operaciones binarias, incluyendo lógicas y relacionales."""
        left = self.visit(node.left)
        right = self.visit(node.right)
        op_type = node.op[0]

        if op_type == PLUS:
            return left + right
        elif op_type == MINUS:
            return left - right
        elif op_type == MUL:
            return left * right
        elif op_type == DIV:
            return left / right
        elif op_type == AND:
            return left and right
        elif op_type == OR:
            return left or right
        elif op_type == EQUALS:
            return left == right
        elif op_type == NOT_EQUALS:
            return left != right
        elif op_type == LESS_THAN:
            return left < right
        elif op_type == GREATER_THAN:
            return left > right
        elif op_type == LESS_EQUAL:
            return left <= right
        elif op_type == GREATER_EQUAL:
            return left >= right
        else:
            raise Exception(f'Operador "{op_type}" no soportado')

    def visit_IfNode(self, node: IfNode) -> None:
        """Ejecuta una estructura condicional."""
        if self.visit(node.condition):
            self._execute_block(node.if_block)
        else:
            for condition, block in node.elif_blocks:
                if self.visit(condition):
                    self._execute_block(block)
                    return
            else:
                if node.else_block is not None:
                    self._execute_block(node.else_block)

    def _execute_block(self, block: list[Any]) -> None:
        """Ejecuta un bloque de código."""
        for statement in block:
            self.visit(statement)

    def visit_UnaryOp(self, node: UnaryOp) -> Any:
        """Realiza operaciones unarias."""
        expr = self.visit(node.expr)
        op_type = node.op[0]
        if op_type == PLUS:
            return +expr
        elif op_type == MINUS:
            return -expr
        elif op_type == NOT:
            return not expr
        else:
            raise Exception(f'Operador unario "{op_type}" no soportado')

    def visit_Assign(self, node: Assign) -> None:
        """Asigna un valor a una variable."""
        var_name = node.left.name
        self.context.variables[var_name] = self.visit(node.right)

    def visit_Var(self, node: Var) -> Any:
        """Devuelve el valor de una variable."""
        var_name = node.name
        val = self.context.variables.get(var_name, None)
        if val is None:
            raise Exception(f'Variable "{var_name}" no definida')
        else:
            return val

    def visit_FuncCall(self, node: FuncCall) -> None:
        """Ejecuta una función nativa."""
        func_name = node.name
        if func_name == 'print':
            final_value = ""
            for arg in node.args:
                final_value += str(self.visit(arg))
            console.print(f"[bold green]{final_value}[/bold green]")
        elif func_name == 'connect_db':
            db_path = self.visit(node.args[0])
            self.connect_db(db_path)
        elif func_name == 'create_api':
            api_title = self.visit(node.args[0])
            self.create_api(api_title)
        elif func_name == 'db_insert':
            table_name = self.visit(node.args[0])
            data = self.visit(node.args[1])
            self.db_insert(table_name, data)
        elif func_name == 'db_query':
            table_name = self.visit(node.args[0])
            self.db_query(table_name)
        elif func_name == 'db_create_table':
            table_name = self.visit(node.args[0])
            columns = self.visit(node.args[1])
            self.db_create_table(table_name, columns)
        else:
            raise Exception(f'Función "{func_name}" no definida')

    def visit_IndexAccess(self, node: IndexAccess) -> Any:
        """Evalúa el acceso a un elemento de un contenedor."""
        container = self.visit(node.container)
        index = self.visit(node.index)

        try:
            return container[index]
        except (TypeError, KeyError, IndexError) as e:
            raise Exception(f'Error al acceder al elemento: {e}')

    def connect_db(self, db_path: str) -> None:
        """Conecta a una base de datos SQLite."""
        console.rule("[red]Step: Conexión con la base de datos[/red]")
        with console.status(f"conectando a la base de datos: {db_path}"):
            self.context.database = sqlite3.connect(db_path, check_same_thread=False)
        console.print(f"[bold blue]Conectado a la base de datos: {db_path}[/bold blue]\n")

    def create_api(self, title: str) -> None:
        """Crea y levanta una API con FastAPI."""
        console.rule("[red]Step: Creando la API[/red]")
        console.print("Running API...:shooting_star:\n")

        with console.status(f"Creando la API: {title}..."):
            self.context.app = APIApp(title).app
            app = self.context.app

            @app.get("/")
            def health_check():
                return {"status": "OK!"}

            def run():
                uvicorn.run(app, host="127.0.0.1", port=8000)

            threading.Thread(target=run).start()

        console.print("[bold magenta]API levantada en http://127.0.0.1:8000[/bold magenta]\n")

    def db_insert(self, table_name: str, data: dict[Any, Any]) -> None:
        """Inserta datos en la base de datos."""
        if not self.context.database:
            raise Exception('No hay conexión a la base de datos.')
        console.rule("[red]Step: Insetando datos[/red]")
        with console.status(f"Insertando datos en la tabla: {table_name}"):
            columns = ', '.join(data.keys())
            placeholders = ', '.join('?' * len(data))
            sql = f'INSERT INTO {table_name} ({columns}) VALUES ({placeholders})'
            self.context.database.execute(sql, tuple(data.values()))
            self.context.database.commit()
            console.print(f"[bold green]Datos insertados en {table_name}[/bold green]\n")

    def db_query(self, table_name: str) -> None:
        """Recupera datos de la base de datos."""
        if not self.context.database:
            raise Exception('No hay conexión a la base de datos.')
        console.rule("[red]Step: Obteniendo datos[/red]")
        with console.status(f"Obteniendo todos los datos de la tabla: {table_name}"):
            cursor = self.context.database.execute(f'SELECT * FROM {table_name}')
            rows = cursor.fetchall()
            for row in rows:
                console.print(f"[bold yellow]{row}[/bold yellow]")

    def db_create_table(self, table_name: str, columns: dict[str, str]) -> None:
        """Crea una tabla en la base de datos."""
        if not self.context.database:
            raise Exception('No hay conexión a la base de datos.')
        console.rule("[red]Step: Creando tabla[/red]")
        with console.status(f"Creando la tabla {table_name}..."):
            columns_def = ', '.join([f"{col_name} {col_type}" for col_name, col_type in columns.items()])
            sql = f'CREATE TABLE IF NOT EXISTS {table_name} ({columns_def});'
            self.context.database.execute('PRAGMA encoding="UTF-8";')
            self.context.database.execute(sql)
            self.context.database.commit()
        console.print(f"[bold green]Tabla '{table_name}' creada con éxito[/bold green]\n")

    def interpret(self) -> None:
        """Interpreta el AST completo."""
        for node in self.tree:
            self.visit(node)
