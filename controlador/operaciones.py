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
        """
        Agrega un nuevo libro a la base de datos

        Args:
            titulo (str): Titulo del libro
            autor (str): Autor del libro
            precio (float): Precio del libro
            categoria_id (int): ID de la categoria a la que pertenece el libro
        """
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
        """
        Da todos los libros registrados en la base de datos

        Returns:
           Una lista con todos los libros y sus categorias
        """
        session = SessionLocal()
        try:
            stmt = select(Libro).options(joinedload(Libro.categoria)).order_by(Libro.id.asc())
            return session.scalars(stmt).all()
        finally:
            session.close()


class BuscarAutor:
    """Filtra libros por autor exacto."""

    def buscar_por_autor(self, autor: str) -> Iterable[Libro]:
        """
        Busca libros por nombre de autor

        Args:
            autor(str): Nombre del autor a buscar

        Returns:
            Lista de libros escritos por el autor
        """
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
        """
        Actualiza el precio de un libro segun su titulo

        Args:
            titulo (str): Titulo del libro a actualizar
            nuevo_precio (float): Nuevo valor del precio

        Returns:
            bool: True si se actualizo algun registro, False en caso contrario
        """
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
        """
        Elimina libros que coincidan con el titulo indicado

        Args:
            titulo (str): Titulo del libro a eliminar

        Returns:
            int: Numero de registros eliminados
        """
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
    """insertar nuevas categorias."""

    def agregar_categoria(self, nombre:str)->None:
        """
        Agrega una nueva categoria a la base de datos.

        Args:
            nombre (str): Nombre de la categoria
        """
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
    """retorna todas las categorias"""

    def listar_categorias(self):
        """
        Da todas las categorias registradas en la base de datos.

        Lista de todas las categorias disponibles
        """
        session = SessionLocal()
        try:
            stmt = select(Categoria).order_by(Categoria.id.asc())
            return session.scalars(stmt).all()
        finally:
            session.close()


class BuscarCategoria:
    """Filtra libros por categora exacta"""

    def buscar_por_categoria(self, categoria_id: int)-> Iterable[Libro]:
        """
        Busca libros segun su categoria.

        Args:
            categoria_id (int): ID de la categoria a buscar

        Returns:
            Lista de libros pertenecientes a esa categoria
        """
        session = SessionLocal()
        try:
            stmt = select(Libro).where(Libro.categoria_id == categoria_id).order_by(Libro.titulo.asc())
            return session.scalars(stmt).all()
        finally:
            session.close()


class EliminarCategoria:
    """Elimina categorias por nombre y retorna la cantidad eliminada"""

    def eliminar_la_categoria(self, nombre: str) -> int:
        """
        Elimina una categoria segun su nombre.

        Args:
            nombre (str): Nombre de la categoria a eliminar

        Returns:
            int: Numero de categorias eliminadas
        """
        session = SessionLocal()
        try:
            stmt = delete(Categoria).where(Categoria.nombre == nombre)
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
