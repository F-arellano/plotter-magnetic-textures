"""
Realiza un diagrama de fases de la red utilizando criterios sobre la configuracion de spines
"""
import numpy as np
from source.path_manager import PathManager
from source.data_manager import DataManager
from source.plotter import Plotter

if __name__ == "__main__":
    # contiene la información de los archivos de entrada y salida para PathManager
    NAMES = {
        "dir_prefix" : "spins/J5/min_files/",
        "file_prefix" : "out",
        "variable_1" : "_DM",
        "variable_2" : "_K",
        "format" : "{:.3f}",
        "structure" : "structure_files/mc_vecinos_L16",
        "output_image" : "testing.png",
    }

    # Contiene el rango en que varía cada parámetro del diagrama de fases
    # OJO, arange excluye término final, además debe usar enteros
    # para entregar resultados consistentes
    VARIABLES = {
        "first" : np.arange(0, 101)/10.,
        "second" : np.arange(-50, 51)/5.,
    }

    TICKS_STEPS = {
        "first" : 5,
        "second" : 5,
    }

    paths = PathManager(NAMES)
    data_manager = DataManager(paths, VARIABLES)

    data_manager.set_data(data_manager.criteria.data_ferro_spiral_skyrmions)

    plotter = Plotter(paths, VARIABLES, TICKS_STEPS)
    plotter.data = data_manager.data
    plotter.plot_phase_diagram()
