import threading
import time
import random


class FilosofosComensal:
    def __init__(self, num_filosofos=5):
        self.num_filosofos = num_filosofos
        self.tenedores = [threading.Lock() for _ in range(num_filosofos)]
        self.estado_filosofos = ['PENSANDO'] * num_filosofos
        self.estado_lock = threading.Lock()

    def obtener_tenedores(self, filosofo):
        tenedor_izq = filosofo
        tenedor_der = (filosofo + 1) % self.num_filosofos

        # Intenta tomar ambos tenedores o ninguno para evitar deadlock
        with self.estado_lock:
            while self.estado_filosofos[filosofo] != 'COMIENDO':
                if (self.estado_filosofos[(filosofo - 1) % self.num_filosofos] != 'COMIENDO' and
                        self.estado_filosofos[(filosofo + 1) % self.num_filosofos] != 'COMIENDO'):

                    if self.tenedores[tenedor_izq].acquire(blocking=False):
                        if self.tenedores[tenedor_der].acquire(blocking=False):
                            self.estado_filosofos[filosofo] = 'COMIENDO'
                            break
                        else:
                            self.tenedores[tenedor_izq].release()
                time.sleep(0.1)

    def liberar_tenedores(self, filosofo):
        tenedor_izq = filosofo
        tenedor_der = (filosofo + 1) % self.num_filosofos

        with self.estado_lock:
            self.estado_filosofos[filosofo] = 'PENSANDO'
            self.tenedores[tenedor_izq].release()
            self.tenedores[tenedor_der].release()

    def filosofo(self, id_filosofo):
        while True:
            # Pensando
            tiempo_pensando = random.uniform(1, 3)
            print(f"Filósofo {id_filosofo} está pensando por {tiempo_pensando:.1f} segundos")
            time.sleep(tiempo_pensando)

            # Hambriento
            print(f"Filósofo {id_filosofo} tiene hambre y quiere comer")
            self.obtener_tenedores(id_filosofo)

            # Comiendo
            tiempo_comiendo = random.uniform(1, 3)
            print(f"Filósofo {id_filosofo} está comiendo por {tiempo_comiendo:.1f} segundos")
            time.sleep(tiempo_comiendo)

            # Terminó de comer
            self.liberar_tenedores(id_filosofo)
            print(f"Filósofo {id_filosofo} terminó de comer y vuelve a pensar")

    def iniciar_simulacion(self):
        filosofos = []
        for i in range(self.num_filosofos):
            filosofo = threading.Thread(target=self.filosofo, args=(i,))
            filosofo.daemon = True
            filosofos.append(filosofo)

        for f in filosofos:
            f.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nFinalizando simulación...")


if __name__ == "__main__":
    simulacion = FilosofosComensal(5)
    simulacion.iniciar_simulacion()