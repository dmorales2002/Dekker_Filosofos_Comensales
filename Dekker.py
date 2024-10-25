import threading
import time

mensaje = []


class DekkerLock:
    def __init__(self):
        # Flags para indicar si un proceso quiere entrar a la sección crítica
        self.flag = [False, False]
        # Variable para indicar de quién es el turno
        self.turn = 0

    def lock(self, process_id):
        other = 1 - process_id  # ID del otro proceso

        # Indica que este proceso quiere entrar
        self.flag[process_id] = True

        # Mientras el otro proceso también quiera entrar
        while self.flag[other]:
            # Si no es nuestro turno
            if self.turn != process_id:
                # Bajamos nuestra bandera y esperamos nuestro turno
                self.flag[process_id] = False
                while self.turn != process_id:
                    time.sleep(0.1)  # Espera activa
                # Volvemos a levantar nuestra bandera
                self.flag[process_id] = True

    def unlock(self, process_id):
        # Cambiamos el turno al otro proceso
        self.turn = 1 - process_id
        # Bajamos nuestra bandera
        self.flag[process_id] = False


# Ejemplo de uso
def proceso_critico(lock, process_id, iterations, tiempo_ejecucion, tiempo_espera):
    for i in range(iterations):
        lock.lock(process_id)
        try:
            # Sección crítica
            print(f"Proceso {process_id} en sección crítica - iteración {i + 1}")
            mensaje.append(f"Proceso {process_id} en sección crítica - iteración {i + 1}")
            time.sleep(tiempo_ejecucion)  # Simulamos trabajo
        finally:
            lock.unlock(process_id)

        # Sección no crítica
        time.sleep(tiempo_espera)  # Simulamos otro trabajo


def inicio():
    # Solicitamos datos para ver los procesos que quiere ejecutar
    dkk1 = int(input("Ingrese la cantidad de procesoso a ejectar en el hilo 0: "))
    dkk2 = int(input("Ingrese la cantidad de procesoso a ejectar en el hilo 1: "))

    tmp_ejecucion = float(input("Ingrese el tiempo en segundos que quiere que dure la ejecucion del trabajo: "))
    tmp_espera = float(input("Ingrese el tiempo en segundos que quiere que dure la espera del siguiente trabajo: "))

    # Crear instancia del candado de Dekker
    dekker_lock = DekkerLock()

    # Crear y ejecutar dos hilos
    t1 = threading.Thread(target=proceso_critico, args=(dekker_lock, 0, dkk1, tmp_ejecucion, tmp_espera))
    t2 = threading.Thread(target=proceso_critico, args=(dekker_lock, 1, dkk2, tmp_ejecucion, tmp_espera))

    t1.start()
    t2.start()

    t1.join()
    t2.join()
