#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NeuroNet: Interfaz Gráfica para Análisis de Grafos Masivos
===========================================================

Sistema híbrido que utiliza C++ (vía Cython) para procesamiento
y Python para visualización interactiva.

Autor: Jose Guadalupe Cornejo Alva
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import sys
import os

try:
    import matplotlib
    matplotlib.use('TkAgg')
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    from matplotlib.figure import Figure
    import networkx as nx
except ImportError:
    print("ERROR: Instalar dependencias con: pip install matplotlib networkx")
    sys.exit(1)

# Importar el módulo Cython compilado
try:
    from grafo_wrapper import PyGrafoDisperso
except ImportError:
    print("ERROR: Módulo 'grafo_wrapper' no encontrado.")
    print("Compilar con: python setup.py build_ext --inplace")
    sys.exit(1)


class NeuroNetGUI:
    """
    Interfaz gráfica principal de NeuroNet
    """
    
    def __init__(self, root):
        self.root = root
        self.root.title("NeuroNet - Análisis de Grafos Masivos")
        self.root.geometry("1400x900")
        self.root.configure(bg='#2b2b2b')
        
        # Motor de grafos C++
        self.grafo = PyGrafoDisperso()
        self.datos_cargados = False
        self.archivo_actual = None
        
        # Inicializar interfaz
        self.crear_widgets()
        
    def crear_widgets(self):
        """Crea todos los widgets de la interfaz"""
        
        # Frame principal con grid
        main_frame = tk.Frame(self.root, bg='#2b2b2b')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # ============= PANEL SUPERIOR: CONTROLES =============
        control_frame = tk.LabelFrame(
            main_frame, 
            text="Panel de Control", 
            bg='#3c3c3c', 
            fg='white',
            font=('Arial', 12, 'bold'),
            padx=10,
            pady=10
        )
        control_frame.grid(row=0, column=0, columnspan=2, sticky='ew', pady=(0, 10))
        
        # Botón cargar datos
        self.btn_cargar = tk.Button(
            control_frame,
            text="Cargar Dataset",
            command=self.cargar_dataset,
            bg='#4CAF50',
            fg='white',
            font=('Arial', 11, 'bold'),
            padx=20,
            pady=10,
            cursor='hand2'
        )
        self.btn_cargar.grid(row=0, column=0, padx=5, pady=5)
        
        # Label del archivo actual
        self.lbl_archivo = tk.Label(
            control_frame,
            text="Ningún archivo cargado",
            bg='#3c3c3c',
            fg='#aaaaaa',
            font=('Arial', 10)
        )
        self.lbl_archivo.grid(row=0, column=1, padx=10, pady=5, sticky='w')
        
        # Botón calcular nodo crítico
        self.btn_grado = tk.Button(
            control_frame,
            text="Nodo Crítico (Mayor Grado)",
            command=self.calcular_nodo_critico,
            bg='#2196F3',
            fg='white',
            font=('Arial', 11, 'bold'),
            padx=20,
            pady=10,
            cursor='hand2',
            state='disabled'
        )
        self.btn_grado.grid(row=0, column=2, padx=5, pady=5)
        
        # Frame para BFS
        bfs_frame = tk.Frame(control_frame, bg='#3c3c3c')
        bfs_frame.grid(row=1, column=0, columnspan=3, pady=10, sticky='w')
        
        tk.Label(
            bfs_frame,
            text="Configuración BFS:",
            bg='#3c3c3c',
            fg='white',
            font=('Arial', 10, 'bold')
        ).grid(row=0, column=0, padx=5)
        
        tk.Label(
            bfs_frame,
            text="Nodo Inicial:",
            bg='#3c3c3c',
            fg='white',
            font=('Arial', 10)
        ).grid(row=0, column=1, padx=5)
        
        self.entry_nodo_inicial = tk.Entry(bfs_frame, width=10, font=('Arial', 10))
        self.entry_nodo_inicial.insert(0, "0")
        self.entry_nodo_inicial.grid(row=0, column=2, padx=5)
        
        tk.Label(
            bfs_frame,
            text="Profundidad:",
            bg='#3c3c3c',
            fg='white',
            font=('Arial', 10)
        ).grid(row=0, column=3, padx=5)
        
        self.entry_profundidad = tk.Entry(bfs_frame, width=10, font=('Arial', 10))
        self.entry_profundidad.insert(0, "2")
        self.entry_profundidad.grid(row=0, column=4, padx=5)
        
        self.btn_bfs = tk.Button(
            bfs_frame,
            text="Ejecutar BFS",
            command=self.ejecutar_bfs,
            bg='#FF9800',
            fg='white',
            font=('Arial', 11, 'bold'),
            padx=20,
            pady=5,
            cursor='hand2',
            state='disabled'
        )
        self.btn_bfs.grid(row=0, column=5, padx=10)
        
        # ============= PANEL IZQUIERDO: MÉTRICAS =============
        metrics_frame = tk.LabelFrame(
            main_frame,
            text="Métricas del Grafo",
            bg='#3c3c3c',
            fg='white',
            font=('Arial', 12, 'bold'),
            padx=10,
            pady=10
        )
        metrics_frame.grid(row=1, column=0, sticky='nsew', padx=(0, 5))
        
        # Métricas
        self.lbl_nodos = self.crear_metrica(metrics_frame, "Nodos:", "0", 0)
        self.lbl_aristas = self.crear_metrica(metrics_frame, "Aristas:", "0", 1)
        self.lbl_memoria = self.crear_metrica(metrics_frame, "Memoria CSR:", "0 MB", 2)
        self.lbl_nodo_critico = self.crear_metrica(metrics_frame, "Nodo Crítico:", "N/A", 3)
        self.lbl_grado_max = self.crear_metrica(metrics_frame, "Grado Máximo:", "0", 4)
        
        # Logs
        logs_frame = tk.LabelFrame(
            metrics_frame,
            text="Logs del Sistema",
            bg='#3c3c3c',
            fg='white',
            font=('Arial', 10, 'bold')
        )
        logs_frame.grid(row=5, column=0, columnspan=2, sticky='nsew', pady=(20, 0))
        
        self.text_logs = scrolledtext.ScrolledText(
            logs_frame,
            bg='#1e1e1e',
            fg='#00ff00',
            font=('Courier', 9),
            height=15,
            wrap=tk.WORD
        )
        self.text_logs.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Redirigir stdout a logs
        sys.stdout = TextRedirector(self.text_logs)
        
        # ============= PANEL DERECHO: VISUALIZACIÓN =============
        viz_frame = tk.LabelFrame(
            main_frame,
            text="Visualización del Subgrafo",
            bg='#3c3c3c',
            fg='white',
            font=('Arial', 12, 'bold'),
            padx=10,
            pady=10
        )
        viz_frame.grid(row=1, column=1, sticky='nsew', padx=(5, 0))
        
        # Canvas de matplotlib
        self.fig = Figure(figsize=(8, 6), facecolor='#2b2b2b')
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor('#1e1e1e')
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=viz_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Configurar grid weights
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_columnconfigure(0, weight=1, minsize=400)
        main_frame.grid_columnconfigure(1, weight=2, minsize=700)
        
        print("[GUI] NeuroNet inicializado correctamente.")
        print("[GUI] Esperando carga de dataset...")
    
    def crear_metrica(self, parent, label, valor, row):
        """Crea un par label-valor para métrica"""
        tk.Label(
            parent,
            text=label,
            bg='#3c3c3c',
            fg='#aaaaaa',
            font=('Arial', 10, 'bold')
        ).grid(row=row, column=0, sticky='w', pady=5)
        
        lbl_valor = tk.Label(
            parent,
            text=valor,
            bg='#3c3c3c',
            fg='#00ff00',
            font=('Arial', 11)
        )
        lbl_valor.grid(row=row, column=1, sticky='w', pady=5, padx=10)
        
        return lbl_valor
    
    def cargar_dataset(self):
        """Carga un dataset desde archivo"""
        archivo = filedialog.askopenfilename(
            title="Seleccionar Dataset",
            filetypes=[
                ("Archivos de texto", "*.txt"),
                ("Todos los archivos", "*.*")
            ]
        )
        
        if not archivo:
            return
        
        try:
            self.archivo_actual = archivo
            self.lbl_archivo.config(text=f"Cargando: {os.path.basename(archivo)}...")
            self.root.update()
            
            # Cargar en el motor C++
            exito = self.grafo.cargar_datos(archivo)
            
            if exito:
                self.datos_cargados = True
                self.lbl_archivo.config(
                    text=f"[OK] {os.path.basename(archivo)}",
                    fg='#00ff00'
                )
                
                # Actualizar métricas
                self.actualizar_metricas()
                
                # Habilitar botones
                self.btn_grado.config(state='normal')
                self.btn_bfs.config(state='normal')
                
                messagebox.showinfo("Éxito", "Dataset cargado correctamente")
            else:
                messagebox.showerror("Error", "No se pudo cargar el dataset")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar archivo:\n{str(e)}")
            print(f"[GUI] ERROR: {str(e)}")
    
    def actualizar_metricas(self):
        """Actualiza las métricas mostradas"""
        self.lbl_nodos.config(text=f"{self.grafo.get_num_nodos():,}")
        self.lbl_aristas.config(text=f"{self.grafo.get_num_aristas():,}")
        self.lbl_memoria.config(text=f"{self.grafo.get_memoria_estimada():.2f} MB")
    
    def calcular_nodo_critico(self):
        """Calcula el nodo con mayor grado"""
        if not self.datos_cargados:
            messagebox.showwarning("Advertencia", "Primero carga un dataset")
            return
        
        try:
            nodo_id, grado = self.grafo.obtener_grado()
            self.lbl_nodo_critico.config(text=str(nodo_id))
            self.lbl_grado_max.config(text=str(grado))
            
            messagebox.showinfo(
                "Nodo Crítico",
                f"Nodo {nodo_id} tiene el mayor grado: {grado} conexiones"
            )
        except Exception as e:
            messagebox.showerror("Error", f"Error al calcular:\n{str(e)}")
    
    def ejecutar_bfs(self):
        """Ejecuta BFS y visualiza el resultado"""
        if not self.datos_cargados:
            messagebox.showwarning("Advertencia", "Primero carga un dataset")
            return
        
        try:
            nodo_inicial = int(self.entry_nodo_inicial.get())
            profundidad = int(self.entry_profundidad.get())
            
            if profundidad < 1:
                messagebox.showwarning("Advertencia", "La profundidad debe ser >= 1")
                return
            
            # Ejecutar BFS en C++
            resultado = self.grafo.bfs(nodo_inicial, profundidad)
            
            if not resultado:
                messagebox.showwarning(
                    "Advertencia",
                    f"Nodo {nodo_inicial} no encontrado en el grafo"
                )
                return
            
            # Visualizar resultado
            self.visualizar_subgrafo(resultado, nodo_inicial)
            
        except ValueError:
            messagebox.showerror("Error", "Ingresa valores numéricos válidos")
        except Exception as e:
            messagebox.showerror("Error", f"Error al ejecutar BFS:\n{str(e)}")
    
    def visualizar_subgrafo(self, nodos_bfs, nodo_raiz):
        """Visualiza el subgrafo resultante de BFS"""
        print(f"[GUI] Visualizando subgrafo con {len(nodos_bfs)} nodos...")
        
        # Limpiar figura
        self.ax.clear()
        
        # Crear grafo NetworkX (solo para visualización)
        G = nx.DiGraph()
        
        # Agregar nodos con sus niveles
        nodos_por_nivel = {}
        for nodo, nivel in nodos_bfs:
            G.add_node(nodo, nivel=nivel)
            if nivel not in nodos_por_nivel:
                nodos_por_nivel[nivel] = []
            nodos_por_nivel[nivel].append(nodo)
        
        # Agregar aristas consultando vecinos desde C++
        for nodo, _ in nodos_bfs:
            vecinos = self.grafo.get_vecinos(nodo)
            for vecino in vecinos:
                if G.has_node(vecino):  # Solo si el vecino está en el BFS
                    G.add_edge(nodo, vecino)
        
        # Layout jerárquico por niveles
        pos = {}
        for nivel, nodos in nodos_por_nivel.items():
            y = -nivel  # Niveles hacia abajo
            for i, nodo in enumerate(nodos):
                x = i - len(nodos) / 2
                pos[nodo] = (x, y)
        
        # Colores por nivel
        colores = []
        for nodo in G.nodes():
            nivel = G.nodes[nodo]['nivel']
            if nodo == nodo_raiz:
                colores.append('#ff0000')  # Rojo para raíz
            else:
                # Gradiente de azul a verde
                intensidad = 1 - (nivel / max(nodos_por_nivel.keys()))
                colores.append((0, intensidad, 1-intensidad))
        
        # Dibujar
        nx.draw(
            G, pos,
            node_color=colores,
            node_size=500,
            with_labels=True,
            font_size=8,
            font_color='white',
            edge_color='#666666',
            arrows=True,
            arrowsize=10,
            ax=self.ax
        )
        
        self.ax.set_title(
            f'BFS desde Nodo {nodo_raiz} - {len(nodos_bfs)} nodos alcanzados',
            color='white',
            fontsize=12,
            fontweight='bold'
        )
        self.ax.axis('off')
        
        self.canvas.draw()
        print("[GUI] Visualización completada.")


class TextRedirector:
    """Redirige stdout a un widget de texto"""
    
    def __init__(self, widget):
        self.widget = widget
    
    def write(self, string):
        self.widget.insert(tk.END, string)
        self.widget.see(tk.END)
    
    def flush(self):
        pass


def main():
    """Función principal"""
    print("="*60)
    print("NeuroNet: Análisis de Grafos Masivos")
    print("Sistema Híbrido C++ + Python")
    print("="*60)
    
    root = tk.Tk()
    app = NeuroNetGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
