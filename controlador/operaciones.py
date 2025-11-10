"""
Módulo: controlador.operaciones
Implementa operaciones CRUD y consultas sobre el modelo Libro.
Incluye manejo explícito de transacciones (commit/rollback) y cierres de sesión.
"""

from typing import Iterable, Optional
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select, update, delete
from modelo.libro import Libro, Categoria, SessionLocal
from sqlalchemy.orm import joinedload


class AgregarLibro:
    """Responsable de insertar libros."""
    def agregar_libro(self, titulo: str, autor: str, precio: float, categoria_id: int) -> None:
        session = SessionLocal()
        try:
            categoria = session.get(Categoria, categoria_id)
            if categoria is None:
                print(f"Error: la categoría con id {categoria_id} no existe.")
                return
            nuevo = Libro(titulo=titulo, autor=autor, precio=precio, categoria_id=categoria_id)
            session.add(nuevo)
            session.commit()# Si algo falla, se capturará y se hará rollback
            print(f"Agregado: {nuevo}")
        except SQLAlchemyError as e:
            session.rollback()
            print("Error al agregar. Transacción revertida.")
            print("Detalle:", e)
        finally:
            session.close()

class ListarLibros:
    """Retorna todos los libros ordenados por id."""
    def listar_libros(self) -> Iterable[Libro]:
        session = SessionLocal()
        try:
            stmt = select(Libro).options(joinedload(Libro.categoria)).order_by(Libro.id.asc())
            return session.scalars(stmt).all()
        finally:
            session.close()


class BuscarAutor:
    """Filtra libros por autor exacto."""
    def buscar_por_autor(self, autor: str) -> Iterable[Libro]:
        session = SessionLocal()
        try:
            stmt = select(Libro).where(Libro.autor == autor).order_by(Libro.titulo.asc())
            return session.scalars(stmt).all()
        finally:
            session.close()

class Actualizar:
    """
    Actualiza el precio del primer libro con ese título.
    Retorna True si se actualizó algún registro.
    """
    def actualizar_precio(self, titulo: str, nuevo_precio: float) -> bool:
        session = SessionLocal()
        try:
            stmt = (
                update(Libro)
                .where(Libro.titulo == titulo)
                .values(precio=nuevo_precio)
            )
            result = session.execute(stmt)
            session.commit()
            return result.rowcount > 0
        except SQLAlchemyError as e:
            session.rollback()
            print("Error en actualización. Transacción revertida.")
            print("Detalle:", e)
            return False
        finally:
            session.close()



class Eliminar:
    """Elimina libros por título. Retorna la cantidad eliminada."""
    def eliminar_por_titulo(self, titulo: str) -> int:
        session = SessionLocal()
        try:
            stmt = delete(Libro).where(Libro.titulo == titulo)
            result = session.execute(stmt)
            session.commit()
            return result.rowcount or 0
        except SQLAlchemyError as e:
            session.rollback()
            print("Error en eliminación. Transacción revertida.")
            print("Detalle:", e)
            return 0
        finally:
            session.close()

class AgregarCategoria:
    def agregar_categoria(self, nombre:str)->None:
        session = SessionLocal()
        try:
            nueva = Categoria(nombre=nombre)
            session.add(nueva)
            session.commit()
            print(f"Se ha agregado la categoria: {nueva.nombre}")
        except SQLAlchemyError as e:
            session.rollback()
            print("Error al agregar. Transacción revertida.")
            print("Detalle:", e)
        finally:
            session.close()

class ListarCategorias:
    def listar_categorias(self):
        """Retorna todas las categorias."""
        session = SessionLocal()
        try:
            stmt = select(Categoria).order_by(Categoria.id.asc())
            return session.scalars(stmt).all()
        finally:
            session.close()

class BuscarCategoria:
    def buscar_por_categoria(self, categoria_id: int)-> Iterable[Libro]:
        """Filtra libros por categoría exacta (usando su ID)."""
        session = SessionLocal()
        try:
            stmt = select(Libro).where(Libro.categoria_id == categoria_id).order_by(Libro.titulo.asc())
            return session.scalars(stmt).all()
        finally:
            session.close()

