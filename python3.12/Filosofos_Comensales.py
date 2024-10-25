import threading
import time
import tkinter as tk

class Filosofo(threading.Thread):
    def __init__(self, mesa, id, left_palillo, right_palillo):
        threading.Thread.__init__(self)
        self.mesa = mesa
        self.id = id
        self.left_palillo = left_palillo
        self.right_palillo = right_palillo
        self.estado = 'Pensando'

    def run(self):
        while True:
            self.pensar()
            self.comer()

    def pensar(self):
        self.estado = 'Pensando'
        self.mesa.actualizar_estado(self.id, self.estado)
        time.sleep(2)

    def comer(self):
        self.estado = 'Hambriento'
        self.mesa.actualizar_estado(self.id, self.estado)
        with self.left_palillo.lock:
            with self.right_palillo.lock:
                self.estado = 'Comiendo'
                self.mesa.actualizar_estado(self.id, self.estado)
                time.sleep(2)

class Palillo:
    def __init__(self):
        self.lock = threading.Lock()

class Mesa:
    def __init__(self, root):
        self.root = root
        self.filosofos = []
        self.palillos = [Palillo() for _ in range(5)]
        self.estados = [tk.StringVar() for _ in range(5)]
        self.crear_interfaz()

    def crear_interfaz(self):
        self.canvas = tk.Canvas(self.root, width=400, height=400)
        self.canvas.pack()

        self.posiciones_filosofos = [
            (200, 50), (350, 150), (300, 300), (100, 300), (50, 150)
        ]
        self.circulos_filosofos = []
        self.textos_filosofos = []

        for i, pos in enumerate(self.posiciones_filosofos):
            x, y = pos
            circulo = self.canvas.create_oval(x-20, y-20, x+20, y+20, fill='white')
            texto = self.canvas.create_text(x, y, text=f'Filósofo {i+1}\nPensando')
            self.circulos_filosofos.append(circulo)
            self.textos_filosofos.append(texto)

    def actualizar_estado(self, id, estado):
        color = 'white'
        if estado == 'Pensando':
            color = 'white'
        elif estado == 'Hambriento':
            color = 'yellow'
        elif estado == 'Comiendo':
            color = 'green'

        self.canvas.itemconfig(self.circulos_filosofos[id], fill=color)
        self.canvas.itemconfig(self.textos_filosofos[id], text=f'Filósofo {id+1}\n{estado}')
        self.root.update_idletasks()

    def iniciar(self):
        for i in range(5):
            filosofo = Filosofo(self, i, self.palillos[i], self.palillos[(i+1) % 5])
            self.filosofos.append(filosofo)
            filosofo.start()

def inicio():
    root = tk.Tk()
    root.title('Filosofos Comensales')
    mesa = Mesa(root)
    mesa.iniciar()
    root.mainloop()