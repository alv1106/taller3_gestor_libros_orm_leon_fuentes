"""
Módulo:modelo.libro
Define la clase ORM 'Libro' y configura la conexión a la base de datos.
"""

from pathlib import Path
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

# 1) Declarative Base : clase base para los modelos ORM
Base = declarative_base()

# 2) Ruta de base de datos ( fuera del có digo fuente )
DATA_DIR = Path("datos")
DATA_DIR . mkdir(exist_ok = True)
DB_URL = f"sqlite:///{(DATA_DIR/'libros.db').as_posix()}"

# 3) Motor de base de datos : echo = True muestra el SQL generado por el ORM
engine = create_engine(DB_URL, echo = True, future = True)

# 4) Fabricante de sesiones : cada operación ORM usa su propia sesión
SessionLocal = sessionmaker(bind = engine, autoflush = False, autocommit =
False, future = True)

class Categoria(Base):
    """
    Crea la base para las categorías, con una primary key
    basada en un id asignado, back_populates relaciona los dos objetos.
    Attributes: lol falta agregarlos.
    """
    __tablename__ = "categorias"
    id = Column(Integer, primary_key = True)
    nombre = Column(String, nullable=False)

    #Para establecer la relación de una categoría muchos libros.
    libros = relationship("Libro", back_populates="categoria")


class Libro(Base):
    """
    Clase ORM que representa la tabla 'libros'.
    -id: clave primaria autoincremental
    -titulo: texto no nulo
    -autor: texto no nulo
    -precio: valor numérico ( float ) no nulo
    """
    __tablename__ ="Libros"
    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column (String, nullable=False)
    autor = Column (String, nullable=False)
    precio = Column (Float, nullable=False)
    #Para relacionarlo a la categoría con su FK.
    categoria_id = Column(Integer, ForeignKey("categorias.id"))

    categoria=relationship("Categoria", back_populates="libros")

    def __repr__ (self)-> str:
        return f"<Libro id ={self.id} titulo='{self.titulo}' autor='{self.autor}' precio ={self.precio:.2f} >"

#5) Crea las bases si no existen.
Base.metadata.create_all(engine)