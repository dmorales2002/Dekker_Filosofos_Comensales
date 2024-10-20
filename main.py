import os
import threading
import time
from distutils.command.clean import clean

flag = []  # Banderas de hilos
turn = 0  # Indica quién entra en la sección crítica
lock = threading.Lock()  # Bloquea la sección crítica cuando está en uso


class Proceso(threading.Thread):
    def __init__(self, id, Cant_procesos, tiempo):
        threading.Thread.__init__(self)
        self.id = id  # ID del hilo (0 o 1)
        self.Cant_procesos = Cant_procesos

    def run(self):
        global flag, turn
        for i in range(self.Cant_procesos):
            flag[self.id] = True  # Hilo 'id' quiere entrar

            # Algoritmo de Dekker para esperar si no es el turno de este hilo
            while flag[1 - self.id]:
                with lock:
                    if turn != self.id:  # Si no es mi turno
                        flag[self.id] = False  # Cedo el turno
                        while turn != self.id:  # Espera activa
                            pass
                        flag[self.id] = True  # Retomo mi intención de entrar

            # Sección crítica
            self.criticalSection(tiempo)

            # Sección de salida
            with lock:
                turn = 1 - self.id  # Cedo el turno al otro hilo
            flag[self.id] = False  # Salgo de la sección crítica

            # Sección no crítica
            self.nonCriticalSection(tiempo)

    def criticalSection(self, tiempo):
        # Simulación de una operación crítica
        print(f"{threading.current_thread().name} está en la sección crítica.")
        time.sleep(tiempo)  # Simula el tiempo de alguna tarea en la sección crítica

    def nonCriticalSection(self, tiempo):
        # Simulación de una operación no crítica
        print(f"{threading.current_thread().name} está en la sección NO crítica.")
        time.sleep(tiempo)  # Tiempo que tarda en la sección no crítica


def ejecutarProcesos(Idproceso, cantProceso, tiempos):
    for i in range(len(Idproceso)):
        t = Proceso(Idproceso[i], cantProceso[i], tiempos[i])  # Crea el nuemero de hilos
        t.start()  # Inicia el proceso
        t.join()  # Espera que termine el proceso





if __name__ == "__main__":
    # Se solicitan los datos de los procesos y el hilo que se ejecuta
    procesos_agregados = []
    cant_prosess_ejecut = []
    tiempos = []

    while True:
        try:
            # Solicita el ID del proceso
            num = int(input("Ingrese el número de ID del proceso: "))

            # Verifica si el ID del proceso ya está agregado a la lista
            if num in procesos_agregados:
                raise ValueError("El ID del proceso ya está agregado.")
            else:
                procesos_agregados.append(num)
                flag.append(False)

            # Solicita la cantidad de procesos para ese ID
            pros = int(input("Ingrese la cantidad de procesos a ejecutar: "))
            cant_prosess_ejecut.append(pros)  # agrega a una lista los procesos a ejecutar

            # Solicita el tiempo que desea que se tarde el proceso
            tiempo = float(input("Ingrese el tiempo que dese que tarde el proceso en segundos: "))
            tiempos.append(tiempo)

            pregunta = int(input("Si desea agregar otro proceso ingres '1' si no precione cualquier tecla: "))

            if pregunta != 1:
                ejecutarProcesos(procesos_agregados, cant_prosess_ejecut, tiempos)
                break  # Sale del ciclo cuando los procesos terminan correctamente

        except ValueError as ve:
            print(ve)
            print("Por favor, ingrese un nuevo ID que no esté agregado.")
