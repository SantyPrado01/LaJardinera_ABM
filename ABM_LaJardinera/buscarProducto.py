import sqlite3
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import tkinter as tk
from editarProducto import *
from comandosSQL import *

def buscar_producto():

    ventana_buscar_producto = Tk()
    ventana_buscar_producto.resizable(width=False, height=False)
    ventana_buscar_producto.title('Buscar Producto')
    
    titulo = Label(ventana_buscar_producto, text='Buscar Producto', font=65)
    titulo.grid(row=0, columnspan=3, padx=10, pady=10)

    criterio_busqueda = StringVar()
    criterio_busqueda.set("Seleccionar Criterio")
    opciones_busqueda = ["Seleccionar Criterio","Nombre", "Categoría","Proveedor"]

    opcion_busqueda = OptionMenu(ventana_buscar_producto, criterio_busqueda, *opciones_busqueda)
    opcion_busqueda.grid(row=1, column=0)

    busqueda_entry = Entry(ventana_buscar_producto, font=45)
    busqueda_entry.grid(row=1, column=1)

    def producto_buscar():

        # Obtén el criterio de búsqueda y el valor de entrada de búsqueda
        criterio = criterio_busqueda.get()
        valor_busqueda = busqueda_entry.get()
        base_datos = sqlite3.connect('LaJardinera.bd')
        cursor = base_datos.cursor()

        # Realiza la búsqueda según el criterio seleccionado
        if criterio == "Nombre":
            cursor.execute("SELECT * FROM producto WHERE nombre LIKE ?", ('%' + valor_busqueda + '%',))
        elif criterio == "Proveedor":
            cursor.execute("SELECT * FROM producto WHERE id_proveedor IN (SELECT id_proveedor FROM proveedor WHERE razon_social LIKE ?)", ('%' + valor_busqueda + '%',))
        elif criterio == "Categoría":
            cursor.execute("SELECT * FROM producto WHERE id_categoria IN (SELECT id_categoria FROM categoria WHERE nombre LIKE ?)", ('%' + valor_busqueda + '%',))
        else:
            cursor.execute('SELECT * FROM producto')

        productos = cursor.fetchall()
        
        if not productos:

            messagebox.showerror('Error', f'{valor_busqueda} No Encontrado' )

        else:
            # Muestra los resultados 
            global tree
            tree = ttk.Treeview(ventana_buscar_producto, columns=('ID',"Nombre","Precio Por Metro","Stock","Proveedor","Categoria"))
            
            tree.column("#0", width=0, stretch=tk.NO)
            tree.heading("#1", text='Codigo Producto',anchor=tk.CENTER) 
            tree.heading("#2", text="Nombre", anchor=tk.CENTER)  # Centrar el encabezado 'Nombre'
            tree.heading("#3", text="Precio Por Metro", anchor=tk.CENTER)  
            tree.heading("#4", text="Stock", anchor=tk.CENTER)
            tree.heading("#5", text="Proveedor", anchor=tk.CENTER)   
            tree.heading("#6", text="Categoria", anchor=tk.CENTER)  
             
            for i in range(1, 7):  
                tree.column(f"#{i}", anchor=tk.CENTER)

            for resultado in productos:
                id, nombre, precio, stock, proveedor_id, categoria_id = resultado

                cursor.execute("SELECT razon_social FROM proveedor WHERE id_proveedor=?", (proveedor_id,))
                proveedor_nombre = cursor.fetchone()[0]

                cursor.execute("SELECT nombre FROM categoria WHERE id_categoria=?", (categoria_id,))
                categoria_nombre = cursor.fetchone()[0]

                tree.insert('','end', values=[id, nombre, precio, stock,proveedor_nombre, categoria_nombre])
                
            tree.grid(row=3, column=0, padx=10, pady=10, columnspan=3)

            boton_editar = Button(ventana_buscar_producto, text='Editar Producto', command=lambda:mostrar_formulario_edicion(tree), font=45)
            boton_editar.grid(row=4, column=0)

            boton_eliminar = Button(ventana_buscar_producto, text='Vender Producto', command=lambda:eliminar_productos(tree), font=45)
            boton_eliminar.grid(row=4, column=1)

        base_datos.close()

    producto_buscar()
    boton_buscar = Button(ventana_buscar_producto, text='Buscar Producto', command=producto_buscar, font=45)
    boton_buscar.grid(row=2, columnspan=3, padx=5, pady=5)

    ventana_buscar_producto.mainloop()

buscar_producto()