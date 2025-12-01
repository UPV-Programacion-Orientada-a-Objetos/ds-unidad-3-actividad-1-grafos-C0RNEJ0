#!/bin/bash
# Script para descargar datasets masivos de SNAP (Stanford Network Analysis Project)

echo "=========================================="
echo "NeuroNet - Descarga de Datasets SNAP"
echo "=========================================="
echo ""

# Crear directorio data si no existe
mkdir -p data
cd data

# Dataset 1: Web-Google (grafía de enlaces web de Google)
echo "[1/5] Descargando Web-Google (~875K nodos, ~5M aristas)..."
if [ ! -f "web-Google.txt" ]; then
    wget https://snap.stanford.edu/data/web-Google.txt.gz
    gunzip web-Google.txt.gz
    echo "OK - Web-Google descargado"
else
    echo "OK - Web-Google ya existe"
fi

echo ""

# Dataset 2: Amazon Product Co-Purchasing Network
echo "[2/5] Descargando Amazon0601 (~400K nodos, ~3.3M aristas)..."
if [ ! -f "amazon0601.txt" ]; then
    wget https://snap.stanford.edu/data/amazon0601.txt.gz
    gunzip amazon0601.txt.gz
    echo "OK - Amazon0601 descargado"
else
    echo "OK - Amazon0601 ya existe"
fi

echo ""

# Dataset 3: Email-Enron (red de emails de Enron - más pequeño)
echo "[3/5] Descargando Email-Enron (~36K nodos, ~183K aristas)..."
if [ ! -f "email-Enron.txt" ]; then
    wget https://snap.stanford.edu/data/email-Enron.txt.gz
    gunzip email-Enron.txt.gz
    echo "OK - Email-Enron descargado"
else
    echo "OK - Email-Enron ya existe"
fi

echo ""

# Dataset 4: Orkut (Red Social - MASIVO)
echo "[4/5] Descargando com-Orkut (~3M nodos, ~117M aristas)..."
echo "Advertencia: Este archivo es muy grande (varios GB descomprimido)."
if [ ! -f "com-Orkut.txt" ]; then
    wget https://snap.stanford.edu/data/com-Orkut.txt.gz
    gunzip com-Orkut.txt.gz
    echo "OK - com-Orkut descargado"
else
    echo "OK - com-Orkut ya existe"
fi

echo ""

# Dataset 5: LiveJournal (Red Social - MASIVO)
echo "[5/5] Descargando soc-LiveJournal1 (~4.8M nodos, ~69M aristas)..."
echo "Advertencia: Este archivo es muy grande."
if [ ! -f "soc-LiveJournal1.txt" ]; then
    wget https://snap.stanford.edu/data/soc-LiveJournal1.txt.gz
    gunzip soc-LiveJournal1.txt.gz
    echo "OK - soc-LiveJournal1 descargado"
else
    echo "OK - soc-LiveJournal1 ya existe"
fi

echo ""
echo "=========================================="
echo "Descarga completada"
echo "=========================================="
echo ""
echo "Datasets disponibles:"
echo "  - test_graph.txt (pequeño, ~28 nodos)"
echo "  - email-Enron.txt (mediano, ~36K nodos)"
echo "  - amazon0601.txt (grande, ~400K nodos)"
echo "  - web-Google.txt (muy grande, ~875K nodos)"
echo "  - com-Orkut.txt (MASIVO, ~3M nodos)"
echo "  - soc-LiveJournal1.txt (MASIVO, ~4.8M nodos)"
echo ""
echo "Usar desde NeuroNet GUI o manualmente."
