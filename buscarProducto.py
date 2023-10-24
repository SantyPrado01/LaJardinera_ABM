import sqlite3
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from venderProducto import *
from comandosSQL import *
from buscarProveedores import buscar_proveedores

def buscar_producto(a):

    ventana_buscar_producto = Toplevel(a)
    ventana_buscar_producto.iconbitmap("icon.ico")
    ventana_buscar_producto.resizable(width=False, height=False)
    ventana_buscar_producto.title('Buscar Producto')
    
    titulo = Label(ventana_buscar_producto, text='Buscar Producto', font=('Helvetica',30))
    titulo.grid(row=0, columnspan=3, padx=10, pady=10)

    criterio_busqueda = StringVar()
    criterio_busqueda.set("Seleccionar Criterio")
    opciones_busqueda = ["Seleccionar Criterio","Nombre", "Categoría","Proveedor"]

    opcion_busqueda = OptionMenu(ventana_buscar_producto, criterio_busqueda, *opciones_busqueda)
    opcion_busqueda.grid(row=1, column=0, padx=5, pady=5)

    busqueda_entry = Entry(ventana_buscar_producto, font=('Helvetica',15))
    busqueda_entry.grid(row=1, column=1, padx=5, pady=5)

    def tree_select(event):

        global datos
        item_seleccionado = tree.selection()
        fila_seleccionada = tree.item(item_seleccionado)
        datos = fila_seleccionada['values']

        nombre_producto.delete(0,'end')
        precio_producto.delete(0,'end')
        stock_producto.config(state='normal')
        stock_producto.delete(0, 'end')
        proveedor_seleccionada.set('Seleccionar Proveedor')
        categoria_seleccionada.set('Seleccionar Categoria')

        nombre_producto.insert(0, datos[1])
        precio_producto.insert(0, datos[2])
        stock_producto.insert(0, datos[3])
        stock_producto.config(state='readonly')
        proveedor_seleccionada.set(datos[4])
        categoria_seleccionada.set(datos[5])

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
            tree.bind("<<TreeviewSelect>>",tree_select)
            tree.column("#0", width=0, stretch=NO)
            tree.heading("#1", text='Codigo Producto',anchor=CENTER) 
            tree.heading("#2", text="Nombre", anchor=CENTER)  # Centrar el encabezado 'Nombre'
            tree.heading("#3", text="Precio Por Metro", anchor=CENTER)  
            tree.heading("#4", text="Stock", anchor=CENTER)
            tree.heading("#5", text="Proveedor", anchor=CENTER)   
            tree.heading("#6", text="Categoria", anchor=CENTER)  
             
            for i in range(1, 7):  
                tree.column(f"#{i}", anchor=CENTER)

            for resultado in productos:
                id, nombre, precio, stock, proveedor_id, categoria_id = resultado

                cursor.execute("SELECT razon_social FROM proveedor WHERE id_proveedor=?", (proveedor_id,))
                proveedor_nombre = cursor.fetchone()[0]

                cursor.execute("SELECT nombre FROM categoria WHERE id_categoria=?", (categoria_id,))
                categoria_nombre = cursor.fetchone()[0]

                tree.insert('','end', values=[id, nombre, precio, stock,proveedor_nombre, categoria_nombre])
                
            tree.grid(row=3, column=0, padx=10, pady=10, columnspan=3)

            boton_eliminar = Button(ventana_buscar_producto, text='Vender Producto', command=lambda:ventana_vender_producto(tree,ventana_buscar_producto), font=('Helvetica',15))
            boton_eliminar.grid(row=4, column=1, padx=5, pady=5)

        base_datos.close()

    producto_buscar()

    boton_buscar = Button(ventana_buscar_producto, text='Buscar Producto', command=producto_buscar, font=('Helvetica',15))
    boton_buscar.grid(row=2, columnspan=3, padx=5, pady=5)

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
    
    def agregar_categoria(a):
        ventana_agregar_categoria = Toplevel(a)
        ventana_agregar_categoria.iconbitmap("icon.ico")
        ventana_agregar_categoria.title('Agregar Categoria')

        agregar_categoria_label = Label(ventana_agregar_categoria, text='Agregar Categoria', font=('Helvetica',40))
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
            consultar_categorias()
            ventana_agregar_categoria.destroy()

        boton_guardar_proveedor = Button(ventana_agregar_categoria, text='Guardar', command=guardar_categoria, font=('Helvetica',15))
        boton_guardar_proveedor.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

    def guardar_producto_nuevo():
        nombre =nombre_producto.get()
        precio = precio_producto.get()
        cantidad = stock_producto.get()
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

        producto_buscar()

        nombre_producto.delete(0, 'end')
        precio_producto.delete(0, 'end')
        stock_producto.delete(0, 'end')
        proveedor_seleccionada.set('Seleccionar Proveedor')
        categoria_seleccionada.set('Seleccionar Categoria')

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
        
        cursor.execute("UPDATE producto SET nombre=?, precio=?, cantidad=?, id_proveedor=?, id_categoria=? WHERE id_producto=?", (nombre, precio, stock, proveedor_id, categoria_id, datos[0]))
        base_datos.commit()
        messagebox.showinfo('Completado','El producto ha sido modificado con éxito.')
        producto_buscar()


    #Frame Formulario Producto

    frame_editar_producto = Frame(ventana_buscar_producto)
    frame_editar_producto.grid(row=0, column=4, rowspan=5)

    titulo = Label(frame_editar_producto, text='Formulario Producto', font=('Helvetica',30))
    titulo.grid(row=0, columnspan=3)

    titulo_producto = Label(frame_editar_producto, text='Nombre Producto', font=('Helvetica',15))
    titulo_producto.grid(row=1, column=0, padx=5, pady=5)

    nombre_producto = Entry(frame_editar_producto, font=('Helvetica',15))
    nombre_producto.grid(row=1, column=1)

    titulo_precio = Label(frame_editar_producto, text='Precio', font=('Helvetica',15))
    titulo_precio.grid(row=2, column=0, padx=5, pady=5)

    precio_producto = Entry(frame_editar_producto, font=('Helvetica',15))
    precio_producto.grid(row=2, column=1, padx=5, pady=5)

    titulo_stock = Label(frame_editar_producto, text='Stock', font=('Helvetica',15))
    titulo_stock.grid(row=3, column=0, padx=5, pady=5)

    stock_producto = Entry(frame_editar_producto, font=('Helvetica',15))
    stock_producto.grid(row=3, column=1, padx=5, pady=5)

    titulo_proveedor = Label(frame_editar_producto, text='Proveedor', font=('Helvetica',15))
    titulo_proveedor.grid(row=4, column=0, padx=5, pady=5)

    proveedor_opciones = consultar_proveedores()
    proveedor_seleccionada = StringVar()

    producto_proveedor_opciones = OptionMenu(frame_editar_producto, proveedor_seleccionada, *proveedor_opciones )
    producto_proveedor_opciones.grid(row=4, column=1, padx=5, pady=5)

    boton_agregar_proveedor = Button(frame_editar_producto, text='+', command=lambda:buscar_proveedores(ventana_buscar_producto), font=('Helvetica',15))
    boton_agregar_proveedor.grid(row=4, column=2, padx=5, pady=5)

    titulo_categoria = Label(frame_editar_producto, text='Categoria', font=('Helvetica',15))
    titulo_categoria.grid(row=5, column=0, padx=5, pady=5)

    categoria_opciones = consultar_categorias()
    categoria_seleccionada = StringVar()

    producto_categoria_opciones = OptionMenu(frame_editar_producto, categoria_seleccionada, *categoria_opciones)
    producto_categoria_opciones.grid(row=5, column=1, padx=5, pady=5)

    boton_agregar_categoria = Button(frame_editar_producto, text='+', command=lambda:agregar_categoria(ventana_buscar_producto), font=('Helvetica',15))
    boton_agregar_categoria.grid(row=5, column=2, padx=5, pady=5)

    boton_guardar_nuevo = Button(frame_editar_producto, text='Guardar Producto', command=guardar_producto_nuevo, font=('Helvetica',15))
    boton_guardar_nuevo.grid(row=6, column=0, padx=5, pady=5)

    boton_modificar = Button(frame_editar_producto, text='Actualizar Producto', command=guardar_cambios, font=('Helvetica', 15))
    boton_modificar.grid(row=6, column=1, padx=5, pady=5)

    boton_eliminar =Button(frame_editar_producto, text='Eliminar Producto', command='liminar_productos', font=('Helvetica',15))
    boton_eliminar.grid(row=6, column=2, padx=5, pady=5)

    ventana_buscar_producto.mainloop()

