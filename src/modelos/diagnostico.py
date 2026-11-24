"""Diagnósticos léxicos recuperables."""

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class DiagnosticoLexico:
    codigo: str
    tipo: str
    descripcion: str
    fragmento: str
    linea: int
    columna: int
    sugerencia: str | None = None

    def como_dict(self) -> dict[str, str | int | None]:
        return asdict(self)

    def __str__(self) -> str:
        sugerencia = f" Sugerencia: {self.sugerencia}" if self.sugerencia else ""
        return (
            f"{self.tipo} {self.codigo} (línea {self.linea}, columna "
            f"{self.columna}): {self.descripcion} [{self.fragmento!r}].{sugerencia}"
        )
