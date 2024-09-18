import attr

from typing import Any, Optional


def _bool_converter(value: str | bool) -> bool:
    if isinstance(value, str):
        return value.lower() == 'true'
    return bool(value)

@attr.s(auto_attribs=True, hash=True)
class Num:
    """Nodo que representa un número."""
    value: int


@attr.s(auto_attribs=True, hash=True)
class String:
    """Nodo que representa una cadena de texto."""
    value: str


@attr.s(auto_attribs=True, hash=True)
class Bool:
    """Nodo que representa un Booleano."""
    value: bool = attr.ib(converter=_bool_converter)


@attr.s(auto_attribs=True)
class DictNode:
    """Nodo que representa un diccionario."""
    pairs: dict[Any, Any]

    def items(self) -> dict[Any, Any]:
        return self.pairs.items()

    def keys(self):
        return self.pairs.keys()


@attr.s(auto_attribs=True)
class BinOp:
    """Nodo que representa una operación binaria."""
    left: Any
    op: tuple
    right: Any

    def __attrs_post_init__(self):
        self.token = self.op


@attr.s(auto_attribs=True)
class UnaryOp:
    """Nodo que representa una operación unaria."""
    op: tuple
    expr: Any

    def __attrs_post_init__(self):
        self.token = self.op


@attr.s(auto_attribs=True)
class Var:
    """Nodo que representa una variable."""
    name: str


@attr.s(auto_attribs=True)
class Assign:
    """Nodo que representa una asignación."""
    left: Var
    right: Any


@attr.s(auto_attribs=True)
class FuncCall:
    """Nodo que representa una llamada a función."""
    name: str
    args: list[Any]

@attr.s(auto_attribs=True)
class IfNode:
    """Nodo que representa una estructura condicional."""
    condition: Any
    if_block: list[Any]
    elif_blocks: Optional[list[tuple[Any, list[Any]]]] = None
    else_block: Optional[list[Any]] = None

@attr.s(auto_attribs=True)
class IndexAccess:
    """Nodo que representa el acceso a un elemento de un contenedor."""
    container: Any
    index: Any
