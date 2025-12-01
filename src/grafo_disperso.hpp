#ifndef GRAFO_DISPERSO_HPP
#define GRAFO_DISPERSO_HPP

#include "grafo_base.hpp"
#include <vector>
#include <string>
#include <map>

/**
 * Clase Concreta: GrafoDisperso
 * Implementa un grafo utilizando estructura CSR (Compressed Sparse Row)
 * para optimizar el uso de memoria en grafos masivos poco densos.
 * 
 * Estructura CSR usa 3 vectores:
 * - row_ptr: Punteros que indican dónde empiezan las adyacencias de cada fila
 * - col_indices: Índices de columna de elementos no-cero
 * - values: Valores (en nuestro caso, 1 para indicar conexión)
 */
class GrafoDisperso : public GrafoBase {
private:
    // Estructura CSR para matriz de adyacencia dispersa
    std::vector<int> row_ptr;       // Tamaño: numNodos + 1
    std::vector<int> col_indices;   // Tamaño: numAristas
    std::vector<int> values;        // Tamaño: numAristas (todos 1s en grafo no ponderado)
    
    int numNodos;
    int numAristas;
    
    // Mapa temporal para construcción del grafo
    std::map<int, std::vector<int>> listaAdyacencia;
    
    /**
     * Convierte la lista de adyacencia temporal a formato CSR
     */
    void convertirACSR();
    
public:
    GrafoDisperso();
    ~GrafoDisperso();
    
    // Implementación de métodos abstractos
    bool cargarDatos(const std::string& nombreArchivo) override;
    std::vector<std::pair<int, int>> BFS(int nodoInicial, int profundidadMaxima) override;
    std::pair<int, int> obtenerGrado() override;
    std::vector<int> getVecinos(int nodo) override;
    int getNumNodos() const override;
    int getNumAristas() const override;
    
    /**
     * Obtiene métricas de memoria estimada en MB
     * @return Memoria estimada en megabytes
     */
    double getMemoriaEstimada() const;
    
    /**
     * Imprime estadísticas del grafo en consola
     */
    void imprimirEstadisticas() const;
};

#endif // GRAFO_DISPERSO_HPP
