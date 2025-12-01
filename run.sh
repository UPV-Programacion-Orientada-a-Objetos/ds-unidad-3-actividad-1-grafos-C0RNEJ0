#!/bin/bash
# Script de uso rápido de NeuroNet

echo "=========================================="
echo "NeuroNet - Guía de Uso Rápido"
echo "=========================================="
echo ""

# Verificar si existe el entorno virtual
# Verificar y configurar entorno virtual
if [ ! -d "venv" ]; then
    echo "Entorno virtual no encontrado. Creando..."
    python3 -m venv venv
fi

source venv/bin/activate

# Verificar si las dependencias están instaladas
if ! python -c "import Cython" &> /dev/null; then
    echo "Instalando dependencias faltantes..."
    pip install --quiet cython networkx matplotlib
    echo "Compilando módulo Cython..."
    python setup.py build_ext --inplace
fi

echo "Entorno virtual listo"

echo ""
echo "Opciones disponibles:"
echo "  1) Ejecutar GUI"
echo "  2) Ejecutar tests básicos"
echo "  3) Compilar módulo Cython"
echo "  4) Descargar datasets SNAP"
echo "  5) Salir"
echo ""
read -p "Selecciona una opción (1-5): " opcion

case $opcion in
    1)
        echo ""
        echo "Iniciando GUI de NeuroNet..."
        source venv/bin/activate
        python neuronet_gui.py
        ;;
    2)
        echo ""
        echo "Ejecutando tests básicos..."
        source venv/bin/activate
        python test_basic.py
        ;;
    3)
        echo ""
        echo "Compilando módulo..."
        source venv/bin/activate
        python setup.py build_ext --inplace
        echo "Compilación completa"
        ;;
    4)
        echo ""
        echo "Descargando datasets SNAP..."
        cd data
        ./download_snap.sh
        cd ..
        ;;
    5)
        echo "Hasta luego!"
        exit 0
        ;;
    *)
        echo "Opción inválida"
        exit 1
        ;;
esac
