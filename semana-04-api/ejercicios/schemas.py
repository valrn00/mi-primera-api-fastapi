from pydantic import BaseModel
from typing import List, Optional

class AutorBase(BaseModel):
    nombre: str
    nacionalidad: Optional[str] = None

class AutorCreate(AutorBase):   
    pass

class Autor(AutorBase):
    id: int

    class Config:
        from_attributes = True
        
class LibroBase(BaseModel):
    titulo: str
    genero: Optional[str] = None
    resumen: Optional[str] = None
    autor_id: int  # Relación con Autor

class LibroCreate(LibroBase):
    pass

class LibroconAutor(LibroBase):
    id: int
    autor: Autor  # Incluir detalles del autor

    class Config:
        from_attributes = True

class AutorconLibros(AutorBase):
    id: int
    libros: List[LibroconAutor] = []  # Lista de libros del autor

    class Config:
        from_attributes = True