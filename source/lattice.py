"""
Contiene la clase Lattice

utilizado para plotear spins y para realizar diagramas de fases
"""

from queue import Queue

import numpy as np

class Lattice:
    """
    Clase que contiene la información de la red de spins, junto con un método 
    capaz de cargar la información a partir de los archivos de entrada.

    ATRIBUTOS:
    ----------
    spins : ndarray
        array 2D conteniendo las componentes de spin para cada átomo.
    position : ndarray
        array conteniendo las posiciones espaciales para cada átomo.
    vecinos : ndarray
        array conteniendo los vecinos más cercanos para cada átomo.
    n_atoms : int
        cantidad de átomos en la red.
    dimensions : ndarray
        array conteniendo la extensión espacial de la red, es decir, la distancia
        entre los puntos más lejanos para cada componente.
    size : float
        extensión máxima de la red en alguna dirección.
    sublattice : ndarray
        array conteniendo la sublattice de cada átomo. Toma valores +-1.
    MÉTODOS:
    --------
    __init__():
        Inicializa los atributos de la clase.
    load_files(structure_file, spin_file):
        Carga la configuración de la red y de los spins a partir de los archivos 
        de entrada especificados.
    make_sublattice():
        Método reservado para futuras implementaciones que generarán una subred 
        a partir de la red principal.
    """

    def __init__(self):
        """
        Inicializa los atributos de la clase con valores predeterminados.
        """

        self.spins = np.array([])
        self.position = np.array([])
        self.vecinos = np.array([])

        self.n_atoms = 0

        self.dimensions = np.zeros(3)
        self.size = 0

        self.sublattice = np.array([])

    def load_files(self, structure_file, spin_file):
        """
        Carga la información de la estructura de la red y la configuración de los 
        spins desde los archivos de entrada.

        Parámetros:
        -----------
        structure_file : str
            Ruta del archivo que contiene la estructura espacial de la red.
        spin_file : str
            Ruta del archivo que contiene la configuración de los spins.

        Ejecución:
        ----------
        1. Lee la estructura espacial desde el archivo `structure_file`.
        2. Lee la configuración de los spins desde el archivo `spin_file`.
        3. Almacena las posiciones, vecinos y spins de los átomos en los arrays 
           correspondientes.
        4. Calcula el tamaño de la red en base a las posiciones de los átomos.
        """

        try:
            # Leer archivo de estructura espacial
            with open(structure_file, 'r', encoding="utf-8") as file:
                lines = file.readlines()

            # Leer archivo de configuración de spins
            with open(spin_file, 'r', encoding="utf-8") as file:
                spin_lines = file.readlines()

        except FileNotFoundError as e:
            print(f"Error: {e}")
            return

        # definimos el numero de atomos en la estructura
        header_data = lines[0].split()
        self.n_atoms = int(header_data[1])

        # Realocamos los np.array
        self.position = np.zeros((self.n_atoms, 3))
        self.sublattice = np.zeros((self.n_atoms,), dtype=int)
        self.spins = np.zeros((self.n_atoms, 3))
        self.vecinos = np.zeros((self.n_atoms, 3), dtype=int)

        # Guardamos la posición de cada átomo, la indexación debe corregirse
        # ya que originalmente estaba para Fortran
        for i, line in enumerate(lines[1:self.n_atoms + 1]):
            atom_data = line.split()
            self.position[i] = [float(atom_data[1]), float(atom_data[2]), float(atom_data[3])]
            self.vecinos[i] = [int(atom_data[4]) - 1, int(atom_data[5]) - 1, int(atom_data[6]) - 1]


        # Guardamos la información de los spins
        for i, line in enumerate(spin_lines[0:self.n_atoms]):
            # obtenemos las componentes del spin del atomo i-esimo
            spin_data = line.split()
            self.spins[i] = [float(spin_data[1]), float(spin_data[2]), float(spin_data[3])]

        # Definir el tamaño de la red
        self.dimensions = np.amax(self.position, axis=0) - np.amin(self.position, axis=0)
        self.size = np.max(self.dimensions)


    def set_sublattice(self):
        """
        Genera una subred a partir de la red principal utilizando un algoritmo de
        búsqueda por anchura (BFS).

        La sublattice se construye asignando valores alternantes (+1 o -1) a los átomos 
        vecinos en la red, partiendo del primer átomo, al que se le asigna un valor de +1.
    """
        # Creamos una cola que contendrá los nodos a iterar,
        # junto con una lista para comprobar los nodos ya visitados
        queue_nodes =  Queue()
        checked = np.zeros(self.n_atoms, dtype=bool)

        # Definimos el primer atomo de alguna sublattice
        self.sublattice[0] = 1
        queue_nodes.put(0)
        checked[0] = True

        # Llenamos las sublattice de forma recursiva.
        # Si el vecino está definido, entonces el átomo toma el valor opuesto,
        # si no está definido y no está en la cola, el vecino se añade a la cola.
        while not queue_nodes.empty():
            node = queue_nodes.get()
            for vecino in self.vecinos[node]:
                if self.sublattice[vecino] != 0:
                    self.sublattice[node] = -self.sublattice[vecino]
                elif not checked[vecino]:
                    queue_nodes.put(vecino)
                    checked[vecino] = True
