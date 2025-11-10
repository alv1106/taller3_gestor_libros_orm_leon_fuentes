"""
Módulo: vista.main
Proporciona una interfaz por consola para probar el controlador.
"""

from controlador.operaciones import (
    AgregarLibro,
    ListarLibros,
    BuscarAutor,
    Actualizar,
    Eliminar,
    AgregarCategoria,
    ListarCategorias,
    BuscarCategoria
)

agregar_li = AgregarLibro()
listar_li = ListarLibros()
buscar_autor = BuscarAutor()
actualizar = Actualizar()
eliminar = Eliminar()
agregar_cate = AgregarCategoria()
listar_cate = ListarCategorias()
buscar_cate = BuscarCategoria()


def mostrar_menu() -> None:
    while True:
        print("\n--- GESTOR DE LIBROS (ORM) ---")
        print("1. Agregar categoria")
        print("2. Agregar libro")
        print("3. Listar todos")
        print("4. Buscar por autor")
        print("5. Actualizar precio por título")
        print("6. Eliminar por título")
        print("7. Buscar por categoria")
        print("8. Salir")

        op = input("Seleccione una opción: ")

        if op == "1":
            if op == "1":
                nombre = input("Nombre de la categoría: ").strip()
                agregar_cate.agregar_categoria(nombre)

        elif op == "2":
            t = input("Título: ")
            a = input("Autor: ")

            try:
                p = float(input("Precio: "))
            except(ValueError):
                print("No se ha digitado un precio valido.")
                continue

            categorias = listar_cate.listar_categorias()
            if not categorias:
                print("No hay categorías. Agrega una primero (opción 1).")
                continue

            print("\nCategorías disponibles:")
            for c in categorias:
                print(f"{c.id}. {c.nombre}")
            
            try:
                cat_id = int(input("Seleccione ID de categoría: "))
            except(ValueError):
                print("No se ha digitado un ID válido.")
                continue
                # verificar que el ID esté en la lista de categorías
            if not any(c.id == cat_id for c in categorias):
                print(f"No existe la categoría con el ID seleccionado.")
                continue
            agregar_li.agregar_libro(t, a, p, cat_id)

        elif op == "3":
            libros = listar_li.listar_libros()
            if libros:
                print("\nID | Título | Autor | Precio | Categoria")
                print("-------------------------------")
                for x in libros:
                    categoria = x.categoria.nombre if x.categoria else "Sin categoría"
                    print(f"{x.id:<2} {x.titulo:<15} {x.autor:<12} {x.precio:>6.2f} {categoria}")
            else:
                print("No hay registros.")

        elif op == "4":
            a = input("Autor: ")
            libros = buscar_autor.buscar_por_autor(a)
            for x in libros:
                print(x)

        elif op == "5":
            t = input("Título: ").strip()
            try:
                np = float(input("Nuevo precio: ").strip())
            except ValueError:
                print("Precio inválido. Operación cancelada.")
                continue
            actualizado = actualizar.actualizar_precio(t, np)
            print("Actualizado." if actualizado else "No se encontró el título.")

        elif op == "6":
            t = input("Título a eliminar: ")
            n = eliminar.eliminar_por_titulo(t)
            print(f"Registros eliminados: {n}")
        elif op == "7":
            categorias = listar_cate.listar_categorias()
            if not categorias:
                print("No hay categorías registradas.")
                continue

            print("\nCategorías disponibles:")
            for c in categorias:
                print(f"{c.id}. {c.nombre}")

            try:
                cat_id = int(input("selecciones una id, para filtar por esa categoria "))
            except ValueError:
                print("ID inválido.")
                continue

            libros = buscar_cate.buscar_por_categoria(cat_id)
            if libros:
                for x in libros:
                    print(x)
            else:
                print("No se encontraron libros en esa categoría.")



        elif op == "8":
            print("Fin de la sesión.")
            break

        else:
            print("Opción no válida.")