"""
Realiza un gráfico 3D de la red de spines mediante VPython
"""

from graph_maker import GraphMaker

if __name__ == "__main__":

    STRUCTURE_FILE = "structure_files/mc_vecinos_L16"
    SPIN_FILE = "spins/test-skyrmion2_spin"

    ROTATE = True
    SUBLATTICE = 0

    a = GraphMaker(STRUCTURE_FILE, SPIN_FILE)
    a.make_canvas(ROTATE)
    a.plot_spins(SUBLATTICE)
