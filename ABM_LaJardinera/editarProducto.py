import sqlite3
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import tkinter as tk
from comandosSQL import *
from agregarProducto import *

def consultar_categorias():
    cursor.execute("SELECT nombre FROM categoria")
    categoria = cursor.fetchall()
    base_datos.commit()
    return ['Seleccionar Categoria'] + [nombre[0] for nombre in categoria]

def consultar_proveedores():
    cursor.execute("SELECT razon_social FROM proveedor")
    proveedores = cursor.fetchall()
    base_datos.commit()
    return ['Seleccionar Proveedor'] + [nombre[0] for nombre in proveedores]

def mostrar_formulario_edicion(tree):

    ventana_formulario_edicion = Toplevel()

    ventana_formulario_edicion.resizable(width=False, height=False)

    ventana_formulario_edicion.title('Editar Producto')

    item_seleccionado = tree.selection()

    if item_seleccionado:

        fila_seleccionada = tree.item(item_seleccionado)
        datos = fila_seleccionada['values']

        titulo = Label(ventana_formulario_edicion, text='Editar Producto', font=65)
        titulo.grid(row=0, columnspan=2, padx=10, pady=10)

        titulo_producto = Label(ventana_formulario_edicion, text='Nombre Producto', font=45)
        titulo_producto.grid(row=1, column=0, padx=5, pady=5)

        nombre_producto = Entry(ventana_formulario_edicion, font=45)
        nombre_producto.grid(row=1, column=1)
        nombre_producto.insert(0, datos[1])  

        titulo_precio = Label(ventana_formulario_edicion, text='Precio', font=45)
        titulo_precio.grid(row=2, column=0, padx=5, pady=5)

        precio_producto = Entry(ventana_formulario_edicion, font=45)
        precio_producto.grid(row=2, column=1)
        precio_producto.insert(0, datos[2]) 

        titulo_stock = Label(ventana_formulario_edicion, text='Stock', font=45)
        titulo_stock.grid(row=3, column=0, padx=5, pady=5)

        stock_producto = Entry(ventana_formulario_edicion, font=45)
        stock_producto.grid(row=3, column=1)
        stock_producto.insert(0, datos[3])  

        titulo_marca = Label(ventana_formulario_edicion, text='Marca', font=45)
        titulo_marca.grid(row=4, column=0)

        proveedor_opciones = consultar_proveedores()
        proveedor_seleccionada = StringVar()
        proveedor_seleccionada.set(datos[4])

        producto_proveedor_opciones = OptionMenu(ventana_formulario_edicion, proveedor_seleccionada, *proveedor_opciones )
        producto_proveedor_opciones.grid(row=4, column=1)

        titulo_categoria = Label(ventana_formulario_edicion, text='Categoria', font=45)
        titulo_categoria.grid(row=5, column=0)

        categoria_opciones = consultar_categorias()
        categoria_seleccionada = StringVar()
        categoria_seleccionada.set(datos[5])

        producto_categoria_opciones = OptionMenu(ventana_formulario_edicion, categoria_seleccionada, *categoria_opciones)
        producto_categoria_opciones.grid(row=5, column=1)

        boton_agregar_categoria = Button(ventana_formulario_edicion, text='+', command=lambda:agregar_categoria(ventana_agregar_producto))
        boton_agregar_categoria.grid(row=5, column=2)

        def guardar_cambios():
            
            nombre = nombre_producto.get()
            precio = precio_producto.get()
            stock = stock_producto.get()
            proveedor = proveedor_seleccionada.get()
            categoria = categoria_seleccionada.get()
            base_datos = sqlite3.connect('LaJardinera.bd')
            cursor = base_datos.cursor()

            cursor.execute("SELECT id_proveedor FROM proveedor WHERE razon_social = ?", (proveedor,))
            proveedor_id = cursor.fetchone()[0]

            cursor.execute("SELECT id_categoria FROM categoria WHERE nombre = ?", (categoria,))
            categoria_id = cursor.fetchone()[0]
            
            cursor.execute("UPDATE producto SET nombre=?, precio=?, cantidad=?, id_proveedor=?, id_categoria=? WHERE producto_id=?", (nombre, precio, stock, proveedor_id, categoria_id, datos[0]))
            base_datos.commit()
            messagebox.showinfo('Completado','El producto ha sido modificado con éxito.')

        def eliminar_productos():

            item_seleccionado = tree.selection()

            if item_seleccionado:
                
                fila_seleccionada = tree.item(item_seleccionado)
                datos = fila_seleccionada['values']

                base_datos =sqlite3.connect('LaJardinera.bd')
                cursor = base_datos.cursor()

                cursor.execute("DELETE FROM producto WHERE id_producto=?", (datos[0],))

                base_datos.commit()

                base_datos.close()

                tree.delete(item_seleccionado)

                messagebox.showinfo('Completado','El producto ha sido eliminado con éxito.')

               
    boton_guardar = Button(ventana_formulario_edicion, text='Guardar Cambios', command=guardar_cambios, font=45)
    boton_guardar.grid(row=6, columnspan=2, padx=5, pady=5)

    boton_eliminar =Button(ventana_formulario_edicion, text='Eliminar Producto', command=eliminar_productos, font=45)
    boton_eliminar.grid(row=7, columnspan=2, padx=5, pady=5)