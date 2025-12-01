#ifndef GRAFO_BASE_HPP
#define GRAFO_BASE_HPP

#include <vector>
#include <string>
#include <utility>

/**
 * Clase Abstracta: GrafoBase
 * Define la interfaz para todas las implementaciones de grafos.
 * Utiliza métodos virtuales puros para forzar la implementación en clases derivadas.
 */
class GrafoBase {
public:
    // Destructor virtual para permitir polimorfismo correcto
    virtual ~GrafoBase() {}
    
    /**
     * Carga un dataset desde un archivo en formato Edge List
     * @param nombreArchivo Ruta al archivo con formato "NodoOrigen NodoDestino"
     * @return true si la carga fue exitosa, false en caso contrario
     */
    virtual bool cargarDatos(const std::string& nombreArchivo) = 0;
    
    /**
     * Ejecuta Breadth-First Search desde un nodo inicial
     * @param nodoInicial Nodo desde el cual iniciar la búsqueda
     * @param profundidadMaxima Profundidad máxima de búsqueda
     * @return Vector de pares (nodo, nivel) encontrados en la búsqueda
     */
    virtual std::vector<std::pair<int, int>> BFS(int nodoInicial, int profundidadMaxima) = 0;
    
    /**
     * Calcula el nodo con mayor grado (más conexiones)
     * @return Par con (nodoID, grado)
     */
    virtual std::pair<int, int> obtenerGrado() = 0;
    
    /**
     * Obtiene los vecinos de un nodo específico
     * @param nodo ID del nodo a consultar
     * @return Vector con IDs de nodos vecinos
     */
    virtual std::vector<int> getVecinos(int nodo) = 0;
    
    /**
     * Obtiene el número total de nodos en el grafo
     * @return Cantidad de nodos
     */
    virtual int getNumNodos() const = 0;
    
    /**
     * Obtiene el número total de aristas en el grafo
     * @return Cantidad de aristas
     */
    virtual int getNumAristas() const = 0;
};

#endif // GRAFO_BASE_HPP
