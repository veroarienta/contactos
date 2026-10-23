

# LISTA DIGITAL DE CONTACTOS
############ IMPORT #############################

############ CLASES (P.O.O) ########################

############ VARIABLES GLOBALES ####################

areas = []

############ FUNCIONES ##############################

def menu_areas():
    """Muestra el menú para administrar las áreas."""
    while True:
        print("\nLISTA DIGITAL DE CONTACTOS")
        print("REGISTRAR ÁREAS")
        print()
        print("1. Agregar áreas")
        print("2. Consultar áreas")
        print("3. Modificar áreas")
        print("4. Eliminar áreas")
        print("0. Fin")
        print()

        opcion = input("OPCIÓN: ").strip()

        if opcion == "0":
            break

        elif opcion == "1":
            print("Agregar áreas")

        elif opcion == "2":
            print("Consultar áreas")

        elif opcion == "3":
            print("Modificar áreas")

        elif opcion == "4":
            print("Eliminar áreas")

        else:
            print("Opción no válida.")


############ FUNCION PRINCIPAL ########################

def principal():
    """Despliega el menú principal y procesa la opción elegida."""
    while True:
        print("\nLISTA DIGITAL DE CONTACTOS")
        print()
        print("1. Registrar áreas")
        print("2. Configuración de lista de contactos")
        print("3. Registrar contactos")
        print("4. Administrar grupos de contactos")
        print("5. Lista de contactos")
        print("6. Ayuda")
        print("7. Acerca de")
        print("0. Fin")
        print()

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "0":
            print("Fin del programa.")
            break

        elif opcion == "1":
            menu_areas()

        elif opcion == "2":
            print("Configuración de lista de contactos")

        elif opcion == "3":
            print("Registrar contactos")

        elif opcion == "4":
            print("Administrar grupos de contactos")

        elif opcion == "5":
            print("Lista de contactos")

        elif opcion == "6":
            print("Ayuda")

        elif opcion == "7":
            print("Acerca de")

        else:
            print("Opción no válida. Intente nuevamente.")


if __name__ == "__main__":
    principal()
