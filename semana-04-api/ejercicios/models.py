from sqlalchemy import Column , Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Autor(Base):
    __tablename__ = "autores"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True)
    biografia = Column(String)

    # Relación: un autor tiene muchos libros
    libros = relationship("Libro", back_populates="autor")

class Libro(Base):
    __tablename__ = "libros"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, index=True)
    genero = Column(String)
    resumen = Column(String)

    # Relación con autor
    autor_id = Column(Integer, ForeignKey("autores.id"))
    autor = relationship("Autor", back_populates="libros")

