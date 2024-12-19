"""
Contiene la clase DataManager

utilizado para realizar diagramas de fases
"""

import numpy as np

from tqdm import tqdm

from path_manager import PathManager
from lattice import Lattice
from criteria import Criteria

class DataManager:
    """
    a
    """
    def __init__(self,
                 path_manager : PathManager,
                 variables : dict,
                 ):
        # Nombres de archivos y variables
        self.path_manager = path_manager

        # Data para el diagrama de fases en RGB
        self.var1_list = variables["first"]
        self.var2_list = variables["second"]

        self.data = np.zeros((len(self.var1_list), len(self.var2_list), 3))

        self.criteria = Criteria()


    def set_data(self, function : callable) -> None:
        """
        a
        """
        for j, var1 in tqdm(enumerate(self.var1_list)):
            for k, var2 in enumerate(self.var2_list):
                print("var1:", var1, "var2:", var2)
                lattice = Lattice()

                structure = self.path_manager.structure
                file = self.path_manager.get_file_path("", var1, var2) + "_spin"
                lattice.load_files(structure, file)

                if self.criteria.len == 0:
                    lattice.set_sublattice()
                    self.criteria.set_values(lattice.n_atoms,
                                             lattice.vecinos,
                                             lattice.sublattice,
                                             lattice.position
                                             )

                self.data[j][k] = function(lattice.spins)
