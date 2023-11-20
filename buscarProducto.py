import sqlite3
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from venderProducto import *
from comandosSQL import *
from tkcalendar import DateEntry 

def buscar_producto(a):

    global ventana_buscar_producto

    ventana_buscar_producto = Frame(a, bg='white')

    frame_buscar = Frame(ventana_buscar_producto, bg='#C798E6')
    estilo_buscar = ttk.Style()
    estilo_buscar.configure('OptionBuscar.TMenubutton', foreground='black', background='#C798E6', font=('Helvetica', 15), relief='raised')
    estilo_buscar.configure('BotonBuscar.TButton', foreground='black', background='#C798E6', font=('Helvetica', 15), padding=(5,5), relief='groove')

    criterio_busqueda = StringVar()
    criterio_busqueda.set("Seleccionar Criterio")
    opciones_busqueda = ["Seleccionar Criterio","Nombre", "Categoría","Proveedor"]

    opcion_busqueda = ttk.OptionMenu(frame_buscar, criterio_busqueda, *opciones_busqueda, style='OptionBuscar.TMenubutton')
    opcion_busqueda.grid(row=1, column=1, pady=10, padx=10)

    busqueda_entry = ttk.Entry(frame_buscar, font=('Helvetica',15))
    busqueda_entry.grid(row=1, column=2, pady=10, padx=10)

    def ver_producto(event):
        seleccion = tree.selection()
        if seleccion:
            item = tree.item(seleccion)
            datos_producto = item['values']
            nuevo_producto(a, datos_producto)

    def producto_buscar():

        # Obtén el criterio de búsqueda y el valor de entrada de búsqueda
        criterio = criterio_busqueda.get()
        valor_busqueda = busqueda_entry.get()
        base_datos = sqlite3.connect('LaJardinera.bd')
        cursor = base_datos.cursor()

        # Realiza la búsqueda según el criterio seleccionado
        if criterio == "Nombre":
            cursor.execute("SELECT * FROM producto WHERE nombre LIKE ? AND estado = 0", ('%' + valor_busqueda + '%',))
        elif criterio == "Proveedor":
            cursor.execute("SELECT * FROM producto WHERE id_proveedor IN (SELECT id_proveedor FROM proveedor WHERE razon_social LIKE ?) AND estado = 0", ('%' + valor_busqueda + '%',))
        elif criterio == "Categoría":
            cursor.execute("SELECT * FROM producto WHERE id_categoria IN (SELECT id_categoria FROM categoria WHERE nombre LIKE ?)AND estado = 0", ('%' + valor_busqueda + '%',))
        else:
            cursor.execute('SELECT * FROM producto WHERE estado = 0')

        productos = cursor.fetchall()

        if not productos:
            def cerrar_ventana():
                ventana_producto_noEncontrado.destroy()

            ventana_producto_noEncontrado = Toplevel(ventana_buscar_producto, bg='white')
            ventana_producto_noEncontrado.resizable(height=False, width=False)
            ventana_producto_noEncontrado.title('Producto No Encontrado')
            texto_noEcontrado_label = ttk.Label(ventana_producto_noEncontrado, text=f'{valor_busqueda} No Encontrado', font=('Helvetica',15), background='white')
            texto_noEcontrado_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

            texto_agregar_label = ttk.Label(ventana_producto_noEncontrado, text='Desea agregar el producto?', font=('Helvetica',15), background='white')
            texto_agregar_label.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

            boton_agregar_producto = ttk.Button(ventana_producto_noEncontrado, text='Si', command=lambda:nuevo_producto(a), style='BotonBuscar.TButton')
            boton_agregar_producto.grid(row=2, column=0, padx=5, pady=5)

            boton_noAgregar = ttk.Button(ventana_producto_noEncontrado, text='No', command=cerrar_ventana, style='BotonBuscar.TButton')
            boton_noAgregar.grid(row=2, column=1, padx=5, pady=5)

        else:
            # Muestra los resultados 
            global tree

            estilo_tree = ttk.Style()
            estilo_tree.configure('Treeview', font=('Helvetica', 12), rowheight=30, padding=5)
            estilo_tree.configure('Treeview.Heading', font=('Helvetica', 14), rowheight=30, padding=5)

            tree = ttk.Treeview(ventana_buscar_producto, columns=('ID',"Nombre","Precio Por Metro","Stock","Proveedor","Categoria"))
            tree.bind("<Double-1>", ver_producto)
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
                id, nombre, precio, stock, proveedor_id, categoria_id, estado = resultado

                cursor.execute("SELECT razon_social FROM proveedor WHERE id_proveedor=?", (proveedor_id,))
                proveedor_nombre = cursor.fetchone()[0]

                cursor.execute("SELECT nombre FROM categoria WHERE id_categoria=?", (categoria_id,))
                categoria_nombre = cursor.fetchone()[0]

                tree.insert('','end', values=[id, nombre, precio, stock,proveedor_nombre, categoria_nombre])
                
            tree.grid(row=5, column=0, pady=10, columnspan=4)

            boton_eliminar = ttk.Button(ventana_buscar_producto, text='Vender Producto', command=lambda:ventana_vender_producto(tree,ventana_buscar_producto), style='BotonProducto.TButton')
            boton_eliminar.grid(row=6, column=1, pady=10)

        base_datos.close()

    producto_buscar()

    boton_buscar = ttk.Button(frame_buscar, text='Buscar Producto', command=producto_buscar, style='BotonBuscar.TButton')
    boton_buscar.grid(row=1, column=3, pady=10, padx=10)

    frame_buscar.grid(row=1, column=0, columnspan=6)

    ventana_buscar_producto.grid(row=1, column=1)


def formulario_producto(a, datos=None):

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
        ventana_agregar_categoria = Toplevel(a, bg='white')
        ventana_agregar_categoria.iconbitmap("icon.ico")
        ventana_agregar_categoria.title('Agregar Categoria')

        agregar_categoria_label = ttk.Label(ventana_agregar_categoria, text='Agregar Categoria',font=('Helvetica',15), background='white')
        agregar_categoria_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

        categoria_nombre_label = ttk.Label(ventana_agregar_categoria, text='Nombre: ', font=('Helvetica',15), background='white')
        categoria_nombre_label.grid(row=1, column=0, padx=5, pady=5)

        categoria_nombre_entry = ttk.Entry(ventana_agregar_categoria,font=('Helvetica',15))
        categoria_nombre_entry.grid(row=1, column=1, padx=5, pady=5)

        def guardar_categoria():
            nombre = categoria_nombre_entry.get()

            cursor.execute('INSERT INTO categoria (nombre) VALUES (?)',
                (nombre,))
            base_datos.commit()
            
            messagebox.showinfo('Completado','La categoria ha sido guardada con éxito.')
            ventana_agregar_categoria.destroy()

        boton_guardar_proveedor = ttk.Button(ventana_agregar_categoria, text='Guardar', command=guardar_categoria, style='BotonProducto.TButton')
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

        if nombre and id_proveedor and id_categoria:
            cursor.execute('INSERT INTO producto (nombre, precio, cantidad, id_proveedor, id_categoria, estado) VALUES (?,?,?,?,?,?)',
                        (nombre, precio, cantidad, id_proveedor[0], id_categoria[0], 0))
            base_datos.commit()

            messagebox.showinfo('Completado','El producto ha sido guardado con éxito.')
        else:
            messagebox.showerror('Error','El Producto tiene que tener nombre, categoria y proveedor.')

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

    def eliminar_producto():
        cursor.execute("UPDATE producto SET estado=?", ('1'))
        base_datos.commit()
        nombre_producto.delete(0, 'end')
        precio_producto.delete(0, 'end')
        stock_producto.config(state=NORMAL)
        stock_producto.delete(0, 'end')
        proveedor_seleccionada.set('Seleccionar Proveedor')
        categoria_seleccionada.set('Seleccionar Categoria')
        messagebox.showinfo('Completado','El producto ha sido eliminado con éxito.')

    global frame_producto

    frame_producto = Frame(a, bg='white')
    frame_producto.grid(row=0, column=0, columnspan=2)

    titulo = Label(frame_producto, text='Formulario Producto', font=('Helvetica',25), bg='white')
    titulo.grid(row=0, columnspan=2)

    titulo_producto = Label(frame_producto, text='Nombre Producto:', font=('Helvetica',15), bg='white')
    titulo_producto.grid(row=1, column=0, pady=10)

    nombre_producto = ttk.Entry(frame_producto, font=('Helvetica',15))
    nombre_producto.grid(row=1, column=1, pady=10)

    titulo_precio = Label(frame_producto, text='Precio:', font=('Helvetica',15), bg='white')
    titulo_precio.grid(row=2, column=0, pady=10)

    precio_producto = ttk.Entry(frame_producto, font=('Helvetica',15))
    precio_producto.grid(row=2, column=1, pady=10)

    titulo_stock = Label(frame_producto, text='Stock:', font=('Helvetica',15), bg='white')
    titulo_stock.grid(row=3, column=0, pady=10)

    stock_producto = ttk.Entry(frame_producto, font=('Helvetica',15))
    stock_producto.grid(row=3, column=1, pady=10)

    proveedor_opciones = consultar_proveedores()
    proveedor_seleccionada = StringVar()

    estilo_option = ttk.Style()
    estilo_option.configure('Option.TMenubutton', foreground='black', background='white', font=('Helvetica', 15), relief='groove')

    estilos_boton_mas = ttk.Style()
    estilos_boton_mas.configure('BotonMas.TButton', foreground='black', background='white', font=('Helvetica', 10), relief='groove')

    producto_proveedor_opciones = ttk.OptionMenu(frame_producto, proveedor_seleccionada, *proveedor_opciones, style='Option.TMenubutton')
    producto_proveedor_opciones.grid(row=4, column=0, pady=10)

    boton_agregar_proveedor = ttk.Button(frame_producto, text='+', command=lambda:nuevo_proveedor(a), style='BotonMas.TButton')
    boton_agregar_proveedor.grid(row=4, column=1, pady=10)

    categoria_opciones = consultar_categorias()
    categoria_seleccionada = StringVar()

    producto_categoria_opciones = ttk.OptionMenu(frame_producto, categoria_seleccionada, *categoria_opciones, style='Option.TMenubutton')
    producto_categoria_opciones.grid(row=5, column=0, pady=10)

    boton_agregar_categoria = ttk.Button(frame_producto, text='+', command=lambda:agregar_categoria(a), style='BotonMas.TButton')
    boton_agregar_categoria.grid(row=5, column=1, pady=10)

    estilos_botones_producto = ttk.Style()

    estilos_botones_producto.configure('BotonProducto.TButton', foreground='black', background='white', font=('Helvetica', 15), padding=(5,5), relief='groove')

    boton_guardar_nuevo = ttk.Button(frame_producto, text='Guardar Producto', command=guardar_producto_nuevo, style='BotonProducto.TButton')
    boton_guardar_nuevo.grid(row=6, column=0, pady=10, columnspan=2)

    boton_modificar = ttk.Button(frame_producto, text='Actualizar Producto', command=guardar_cambios, style='BotonProducto.TButton', state=DISABLED)
    boton_modificar.grid(row=7, column=0, pady=10, columnspan=2)

    boton_eliminar = ttk.Button(frame_producto, text='Eliminar Producto', command=eliminar_producto, style='BotonProducto.TButton', state=DISABLED)
    boton_eliminar.grid(row=8, column=0, pady=10, columnspan=2)

    frame_producto.grid(row=1, column=1)

    if datos:
        nombre_producto.insert(0, datos[1])
        precio_producto.insert(0, datos[2])
        stock_producto.insert(0, datos[3])
        stock_producto.config(state=DISABLED)
        proveedor_seleccionada.set(datos[4])
        categoria_seleccionada.set(datos[5])

        boton_guardar_nuevo.config(state=DISABLED)
        boton_modificar.config(state=NORMAL)
        boton_eliminar.config(state=NORMAL)

def buscar_proveedores(a):

    global ventana_buscar_proveedores
    ventana_buscar_proveedores = Frame(a, bg='white')

    frame_buscar = Frame(ventana_buscar_proveedores, bg='#C798E6')
    estilo_buscar = ttk.Style()
    estilo_buscar.configure('OptionBuscar.TMenubutton', foreground='black', background='#C798E6', font=('Helvetica', 15), relief='raised')
    estilo_buscar.configure('BotonBuscar.TButton', foreground='black', background='#C798E6', font=('Helvetica', 15), padding=(5,5), relief='groove')

    criterio_busqueda = StringVar()
    criterio_busqueda.set("Seleccionar Criterio")
    opciones_busqueda = ["Seleccionar Criterio","Nombre"]

    opcion_busqueda = ttk.OptionMenu(frame_buscar, criterio_busqueda, *opciones_busqueda, style='OptionBuscar.TMenubutton')
    opcion_busqueda.grid(row=1, column=0, padx=5, pady=5)

    busqueda_entry = ttk.Entry(frame_buscar, font=('Helvetica',15))
    busqueda_entry.grid(row=1, column=1, padx=5, pady=5)
    
    def ver_proveedor(event):
        seleccion = tree.selection()
        if seleccion:
            item = tree.item(seleccion)
            datos_proveedor = item['values']
            nuevo_proveedor(a, datos_proveedor)

    def proveedor_buscar():

        # Obtén el criterio de búsqueda y el valor de entrada de búsqueda
        criterio = criterio_busqueda.get()
        valor_busqueda = busqueda_entry.get()
        base_datos = sqlite3.connect('LaJardinera.bd')
        cursor = base_datos.cursor()

        # Realiza la búsqueda según el criterio seleccionado
        if criterio == "Nombre":
            cursor.execute("SELECT * FROM proveedor WHERE razon_social LIKE ?", ('%' + valor_busqueda + '%',))
        else:
            cursor.execute('SELECT * FROM proveedor')

        proveedor = cursor.fetchall()

        if not proveedor:
            def cerrar_ventana():
                ventana_proveedor_noEncontrado.destroy()

            ventana_proveedor_noEncontrado = Toplevel(ventana_buscar_proveedores)
            ventana_proveedor_noEncontrado.resizable(height=False, width=False)
            ventana_proveedor_noEncontrado.title('Proveedor No Encontrado')
            texto_noEcontrado_label = Label(ventana_proveedor_noEncontrado, text=f'{valor_busqueda} No Encontrado', font=('Helvetica',30))
            texto_noEcontrado_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

            texto_agregar_label = Label(ventana_proveedor_noEncontrado, text='Desea agregar el proveedor?', font=('Helvetica',15))
            texto_agregar_label.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

            boton_agregar_proveedor = Button(ventana_proveedor_noEncontrado, text='Si', command=lambda:formulario_proveedor(a), font=('Helvetica',15))
            boton_agregar_proveedor.grid(row=2, column=0, padx=5, pady=5)

            boton_noAgregar = Button(ventana_proveedor_noEncontrado, text='No', command=cerrar_ventana, font=('Helvetica',15))
            boton_noAgregar.grid(row=2, column=1, padx=5, pady=5)

        else:
            # Muestra los resultados 
            global tree
            tree = ttk.Treeview(ventana_buscar_proveedores, columns=("ID","Razon Social","CUIT","Domicilio","Numero Telefonico","Email"))
            tree.bind("<Double-1>", ver_proveedor)
            tree.column("#0", width=0, stretch=NO)
            tree.heading("#1", text='Identificador', anchor=CENTER)
            tree.heading("#2", text='Razon Social',anchor=CENTER) 
            tree.heading("#3", text='CUIT', anchor=CENTER)  # Centrar el encabezado 'Nombre'
            tree.heading("#4", text='Domicilio', anchor=CENTER)  
            tree.heading("#5", text='Numero Telefonico', anchor=CENTER)
            tree.heading("#6", text='Email', anchor=CENTER)    
             
            for i in range(1, 7):  
                tree.column(f"#{i}", anchor=CENTER)

            for resultado in proveedor:
                id, nombre, cuit, domicilio, numeroTelefonico, email = resultado

                tree.insert('','end', values=[id, nombre, cuit, domicilio, numeroTelefonico, email])
                
            tree.grid(row=3, column=0, padx=10, pady=10, columnspan=3)

        base_datos.close()

    proveedor_buscar()

    boton_buscar = ttk.Button(frame_buscar, text='Buscar Proveedor', command=proveedor_buscar, style='BotonBuscar.TButton')
    boton_buscar.grid(row=1, column=2, padx=5, pady=5)

    frame_buscar.grid(row=1, column=0, columnspan=6)

    ventana_buscar_proveedores.grid(row=1, column=1)

def formulario_proveedor(a, datos=None):

    def guardar_cambios():
        nombre = nombre_proveedor.get()
        cuit = cuit_proveedor.get()
        domicilio = domicilio_proveedor.get()
        numero = numero_proveedor.get()
        email = email_proveedor.get()

        base_datos = sqlite3.connect('LaJardinera.bd')
        cursor = base_datos.cursor()
    
        cursor.execute("UPDATE proveedor SET razon_social=?, cuit=?, domicilio=?, numero_telefono=?, email=? WHERE id_proveedor=?", (nombre, cuit, domicilio, numero, email, datos[0]))
        base_datos.commit()
        messagebox.showinfo('Completado','El proveedor ha sido modificado con éxito.')

    def guardar_proveedor():
        razon_social = nombre_proveedor.get()
        cuit = cuit_proveedor.get()
        domicilio = domicilio_proveedor.get()
        numeroTelefono = numero_proveedor.get()
        email = email_proveedor.get()

        if razon_social:
            cursor.execute('INSERT INTO proveedor (razon_social, cuit, domicilio, numero_telefono, email) VALUES (?,?,?,?,?)',
                (razon_social, cuit, domicilio, numeroTelefono, email))
            base_datos.commit()
            messagebox.showinfo('Completado','El proveedor ha sido guardado con éxito.')
        else:
            messagebox.showerror('Error','El proveedor tiene que tener un nombre.')

    global frame_proveedor

    frame_proveedor = Frame(a, bg='white')
    frame_proveedor.grid(row=0, column=4, rowspan=4)

    titulo = Label(frame_proveedor, text='Formulario Proveedor', font=('Helvetica',25), bg='white')
    titulo.grid(row=0, columnspan=2)

    titulo_proveedor = Label(frame_proveedor, text='Razon Social', font=('Helvetica',15), bg='white')
    titulo_proveedor.grid(row=1, column=0, pady=10)

    nombre_proveedor = ttk.Entry(frame_proveedor, font=('Helvetica',15))
    nombre_proveedor.grid(row=1, column=1,pady=10)

    titulo_cuit = Label(frame_proveedor, text='CUIT', font=('Helvetica',15), bg='white')
    titulo_cuit.grid(row=2, column=0, pady=10)

    cuit_proveedor = ttk.Entry(frame_proveedor, font=('Helvetica',15))
    cuit_proveedor.grid(row=2, column=1, pady=10)

    titulo_domicilio = Label(frame_proveedor, text='Domicilio', font=('Helvetica',15), bg='white')
    titulo_domicilio.grid(row=3, column=0, pady=10)

    domicilio_proveedor = ttk.Entry(frame_proveedor, font=('Helvetica',15))
    domicilio_proveedor.grid(row=3, column=1, pady=10)  

    titulo_numero = Label(frame_proveedor, text='Numero Telefonico', font=('Helvetica',15), bg='white')
    titulo_numero.grid(row=4, column=0, pady=10)

    numero_proveedor = ttk.Entry(frame_proveedor, font=('Helvetica',15))
    numero_proveedor.grid(row=4, column=1, pady=10)

    titulo_email = Label(frame_proveedor, text='Email', font=('Helvetica',15), bg='white')
    titulo_email.grid(row=5, column=0, pady=10)

    email_proveedor = ttk.Entry(frame_proveedor, font=('Helvetica',15))
    email_proveedor.grid(row=5, column=1, pady=10)

    estilos_botones_proveedor = ttk.Style()
    estilos_botones_proveedor.configure('BotonProveedor.TButton', foreground='black', background='white', font=('Helvetica', 15), padding=(5,5), relief='groove')

    boton_guardar_nuevo = ttk.Button(frame_proveedor, text='Guardar Proveedor', command=guardar_proveedor, style='BotonProveedor.TButton')
    boton_guardar_nuevo.grid(row=6, column=0, pady=10, columnspan=2)

    boton_modificar = ttk.Button(frame_proveedor, text='Actualizar Proveedor', command=guardar_cambios, style='BotonProveedor.TButton', state=DISABLED)
    boton_modificar.grid(row=7, column=0, pady=10, columnspan=2)

    boton_eliminar = ttk.Button(frame_proveedor, text='Eliminar Proveedor', command='', style='BotonProveedor.TButton', state=DISABLED)
    boton_eliminar.grid(row=8, column=0, pady=10, columnspan=2)

    frame_proveedor.grid(row=1, column=1)

    if datos:
        nombre_proveedor.insert(0, datos[1])
        cuit_proveedor.insert(0, datos[2])
        domicilio_proveedor.insert(0, datos[3])
        numero_proveedor.insert(0, datos[4])
        email_proveedor.insert(0, datos[5])

        boton_guardar_nuevo.config(state=DISABLED)
        boton_modificar.config(state=NORMAL)
        boton_eliminar.config(state=NORMAL)

def generar_informe(a):

    global ventana_generar_informe

    ventana_generar_informe = Frame(a, bg='white')
    frame_buscar = Frame(ventana_generar_informe, bg='#C798E6')
    estilo_buscar = ttk.Style()
    estilo_buscar.configure('OptionBuscar.TMenubutton', foreground='black', background='#C798E6', font=('Helvetica', 15), relief='raised')
    estilo_buscar.configure('BotonBuscar.TButton', foreground='black', background='#C798E6', font=('Helvetica', 15), padding=(5,5), relief='groove')

    criterio_busqueda = StringVar()
    criterio_busqueda.set("Seleccionar Criterio")
    opciones_busqueda = ["Seleccionar Criterio","Nombre", "Categoría","Proveedor"]

    opcion_busqueda = ttk.OptionMenu(frame_buscar, criterio_busqueda, *opciones_busqueda, style='OptionBuscar.TMenubutton')
    opcion_busqueda.grid(row=1, column=0)

    busqueda_entry = Entry(frame_buscar, font=('Helvetica',15))
    busqueda_entry.grid(row=1, column=1, padx=10)

    date_picker = DateEntry(frame_buscar, width=20, background='darkblue', foreground='white', borderwidth=2)
    date_picker.grid(row=1, column=2)

    def informes_buscar():

        # Obtén el criterio de búsqueda y el valor de entrada de búsqueda
        criterio = criterio_busqueda.get()
        valor_busqueda = busqueda_entry.get()
        fecha_seleccionada = date_picker.get_date()
        base_datos = sqlite3.connect('LaJardinera.bd')
        cursor = base_datos.cursor()

        # Define la consulta base sin criterios de fecha
        consulta_base = '''
            SELECT ventas.id_venta, ventas.fecha, producto.nombre, ventas.cantidad, ventas.precio_unitario, 
            (ventas.cantidad * ventas.precio_unitario) as total_venta, categoria.nombre as categoria, 
            proveedor.razon_social as proveedor
            FROM ventas
            INNER JOIN producto ON ventas.id_producto = producto.id_producto
            LEFT JOIN categoria ON producto.id_categoria = categoria.id_categoria
            LEFT JOIN proveedor ON producto.id_proveedor = proveedor.id_proveedor
        '''
        
        # Lista para almacenar las consultas que se ejecutarán
        consultas = []
        
        if fecha_seleccionada:
            consulta_base += ' WHERE ventas.fecha = ?'
            consultas.append(fecha_seleccionada)
        
        if criterio == "Nombre":
            consulta_base += ' AND producto.nombre LIKE ?'
            consultas.append('%' + valor_busqueda + '%')
        elif criterio == "Categoria":
            consulta_base += ' AND categoria.nombre LIKE ?'
            consultas.append('%' + valor_busqueda + '%')
        elif criterio == "Proveedor":
            consulta_base += ' AND proveedor.razon_social LIKE ?'
            consultas.append('%' + valor_busqueda + '%')
        
        cursor.execute(consulta_base, consultas)
        productos = cursor.fetchall()

        if not productos:

            messagebox.showerror('Error', f'{valor_busqueda} No Encontrado' )

        else:
            # Muestra los resultados 
            global tree
            tree = ttk.Treeview(ventana_generar_informe, columns=("Fecha","Producto","Cantidad","Precio Unitario","Total","Categoria","Proveedor"))
            
            tree.column("#0", width=0, stretch=NO)
            tree.heading("#1", text='Fecha',anchor=CENTER) 
            tree.heading("#2", text="Producto", anchor=CENTER)  # Centrar el encabezado 'Nombre'
            tree.heading("#3", text="Cantidad", anchor=CENTER)
            tree.heading("#4", text="Precio Unitario", anchor=CENTER)  
            tree.heading("#5", text="Total", anchor=CENTER)
            tree.heading("#6", text="Categoria", anchor=CENTER)   
            tree.heading("#7", text="Proveedor", anchor=CENTER)  
             
            for i in range(1, 8):  
                tree.column(f"#{i}", anchor=CENTER)

            for i in productos:

                tree.insert('', 'end', values=[i[1], i[2], i[3], i[4], i[5], i[6], i[7]])
                
            tree.grid(row=3, column=0, padx=10, pady=10, columnspan=3)

        base_datos.close()

    informes_buscar()   
    boton_ventas = ttk.Button(frame_buscar, text='Buscar Ventas', command=informes_buscar, style='BotonBuscar.TButton')
    boton_ventas.grid(row=1, column=3, padx=5, pady=5)
    frame_buscar.grid(row=1, columnspan=5)
    ventana_generar_informe.grid(row=1, column=1)


ventana_generar_informe = None
ventana_buscar_producto = None
frame_producto = None
ventana_buscar_proveedores = None
frame_proveedor = None

def destruir_frame(frame):
    if frame:
        frame.destroy()

def nuevo_producto(a, datos=None):
    global ventana_buscar_proveedores, ventana_buscar_producto, frame_proveedor, ventana_generar_informe
    destruir_frame(ventana_buscar_producto)
    destruir_frame(ventana_generar_informe)
    destruir_frame(ventana_buscar_proveedores)
    destruir_frame(frame_proveedor)
    formulario_producto(a, datos)

def buscar_productos(a):
    global ventana_buscar_proveedores, frame_proveedor, frame_producto, ventana_generar_informe
    destruir_frame(ventana_buscar_proveedores)
    destruir_frame(ventana_generar_informe)
    destruir_frame(frame_producto)
    destruir_frame(frame_proveedor)
    buscar_producto(a)

def buscar_proveedor(a):
    global ventana_buscar_producto, frame_proveedor, frame_producto, ventana_generar_informe
    destruir_frame(ventana_buscar_producto)
    destruir_frame(ventana_generar_informe)
    destruir_frame(frame_producto)
    destruir_frame(frame_proveedor)
    buscar_proveedores(a)

def nuevo_proveedor(a, datos=None):
    global ventana_buscar_proveedores, ventana_buscar_producto, frame_producto, ventana_generar_informe
    destruir_frame(ventana_buscar_producto)
    destruir_frame(ventana_generar_informe)
    destruir_frame(ventana_buscar_proveedores)
    destruir_frame(frame_producto)
    formulario_proveedor(a, datos)

def buscar_informes(a):
    global ventana_buscar_proveedores, ventana_buscar_producto, frame_proveedor, frame_producto
    destruir_frame(ventana_buscar_producto)
    destruir_frame(frame_proveedor)
    destruir_frame(ventana_buscar_proveedores)
    destruir_frame(frame_producto)
    generar_informe(a)