from tkinter import *
import sqlite3
from tkinter import filedialog
from tkinter import messagebox
import os

base_datos = sqlite3.connect('LaJardinera.bd')
cursor = base_datos.cursor()


def agregar_proveedor(a):
    ventana_agregar_proveedor = Toplevel(a)
    ventana_agregar_proveedor.title('Agregar Proveedor')

    agregar_proveedor_label = Label(ventana_agregar_proveedor, text='Agregar Proveedor', font=('Helvetica',60))
    agregar_proveedor_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

    proveedor_razon_social_label = Label(ventana_agregar_proveedor, text='Razon Social: ', font=('Helvetica',15))
    proveedor_razon_social_label.grid(row=1, column=0, padx=5, pady=5)

    proveedor_razon_social_entry = Entry(ventana_agregar_proveedor)
    proveedor_razon_social_entry.grid(row=1, column=1, padx=5, pady=5)

    proveedor_cuit_label = Label(ventana_agregar_proveedor, text='CUIT: ', font=('Helvetica',15))
    proveedor_cuit_label.grid(row=2, column=0, padx=5, pady=5)

    proveedor_cuit_entry = Entry(ventana_agregar_proveedor)
    proveedor_cuit_entry.grid(row=2, column=1, padx=5, pady=5)

    proveedor_domicilio_label = Label(ventana_agregar_proveedor, text='Domicilio: ', font=('Helvetica',15))
    proveedor_domicilio_label.grid(row=3, column=0, padx=5, pady=5)

    proveedor_domicilio_entry = Entry(ventana_agregar_proveedor)
    proveedor_domicilio_entry.grid(row=3, column=1, padx=5, pady=5)

    proveedor_telefono_label = Label(ventana_agregar_proveedor, text='Telefono: ', font=('Helvetica',15))
    proveedor_telefono_label.grid(row=4, column=0, padx=5, pady=5)

    proveedor_telefono_entry = Entry(ventana_agregar_proveedor)
    proveedor_telefono_entry.grid(row=4, column=1, padx=5, pady=5)

    proveedor_email_label = Label(ventana_agregar_proveedor, text='Email: ', font=('Helvetica',15))
    proveedor_email_label.grid(row=5, column=0, padx=5, pady=5)

    proveedor_email_entry = Entry(ventana_agregar_proveedor)
    proveedor_email_entry.grid(row=5, column=1, padx=5, pady=5)

    def guardar_proveedor():
        razon_social = proveedor_razon_social_entry.get()
        cuit = proveedor_cuit_entry.get()
        domicilio = proveedor_domicilio_entry.get()
        numeroTelefono = proveedor_telefono_entry.get()
        email = proveedor_email_entry.get()

        cursor.execute('INSERT INTO proveedor (razon_social, cuit, domicilio, numero_telefono, email) VALUES (?,?,?,?,?)',
               (razon_social, cuit, domicilio, numeroTelefono, email))
        base_datos.commit()
        
        messagebox.showinfo('Completado','El proveedor ha sido guardado con éxito.')
        ventana_agregar_proveedor.destroy()

    boton_guardar_proveedor = Button(ventana_agregar_proveedor, text='Guardar', command=guardar_proveedor, font=('Helvetica',15))
    boton_guardar_proveedor.grid(row=6, column=0, columnspan=2)

def consultar_proveedores():
    cursor.execute("SELECT razon_social FROM proveedor")
    proveedores = cursor.fetchall()
    base_datos.commit()
    return ['Seleccionar Proveedor'] + [nombre[0] for nombre in proveedores]

def agregar_categoria(a):
    ventana_agregar_categoria = Toplevel(a)
    ventana_agregar_categoria.title('Agregar Categoria')

    agregar_categoria_label = Label(ventana_agregar_categoria, text='Agregar Categoria', font=('Helvetica',60))
    agregar_categoria_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

    categoria_nombre_label = Label(ventana_agregar_categoria, text='Nombre: ', font=('Helvetica',15))
    categoria_nombre_label.grid(row=1, column=0, padx=5, pady=5)

    categoria_nombre_entry = Entry(ventana_agregar_categoria)
    categoria_nombre_entry.grid(row=1, column=1, padx=5, pady=5)

    def guardar_categoria():
        nombre = categoria_nombre_entry.get()

        cursor.execute('INSERT INTO categoria (nombre) VALUES (?)',
               (nombre,))
        base_datos.commit()
        
        messagebox.showinfo('Completado','La categoria ha sido guardada con éxito.')
        ventana_agregar_categoria.destroy()

    boton_guardar_proveedor = Button(ventana_agregar_categoria, text='Guardar', command=guardar_categoria, font=('Helvetica',15))
    boton_guardar_proveedor.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

def consultar_categorias():
    cursor.execute("SELECT nombre FROM categoria")
    categoria = cursor.fetchall()
    base_datos.commit()
    return ['Seleccionar Categoria'] + [nombre[0] for nombre in categoria]

def ventana_agregar_producto(a):

    def guardar_producto():
        nombre = producto_nombre_entry.get()
        precio = producto_precio_entry.get()
        cantidad = producto_cantidad_entry.get()
        proveedor = proveedor_seleccionada.get()
        categoria = categoria_seleccionada.get()
        
        cursor.execute('SELECT id_proveedor FROM proveedor WHERE razon_social = ?', (proveedor, ))
        id_proveedor = cursor.fetchone()

        cursor.execute('SELECT id_categoria FROM categoria WHERE nombre = ?', (categoria, ))
        id_categoria = cursor.fetchone()

        cursor.execute('INSERT INTO producto (nombre, precio, cantidad, id_proveedor, id_categoria) VALUES (?,?,?,?,?)',
                    (nombre, precio, cantidad, id_proveedor[0], id_categoria[0]))
        base_datos.commit()

        messagebox.showinfo('Completado','El producto ha sido guardado con éxito.')

        producto_nombre_entry.delete(0, 'end')
        producto_precio_entry.delete(0, 'end')
        producto_cantidad_entry.delete(0, 'end')
        proveedor_seleccionada.set('Seleccionar Proveedor')
        categoria_seleccionada.set('Seleccionar Categoria')

    ventana_agregar_producto = Toplevel(a)

    ventana_agregar_producto.title('Agregar Producto')
    ventana_agregar_producto.resizable(height=False, width=False)

    agregar_producto_titulo = Label(ventana_agregar_producto, text='Agregar Productos', font=('Helvetica',60))
    agregar_producto_titulo.grid(row=0, column=0, columnspan=3, padx=5, pady=5)

    producto_nombre_label = Label(ventana_agregar_producto, text='Nombre: ', font=('Helvetica',15))
    producto_nombre_label.grid(row=1, column=0, padx=5, pady=5)

    producto_nombre_entry= Entry(ventana_agregar_producto)
    producto_nombre_entry.grid(row=1, column=1, padx=5, pady=5)

    producto_precio_label = Label(ventana_agregar_producto, text='Precio por metro: ', font=('Helvetica',15))
    producto_precio_label.grid(row=2, column=0, padx=5, pady=5)

    producto_precio_entry = Entry(ventana_agregar_producto)
    producto_precio_entry.grid(row=2, column=1, padx=5, pady=5)

    producto_cantidad_label = Label(ventana_agregar_producto, text='Cantidad: ', font=('Helvetica',15))
    producto_cantidad_label.grid(row=3, column=0, padx=5, pady=5)

    producto_cantidad_entry = Entry(ventana_agregar_producto)
    producto_cantidad_entry.grid(row=3, column=1, padx=5, pady=5)

    producto_proveedor_label = Label(ventana_agregar_producto, text='Proveedor: ', font=('Helvetica',15))
    producto_proveedor_label.grid(row=4, column=0, padx=5, pady=5)

    proveedor_opciones = consultar_proveedores()
    proveedor_seleccionada = StringVar()
    proveedor_seleccionada.set(proveedor_opciones[0])

    producto_proveedor_opciones = OptionMenu(ventana_agregar_producto, proveedor_seleccionada, *proveedor_opciones )
    producto_proveedor_opciones.grid(row=4, column=1, padx=5, pady=5)

    boton_agregar_proveedor = Button(ventana_agregar_producto, text='+', command=lambda:agregar_proveedor(ventana_agregar_producto), font=('Helvetica',15))
    boton_agregar_proveedor.grid(row=4, column=2, padx=5, pady=5)

    producto_categoria_label = Label(ventana_agregar_producto, text='Categoria: ', font=('Helvetica',15))
    producto_categoria_label.grid(row=5, column=0, padx=5, pady=5)

    categoria_opciones = consultar_categorias()
    categoria_seleccionada = StringVar()
    categoria_seleccionada.set(categoria_opciones[0])

    producto_categoria_opciones = OptionMenu(ventana_agregar_producto, categoria_seleccionada, *categoria_opciones)
    producto_categoria_opciones.grid(row=5, column=1, padx=5, pady=5)

    boton_agregar_categoria = Button(ventana_agregar_producto, text='+', command=lambda:agregar_categoria(ventana_agregar_producto), font=('Helvetica',15))
    boton_agregar_categoria.grid(row=5, column=2, padx=5, pady=5)

    boton_agregar_producto = Button(ventana_agregar_producto, text='Agregar Prodcuto', command=guardar_producto, font=('Helvetica',15))
    boton_agregar_producto.grid(row=6, column=0, columnspan=3, padx=5, pady=5)

    ventana_agregar_producto.mainloop()
    

