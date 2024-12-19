"""
Contiene la clase Plotter
"""

import numpy as np
import matplotlib.pyplot as plt

from path_manager import PathManager

class Plotter:
    """
    Clase para generar diagramas de fases

    ATRIBUTOS:
    ----------
    path_manager : PathManager
        Instancia de la clase PathManager, permite generar y manejar los path de los archivos.
    var1_list : list 
        lista con todos los valores tomados por la primera variable
    var2_list : list 
        lista con todos los valores tomados por la segunda variable
    data: np.array
        array de N*M*3 con los valores de color del diagrama de fases

    METODOS:
    --------
    same_color(a,b) : bool
        determina si los colores a y b son los mismos
    plot_phase_diagram() :
        Genera el gráfico del diagrama de fases
    """

    def __init__(self,
                 path_manager: PathManager,
                 variables: dict,
                 ticks_steps : dict,
                 ):

        self.path_manager = path_manager

        self.var1_list = variables["first"]
        self.var2_list = variables["second"]

        self.yticks_step = ticks_steps["first"]
        self.xticks_step = ticks_steps["second"]

        self.data = np.zeros([len(variables["first"]), len(variables["second"]), 3])


    def same_color(self, a, b) -> bool:
        """
        Compara dos colores y determina si son iguales.

        Parámetros
        ----------
        a : list o array-like
            Primer color a comparar.
        b : list o array-like
            Segundo color a comparar.

        Retorno
        -------
        bool
            True si ambos colores son iguales, False en caso contrario.
        """
        if a[0]==b[0] and a[1]==b[1] and a[2]==b[2]:
            return True
        return False


    def plot_phase_diagram(self):
        """
        Genera un gráfico del diagrama de fases basado en los datos de mínima energía 
        y las variables a iterar.

        Este método configura los ejes, genera líneas para delimitar las fases
        y muestra el gráfico resultante.
        """
        # configuramos el gráfico para que los tics queden en medio de cada valor var1, var2
        dx = (self.var2_list[1]-self.var2_list[0])/2.
        dy = (self.var1_list[1]-self.var1_list[0])/2.

        extent = [
            self.var2_list[0]-dx,
            self.var2_list[-1]+dx,
            self.var1_list[0]-dy,
            self.var1_list[-1]+dy
            ]

        # guardamos en una lista las lineas que delimitarán las distintas
        # fases del diagrama
        x_lines, y_lines = [], []

        # Para cada pixel, revisaremos si algún pixel adyacente es de otro color,
        # en cuyo caso habrá una linea en el diagrama de fases
        for j, var1 in enumerate(self.var1_list):
            for k, var2 in enumerate(self.var2_list):
                # Lineas horizontales (limite al variar j), hay una linea si no corresponde
                # a un borde y hay 2 colores adyacentes
                if j!=len(self.var1_list) - 1:
                    if not self.same_color(self.data[j][k], self.data[j+1][k]):
                        x_lines.append((var2 - dx, var2 + dx))
                        y_lines.append((var1 + dy, var1 + dy))

                # Lineas verticales (limite al variar k), hay una linea si no corresponde
                # a un borde y hay 2 colores adyacentes
                if k!=len(self.var2_list) - 1:
                    if not self.same_color(self.data[j][k], self.data[j][k+1]):
                        x_lines.append((self.var2_list[k] + dx, self.var2_list[k] + dx))
                        y_lines.append((self.var1_list[j] - dy, self.var1_list[j] + dy))

        # Graficamos
        plt.figure(figsize=(15,9))
        plt.imshow(self.data[::-1], cmap='hot', interpolation='none', extent=extent)

        # Colocamos los labels de los ejes
        label_x = self.path_manager.var2_name[1:] + " [meV]"
        label_y = self.path_manager.var1_name[1:] + " [meV]"
        plt.xlabel(label_x)
        plt.ylabel(label_y)

        plt.xticks(self.var2_list * self.xticks_step)
        plt.yticks(self.var1_list * self.yticks_step)

        plt.grid(color='gray', linestyle='--', linewidth=1)

        # Añadimos lineas negras separando diferentes fases
        for (x, y) in zip(x_lines, y_lines):
            plt.plot(x, y, color="black")

        plt.savefig("out.png")
