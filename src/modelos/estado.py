from dataclasses import dataclass


@dataclass
class Estado:
    """
    Estado de un autómata finito.
    """
    nombre: str
    es_inicial: bool = False
    es_final: bool = False
    descripcion: str = ""

    def __post_init__(self) -> None:
        if not self.nombre or not self.nombre.strip():
            raise ValueError("El estado debe tener un nombre válido.")
