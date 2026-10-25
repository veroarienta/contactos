
"""
Lista Digital de Contactos
Etapa 1: menú principal y administración de áreas.
"""
import re

############ VARIABLES GLOBALES ####################

# Cada área se guarda como una tupla: (código, nombre).
areas = []
area_predeterminada = None
tipo_telefono_predeterminado = None
contactos = []

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


def buscar_contacto(telefono, codigo_area):
    """Busca un contacto por teléfono y código de área."""
    for posicion, contacto in enumerate(contactos):
        if contacto[0] == telefono and contacto[1] == codigo_area:
            return posicion

    return -1


def leer_telefono():
    """Solicita un teléfono de entre 5 y 12 dígitos."""
    while True:
        telefono = input("Teléfono (5-12 dígitos): ").strip()

        if telefono.isdigit() and 5 <= len(telefono) <= 12:
            return telefono

        print("Error: el teléfono debe contener entre 5 y 12 dígitos.")


def leer_correo():
    """Valida un correo electrónico sin espacios."""
    while True:
        correo = input("Correo electrónico: ").strip()

        if re.fullmatch(r"[^\s@]+@[^\s@]+", correo):
            return correo

        print("Error: ingrese un correo válido, sin espacios.")


def leer_fecha():
    """Solicita una fecha válida o 0 si se desconoce."""
    from datetime import date

    while True:
        fecha = input(
            "Fecha de nacimiento (dd/mm/aaaa o 0 si se desconoce): "
        ).strip()

        if fecha == "0":
            return fecha

        partes = fecha.split("/")

        if (
            len(partes) == 3
            and len(partes[0]) == 2
            and len(partes[1]) == 2
            and len(partes[2]) == 4
            and all(parte.isdigit() for parte in partes)
        ):
            dia, mes, año = map(int, partes)
            año_validacion = año if año != 0 else 2000

            try:
                date(año_validacion, mes, dia)
                return fecha
            except ValueError:
                pass

        print("Error: ingrese una fecha válida o escriba 0.")


def leer_tipo_telefono():
    """Solicita un tipo de teléfono válido."""
    while True:
        tipo = input(
            "Tipo de teléfono: M=Móvil, C=Casa, T=Trabajo, O=Otro: "
        ).strip().upper()

        if tipo in ("M", "C", "T", "O"):
            return tipo

        print("Error: seleccione M, C, T u O.")

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

def agregar_contacto():
    """Registra un contacto y valida sus datos."""

    print("\nAGREGAR CONTACTO")

    if not areas:
        print("Primero debe registrar al menos un área.")
        return

    telefono = leer_telefono()

    consultar_areas()

    while True:
        entrada = input("Código del área: ").strip()

        if not entrada.isdigit():
            print("Error: ingrese un código numérico.")
            continue

        codigo_area = int(entrada)

        if buscar_area(codigo_area) == -1:
            print("Error: el área no existe.")
            continue

        break

    if buscar_contacto(telefono, codigo_area) != -1:
        print("Error: ya existe un contacto con ese teléfono y área.")
        return

    tipos = {
        "M": "Móvil",
        "C": "Casa",
        "T": "Trabajo",
        "O": "Otro"
    }

    if tipo_telefono_predeterminado in tipos:
        sugerido = tipo_telefono_predeterminado
        entrada = input(
            f"Tipo de teléfono (M/C/T/O) [{sugerido}]: "
        ).strip().upper()

        if entrada == "":
            tipo = sugerido
        elif entrada in tipos:
            tipo = entrada
        else:
            print("Error: tipo de teléfono no válido.")
            return
    else:
        tipo = leer_tipo_telefono()

    while True:
        nombre = input("Nombre completo (1-50 caracteres): ").strip()

        if 1 <= len(nombre) <= 50:
            break

        print("Error: el nombre debe tener entre 1 y 50 caracteres.")

    correo = leer_correo()

    while True:
        direccion = input(
            "Dirección física (máximo 80 caracteres): "
        ).strip()

        if len(direccion) <= 80:
            break

        print("Error: la dirección no puede superar 80 caracteres.")

    fecha = leer_fecha()

    while True:
        pasatiempos = input(
            "Pasatiempos (máximo 60 caracteres): "
        ).strip()

        if len(pasatiempos) <= 60:
            break

        print("Error: los pasatiempos no pueden superar 60 caracteres.")

    while True:
        notas = input("Notas (máximo 60 caracteres): ").strip()

        if len(notas) <= 60:
            break

        print("Error: las notas no pueden superar 60 caracteres.")

    contacto = [
        telefono,
        codigo_area,
        tipo,
        nombre,
        correo,
        direccion,
        fecha,
        pasatiempos,
        notas
    ]

    contactos.append(contacto)
    print("Contacto registrado correctamente.")

def menu_contactos():
    """Muestra el menú de registro de contactos."""

    while True:
        print("\nREGISTRAR CONTACTOS")
        print("1. Agregar contacto")
        print("0. Volver al menú principal")

        opcion = input("Seleccione una opción: ").strip()

        match opcion:
            case "1":
                agregar_contacto()
            case "0":
                break
            case _:
                print("Opción no válida.")


def menu_grupos():
    """Pendiente de implementación."""
    print("Administración de grupos: pendiente de implementación.")



def lista_contactos():
    """Muestra los contactos registrados."""

    print("\nLISTA DE CONTACTOS")

    if not contactos:
        print("No hay contactos registrados.")
        return

    for numero, contacto in enumerate(contactos, start=1):
        telefono, codigo_area, tipo, nombre, correo, direccion, fecha, pasatiempos, notas = contacto

        posicion_area = buscar_area(codigo_area)
        if posicion_area != -1:
            nombre_area = areas[posicion_area][1]
        else:
            nombre_area = "Área no disponible"

        tipos = {
            "M": "Móvil",
            "C": "Casa",
            "T": "Trabajo",
            "O": "Otro"
        }

        print(f"\nCONTACTO {numero}")
        print(f"Nombre: {nombre}")
        print(f"Teléfono: {telefono}")
        print(f"Área: {nombre_area} (código {codigo_area})")
        print(f"Tipo de teléfono: {tipos.get(tipo, tipo)}")
        print(f"Correo: {correo}")
        print(f"Dirección: {direccion}")
        print(f"Fecha de nacimiento: {fecha}")
        print(f"Pasatiempos: {pasatiempos}")
        print(f"Notas: {notas}")


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
