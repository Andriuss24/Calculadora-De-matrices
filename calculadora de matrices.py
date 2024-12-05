# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 15:48:57 2024

@authores:  Jairo Pizarro
            Anyelo Daniel Ruiz 
            Brayan Perenguez
            Sebastian Barahona
"""

import numpy as np
import tkinter as tk
from tkinter import messagebox

# Funciones de operaciones con matrices


def mostrar_matriz(matriz):
    return "\n".join([" ".join(f"{x:10.3f}" if abs(x) > 1e-10 else f"{0:10.3f}" for x in fila) for fila in matriz])


def metodo_gauss(matriz):
    filas, columnas = matriz.shape
    matriz = matriz.astype(float)
    pasos = []
    for i in range(filas):
        pivote = matriz[i][i]
        if pivote == 0:
            messagebox.showerror(
                "Error", "El pivote es cero. No se puede continuar.")
            return
        pasos.append(
            f"\nNormalizando la fila {i + 1} dividiendo por el pivote {pivote:.3f}.")
        matriz[i] /= pivote
        pasos.append(mostrar_matriz(matriz))

        for k in range(i + 1, filas):
            factor = matriz[k][i]
            pasos.append(
                f"\nEliminando elemento en la fila {k + 1}, columna {i + 1} usando el factor {factor:.3f}.")
            matriz[k] -= factor * matriz[i]
            pasos.append(mostrar_matriz(matriz))

    soluciones = np.zeros(filas)
    for i in range(filas - 1, -1, -1):
        sumatoria = sum(matriz[i][j] * soluciones[j]
                        for j in range(i + 1, filas))
        soluciones[i] = matriz[i][-1] - sumatoria

    pasos.append("\nSoluciones del sistema:")
    pasos.extend([f"x{i + 1} = {sol:.3f}" for i, sol in enumerate(soluciones)])
    return "\n".join(pasos)


def metodo_gauss_jordan(matriz):
    filas, columnas = matriz.shape
    matriz = matriz.astype(float)
    pasos = []
    for i in range(filas):
        pivote = matriz[i][i]
        if pivote == 0:
            messagebox.showerror(
                "Error", "El pivote es cero. No se puede continuar.")
            return
        pasos.append(
            f"\nNormalizando la fila {i + 1} dividiendo por el pivote {pivote:.3f}.")
        matriz[i] /= pivote
        pasos.append(mostrar_matriz(matriz))

        for k in range(filas):
            if k != i:
                factor = matriz[k][i]
                pasos.append(
                    f"\nEliminando elemento en la fila {k + 1}, columna {i + 1} usando el factor {factor:.3f}.")
                matriz[k] -= factor * matriz[i]
                pasos.append(mostrar_matriz(matriz))

    pasos.append("\nSoluciones del sistema:")
    soluciones = matriz[:, -1]
    pasos.extend([f"x{i + 1} = {sol:.3f}" for i, sol in enumerate(soluciones)])
    return "\n".join(pasos)

# Interfaz gráfica con tkinter


def iniciar_gui():
    def generar_matriz():
        try:
            ecuaciones = int(entry_ecuaciones.get())
            if ecuaciones <= 0:
                raise ValueError(
                    "El número de ecuaciones debe ser mayor que cero.")

            # Limpiar las casillas anteriores
            limpiar_todo()

            global entries
            entries = []
            for i in range(ecuaciones):
                row_entries = []
                for j in range(ecuaciones + 1):  # +1 para el término independiente
                    entry = tk.Entry(matrix_frame, width=7)
                    entry.grid(row=i, column=j, padx=5, pady=5, sticky="nsew")
                    row_entries.append(entry)
                entries.append(row_entries)

            # Etiquetas de ayuda para columnas
            for j in range(ecuaciones):
                tk.Label(
                    matrix_frame, text=f"x{j+1}", width=5).grid(row=ecuaciones, column=j, padx=5, pady=5)
            tk.Label(matrix_frame, text="Ind", width=5).grid(
                row=ecuaciones, column=ecuaciones, padx=5, pady=5)

        except ValueError:
            messagebox.showerror(
                "Error", "Ingresa un número válido para las ecuaciones.")

    def realizar_operacion():
        try:
            matriz = []
            for row_entries in entries:
                row = [float(entry.get()) for entry in row_entries]
                matriz.append(row)
            matriz = np.array(matriz)

            operacion = opcion.get()
            resultado = None

            if operacion == "Método de Gauss":
                resultado = metodo_gauss(matriz)
            elif operacion == "Método de Gauss-Jordan":
                resultado = metodo_gauss_jordan(matriz)

            text_resultado.delete(1.0, tk.END)
            text_resultado.insert(tk.END, resultado)

        except ValueError:
            messagebox.showerror(
                "Error", "Verifica que todas las celdas contengan números válidos.")

    def limpiar_todo():
        # Limpiar las casillas de la matriz
        for widget in matrix_frame.winfo_children():
            widget.destroy()
        # Limpiar la salida de resultados
        text_resultado.delete(1.0, tk.END)

    root = tk.Tk()
    root.title("Resolución de Sistemas de Ecuaciones")
    root.geometry("900x700")  # Tamaño inicial de la ventana
    root.minsize(700, 500)  # Tamaño mínimo para evitar recortes
    root.columnconfigure(1, weight=1)  # Permitir que las columnas se expandan
    root.rowconfigure(4, weight=1)  # Hacer el cuadro de texto ajustable

    tk.Label(root, text="Número de ecuaciones:").grid(
        row=0, column=0, sticky="w", padx=10, pady=5)
    entry_ecuaciones = tk.Entry(root)
    entry_ecuaciones.grid(row=0, column=1, padx=10, pady=5)

    tk.Button(root, text="Generar matriz", command=generar_matriz).grid(
        row=1, column=0, columnspan=2, pady=5)

    global matrix_frame
    matrix_frame = tk.Frame(root)
    matrix_frame.grid(row=2, column=0, columnspan=2,
                      padx=10, pady=5, sticky="nsew")
    root.rowconfigure(2, weight=1)

    tk.Label(root, text="Operación:").grid(
        row=3, column=0, sticky="w", padx=10)
    opcion = tk.StringVar(root)
    opcion.set("Método de Gauss")  # Valor por defecto
    operacion_menu = tk.OptionMenu(
        root, opcion, "Método de Gauss", "Método de Gauss-Jordan")
    operacion_menu.grid(row=3, column=1, sticky="w", padx=10)

    boton_calcular = tk.Button(
        root, text="Realizar operación", command=realizar_operacion)
    boton_calcular.grid(row=4, column=0, columnspan=2, pady=5)

    boton_limpiar = tk.Button(root, text="Limpiar todo", command=limpiar_todo)
    boton_limpiar.grid(row=5, column=0, columnspan=2, pady=5)

    text_resultado = tk.Text(root, wrap="word")
    text_resultado.grid(row=6, column=0, columnspan=2,
                        padx=10, pady=5, sticky="nsew")
    # Aumenta el peso para que sea más alto y ajustable
    root.rowconfigure(6, weight=2)

    root.mainloop()


# Iniciar la interfaz gráfica
if __name__ == "__main__":
    iniciar_gui()
