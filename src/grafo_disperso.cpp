#include "grafo_disperso.hpp"
#include <fstream>
#include <iostream>
#include <sstream>
#include <queue>
#include <set>
#include <algorithm>
#include <chrono>

GrafoDisperso::GrafoDisperso() : numNodos(0), numAristas(0) {
    std::cout << "[C++ Core] Inicializando GrafoDisperso..." << std::endl;
}

GrafoDisperso::~GrafoDisperso() {
    // Limpieza automática de vectores
}

bool GrafoDisperso::cargarDatos(const std::string& nombreArchivo) {
    std::cout << "[C++ Core] Cargando dataset '" << nombreArchivo << "'..." << std::endl;
    
    auto inicio = std::chrono::high_resolution_clock::now();
    
    std::ifstream archivo(nombreArchivo);
    if (!archivo.is_open()) {
        std::cerr << "[C++ Core] ERROR: No se pudo abrir el archivo " << nombreArchivo << std::endl;
        return false;
    }
    
    listaAdyacencia.clear();
    std::set<int> nodosUnicos;
    int aristasCargadas = 0;
    
    std::string linea;
    while (std::getline(archivo, linea)) {
        // Ignorar líneas vacías y comentarios
        if (linea.empty() || linea[0] == '#') {
            continue;
        }
        
        std::istringstream iss(linea);
        int origen, destino;
        
        if (iss >> origen >> destino) {
            listaAdyacencia[origen].push_back(destino);
            nodosUnicos.insert(origen);
            nodosUnicos.insert(destino);
            aristasCargadas++;
        }
    }
    
    archivo.close();
    
    numNodos = nodosUnicos.size();
    numAristas = aristasCargadas;
    
    // Convertir a estructura CSR
    convertirACSR();
    
    auto fin = std::chrono::high_resolution_clock::now();
    auto duracion = std::chrono::duration_cast<std::chrono::milliseconds>(fin - inicio);
    
    std::cout << "[C++ Core] Carga completa. Nodos: " << numNodos 
              << " | Aristas: " << numAristas << std::endl;
    std::cout << "[C++ Core] Tiempo de carga: " << duracion.count() << "ms" << std::endl;
    std::cout << "[C++ Core] Estructura CSR construida. Memoria estimada: " 
              << getMemoriaEstimada() << " MB." << std::endl;
    
    return true;
}

void GrafoDisperso::convertirACSR() {
    // Inicializar row_ptr
    row_ptr.clear();
    row_ptr.resize(numNodos + 1, 0);
    
    col_indices.clear();
    values.clear();
    
    // Crear mapeo de IDs de nodos a índices consecutivos
    std::map<int, int> nodoAIndice;
    int indice = 0;
    for (const auto& par : listaAdyacencia) {
        if (nodoAIndice.find(par.first) == nodoAIndice.end()) {
            nodoAIndice[par.first] = indice++;
        }
        for (int vecino : par.second) {
            if (nodoAIndice.find(vecino) == nodoAIndice.end()) {
                nodoAIndice[vecino] = indice++;
            }
        }
    }
    
    // Construir CSR
    int offset = 0;
    for (int i = 0; i < numNodos; i++) {
        row_ptr[i] = offset;
        
        // Buscar el nodo original correspondiente a este índice
        int nodoOriginal = -1;
        for (const auto& par : nodoAIndice) {
            if (par.second == i) {
                nodoOriginal = par.first;
                break;
            }
        }
        
        if (nodoOriginal != -1 && listaAdyacencia.find(nodoOriginal) != listaAdyacencia.end()) {
            for (int vecino : listaAdyacencia[nodoOriginal]) {
                col_indices.push_back(nodoAIndice[vecino]);
                values.push_back(1); // Grafo no ponderado
                offset++;
            }
        }
    }
    row_ptr[numNodos] = offset;
}

std::vector<std::pair<int, int>> GrafoDisperso::BFS(int nodoInicial, int profundidadMaxima) {
    std::cout << "[C++ Core] Ejecutando BFS desde nodo " << nodoInicial 
              << ", profundidad " << profundidadMaxima << "..." << std::endl;
    
    auto inicio = std::chrono::high_resolution_clock::now();
    
    std::vector<std::pair<int, int>> resultado;
    
    if (listaAdyacencia.find(nodoInicial) == listaAdyacencia.end()) {
        std::cout << "[C++ Core] Nodo inicial no encontrado en el grafo." << std::endl;
        return resultado;
    }
    
    std::queue<std::pair<int, int>> cola; // (nodo, nivel)
    std::set<int> visitados;
    
    cola.push({nodoInicial, 0});
    visitados.insert(nodoInicial);
    
    while (!cola.empty()) {
        auto [nodoActual, nivelActual] = cola.front();
        cola.pop();
        
        resultado.push_back({nodoActual, nivelActual});
        
        if (nivelActual < profundidadMaxima) {
            if (listaAdyacencia.find(nodoActual) != listaAdyacencia.end()) {
                for (int vecino : listaAdyacencia[nodoActual]) {
                    if (visitados.find(vecino) == visitados.end()) {
                        visitados.insert(vecino);
                        cola.push({vecino, nivelActual + 1});
                    }
                }
            }
        }
    }
    
    auto fin = std::chrono::high_resolution_clock::now();
    auto duracion = std::chrono::duration_cast<std::chrono::microseconds>(fin - inicio);
    
    std::cout << "[C++ Core] BFS completo. Nodos encontrados: " << resultado.size() 
              << ". Tiempo: " << duracion.count() / 1000.0 << "ms" << std::endl;
    
    return resultado;
}

std::pair<int, int> GrafoDisperso::obtenerGrado() {
    int maxGrado = 0;
    int nodoMaxGrado = -1;
    
    for (const auto& par : listaAdyacencia) {
        int grado = par.second.size();
        if (grado > maxGrado) {
            maxGrado = grado;
            nodoMaxGrado = par.first;
        }
    }
    
    std::cout << "[C++ Core] Nodo con mayor grado: " << nodoMaxGrado 
              << " (grado=" << maxGrado << ")" << std::endl;
    
    return {nodoMaxGrado, maxGrado};
}

std::vector<int> GrafoDisperso::getVecinos(int nodo) {
    if (listaAdyacencia.find(nodo) != listaAdyacencia.end()) {
        return listaAdyacencia[nodo];
    }
    return std::vector<int>();
}

int GrafoDisperso::getNumNodos() const {
    return numNodos;
}

int GrafoDisperso::getNumAristas() const {
    return numAristas;
}

double GrafoDisperso::getMemoriaEstimada() const {
    size_t bytesRowPtr = row_ptr.size() * sizeof(int);
    size_t bytesColIndices = col_indices.size() * sizeof(int);
    size_t bytesValues = values.size() * sizeof(int);
    size_t totalBytes = bytesRowPtr + bytesColIndices + bytesValues;
    
    return totalBytes / (1024.0 * 1024.0); // Convertir a MB
}

void GrafoDisperso::imprimirEstadisticas() const {
    std::cout << "========================================" << std::endl;
    std::cout << "Estadísticas del Grafo" << std::endl;
    std::cout << "========================================" << std::endl;
    std::cout << "Nodos: " << numNodos << std::endl;
    std::cout << "Aristas: " << numAristas << std::endl;
    std::cout << "Memoria CSR: " << getMemoriaEstimada() << " MB" << std::endl;
    std::cout << "========================================" << std::endl;
}
