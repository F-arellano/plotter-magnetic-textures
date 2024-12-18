"""
Contiene la clase GraphMaker para visualizar redes de spins utilizando vpython.

utilizado para plotear spins
"""

import numpy as np
import vpython as vp

from lattice import Lattice

class GraphMaker:
    """
    Clase para generar y visualizar una red de spins en un entorno 3D utilizando vpython.

    ATRIBUTOS:
    ----------
    lattice : Lattice
        Objeto de la clase Lattice que contiene la red de spins a visualizar.
    scene : vp.canvas
        Objeto canvas de vpython donde se renderizará la visualización.
    colors : dict
        Diccionario que mapea las direcciones de los spins (up, down, mid) a colores específicos.
    
    MÉTODOS:
    --------
    __init__(structure_file, spin_file):
        Inicializa el objeto GraphMaker cargando la red de spins desde los archivos proporcionados.
    get_vpython_vector(array):
        Convierte un array numpy en un vector de vpython.
    make_canvas(rotate):
        Crea el canvas de vpython donde se visualizará la red de spins,
        con la opción de rotar la vista.
    plot_spins(sublattice):
        Visualiza los spins en el canvas, con la opción de de mostrar una subred específica.
    """

    def __init__(self, structure_file : str, spin_file : str):
        """
        Inicializa un objeto GraphMaker.

        Parámetros:
        -----------
        structure_file : str
            Ruta al archivo que contiene la estructura espacial de la red.
        spin_file : str
            Ruta al archivo que contiene la configuración de los spins.

        Ejecución:
        ----------
        1. Inicializa la red de spins a partir de los archivos proporcionados.
        2. Define un canvas de vpython para la visualización.
        3. Asigna un conjunto de colores para representar diferentes orientaciones de spins.
        """
        self.lattice = Lattice()
        self.scene = vp.canvas()

        self.colors = {
            "up" : vp.vector(.9,0.1,0.1),
            "down" : vp.vector(0.1,0.9,0.1),
            "mid" : vp.vector(0.9,0.9,0.1),
        }

        self.lattice.load_files(structure_file, spin_file)


    def get_vpython_vector(self, array : np.array) -> vp.vector:
        """
        Convierte un array de numpy en un vector de vpython.

        PARAMETROS:
        -----------
        array : np.array
            Array numpy con 3 elementos que representan un vector en el espacio
            o un color.

        RETORNO:
        --------
        vp.vector
            Vector de vpython con los mismos valores que el array de entrada.
        """
        return vp.vector(array[0], array[1], array[2])


    def get_spin_color(self, spin : np.array) -> vp.vector:
        """
        Determina el color de un spin basado en su componente z utilizando un gradiente de colores.

        PARAMETROS:
        -----------
        spin : np.array
            Array de 3 elementos que representa el vector de spin en el espacio.

        RETORNO:
        --------
        vp.vector
            Vector de vpython que representa el color del spin.
        """
        # Definimos el color del spin mediante un gradiente de color: A*r + B(1-r).
        # Se tomará como parámetro la componente z del spin.
        r = np.abs(spin[2])

        # Hay un gradiente de color desde sz=1 a sz=0 y otro de sz=0 a sz=-1
        if spin[2] < 0:
            color = self.colors["down"]*r + self.colors["mid"]*(1-r)
        else:
            color = self.colors["up"]*r + self.colors["mid"]*(1-r)
        return color


    def make_canvas(self, rotate : bool) -> None:
        """
        Crea y configura un canvas de vpython donde se visualizará la red de spins.

        PARAMETROS:
        -----------
        rotate : bool
            Si es True, rota la vista inicial del canvas para que la cámara apunte hacia el eje x.
        """
        center = self.get_vpython_vector(0.5*self.lattice.dimensions)

        self.scene=vp.canvas(width = 2500,
                             height = 1300,
                             center = center,
                             background = vp.vector(1.0,1.0,0.97)
                            )

        # Ajustamos la amplitud de la camara
        self.scene.autoscale = False
        self.scene.range = np.max(self.lattice.size)*0.38
        self.scene.fov=1e-2

        if rotate:
            self.scene.up = vp.vector(1, 0, 0)

    def plot_spins(self, sublattice : int) -> None:
        """
        Visualiza la red de spins en el canvas de vpython.

        PARAMETROS:
        -----------
        rotate : bool
            Si es True, rota la vista inicial del canvas para que la cámara apunte hacia el eje x.
        sublattice : int
            Si es diferente de 0, se visualizará solo la subred especificada. 
            Toma valores -1, 0, +1.
        """

        # En caso de querer visualizar solo una sublattice, se determinan los átomos 
        # correspondientes.
        if sublattice != 0:
            self.lattice.set_sublattice()

        # arrays que contendrán los objetos del canvas
        balls=[]
        arrows=[]

        # Graficamos cada uno de los spines
        for i in range(self.lattice.n_atoms):
            if sublattice not in (0, self.lattice.sublattice[i]):
                continue

            # Definimos la posición y dirección del spin mediante
            # vectores de vpython
            position = self.get_vpython_vector(self.lattice.position[i])
            direction = self.get_vpython_vector(self.lattice.spins[i])

            # Creamos una esfera en el origen del spin
            ball = vp.sphere(color=vp.vector(0.4,0.2,0.9), radius=0.4)
            ball.pos = position

            balls.append(ball)

            # Creamos una flecha en la dirección del spin con el gradiente de color
            arrow_size = 7.
            color_arrow = self.get_spin_color(self.lattice.spins[i])

            arrow = vp.arrow(shaftwidth=arrow_size/10, color=color_arrow, round=True)
            arrow.pos = position
            arrow.axis = arrow_size*vp.vector(direction)
            arrows.append(arrow)
