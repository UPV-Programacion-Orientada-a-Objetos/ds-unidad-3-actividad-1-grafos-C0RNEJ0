#!/bin/bash
# Script para limpiar el proyecto de archivos generados y temporales

echo "🧹 Iniciando limpieza del proyecto..."

# Eliminar entorno virtual
if [ -d "venv" ]; then
    echo "🗑️  Eliminando entorno virtual (venv)..."
    rm -rf venv
fi

# Eliminar carpeta de build
if [ -d "build" ]; then
    echo "🗑️  Eliminando carpeta build..."
    rm -rf build
fi

# Eliminar archivos compilados (.so)
echo "🗑️  Eliminando archivos compilados (.so)..."
rm -f *.so

# Eliminar código C++ generado por Cython
if [ -f "src/grafo_wrapper.cpp" ]; then
    echo "🗑️  Eliminando código generado (src/grafo_wrapper.cpp)..."
    rm -f src/grafo_wrapper.cpp
fi

# Eliminar caché de Python (__pycache__)
echo "🗑️  Eliminando caché de Python..."
find . -type d -name "__pycache__" -exec rm -rf {} +

echo "✨ Limpieza completa. El proyecto está listo para compartir."
echo "ℹ️  Para reinstalar todo, simplemente ejecuta: ./run.sh"
