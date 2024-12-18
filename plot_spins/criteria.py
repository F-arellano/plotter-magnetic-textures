"""
contiene la clase Criteria

utilizado para realizar diagramas de fases
"""

import numpy as np

class Criteria:
    """
    Clase para determinar diferentes criterios de alineación de espines en un sistema de redes.

    Atributos:
    ----------
    len : int
        Número de átomos en el sistema.
    vecinos : ndarray
        array conteniendo los vecinos más cercanos para cada átomo.
    sublattice : ndarray
        array que indica la subred a la que pertenece cada átomo.
    positions : ndarray
        array de posiciones de cada átomo.
    """

    def __init__(self):
        self.len = 0
        self.vecinos = np.array([])
        self.sublattice = []
        self.positions = []


    def set_values(self, n_atoms, vecinos, sublattice, positions):
        """
        Establece los valores de los atributos de la clase.

        Parámetros:
        -----------
        n_atoms : int
            Número de átomos en el sistema.
        vecinos : list
            Lista de vecinos para cada átomo.
        sublattice : list
            Lista que indica la subred a la que pertenece cada átomo.
        positions : list
            Lista de posiciones de cada átomo.
        """

        self.len = n_atoms
        self.vecinos = vecinos
        self.sublattice = sublattice
        self.positions = positions


    def is_ferro_z_aligned(self, spins):
        """
        Determina si el sistema presenta ferromagnetismo global en la dirección Z.

        Parámetros:
        -----------
        spins : list
            Lista de vectores de espines en el sistema.

        Retorna:
        --------
        bool
            True si el sistema está alineado ferromagnéticamente en Z, False en caso contrario.
        """
        mag_z = np.sum([spins[n][2] for n in range(self.len)])
        value = np.abs(mag_z) / self.len
        return value > 0.99


    def is_antiferro_z_aligned(self, spins):
        """
        Determina si el sistema presenta antiferromagnetismo global en la dirección Z.

        Parámetros:
        -----------
        spins : list
            Lista de vectores de espines en el sistema.

        Retorna:
        --------
        bool
            True si el sistema está alineado antiferromagnéticamente en Z, False en caso contrario.
        """
        mag_z = np.sum([spins[n][2] * self.sublattice[n] for n in range(self.len)])
        value = np.abs(mag_z) / self.len
        return value > 0.99


    def is_ferro_xy_aligned(self, spins):
        """
        Determina si el sistema presenta ferromagnetismo global en el plano XY.

        Parámetros:
        -----------
        spins : list
            Lista de vectores de espines en el sistema.

        Retorna:
        --------
        bool
            True si el sistema está alineado ferromagnéticamente en el plano XY,
            False en caso contrario.
        """

        mag_x = np.sum([spins[n][0] for n in range(self.len)])
        mag_y = np.sum([spins[n][1] for n in range(self.len)])
        mag_z = np.abs(np.sum([spins[n][2] for n in range(self.len)])) / self.len
        mag = np.sqrt(mag_x**2 + mag_y**2 + mag_z**2) / self.len

        return mag_z < 0.1 and mag > 0.9


    def is_antiferro_xy_aligned(self, spins):
        """
        Determina si el sistema presenta antiferromagnetismo global en el plano XY.

        Parámetros:
        -----------
        spins : list
            Lista de vectores de espines en el sistema.

        Retorna:
        --------
        bool
            True si el sistema está alineado antiferromagnéticamente en el plano XY,
            False en caso contrario.
        """
        mag_x = np.sum([spins[n][0] * self.sublattice[n] for n in range(self.len)])
        mag_y = np.sum([spins[n][1] * self.sublattice[n] for n in range(self.len)])
        mag_z = np.sum([spins[n][2] * self.sublattice[n] for n in range(self.len)]) / self.len
        mag = np.sqrt(mag_x**2 + mag_y**2 + mag_z**2) / self.len

        return np.abs(mag_z) < 0.1 and mag > 0.9


    def is_xyz_aligned(self, spins):
        """
        Determina si los espines están alineados localmente en las direcciones Z o en el plano XY.

        Parámetros:
        -----------
        spins : list
            Lista de vectores de espines en el sistema.

        Retorna:
        --------
        tuple
            (bool, bool): Dos booleanos indicando si los espines están 
            alineados en Z o en XY respectivamente.
        """

        counter_z = np.sum([1 for n in range(self.len) if np.abs(spins[n][2]) > 0.95]) / self.len
        counter_xy = np.sum([1 for n in range(self.len) if np.abs(spins[n][2]) < 0.05]) / self.len

        is_z_aligned = counter_z > 0.7
        is_xy_aligned = counter_xy > 0.8

        return is_z_aligned, is_xy_aligned


    def is_local_ferro_antiferro(self, spins):
        """
        Determina si el sistema presenta ferromagnetismo o antiferromagnetismo local.

        Parámetros:
        -----------
        spins : list
            Lista de vectores de espines en el sistema.

        Retorna:
        --------
        tuple
            (bool, bool): Dos booleanos indicando si el sistema es ferromagnético 
            localmente o antiferromagnético localmente.
        """
        counter_ferro = 0
        counter_antiferro = 0

        for n in range(self.len):
            spin_n = spins[n]
            m_value = np.sum([spin_n.dot(spins[m]) for m in self.vecinos[n]]) / len(self.vecinos[n])

            if m_value > 0.99:
                counter_ferro += 1
            elif m_value < -0.99:
                counter_antiferro += 1

        is_ferro = counter_ferro / self.len > 0.65
        is_antiferro = counter_antiferro / self.len > 0.65

        return is_ferro, is_antiferro


    def domain_wall_ferro_z_align(self, spins):
        """
        Verifica la presencia de paredes de dominio con inversión de espines en Z en la subred.

        Parámetros:
        -----------
        spins : list
            Lista de vectores de espines en el sistema.

        Retorna:
        --------
        bool
            True si se detecta una inversión de espines en Z en la subred, False en caso contrario.
        """

        spin_up = np.array([0., 0., 1.])
        spin_down = np.array([0., 0., -1.])
        min_up = 1
        min_down = 1

        for i in range(self.len):
            if self.sublattice[i] == 1:
                spin_i = spins[i]
                min_up = min(min_up, spin_up.dot(spin_i))
                min_down = min(min_down, spin_down.dot(spin_i))
                if (min_up < -0.9 and min_down < -0.9):
                    return True

        return False

    # spines localmente aleatorios
    def is_random(self, spins):
        """
        Determina si los espines están distribuidos aleatoriamente.

        Parámetros:
        -----------
        spins : list
            Lista de vectores de espines en el sistema.

        Retorna:
        --------
        bool
            True si los espines están distribuidos aleatoriamente, False en caso contrario.
        """

        dot_value = np.sum([
            np.sum([spins[n].dot(spins[m]) for m in self.vecinos[n]]) / len(self.vecinos[n])
            for n in range(self.len)
        ])

        return np.abs(dot_value) < 0.01


    def is_conical(self, spins):
        """
        Determina si los espines forman una configuración espiral (conica o helicoidal).

        Parámetros:
        -----------
        spins : list
            Lista de vectores de espines en el sistema.

        Retorna:
        --------
        tuple
            (bool, bool): Dos booleanos indicando si el sistema tiene
            una estructura cónica o helicoidal.
        """

        rotation_vec = np.zeros(3)
        traslation_vec = np.zeros(3)

        count = 0

        for i, (spin_i, position_i) in enumerate(zip(spins, self.positions)):
            for j in self.vecinos[i]:
                cross_vec = np.cross(spin_i, spins[j])
                mag_cross = np.linalg.norm(cross_vec)
                # el caso (i x j) y el caso (j x i) dan signos opuestos.
                # Invertiremos el que vaya en direccion opuesta al eje de rotacion
                if cross_vec.dot(rotation_vec) < 0:
                    cross_vec = -1.*cross_vec

                # si mag_cross es no nulo, estamos considerando spines que rotan.
                # Actualizamos rotation_vec
                if mag_cross > 0.01:
                    rotation_vec += cross_vec
                    count += 1

                # si mag_cross es nulo, los spines son paralelos, actualiamos traslation_vec
                else:
                    r_vec = position_i - self.positions[j]
                    if r_vec[1] < 0.:
                        r_vec = -1.*r_vec
                    traslation_vec += r_vec

        if count:
            rotation_mag = np.sqrt(rotation_vec.dot(rotation_vec))
            rotation_vec /= rotation_mag
            mean_dot_value = np.sum([np.abs(spin_i.dot(rotation_vec)) for spin_i in spins]) / count
            max_dot_value = np.amax([np.abs(spin_i.dot(rotation_vec)) for spin_i in spins])

        else:
            mean_dot_value = float("inf")
            max_dot_value = float("inf")

        print("mean dot value:", mean_dot_value)

        is_locally_conical = mean_dot_value < 0.1
        is_globally_conical = max_dot_value < 0.1


        return is_locally_conical, is_globally_conical

#============================================================================================
#======================== convertimos los criterios a mapas de color ========================
#============================================================================================

    def data_ferro_and_align_with_domain_walls(self, spins):
        """
        Genera un mapa de color en función del estado magnetico del sistema,
        considerando (anti)ferromagnetismo en el eje (XY)Z, 
        junto con la presencia de paredes de dominio

        Parámetros:
        -----------
        spins : list
            Lista de vectores de espines en el sistema.

        Retorna:
        --------
        numpy.array
            Un array RGB representando el color asociado a la fase detectada.
        """
        is_ferro_local, is_antiferro_local = self.is_local_ferro_antiferro(spins)
        is_z_aligned, is_xy_aligned = self.is_xyz_aligned(spins)
        domain_wall = self.domain_wall_ferro_z_align(spins)

        is_ferro_in_z = self.is_ferro_z_aligned(spins)
        is_ferro_in_xy = self.is_ferro_xy_aligned(spins)
        is_antiferro_in_z = self.is_antiferro_z_aligned(spins)
        is_antiferro_in_xy = self.is_antiferro_xy_aligned(spins)

        is_random = self.is_random(spins)

        color = np.array([0., 0., 0.])

        #  ==================Regiones intermedias =======================
        if is_antiferro_local and not is_z_aligned and not is_xy_aligned:
            # color cian
            color = np.array([113,255,240])/255

        elif is_z_aligned and not is_ferro_local and not is_antiferro_local:
            # color verde claro
            color = np.array([194,255,113])/255

        elif is_xy_aligned and not is_ferro_local and not is_antiferro_local:
            # color lavanda
            color = np.array([177,113,255])/255

        elif is_ferro_local and not is_z_aligned and not is_xy_aligned:
            # color rojo claro
            color = np.array([255,113,113])/255

        #  ================= 4 fases principales =========================
        elif is_ferro_in_z:
            # color amarillo
            color = np.array([255,231,113])/255

        elif is_antiferro_in_z:
            # color verde
            color = np.array([113,255,133])/255

        elif is_ferro_in_xy:
            # color rosa
            color = np.array([255,113,180])/255

        elif is_antiferro_in_xy:
            # color celeste oscuro
            color = np.array([113,193,255])/255

        # paredes de dominio
        elif is_ferro_local and is_z_aligned and domain_wall:
            color = np.array([255,150,113])/255
        elif is_antiferro_local and is_z_aligned and domain_wall:
            color = np.array([50,194,78])/255

        # paramagnetismo
        elif is_random:
            color = np.array([0.,0.,0.])
        # without criteria
        else:
            color = np.array([255,255,255])/255

        return color


    def data_ferro_spiral_skyrmions(self, spins):
        """
        Genera un mapa de color del estado en función del estado magnético,
        distinguiendo entre configuraciones ferro, antiferro, espirales y skyrmiones.

        Parámetros:
        -----------
        spins : list
            Lista de vectores de espines en el sistema.

        Retorna:
        --------
        numpy.array
            Un array RGB representando el color asociado a la fase detectada.
        """
        is_ferro_in_z = self.is_ferro_z_aligned(spins)
        is_ferro_in_xy = self.is_ferro_xy_aligned(spins)
        is_antiferro_in_z = self.is_antiferro_z_aligned(spins)
        is_antiferro_in_xy = self.is_antiferro_xy_aligned(spins)

        is_locally_conical, is_globally_conical = self.is_conical(spins)

        color = np.array([0., 0., 0.])

        # ================= casos ferro/antiferro en XY/Z ===============
        if is_ferro_in_z:
            # color amarillo
            color = np.array([255,231,113])/255

        elif is_antiferro_in_z:
            # color verde
            color = np.array([113,255,133])/255

        elif is_ferro_in_xy:
            # color rosa
            color = np.array([255,113,180])/255

        elif is_antiferro_in_xy:
            # color celeste oscuro
            color = np.array([113,193,255])/255

        # ================== casos espirales =======================
        elif is_globally_conical:
            # color lavanda
            color = np.array([177,113,255])/255

        elif is_locally_conical:
            # color rojo claro
            color = np.array([255,113,113])/255

        # without criteria
        else:
            color = np.array([255,255,255])/255

        return color
