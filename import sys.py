import sys
import heapq

class Nodo():
    def __init__(self, estado, padre, accion, costo=0):
        self.estado = estado
        self.padre = padre
        self.accion = accion
        self.costo = costo

    def __lt__(self, otro):
        return self.costo < otro.costo

class FronteraStack():
    def __init__(self):
        self.frontera = []

    def agregar(self, nodo):
        self.frontera.append(nodo)

    def contiene_estado(self, estado):
        return any(nodo.estado == estado for nodo in self.frontera)

    def vacia(self):
        return len(self.frontera) == 0

    def quitar(self):
        if self.vacia():
            raise Exception("frontera vacía")
        else:
            return self.frontera.pop()

class FronteraCola(FronteraStack):
    def quitar(self):
        if self.vacia():
            raise Exception("frontera vacía")
        else:
            return self.frontera.pop(0)

class FronteraColaPrioridad(FronteraStack):
    def __init__(self):
        self.frontera = []

    def agregar(self, nodo):
        heapq.heappush(self.frontera, (nodo.costo, nodo))

    def quitar(self):
        if self.vacia():
            raise Exception("frontera vacía")
        else:
            return heapq.heappop(self.frontera)[1]

class Laberinto():
    def __init__(self, filename):
        with open(filename) as f:
            contenido = f.read().splitlines()

        self.altura = len(contenido)
        self.ancho = max(len(linea) for linea in contenido)

        self.paredes = []
        for i in range(self.altura):
            fila = []
            for j in range(self.ancho):
                if j < len(contenido[i]):
                    if contenido[i][j] == "A":
                        self.inicio = (i, j)
                        fila.append(False)
                    elif contenido[i][j] == "B":
                        self.meta = (i, j)
                        fila.append(False)
                    elif contenido[i][j] == " ":
                        fila.append(False)
                    else:
                        fila.append(True)
                else:
                    fila.append(False)
            self.paredes.append(fila)

        self.solucion = None

    def vecinos(self, estado):
        fila, col = estado
        candidatos = [
            ("arriba", (fila - 1, col)),
            ("abajo", (fila + 1, col)),
            ("izquierda", (fila, col - 1)),
            ("derecha", (fila, col + 1))
        ]

        resultado = []
        for accion, (f, c) in candidatos:
            if 0 <= f < self.altura and 0 <= c < self.ancho and not self.paredes[f][c]:
                resultado.append((accion, (f, c)))
        return resultado

    def costo_heuristico(self, estado):
        return abs(estado[0] - self.meta[0]) + abs(estado[1] - self.meta[1])

    def resolver(self, algoritmo='dfs'):
        self.num_explorados = 0
        inicio = Nodo(estado=self.inicio, padre=None, accion=None)
        
        if algoritmo == 'dfs':
            frontera = FronteraStack()
        elif algoritmo == 'bfs':
            frontera = FronteraCola()
        elif algoritmo == 'astar':
            frontera = FronteraColaPrioridad()
            inicio.costo = self.costo_heuristico(inicio.estado)
        else:
            raise ValueError("Algoritmo inválido")

        frontera.agregar(inicio)
        self.explorado = set()

        while True:
            if frontera.vacia():
                raise Exception("No hay solución")

            nodo = frontera.quitar()
            self.num_explorados += 1

            if nodo.estado == self.meta:
                acciones = []
                celdas = []
                while nodo.padre is not None:
                    acciones.append(nodo.accion)
                    celdas.append(nodo.estado)
                    nodo = nodo.padre
                acciones.reverse()
                celdas.reverse()
                self.solucion = (acciones, celdas)
                return

            self.explorado.add(nodo.estado)

            for accion, estado in self.vecinos(nodo.estado):
                if not frontera.contiene_estado(estado) and estado not in self.explorado:
                    hijo = Nodo(estado=estado, padre=nodo, accion=accion)
                    if algoritmo == 'astar':
                        hijo.costo = nodo.costo + 1 + self.costo_heuristico(estado)
                    frontera.agregar(hijo)

    def imprimir(self):
        solucion = self.solucion[1] if self.solucion is not None else None
        for i, fila in enumerate(self.paredes):
            for j, es_pared in enumerate(fila):
                if es_pared:
                    print("#", end="")
                elif (i, j) == self.inicio:
                    print("A", end="")
                elif (i, j) == self.meta:
                    print("B", end="")
                elif solucion is not None and (i, j) in solucion:
                    print("*", end="")
                else:
                    print(" ", end="")
            print()

def main():
    if len(sys.argv) != 2:
        sys.exit("Uso: python laberinto.py archivo_laberinto.txt")

    laberinto = Laberinto(sys.argv[1])
    print("Laberinto cargado:")
    laberinto.imprimir()

    while True:
        print("\nElija un algoritmo:")
        print("1. DFS (Búsqueda en Profundidad)")
        print("2. BFS (Búsqueda en Amplitud)")
        print("3. A*")
        print("4. Salir")
        
        opcion = input("Ingrese su elección (1-4): ")
        
        if opcion == '1':
            algoritmo = 'dfs'
        elif opcion == '2':
            algoritmo = 'bfs'
        elif opcion == '3':
            algoritmo = 'astar'
        elif opcion == '4':
            print("Saliendo...")
            break
        else:
            print("Opción inválida. Intente de nuevo.")
            continue
        
        print(f"\nResolviendo con {algoritmo.upper()}...")
        laberinto.resolver(algoritmo)
        print(f"Estados explorados: {laberinto.num_explorados}")
        print("Solución:")
        laberinto.imprimir()

if __name__ == "__main__":
    main()