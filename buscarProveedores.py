import sqlite3
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from editarProducto import *
from venderProducto import *
from comandosSQL import *


def mostrar_formulario_edicion(tree):

    ventana_formulario_edicion = Toplevel()
    ventana_formulario_edicion.iconbitmap("icon.ico")
    
    ventana_formulario_edicion.resizable(width=False, height=False)

    ventana_formulario_edicion.title('Editar Proveedor')

    proveedor_seleccionado = tree.selection()

    if proveedor_seleccionado:

        fila_seleccionada = tree.item(proveedor_seleccionado)
        datos = fila_seleccionada['values']

        titulo = Label(ventana_formulario_edicion, text='Editar Proveedor', font=('Helvetica',60))
        titulo.grid(row=0, columnspan=2, padx=10, pady=10)

        titulo_proveedor = Label(ventana_formulario_edicion, text='Razon Social', font=('Helvetica',15))
        titulo_proveedor.grid(row=1, column=0, padx=5, pady=5)

        nombre_proveedor = Entry(ventana_formulario_edicion, font=('Helvetica',15))
        nombre_proveedor.grid(row=1, column=1)
        nombre_proveedor.insert(0, datos[1])  

        titulo_precio = Label(ventana_formulario_edicion, text='CUIT', font=('Helvetica',15))
        titulo_precio.grid(row=2, column=0, padx=5, pady=5)

        cuit_proveedor = Entry(ventana_formulario_edicion, font=('Helvetica',15))
        cuit_proveedor.grid(row=2, column=1, padx=5, pady=5)
        cuit_proveedor.insert(0, datos[2]) 

        titulo_domicilio = Label(ventana_formulario_edicion, text='Domicilio', font=('Helvetica',15))
        titulo_domicilio.grid(row=3, column=0, padx=5, pady=5)

        domicilio_proveedor = Entry(ventana_formulario_edicion, font=('Helvetica',15))
        domicilio_proveedor.grid(row=3, column=1, padx=5, pady=5)
        domicilio_proveedor.insert(0, datos[3])  

        titulo_numero = Label(ventana_formulario_edicion, text='Numero Telefonico', font=('Helvetica',15))
        titulo_numero.grid(row=4, column=0, padx=5, pady=5)

        numero_proveedor = Entry(ventana_formulario_edicion, font=('Helvetica',15))
        numero_proveedor.grid(row=4, column=1, padx=5, pady=5)
        numero_proveedor.insert(0, datos[4])

        titulo_email = Label(ventana_formulario_edicion, text='Email', font=('Helvetica',15))
        titulo_email.grid(row=5, column=0, padx=5, pady=5)

        email_proveedor = Entry(ventana_formulario_edicion, font=('Helvetica',15))
        email_proveedor.grid(row=5, column=1, padx=5, pady=5)
        email_proveedor.insert(0, datos[5])

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

        def eliminar_proveedor():

            proveedor_seleccionado = tree.selection()

            if proveedor_seleccionado:
                
                fila_seleccionada = tree.item(proveedor_seleccionado)
                datos = fila_seleccionada['values']

                base_datos =sqlite3.connect('LaJardinera.bd')
                cursor = base_datos.cursor()

                cursor.execute("DELETE FROM proveedor WHERE id_proveedor=?", (datos[0],))

                base_datos.commit()

                base_datos.close()

                tree.delete(proveedor_seleccionado)

                messagebox.showinfo('Completado','El proveedor ha sido eliminado con éxito.')

               
    boton_guardar = Button(ventana_formulario_edicion, text='Guardar Cambios', command=guardar_cambios, font=('Helvetica',15))
    boton_guardar.grid(row=6, columnspan=2, padx=5, pady=5)

    boton_eliminar =Button(ventana_formulario_edicion, text='Eliminar Proveedor', command=eliminar_proveedor, font=('Helvetica',15))
    boton_eliminar.grid(row=7, columnspan=2, padx=5, pady=5)

def buscar_proveedores(a):

    ventana_buscar_proveedores = Toplevel(a)
    ventana_buscar_proveedores.iconbitmap("icon.ico")
    ventana_buscar_proveedores.resizable(width=False, height=False)
    ventana_buscar_proveedores.title('Buscar Proveedor')
    
    titulo = Label(ventana_buscar_proveedores, text='Buscar Proveedor', font=('Helvetica',60))
    titulo.grid(row=0, columnspan=3, padx=10, pady=10)

    criterio_busqueda = StringVar()
    criterio_busqueda.set("Seleccionar Criterio")
    opciones_busqueda = ["Seleccionar Criterio","Nombre"]

    opcion_busqueda = OptionMenu(ventana_buscar_proveedores, criterio_busqueda, *opciones_busqueda)
    opcion_busqueda.grid(row=1, column=0, padx=5, pady=5)

    busqueda_entry = Entry(ventana_buscar_proveedores, font=('Helvetica',15))
    busqueda_entry.grid(row=1, column=1, padx=5, pady=5)

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
            ventana_proveedor_noEncontrado.title('Proveedor No Encontrado')
            texto_noEcontrado_label = Label(ventana_proveedor_noEncontrado, text=f'{valor_busqueda} No Encontrado')
            texto_noEcontrado_label.grid(row=0, column=0, columnspan=2)

            texto_agregar_label = Label(ventana_proveedor_noEncontrado, text='Desea agregar el proveedor?')
            texto_agregar_label.grid(row=1, column=0, columnspan=2)

            boton_agregar_proveedor = Button(ventana_proveedor_noEncontrado, text='Si', command=lambda:ventana_agregar_producto(a))
            boton_agregar_proveedor.grid(row=2, column=0)

            boton_noAgregar = Button(ventana_proveedor_noEncontrado, text='No', command=cerrar_ventana)
            boton_noAgregar.grid(row=2, column=1)

        else:
            # Muestra los resultados 
            global tree
            tree = ttk.Treeview(ventana_buscar_proveedores, columns=("ID","Razon Social","CUIT","Domicilio","Numero Telefonico","Email"))
            
            tree.column("#0", width=0, stretch=tk.NO)
            tree.heading("#1", text='Identificador', anchor=tk.CENTER)
            tree.heading("#2", text='Razon Social',anchor=tk.CENTER) 
            tree.heading("#3", text='CUIT', anchor=tk.CENTER)  # Centrar el encabezado 'Nombre'
            tree.heading("#4", text='Domicilio', anchor=tk.CENTER)  
            tree.heading("#5", text='Numero Telefonico', anchor=tk.CENTER)
            tree.heading("#6", text='Email', anchor=tk.CENTER)    
             
            for i in range(1, 7):  
                tree.column(f"#{i}", anchor=tk.CENTER)

            for resultado in proveedor:
                id, nombre, cuit, domicilio, numeroTelefonico, email = resultado

                tree.insert('','end', values=[id, nombre, cuit, domicilio, numeroTelefonico, email])
                
            tree.grid(row=3, column=0, padx=10, pady=10, columnspan=3)

            boton_editar = Button(ventana_buscar_proveedores, text='Editar Proveedor', command=lambda:mostrar_formulario_edicion(tree), font=('Helvetica',15))
            boton_editar.grid(row=4, column=0, padx=5, pady=5, columnspan=3)

        base_datos.close()

    proveedor_buscar()
    boton_buscar = Button(ventana_buscar_proveedores, text='Buscar Proveedor', command=proveedor_buscar, font=('Helvetica',15))
    boton_buscar.grid(row=2, columnspan=3, padx=5, pady=5)

    ventana_buscar_proveedores.mainloop()

