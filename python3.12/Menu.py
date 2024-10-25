import Dekker
import Filosofos_Comensales

# menu_principal.py
def mostrar_menu():
    while True:
        print("\n=== MENÚ PRINCIPAL ===")
        print("1. Ir al Algoritmo de dekker")
        print("2. Ir a Filosofos comensales")
        print("3. Salir")

        opcion = input("\nSeleccione una opción (1-3): ")

        if opcion == "1":
            Dekker.inicio()
        elif opcion == "2":
            Filosofos_Comensales.inicio()
        elif opcion == "3":
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida. Por favor, intente nuevamente.")


if __name__ == "__main__":
    mostrar_menu()

