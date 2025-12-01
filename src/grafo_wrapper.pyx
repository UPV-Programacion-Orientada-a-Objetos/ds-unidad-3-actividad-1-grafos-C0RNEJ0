# distutils: language = c++
# cython: language_level=3

from grafo_wrapper cimport GrafoDisperso
from libcpp.vector cimport vector
from libcpp.pair cimport pair
from libcpp.string cimport string

cdef class PyGrafoDisperso:
    """
    Wrapper de Python para la clase C++ GrafoDisperso.
    Expone todos los métodos de procesamiento de grafos a Python.
    """
    cdef GrafoDisperso* c_grafo  # Puntero a la instancia C++
    
    def __cinit__(self):
        """Constructor: crea instancia de GrafoDisperso en C++"""
        self.c_grafo = new GrafoDisperso()
    
    def __dealloc__(self):
        """Destructor: libera memoria de C++"""
        del self.c_grafo
    
    def cargar_datos(self, str nombre_archivo):
        """
        Carga un dataset desde archivo en formato Edge List.
        
        Args:
            nombre_archivo: Ruta al archivo con formato "NodoOrigen NodoDestino"
        
        Returns:
            True si la carga fue exitosa, False en caso contrario
        """
        cdef string cpp_nombre = nombre_archivo.encode('utf-8')
        return self.c_grafo.cargarDatos(cpp_nombre)
    
    def bfs(self, int nodo_inicial, int profundidad_maxima):
        """
        Ejecuta Breadth-First Search desde un nodo inicial.
        
        Args:
            nodo_inicial: Nodo desde donde iniciar la búsqueda
            profundidad_maxima: Profundidad máxima de búsqueda
        
        Returns:
            Lista de tuplas (nodo, nivel) encontrados en la búsqueda
        """
        print(f"[Cython] Solicitud recibida: BFS desde Nodo {nodo_inicial}, Profundidad {profundidad_maxima}.")
        
        cdef vector[pair[int, int]] resultado_cpp = self.c_grafo.BFS(nodo_inicial, profundidad_maxima)
        
        # Convertir vector de C++ a lista de Python
        resultado_py = []
        cdef pair[int, int] item
        for item in resultado_cpp:
            resultado_py.append((item.first, item.second))
        
        print(f"[Cython] Retornando {len(resultado_py)} nodos a Python.")
        return resultado_py
    
    def obtener_grado(self):
        """
        Calcula el nodo con mayor grado (más conexiones).
        
        Returns:
            Tupla (nodo_id, grado)
        """
        cdef pair[int, int] resultado = self.c_grafo.obtenerGrado()
        return (resultado.first, resultado.second)
    
    def get_vecinos(self, int nodo):
        """
        Obtiene los vecinos de un nodo específico.
        
        Args:
            nodo: ID del nodo a consultar
        
        Returns:
            Lista con IDs de nodos vecinos
        """
        cdef vector[int] vecinos_cpp = self.c_grafo.getVecinos(nodo)
        
        # Convertir vector de C++ a lista de Python
        vecinos_py = []
        cdef int vecino
        for vecino in vecinos_cpp:
            vecinos_py.append(vecino)
        
        return vecinos_py
    
    def get_num_nodos(self):
        """
        Obtiene el número total de nodos en el grafo.
        
        Returns:
            Cantidad de nodos
        """
        return self.c_grafo.getNumNodos()
    
    def get_num_aristas(self):
        """
        Obtiene el número total de aristas en el grafo.
        
        Returns:
            Cantidad de aristas
        """
        return self.c_grafo.getNumAristas()
    
    def get_memoria_estimada(self):
        """
        Obtiene la memoria estimada en MB utilizada por la estructura CSR.
        
        Returns:
            Memoria en megabytes
        """
        return self.c_grafo.getMemoriaEstimada()
    
    def imprimir_estadisticas(self):
        """
        Imprime estadísticas del grafo en consola (desde C++)
        """
        self.c_grafo.imprimirEstadisticas()
