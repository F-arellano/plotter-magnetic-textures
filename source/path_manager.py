"""
Contiene la clase PathManager.
"""

class PathManager:
    """
    Clase para gestionar y generar rutas de archivos y carpetas basadas en prefijos y variables.

    ATRIBUTOS
    ---------
    dir_prefix : str
        prefijo común de todas las carpetas a iterar
    name_prefix : str
        prefijo común a todos los archivos
    var1_name : str
        nombre de la primera variable (tal como aparece en el archivo)
    var2_name : str
        nombre de la segunda variable (tal como aparece en el archivo)
    var_format : str
        formato con la cantidad de decimales para el valor de cada variable
    
    METODOS
    -------
    get_file_path(folder, var1, var2) : str
        retorna el path completo para el archivo con condición inicial asociada 
        al sufijo 'folder' y valores 'var1' y 'var2' para cada variable
    get_folder_path(folder) : str
        retorna el path de la carpeta con la condición inicial asociada al sufijo 'folder'
    get_min_path() :
        retorna el path de la carpeta de output
    var_to_str(var) : str
        retorna var como string en el formato necesario para el nombre del archivo
    """
    def __init__(self,
                 names : dict,
                 ):
        """
        Setea los atributos de la clase
        """

        self.dir_prefix = names["dir_prefix"]
        self.name_prefix = names["file_prefix"]
        self.var1_name = names["variable_1"]
        self.var2_name = names["variable_2"]
        self.var_format = names["format"]

        self.structure = names["structure"]
        self.output_img = names["output_image"]


    def get_file_path(self, folder: str, var1: float, var2: float) -> str:
        """
        Genera el path completo asociado a la condición inicial 'folder' (sufijo) y los valores 
        de las variables iniciales var1 y var2.

        Parámetros
        ----------
        folder : str
            Nombre o sufijo de la carpeta que contiene los archivos.
        var1 : float
            Valor de la primera variable.
        var2 : float
            Valor de la segunda variable.

        Retorno
        -------
        str
        Path completo del archivo.
        """

        dir_path = self.dir_prefix + folder + "/"
        file_name = self.name_prefix + self.var1_name + self.var_to_str(var1)
        file_name += self.var2_name + self.var_to_str(var2)

        return dir_path + file_name


    def get_folder_path(self, folder: str) -> str:
        """
        Genera el path de la carpeta con la condición inicial 'folder' (sufijo)
        """
        return self.dir_prefix + folder + "/"


    def get_min_path(self) -> str:
        """
        Genera el path de la carpeta que contendrá los archivos de mínima energía
        """
        return self.dir_prefix + "min_files/"


    def var_to_str(self, var: float) -> str:
        """
        Converte el valor numérico de la variable a string en el formato requerido
        Parámetros
        ----------
        var : float
            Valor numérico de la variable a convertir.

        Retorno
        -------
        str
        Representación en string del valor formateado según 'var_format',
        corresponderá al valor de la variable en el nombre del archivo.
        """

        return self.var_format.format(var)
