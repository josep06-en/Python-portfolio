import sqlite3
from flask import Flask, request, jsonify
import tkinter as tk
from tkinter import messagebox
import pandas as pd
import matplotlib.pyplot as plt
import threading

# Inicializar la aplicación Flask
app = Flask(__name__)

# Conectar a la base de datos SQLite
def connect_db():
    conn = sqlite3.connect("inventario.db", check_same_thread=False)
    return conn

# Crear la tabla de productos
def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            cantidad INTEGER NOT NULL,
            precio REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Ruta para agregar un producto
@app.route("/producto", methods=["POST"])
def add_product():
    data = request.json
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO productos (nombre, cantidad, precio) VALUES (?, ?, ?)",
                   (data["nombre"], data["cantidad"], data["precio"]))
    conn.commit()
    conn.close()
    return jsonify({"message": "Producto agregado correctamente"})

# Ruta para obtener todos los productos
@app.route("/productos", methods=["GET"])
def get_products():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    conn.close()
    return jsonify(productos)

# Función para generar un reporte en CSV
def generar_reporte():
    conn = connect_db()
    df = pd.read_sql_query("SELECT * FROM productos", conn)
    df.to_csv("reporte_inventario.csv", index=False)
    conn.close()
    messagebox.showinfo("Reporte", "Reporte generado correctamente como reporte_inventario.csv")

# Interfaz gráfica con Tkinter
def interfaz_grafica():
    root = tk.Tk()
    root.title("Gestión de Inventarios")
    tk.Button(root, text="Generar Reporte", command=generar_reporte).pack()
    root.mainloop()

# Ejecutar Flask y la interfaz en hilos separados
if __name__ == "__main__":
    create_table()
    threading.Thread(target=app.run, kwargs={"debug": True, "use_reloader": False}).start()
    interfaz_grafica()
