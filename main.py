
"""
Lista Digital de Contactos
Etapa 1: menú principal y administración de áreas.
"""

############ VARIABLES GLOBALES ####################

# Cada área se guarda como una tupla: (código, nombre).
areas = []
area_predeterminada = None
tipo_telefono_predeterminado = None

############ FUNCIONES DE ÁREAS ####################

def leer_codigo(mensaje="Código del área: "):
    """Solicita un código entero entre 1 y 999."""
    while True:
        entrada = input(mensaje).strip()

        if not entrada.isdigit():
            print("Error: ingrese un número entero.")
            continue

        codigo = int(entrada)

        if 1 <= codigo <= 999:
            return codigo

        print("Error: el código debe estar entre 1 y 999.")


def buscar_area(codigo):
    """Devuelve la posición de un área o -1 si no existe."""
    for posicion, area in enumerate(areas):
        if area[0] == codigo:
            return posicion

    return -1


def agregar_area():
    """Registra un área con código único y nombre válido."""
    print("\nAGREGAR ÁREA")

    codigo = leer_codigo()

    if buscar_area(codigo) != -1:
        print("Error: ya existe un área con ese código.")
        return

    while True:
        nombre = input("Nombre del área (1-40 caracteres): ").strip()

        if 1 <= len(nombre) <= 40:
            break

        print("Error: el nombre debe tener entre 1 y 40 caracteres.")

    areas.append((codigo, nombre))
    print("Área registrada correctamente.")


def consultar_areas():
    """Muestra todas las áreas registradas."""
    print("\nCONSULTAR ÁREAS")

    if not areas:
        print("No hay áreas registradas.")
        return

    print(f"{'CÓDIGO':<10} NOMBRE")
    print("-" * 45)

    for codigo, nombre in areas:
        print(f"{codigo:<10} {nombre}")


def modificar_area():
    """Modifica el nombre de un área existente."""
    print("\nMODIFICAR ÁREA")

    if not areas:
        print("No hay áreas para modificar.")
        return

    codigo = leer_codigo()
    posicion = buscar_area(codigo)

    if posicion == -1:
        print("Error: no existe un área con ese código.")
        return

    nombre_actual = areas[posicion][1]
    print(f"Nombre actual: {nombre_actual}")

    while True:
        nuevo_nombre = input(
            "Nuevo nombre (1-40 caracteres): "
        ).strip()

        if 1 <= len(nuevo_nombre) <= 40:
            break

        print("Error: el nombre debe tener entre 1 y 40 caracteres.")

    areas[posicion] = (codigo, nuevo_nombre)
    print("Área modificada correctamente.")


def eliminar_area():
    """Elimina un área existente si no tiene contactos asociados."""
    print("\nELIMINAR ÁREA")

    if not areas:
        print("No hay áreas para eliminar.")
        return

    codigo = leer_codigo()
    posicion = buscar_area(codigo)

    if posicion == -1:
        print("Error: no existe un área con ese código.")
        return

    # La validación de contactos asociados se añadirá
    # cuando implementemos el registro de contactos.
    confirmacion = input(
        f"¿Desea eliminar el área {areas[posicion][1]}? (S/N): "
    ).strip().upper()

    if confirmacion == "S":
        areas.pop(posicion)
        print("Área eliminada correctamente.")
    else:
        print("Operación cancelada.")


def menu_areas():
    """Muestra y procesa el submenú de administración de áreas."""
    while True:
        print("\nLISTA DIGITAL DE CONTACTOS")
        print("REGISTRAR ÁREAS")
        print("1. Agregar áreas")
        print("2. Consultar áreas")
        print("3. Modificar áreas")
        print("4. Eliminar áreas")
        print("0. Volver al menú principal")

        opcion = input("OPCIÓN: ").strip()

        match opcion:
            case "1":
                agregar_area()
            case "2":
                consultar_areas()
            case "3":
                modificar_area()
            case "4":
                eliminar_area()
            case "0":
                break
            case _:
                print("Opción no válida.")


############ FUNCIONES PENDIENTES ####################

def configuracion():
    """Permite configurar el área y tipo de teléfono predeterminados."""

    global area_predeterminada, tipo_telefono_predeterminado

    tipos_telefono = {
        "M": "Móvil",
        "C": "Casa",
        "T": "Trabajo",
        "O": "Otro"
    }

    while True:
        print("\nCONFIGURACIÓN DE LISTA DE CONTACTOS")
        print("1. Seleccionar área predeterminada")
        print("2. Seleccionar tipo de teléfono predeterminado")
        print("3. Consultar configuración actual")
        print("0. Volver al menú principal")

        opcion = input("Seleccione una opción: ").strip()

        match opcion:
            case "1":
                if not areas:
                    print("Primero debe registrar al menos un área.")
                    continue

                consultar_areas()
                codigo = leer_codigo(
                    "Código del área predeterminada: "
                )
                posicion = buscar_area(codigo)

                if posicion == -1:
                    print("Error: el área no existe.")
                else:
                    area_predeterminada = codigo
                    print("Área predeterminada configurada.")

            case "2":
                print("\nTIPOS DE TELÉFONO")
                for codigo, nombre in tipos_telefono.items():
                    print(f"{codigo}. {nombre}")

                tipo = input(
                    "Seleccione el tipo predeterminado: "
                ).strip().upper()

                if tipo in tipos_telefono:
                    tipo_telefono_predeterminado = tipo
                    print("Tipo de teléfono configurado.")
                else:
                    print("Error: tipo de teléfono no válido.")

            case "3":
                print("\nCONFIGURACIÓN ACTUAL")

                if area_predeterminada is None:
                    print("Área predeterminada: no configurada.")
                else:
                    posicion = buscar_area(area_predeterminada)
                    if posicion != -1:
                        print(
                            "Área predeterminada:",
                            areas[posicion][1]
                        )

                if tipo_telefono_predeterminado is None:
                    print("Tipo de teléfono: no configurado.")
                else:
                    print(
                        "Tipo de teléfono:",
                        tipos_telefono[tipo_telefono_predeterminado]
                    )

            case "0":
                break

            case _:
                print("Opción no válida.")


def menu_contactos():
    """Pendiente de implementación."""
    print("Registro de contactos: pendiente de implementación.")


def menu_grupos():
    """Pendiente de implementación."""
    print("Administración de grupos: pendiente de implementación.")


def lista_contactos():
    """Pendiente de implementación."""
    print("Lista de contactos: pendiente de implementación.")


def ayuda():
    """Pendiente de implementación."""
    print("Ayuda: pendiente de implementación.")


def acerca_de():
    """Muestra información básica del programa."""
    print("\nACERCA DE")
    print("Programa: Lista Digital de Contactos")
    print("Versión: 1.0")
    print("Fecha de creación: octubre de 2026")
    print("Autor: Veronika Arienta")


############ FUNCIÓN PRINCIPAL ####################

def principal():
    """Muestra el menú principal y procesa la opción elegida."""
    while True:
        print("\nLISTA DIGITAL DE CONTACTOS")
        print("1. Registrar áreas")
        print("2. Configuración de lista de contactos")
        print("3. Registrar contactos")
        print("4. Administrar grupos de contactos")
        print("5. Lista de contactos")
        print("6. Ayuda")
        print("7. Acerca de")
        print("0. Fin")

        opcion = input("Seleccione una opción: ").strip()

        match opcion:
            case "1":
                menu_areas()
            case "2":
                configuracion()
            case "3":
                menu_contactos()
            case "4":
                menu_grupos()
            case "5":
                lista_contactos()
            case "6":
                ayuda()
            case "7":
                acerca_de()
            case "0":
                print("Fin del programa.")
                break
            case _:
                print("Opción no válida. Intente nuevamente.")


if __name__ == "__main__":
    principal()
