import sqlite3
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from editarProducto import *
from venderProducto import *
from comandosSQL import *
from agregarProducto import ventana_agregar_producto

def buscar_producto(a):

    ventana_buscar_producto = Toplevel(a)
    ventana_buscar_producto.iconbitmap("icon.ico")
    ventana_buscar_producto.resizable(width=False, height=False)
    ventana_buscar_producto.title('Compra a Proveedores')
    
    titulo = Label(ventana_buscar_producto, text='Buscar Producto', font=('Helvetica',60))
    titulo.grid(row=0, columnspan=3, padx=10, pady=10)

    criterio_busqueda = StringVar()
    criterio_busqueda.set("Seleccionar Criterio")
    opciones_busqueda = ["Seleccionar Criterio","Nombre", "Categoría","Proveedor"]

    opcion_busqueda = OptionMenu(ventana_buscar_producto, criterio_busqueda, *opciones_busqueda)
    opcion_busqueda.grid(row=1, column=0, padx=5, pady=5)

    busqueda_entry = Entry(ventana_buscar_producto, font=('Helvetica',15))
    busqueda_entry.grid(row=1, column=1, padx=5, pady=5)

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
            def cerrar_ventana():
                ventana_producto_noEncontrado.destroy()

            ventana_producto_noEncontrado = Toplevel(ventana_buscar_producto)
            ventana_producto_noEncontrado.title('Producto No Encontrado')
            texto_noEcontrado_label = Label(ventana_producto_noEncontrado, text=f'{valor_busqueda} No Encontrado')
            texto_noEcontrado_label.grid(row=0, column=0, columnspan=2)

            texto_agregar_label = Label(ventana_producto_noEncontrado, text='Desea agregar el producto?')
            texto_agregar_label.grid(row=1, column=0, columnspan=2)

            boton_agregar_producto = Button(ventana_producto_noEncontrado, text='Si', command=lambda:ventana_agregar_producto(a))
            boton_agregar_producto.grid(row=2, column=0)

            boton_noAgregar = Button(ventana_producto_noEncontrado, text='No', command=cerrar_ventana)
            boton_noAgregar.grid(row=2, column=1)

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


            boton_eliminar = Button(ventana_buscar_producto, text='Registrar Compra a Proveedor', command=lambda:ventana_vender_producto(tree,ventana_buscar_producto), font=('Helvetica',15))
            boton_eliminar.grid(row=4, column=1, padx=5, pady=5)

        base_datos.close()

    producto_buscar()

    boton_buscar = Button(ventana_buscar_producto, text='Buscar Producto', command=producto_buscar, font=('Helvetica',15))
    boton_buscar.grid(row=2, columnspan=3, padx=5, pady=5)

    ventana_buscar_producto.mainloop()