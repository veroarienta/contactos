
"""
Lista Digital de Contactos
"""
import re
from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
)
from reportlab.lib.units import cm
from xml.sax.saxutils import escape


############ VARIABLES GLOBALES ####################

# Cada área se guarda como una tupla: (código, nombre).
areas = []
area_predeterminada = None
tipo_telefono_predeterminado = None
contactos = []
grupos = []
contactos_por_grupo = []
TIPOS_TELEFONO = (
    ("M", "Móvil"),
    ("C", "Casa"),
    ("T", "Trabajo"),
    ("O", "Otro"),
)

############ FUNCIONES DE ÁREAS ####################

def es_numero_ascii(valor):
    """Indica si una cadena contiene únicamente dígitos ASCII."""
    return valor.isascii() and valor.isdigit()


def confirmar_dato(etiqueta, valor):
    """Confirma un dato antes de guardarlo."""
    while True:
        opcion = input(
            f"¿Aceptar {etiqueta} «{valor}»? (A=aceptar/C=cancelar): "
        ).strip().upper()

        if opcion == "A":
            return True
        if opcion == "C":
            return False

        print("Opción no válida. Escriba A para aceptar o C para cancelar.")


def leer_codigo(mensaje="Código del área: ", permitir_cancelar=False):
    """Solicita un código entero entre 1 y 999."""
    while True:
        entrada = input(mensaje).strip()

        if permitir_cancelar and entrada.upper() == "C":
            return None

        if not es_numero_ascii(entrada):
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


def mostrar_contacto(contacto):
    """Muestra todos los datos de un contacto."""
    telefono, codigo_area, tipo, nombre, correo, direccion, fecha, pasatiempos, notas = contacto
    posicion_area = buscar_area(codigo_area)
    nombre_area = (
        areas[posicion_area][1]
        if posicion_area != -1
        else "Área no disponible"
    )

    print(f"Nombre: {nombre}")
    print(f"Teléfono: {telefono}")
    print(f"Área: {nombre_area} (código {codigo_area})")
    print(f"Tipo de teléfono: {nombre_tipo_telefono(tipo)}")
    print(f"Correo: {correo}")
    print(f"Dirección: {direccion}")
    print(f"Fecha de nacimiento: {fecha}")
    print(f"Pasatiempos: {pasatiempos}")
    print(f"Notas: {notas}")


def leer_telefono(permitir_cancelar=False):
    """Solicita un teléfono de entre 5 y 12 dígitos."""
    while True:
        telefono = input("Teléfono (5-12 dígitos): ").strip()

        if permitir_cancelar and telefono.upper() == "C":
            return None

        if es_numero_ascii(telefono) and 5 <= len(telefono) <= 12:
            return telefono

        print("Error: el teléfono debe contener entre 5 y 12 dígitos.")


def leer_texto(mensaje, minimo, maximo, permitir_vacio=False,
               valor_actual=None, permitir_cancelar=False):
    """Lee texto con límites de longitud y opciones de conservar o cancelar."""
    while True:
        entrada = input(mensaje).strip()

        if permitir_cancelar and entrada.upper() == "C":
            return None

        if entrada == "" and valor_actual is not None:
            return valor_actual

        if (permitir_vacio and entrada == "") or minimo <= len(entrada) <= maximo:
            return entrada

        if minimo == maximo:
            print(f"El texto debe tener exactamente {minimo} caracteres.")
        else:
            print(f"El texto debe tener entre {minimo} y {maximo} caracteres.")


def leer_correo(permitir_cancelar=False, valor_actual=None):
    """Valida un correo electrónico sin espacios."""
    while True:
        mensaje = "Correo electrónico"
        if valor_actual is not None:
            mensaje += " (Enter=conservar"
            if permitir_cancelar:
                mensaje += "/C=volver"
            mensaje += ")"
        elif permitir_cancelar:
            mensaje += " (C=cancelar)"
        correo = input(f"{mensaje}: ").strip()

        if permitir_cancelar and correo.upper() == "C":
            return None

        if correo == "" and valor_actual is not None:
            return valor_actual

        if re.fullmatch(r"[^\s@]+@[^\s@]+", correo):
            return correo

        print("Error: ingrese un correo válido, sin espacios.")


def leer_fecha(permitir_cancelar=False, valor_actual=None):
    """Solicita una fecha válida o 0 si se desconoce."""
    from datetime import date

    while True:
        mensaje = "Fecha de nacimiento (dd/mm/aaaa o 0 si se desconoce"
        if valor_actual is not None:
            mensaje += ", Enter=conservar"
        if permitir_cancelar:
            mensaje += ", C=volver" if valor_actual is not None else ", C=cancelar"
        fecha = input(f"{mensaje}): ").strip()

        if permitir_cancelar and fecha.upper() == "C":
            return None

        if fecha == "" and valor_actual is not None:
            return valor_actual

        if fecha == "0":
            return fecha

        partes = fecha.split("/")

        if (
            len(partes) == 3
            and len(partes[0]) == 2
            and len(partes[1]) == 2
            and len(partes[2]) == 4
            and all(es_numero_ascii(parte) for parte in partes)
        ):
            dia, mes, año = map(int, partes)
            año_validacion = año if año != 0 else 2000

            try:
                date(año_validacion, mes, dia)
                return fecha
            except ValueError:
                pass

        print("Error: ingrese una fecha válida o escriba 0.")


def leer_tipo_telefono(permitir_cancelar=False, valor_actual=None,
                       codigo_cancelacion="0"):
    """Solicita un tipo de teléfono válido."""
    while True:
        mensaje = "Tipo de teléfono: M=Móvil, C=Casa, T=Trabajo, O=Otro"
        if valor_actual is not None:
            mensaje += ", Enter=conservar"
        if permitir_cancelar:
            mensaje += f", {codigo_cancelacion}=cancelar"
        tipo = input(f"{mensaje}: ").strip().upper()

        if permitir_cancelar and tipo == codigo_cancelacion:
            return None

        if tipo == "" and valor_actual is not None:
            return valor_actual

        if any(codigo == tipo for codigo, _ in TIPOS_TELEFONO):
            return tipo

        print("Error: seleccione M, C, T u O.")


def nombre_tipo_telefono(tipo):
    """Devuelve el nombre correspondiente al tipo de teléfono."""
    for codigo, nombre in TIPOS_TELEFONO:
        if codigo == tipo:
            return nombre

    return "Desconocido"


def agregar_area():
    """Registra un área con código único y nombre válido."""
    print("\nAGREGAR ÁREA")

    while True:
        codigo = leer_codigo("Código del área (1-999, C=cancelar): ",
                             permitir_cancelar=True)
        if codigo is None:
            print("Registro de área cancelado.")
            return

        if buscar_area(codigo) != -1:
            print("Error: ya existe un área con ese código. Intente de nuevo.")
            continue

        if not confirmar_dato("el código", codigo):
            print("Registro de área cancelado.")
            return
        break

    nombre = leer_texto(
        "Nombre del área (1-40 caracteres, C=cancelar): ",
        1, 40, permitir_cancelar=True
    )
    if nombre is None:
        print("Registro de área cancelado.")
        return

    if not confirmar_dato("el nombre", nombre):
        print("Registro de área cancelado.")
        return

    areas.append((codigo, nombre))
    print("Área registrada correctamente.")


def consultar_areas(mostrar_detalle=True):
    """Lista las áreas y permite consultar una por código."""
    print("\nCONSULTAR ÁREAS")

    if not areas:
        print("No hay áreas registradas.")
        return

    print(f"{'CÓDIGO':<10} NOMBRE")
    print("-" * 45)

    for codigo, nombre in areas:
        print(f"{codigo:<10} {nombre}")

    if not mostrar_detalle:
        return

    while True:
        entrada = input(
            "\nCódigo del área para ver su detalle (A=terminar): "
        ).strip()
        if entrada.upper() == "A":
            return
        if not es_numero_ascii(entrada):
            print("Ingrese un código numérico o A para terminar.")
            continue

        codigo = int(entrada)
        posicion = buscar_area(codigo)
        if posicion == -1:
            print("No existe un área con ese código.")
            continue

        print(f"Área: {areas[posicion][1]} (código {codigo})")
        opcion = input(
            "A=ACEPTAR esta consulta, C=seleccionar otra área: "
        ).strip().upper()
        if opcion == "A":
            return
        if opcion != "C":
            print("Opción no válida.")


def modificar_area():
    """Modifica el nombre de un área existente."""
    print("\nMODIFICAR ÁREA")

    if not areas:
        print("No hay áreas para modificar.")
        return

    codigo = leer_codigo("Código del área (C=cancelar): ",
                         permitir_cancelar=True)
    if codigo is None:
        print("Modificación cancelada.")
        return
    posicion = buscar_area(codigo)

    if posicion == -1:
        print("Error: no existe un área con ese código.")
        return

    nombre_actual = areas[posicion][1]
    print(f"Nombre actual: {nombre_actual}")

    nuevo_nombre = leer_texto(
        "Nuevo nombre (Enter=conservar, C=cancelar): ",
        1, 40, valor_actual=nombre_actual, permitir_cancelar=True
    )
    if nuevo_nombre is None:
        print("Modificación cancelada.")
        return

    if nuevo_nombre == nombre_actual:
        print("El nombre se conserva sin cambios.")
        return

    if not confirmar_dato("el nuevo nombre", nuevo_nombre):
        print("Modificación cancelada.")
        return

    areas[posicion] = (codigo, nuevo_nombre)
    print("Área modificada correctamente.")


def eliminar_area():
    """Elimina un área existente si no tiene contactos asociados."""
    global area_predeterminada

    print("\nELIMINAR ÁREA")

    if not areas:
        print("No hay áreas para eliminar.")
        return

    codigo = leer_codigo("Código del área (C=cancelar): ",
                         permitir_cancelar=True)
    if codigo is None:
        print("Eliminación cancelada.")
        return
    posicion = buscar_area(codigo)

    if posicion == -1:
        print("Error: no existe un área con ese código.")
        return

    if any(contacto[1] == codigo for contacto in contactos):
        print(
            "No se puede eliminar el área porque tiene contactos asociados."
        )
        return

    print(f"Área seleccionada: {areas[posicion][1]} (código {codigo})")
    confirmacion = input(
        "¿Eliminar esta área? (A=aceptar/C=cancelar): "
    ).strip().upper()

    if confirmacion == "A":
        areas.pop(posicion)
        if area_predeterminada == codigo:
            area_predeterminada = None
        print("Área eliminada correctamente.")
    elif confirmacion == "C":
        print("Operación cancelada.")
    else:
        print("Opción no válida; el área no se eliminó.")


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


def configuracion():
    """Actualiza en una sola operación los valores predeterminados."""

    global area_predeterminada, tipo_telefono_predeterminado

    print("\nCONFIGURACIÓN DE LISTA DE CONTACTOS")
    if area_predeterminada is None:
        area_actual = "No configurada"
    else:
        posicion = buscar_area(area_predeterminada)
        area_actual = (
            areas[posicion][1] if posicion != -1 else "No disponible"
        )
    tipo_actual = nombre_tipo_telefono(tipo_telefono_predeterminado)
    if tipo_actual == "Desconocido":
        tipo_actual = "No configurado"

    print(f"Área predeterminada actual: {area_actual}")
    print(f"Tipo de teléfono actual: {tipo_actual}")

    nueva_area = area_predeterminada
    nueva_tipo = tipo_telefono_predeterminado

    if areas:
        consultar_areas(mostrar_detalle=False)
        while True:
            entrada = input(
                "Nuevo código de área (Enter=conservar, C=cancelar): "
            ).strip()
            if entrada.upper() == "C":
                print("Configuración cancelada.")
                return
            if entrada == "":
                break
            if not es_numero_ascii(entrada):
                print("Ingrese únicamente dígitos ASCII.")
                continue
            codigo = int(entrada)
            if buscar_area(codigo) == -1:
                print("El área no existe. Intente de nuevo.")
                continue
            nueva_area = codigo
            break
    else:
        print("No hay áreas registradas; se conservará el valor actual.")

    print("\nTIPOS DE TELÉFONO")
    for codigo, nombre in TIPOS_TELEFONO:
        print(f"{codigo}. {nombre}")

    while True:
        entrada = input(
            "Nuevo tipo (Enter=conservar, 0=cancelar): "
        ).strip().upper()
        if entrada == "0":
            print("Configuración cancelada.")
            return
        if entrada == "":
            break
        if nombre_tipo_telefono(entrada) == "Desconocido":
            print("Tipo de teléfono no válido. Intente de nuevo.")
            continue
        nueva_tipo = entrada
        break

    area_propuesta = (
        str(nueva_area) if nueva_area is not None else "No configurada"
    )
    tipo_propuesto = nombre_tipo_telefono(nueva_tipo)
    if tipo_propuesto == "Desconocido":
        tipo_propuesto = "No configurado"

    print(f"Configuración propuesta: área {area_propuesta}, tipo {tipo_propuesto}.")
    confirmacion = input("¿Guardar la configuración? (A/C): ").strip().upper()
    if confirmacion == "A":
        area_predeterminada = nueva_area
        tipo_telefono_predeterminado = nueva_tipo
        print("Configuración guardada.")
    elif confirmacion == "C":
        print("Configuración cancelada; no se realizaron cambios.")
    else:
        print("Opción no válida; no se realizaron cambios.")

def agregar_contacto():
    """Registra un contacto y valida sus datos."""

    print("\nAGREGAR CONTACTO")

    if not areas:
        print("Primero debe registrar al menos un área.")
        return

    consultar_areas(mostrar_detalle=False)
    area_sugerida = (
        area_predeterminada
        if buscar_area(area_predeterminada) != -1
        else None
    )
    mensaje_codigo = "Código del área"
    if area_sugerida is not None:
        mensaje_codigo += f" [{area_sugerida}]"

    while True:
        telefono = leer_telefono(permitir_cancelar=True)
        if telefono is None:
            print("Registro de contacto cancelado.")
            return
        if not confirmar_dato("el teléfono", telefono):
            print("Registro de contacto cancelado.")
            return

        while True:
            entrada = input(
                f"{mensaje_codigo} (C=cancelar): "
            ).strip()
            if entrada.upper() == "C":
                print("Registro de contacto cancelado.")
                return
            if entrada == "" and area_sugerida is not None:
                codigo_area = area_sugerida
            elif not es_numero_ascii(entrada):
                print("Ingrese un código numérico ASCII.")
                continue
            else:
                codigo_area = int(entrada)

            if buscar_area(codigo_area) == -1:
                print("El área no existe. Intente de nuevo.")
                continue
            break

        if not confirmar_dato("el código del área", codigo_area):
            print("Registro de contacto cancelado.")
            return

        if buscar_contacto(telefono, codigo_area) != -1:
            print(
                "Ya existe un contacto con ese teléfono y área. "
                "Ingrese nuevamente el teléfono."
            )
            continue
        break

    sugerido = tipo_telefono_predeterminado
    if nombre_tipo_telefono(sugerido) != "Desconocido":
        while True:
            entrada = input(
                f"Tipo (M/C/T/O) [{sugerido}], 0=cancelar: "
            ).strip().upper()
            if entrada == "0":
                print("Registro de contacto cancelado.")
                return
            tipo = entrada or sugerido
            if nombre_tipo_telefono(tipo) != "Desconocido":
                break
            print("Tipo de teléfono no válido. Intente de nuevo.")
    else:
        tipo = leer_tipo_telefono(permitir_cancelar=True)
        if tipo is None:
            print("Registro de contacto cancelado.")
            return
    if not confirmar_dato("el tipo de teléfono", nombre_tipo_telefono(tipo)):
        print("Registro de contacto cancelado.")
        return

    nombre = leer_texto(
        "Nombre completo (1-50 caracteres, C=cancelar): ",
        1, 50, permitir_cancelar=True
    )
    if nombre is None or not confirmar_dato("el nombre", nombre):
        print("Registro de contacto cancelado.")
        return

    correo = leer_correo(permitir_cancelar=True)
    if correo is None or not confirmar_dato("el correo", correo):
        print("Registro de contacto cancelado.")
        return

    direccion = leer_texto(
        "Dirección física (máximo 80 caracteres, C=cancelar): ",
        0, 80, permitir_vacio=True, permitir_cancelar=True
    )
    if direccion is None or not confirmar_dato("la dirección", direccion):
        print("Registro de contacto cancelado.")
        return

    fecha = leer_fecha(permitir_cancelar=True)
    if fecha is None or not confirmar_dato("la fecha de nacimiento", fecha):
        print("Registro de contacto cancelado.")
        return

    pasatiempos = leer_texto(
        "Pasatiempos (máximo 60 caracteres, C=cancelar): ",
        0, 60, permitir_vacio=True, permitir_cancelar=True
    )
    if pasatiempos is None or not confirmar_dato("los pasatiempos", pasatiempos):
        print("Registro de contacto cancelado.")
        return

    notas = leer_texto(
        "Notas (máximo 60 caracteres, C=cancelar): ",
        0, 60, permitir_vacio=True, permitir_cancelar=True
    )
    if notas is None or not confirmar_dato("las notas", notas):
        print("Registro de contacto cancelado.")
        return

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


def modificar_contacto():
    """Permite modificar los datos de un contacto."""

    print("\nMODIFICAR CONTACTO")

    if not contactos:
        print("No hay contactos registrados.")
        return

    telefono = leer_telefono(permitir_cancelar=True)
    if telefono is None:
        print("Modificación cancelada.")
        return
    codigo_area = leer_codigo(
        "Código del área del contacto (C=cancelar): ",
        permitir_cancelar=True
    )
    if codigo_area is None:
        print("Modificación cancelada.")
        return
    posicion = buscar_contacto(telefono, codigo_area)

    if posicion == -1:
        print("No se encontró el contacto.")
        return

    while True:
        print("\n¿Qué dato desea modificar?")
        print("1. Nombre")
        print("2. Tipo de teléfono")
        print("3. Correo electrónico")
        print("4. Dirección")
        print("5. Fecha de nacimiento")
        print("6. Pasatiempos")
        print("7. Notas")
        print("0. Terminar")

        opcion = input("Seleccione una opción: ").strip()

        match opcion:
            case "1":
                nuevo = leer_texto(
                    "Nuevo nombre (Enter=conservar, C=volver): ",
                    1, 50, valor_actual=contactos[posicion][3],
                    permitir_cancelar=True
                )
                if nuevo is None:
                    continue
                if nuevo != contactos[posicion][3] and confirmar_dato(
                    "el nuevo nombre", nuevo
                ):
                    contactos[posicion][3] = nuevo

            case "2":
                nuevo = leer_tipo_telefono(
                    permitir_cancelar=True,
                    valor_actual=contactos[posicion][2]
                )
                if nuevo is not None and nuevo != contactos[posicion][2]:
                    if confirmar_dato(
                        "el nuevo tipo", nombre_tipo_telefono(nuevo)
                    ):
                        contactos[posicion][2] = nuevo

            case "3":
                nuevo = leer_correo(
                    permitir_cancelar=True,
                    valor_actual=contactos[posicion][4]
                )
                if nuevo is not None and nuevo != contactos[posicion][4]:
                    if confirmar_dato("el nuevo correo", nuevo):
                        contactos[posicion][4] = nuevo

            case "4":
                nuevo = leer_texto(
                    "Nueva dirección (Enter=conservar, C=volver): ",
                    0, 80, permitir_vacio=True,
                    valor_actual=contactos[posicion][5],
                    permitir_cancelar=True
                )
                if nuevo is not None and nuevo != contactos[posicion][5]:
                    if confirmar_dato("la nueva dirección", nuevo):
                        contactos[posicion][5] = nuevo

            case "5":
                nuevo = leer_fecha(
                    permitir_cancelar=True,
                    valor_actual=contactos[posicion][6]
                )
                if nuevo is not None and nuevo != contactos[posicion][6]:
                    if confirmar_dato("la nueva fecha", nuevo):
                        contactos[posicion][6] = nuevo

            case "6":
                nuevo = leer_texto(
                    "Nuevos pasatiempos (Enter=conservar, C=volver): ",
                    0, 60, permitir_vacio=True,
                    valor_actual=contactos[posicion][7],
                    permitir_cancelar=True
                )
                if nuevo is not None and nuevo != contactos[posicion][7]:
                    if confirmar_dato("los nuevos pasatiempos", nuevo):
                        contactos[posicion][7] = nuevo

            case "7":
                nuevo = leer_texto(
                    "Nuevas notas (Enter=conservar, C=volver): ",
                    0, 60, permitir_vacio=True,
                    valor_actual=contactos[posicion][8],
                    permitir_cancelar=True
                )
                if nuevo is not None and nuevo != contactos[posicion][8]:
                    if confirmar_dato("las nuevas notas", nuevo):
                        contactos[posicion][8] = nuevo

            case "0":
                print("Modificación finalizada.")
                return

            case _:
                print("Opción no válida.")


def consultar_contacto():
    """Busca y muestra un contacto por teléfono y código de área."""
    print("\nCONSULTAR CONTACTO")

    if not contactos:
        print("No hay contactos registrados.")
        return

    while True:
        telefono = leer_telefono(permitir_cancelar=True)
        if telefono is None:
            print("Consulta cancelada.")
            return
        codigo_area = leer_codigo(
            "Código del área del contacto (C=cancelar): ",
            permitir_cancelar=True
        )
        if codigo_area is None:
            print("Consulta cancelada.")
            return

        posicion = buscar_contacto(telefono, codigo_area)
        if posicion != -1:
            mostrar_contacto(contactos[posicion])
            input("Presione Enter para aceptar y volver...")
            return

        print("No se encontró el contacto. Intente nuevamente o cancele.")


def eliminar_contacto():
    """Elimina un contacto seleccionado por teléfono y área."""

    print("\nELIMINAR CONTACTO")

    if not contactos:
        print("No hay contactos registrados.")
        return

    telefono = leer_telefono(permitir_cancelar=True)
    if telefono is None:
        print("Eliminación cancelada.")
        return
    codigo_area = leer_codigo(
        "Código del área del contacto (C=cancelar): ",
        permitir_cancelar=True
    )
    if codigo_area is None:
        print("Eliminación cancelada.")
        return
    posicion = buscar_contacto(telefono, codigo_area)

    if posicion == -1:
        print("No se encontró el contacto.")
        return

    print("\nContacto que se eliminará:")
    mostrar_contacto(contactos[posicion])
    confirmacion = input(
        "¿Eliminar este contacto? (A=aceptar/C=cancelar): "
    ).strip().upper()

    if confirmacion == "A":
        referencia = (telefono, codigo_area)
        for contactos_grupo in contactos_por_grupo:
            while referencia in contactos_grupo:
                contactos_grupo.remove(referencia)

        contactos.pop(posicion)
        print("Contacto eliminado correctamente.")
    elif confirmacion == "C":
        print("Operación cancelada.")
    else:
        print("Opción no válida; el contacto no se eliminó.")


def menu_contactos():
    """Muestra el menú de administración de contactos."""

    while True:
        print("\nADMINISTRACIÓN DE CONTACTOS")
        print("1. Agregar contacto")
        print("2. Consultar contactos")
        print("3. Modificar contacto")
        print("4. Eliminar contacto")
        print("0. Volver al menú principal")

        opcion = input("Seleccione una opción: ").strip()

        match opcion:
            case "1":
                agregar_contacto()
            case "2":
                consultar_contacto()
            case "3":
                modificar_contacto()
            case "4":
                eliminar_contacto()
            case "0":
                break
            case _:
                print("Opción no válida.")





def buscar_grupo(nombre):
    """Devuelve la posición de un grupo o -1 si no existe."""
    for posicion, grupo in enumerate(grupos):
        if grupo.casefold() == nombre.casefold():
            return posicion
    return -1


def crear_grupo():
    """Crea un grupo con un nombre único."""

    while True:
        nombre = leer_texto(
            "Nombre del grupo (1-40 caracteres, C=cancelar): ",
            1, 40, permitir_cancelar=True
        )
        if nombre is None:
            print("Creación de grupo cancelada.")
            return
        if buscar_grupo(nombre) == -1:
            break
        print("Ya existe un grupo con ese nombre. Intente nuevamente.")

    if not confirmar_dato("el nombre del grupo", nombre):
        print("Creación de grupo cancelada.")
        return

    grupos.append(nombre)
    contactos_por_grupo.append([])
    print("Grupo creado correctamente.")


def modificar_grupo():
    """Modifica el nombre de un grupo existente."""
    if not grupos:
        print("No hay grupos para modificar.")
        return

    consultar_grupos()
    nombre_actual = input(
        "\nNombre del grupo que desea modificar (C=cancelar): "
    ).strip()
    if nombre_actual.upper() == "C":
        print("Modificación cancelada.")
        return

    posicion = buscar_grupo(nombre_actual)

    if posicion == -1:
        print("No existe un grupo con ese nombre.")
        return

    nuevo_nombre = leer_texto(
        "Nuevo nombre (Enter=conservar, C=cancelar): ",
        1, 40, valor_actual=grupos[posicion], permitir_cancelar=True
    )
    if nuevo_nombre is None:
        print("Modificación cancelada.")
        return

    if nuevo_nombre == grupos[posicion]:
        print("El nombre se conserva sin cambios.")
        return

    if not confirmar_dato("el nuevo nombre", nuevo_nombre):
        print("Modificación cancelada.")
        return

    posicion_existente = buscar_grupo(nuevo_nombre)
    if posicion_existente != -1 and posicion_existente != posicion:
        nombre_destino = grupos[posicion_existente]
        for referencia in contactos_por_grupo[posicion]:
            if referencia not in contactos_por_grupo[posicion_existente]:
                contactos_por_grupo[posicion_existente].append(referencia)
        grupos.pop(posicion)
        contactos_por_grupo.pop(posicion)
        print(
            f"Grupo fusionado con «{nombre_destino}»; "
            "sus contactos se combinaron sin duplicados."
        )
        return

    grupos[posicion] = nuevo_nombre
    print("Grupo modificado correctamente.")


def consultar_grupos():
    """Muestra los grupos registrados y sus contactos."""

    if not grupos:
        print("No hay grupos registrados.")
        return

    for posicion, nombre in enumerate(grupos):
        print(f"\nGrupo: {nombre}")

        if not contactos_por_grupo[posicion]:
            print("  Sin contactos asociados.")
            continue

        for telefono, codigo_area in contactos_por_grupo[posicion]:
            pos = buscar_contacto(telefono, codigo_area)

            if pos != -1:
                print(f"  {contactos[pos][3]} - Teléfono: {telefono}")
            else:
                print(f"  Contacto no disponible - Teléfono: {telefono}")


def agregar_contacto_a_grupo():
    """Asocia un contacto existente a un grupo."""

    if not grupos:
        print("Primero debe crear un grupo.")
        return

    if not contactos:
        print("Primero debe registrar un contacto.")
        return

    consultar_grupos()
    nombre = input("\nNombre del grupo (C=cancelar): ").strip()
    if nombre.upper() == "C":
        print("Asociación cancelada.")
        return
    posicion_grupo = buscar_grupo(nombre)

    if posicion_grupo == -1:
        print("No existe un grupo con ese nombre.")
        return

    while True:
        telefono = leer_telefono(permitir_cancelar=True)
        if telefono is None:
            print("Asociación cancelada.")
            return
        codigo_area = leer_codigo(
            "Código del área del contacto (C=cancelar): ",
            permitir_cancelar=True
        )
        if codigo_area is None:
            print("Asociación cancelada.")
            return

        posicion_contacto = buscar_contacto(telefono, codigo_area)
        if posicion_contacto != -1:
            break
        print("No existe ese contacto. Intente nuevamente o cancele.")

    referencia = (telefono, codigo_area)

    if referencia in contactos_por_grupo[posicion_grupo]:
        print("El contacto ya pertenece a ese grupo.")
        return

    print("\nContacto seleccionado:")
    mostrar_contacto(contactos[posicion_contacto])
    if not confirmar_dato("la asociación al grupo", grupos[posicion_grupo]):
        print("Asociación cancelada.")
        return

    contactos_por_grupo[posicion_grupo].append(referencia)
    print("Contacto agregado al grupo correctamente.")


def quitar_contacto_de_grupo():
    """Quita un contacto de un grupo sin eliminarlo de la lista general."""

    if not grupos:
        print("No hay grupos registrados.")
        return

    consultar_grupos()
    nombre = input("\nNombre del grupo (C=cancelar): ").strip()
    if nombre.upper() == "C":
        print("Eliminación de asociación cancelada.")
        return
    posicion_grupo = buscar_grupo(nombre)

    if posicion_grupo == -1:
        print("No existe un grupo con ese nombre.")
        return

    telefono = leer_telefono(permitir_cancelar=True)
    if telefono is None:
        print("Eliminación de asociación cancelada.")
        return
    codigo_area = leer_codigo(
        "Código del área del contacto (C=cancelar): ",
        permitir_cancelar=True
    )
    if codigo_area is None:
        print("Eliminación de asociación cancelada.")
        return
    referencia = (telefono, codigo_area)

    if referencia not in contactos_por_grupo[posicion_grupo]:
        print("Ese contacto no pertenece al grupo.")
        return

    posicion_contacto = buscar_contacto(telefono, codigo_area)
    if posicion_contacto != -1:
        mostrar_contacto(contactos[posicion_contacto])
    confirmacion = input(
        "¿Quitar este contacto del grupo? (A=aceptar/C=cancelar): "
    ).strip().upper()
    if confirmacion != "A":
        print("Operación cancelada.")
        return

    contactos_por_grupo[posicion_grupo].remove(referencia)
    print("Contacto quitado del grupo.")


def eliminar_grupo():
    """Elimina un grupo y su lista de asociaciones."""

    if not grupos:
        print("No hay grupos para eliminar.")
        return

    consultar_grupos()
    nombre = input(
        "\nNombre del grupo que desea eliminar (C=cancelar): "
    ).strip()
    if nombre.upper() == "C":
        print("Eliminación cancelada.")
        return
    posicion = buscar_grupo(nombre)

    if posicion == -1:
        print("No existe un grupo con ese nombre.")
        return

    confirmacion = input(
        f"¿Eliminar el grupo «{grupos[posicion]}»? (A/C): "
    ).strip().upper()

    if confirmacion == "A":
        grupos.pop(posicion)
        contactos_por_grupo.pop(posicion)
        print("Grupo eliminado correctamente.")
    elif confirmacion == "C":
        print("Operación cancelada.")
    else:
        print("Opción no válida; el grupo no se eliminó.")


def menu_grupos():
    """Muestra el menú de administración de grupos."""

    while True:
        print("\nADMINISTRAR GRUPOS DE CONTACTOS")
        print("1. Crear grupo")
        print("2. Consultar grupos")
        print("3. Agregar contacto a grupo")
        print("4. Quitar contacto de grupo")
        print("5. Modificar grupo")
        print("6. Eliminar grupo")
        print("0. Volver al menú principal")

        opcion = input("Seleccione una opción: ").strip()

        match opcion:
            case "1":
                crear_grupo()
            case "2":
                consultar_grupos()
            case "3":
                agregar_contacto_a_grupo()
            case "4":
                quitar_contacto_de_grupo()
            case "5":
                modificar_grupo()
            case "6":
                eliminar_grupo()
            case "0":
                break
            case _:
                print("Opción no válida.")


def coincide_filtro(valor, filtro):
    """Compara un valor con un filtro que admite % como comodín."""

    filtro = filtro.strip()

    if filtro == "":
        return True

    patron = re.escape(filtro).replace("%", ".*")

    return re.fullmatch(
        patron,
        str(valor),
        flags=re.IGNORECASE
    ) is not None



def generar_pdf(contactos_filtrados):
    """Genera un PDF con los contactos seleccionados."""

    documento = SimpleDocTemplate(
        "contactos.pdf",
        pagesize=landscape(A4),
        rightMargin=1 * cm,
        leftMargin=1 * cm,
        topMargin=1 * cm,
        bottomMargin=1 * cm
    )

    estilos = getSampleStyleSheet()
    contenido = [
        Paragraph("Lista de contactos", estilos["Title"]),
        Spacer(1, 0.4 * cm)
    ]

    encabezados = [
        "Nombre", "Teléfono", "Área", "Tipo",
        "Correo", "Dirección", "Nacimiento",
        "Pasatiempos", "Notas"
    ]

    datos = [encabezados]

    for contacto in contactos_filtrados:
        telefono, codigo_area, tipo, nombre, correo, direccion, fecha, pasatiempos, notas = contacto

        posicion_area = buscar_area(codigo_area)

        if posicion_area != -1:
            nombre_area = areas[posicion_area][1]
        else:
            nombre_area = "Área no disponible"

        fila = [
            nombre,
            str(telefono),
            f"{nombre_area} ({codigo_area})",
            nombre_tipo_telefono(tipo),
            correo,
            direccion,
            fecha,
            pasatiempos,
            notas
        ]

        datos.append([
            Paragraph(escape(str(valor)), estilos["BodyText"])
            for valor in fila
        ])

    tabla = Table(datos, repeatRows=1)

    tabla.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("FONTSIZE", (0, 0), (-1, -1), 7),
    ]))

    contenido.append(tabla)
    try:
        documento.build(contenido)
    except PermissionError:
        print(
            "No se pudo guardar contactos.pdf. Cierre el archivo PDF si está "
            "abierto e intente nuevamente."
        )
        return
    except OSError as error:
        print(f"No se pudo generar contactos.pdf: {error}")
        return

    print("PDF generado: contactos.pdf")


def lista_contactos():
    """Muestra y filtra los contactos y permite generar un PDF con ellos."""

    print("\nLISTA DE CONTACTOS")

    if not contactos:
        print("No hay contactos registrados.")
        return

    print("Dejá el filtro vacío para incluir cualquier valor.")
    print("Podés usar % como comodín. Ejemplo: Ana%")

    filtro_nombre = input("Filtrar por nombre: ")
    filtro_telefono = input("Filtrar por teléfono: ")
    filtro_area = input("Filtrar por área (código): ")
    filtro_fecha = input("Filtrar por fecha de nacimiento: ")
    filtro_pasatiempos = input("Filtrar por pasatiempos: ")
    filtro_grupo = input("Filtrar por grupo: ")

    contactos_filtrados = []

    for contacto in contactos:
        telefono, codigo_area, tipo, nombre, correo, direccion, fecha, pasatiempos, notas = contacto

        if not coincide_filtro(nombre, filtro_nombre):
            continue

        if not coincide_filtro(telefono, filtro_telefono):
            continue

        if not coincide_filtro(codigo_area, filtro_area):
            continue

        if not coincide_filtro(fecha, filtro_fecha):
            continue

        if not coincide_filtro(pasatiempos, filtro_pasatiempos):
            continue

        if filtro_grupo.strip():
            pertenece = False

            for posicion, grupo in enumerate(grupos):
                if coincide_filtro(grupo, filtro_grupo):
                    if any(
                        telefono_grupo == telefono
                        and area_grupo == codigo_area
                        for telefono_grupo, area_grupo
                        in contactos_por_grupo[posicion]
                    ):
                        pertenece = True
                        break

            if not pertenece:
                continue

        contactos_filtrados.append(contacto)

    if not contactos_filtrados:
        print("No se encontraron contactos con esos filtros.")
        return

    for numero, contacto in enumerate(contactos_filtrados, start=1):
        telefono, codigo_area, tipo, nombre, correo, direccion, fecha, pasatiempos, notas = contacto

        posicion_area = buscar_area(codigo_area)

        if posicion_area != -1:
            nombre_area = areas[posicion_area][1]
        else:
            nombre_area = "Área no disponible"

        print(f"\nCONTACTO {numero}")
        print(f"Nombre: {nombre}")
        print(f"Teléfono: {telefono}")
        print(f"Área: {nombre_area} (código {codigo_area})")
        print(f"Tipo de teléfono: {nombre_tipo_telefono(tipo)}")
        print(f"Correo: {correo}")
        print(f"Dirección: {direccion}")
        print(f"Fecha de nacimiento: {fecha}")
        print(f"Pasatiempos: {pasatiempos}")
        print(f"Notas: {notas}")

    while True:
        opcion_pdf = input(
            "\n¿Desea generar el PDF de estos contactos? (A/C): "
        ).strip().upper()
        if opcion_pdf == "A":
            generar_pdf(contactos_filtrados)
            break
        if opcion_pdf == "C":
            print("Generación del PDF cancelada.")
            break
        print("Opción no válida. Escriba A para generar o C para cancelar.")

def ayuda():


    """Muestra el manual de usuario del programa."""

    print("\n" + "=" * 55)
    print("       MANUAL DE USUARIO")
    print("       LISTA DIGITAL DE CONTACTOS")
    print("=" * 55)

    print("""

DESCRIPCIÓN
Este programa permite administrar áreas, configurar la lista
de contactos, registrar contactos, crear grupos y consultar
contactos por sus datos. También permite filtrar la lista y
generar un PDF.

MENÚ PRINCIPAL
1. Registrar áreas:
   Agrega áreas con código único, consulta por código, modifica
   el nombre y elimina áreas que no tengan contactos asociados.
   En los formularios puede escribir C para cancelar. Para
   conservar un valor durante una modificación, presione Enter.

2. Configuración de lista de contactos:
   Configura en una pantalla el área y el tipo de teléfono
   predeterminados. Enter conserva el valor actual; A guarda y
   C descarta la configuración propuesta.

3. Registrar contactos:
   Agrega contactos con validación de datos, consulta por
   teléfono y código de área, modifica campos y elimina
   contactos después de mostrar sus datos. Las modificaciones
   se confirman campo por campo. Al eliminar un contacto también
   se quitan sus referencias de los grupos.

4. Administrar grupos de contactos:
   Permite crear, consultar, renombrar, fusionar y eliminar
   grupos, además de agregar o quitar contactos. Al renombrar
   hacia un grupo existente, se fusionan las asociaciones sin
   duplicar contactos. Quitar una asociación requiere confirmar.

5. Lista de contactos:
   Filtra la lista y ofrece generar contactos.pdf con los
   resultados. La generación del PDF se puede aceptar o
   cancelar.

6. Ayuda:
   Muestra este manual de usuario.

7. Acerca de:
   Muestra la información del programa y su autor.

0. Fin:
   Termina la ejecución del programa.

USO DE LOS FILTROS
Al consultar la lista, escriba un valor para filtrar por nombre,
teléfono, código de área, fecha, pasatiempos o grupo. Deje el
campo vacío para no aplicar ese criterio.

El símbolo % representa cero o más caracteres. Sin comodines,
el valor debe coincidir exactamente. Las búsquedas no distinguen
entre mayúsculas y minúsculas.

VALIDACIÓN
Los códigos de área aceptan dígitos ASCII entre 1 y 999. Los
teléfonos deben contener entre 5 y 12 dígitos ASCII. Se valida
el formato del correo, las fechas reales y los límites de
longitud de los campos de texto. Escriba C en los campos que
ofrecen cancelación para abandonar la operación. En el selector
de tipo telefónico, C es un tipo válido (Casa), por lo que 0
se usa para cancelar esa selección.

GENERACIÓN DE PDF
Cuando una búsqueda encuentra contactos, el programa pregunta
si desea generar contactos.pdf en el directorio de ejecución.
Si el archivo está abierto y no se puede sobrescribir, ciérrelo
y vuelva a intentar.

RECOMENDACIONES
- Registre las áreas antes de asignarlas a los contactos.
- Configure los valores predeterminados para agilizar el alta.
- Confirme cada dato antes de guardarlo.
- Utilice la consulta por teléfono y área para ver un contacto.
- Use los filtros para localizar información específica.
- Cierre el PDF antes de generar una nueva versión.

""")

    input("Presioná Enter para volver al menú principal...")


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
