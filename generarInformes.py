import sqlite3
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import DateEntry 
from editarProducto import *
from venderProducto import *
from comandosSQL import *

def generar_informe(a):

    ventana_generar_informe = Toplevel(a)
    ventana_generar_informe.iconbitmap("icon.ico")
    ventana_generar_informe.resizable(width=False, height=False)
    ventana_generar_informe.title('Generar Informes')
    
    titulo = Label(ventana_generar_informe, text='Buscar Informe', font=('Helvetica',60))
    titulo.grid(row=0, columnspan=3, padx=10, pady=10)

    criterio_busqueda = StringVar()
    criterio_busqueda.set("Seleccionar Criterio")
    opciones_busqueda = ["Seleccionar Criterio","Nombre", "Categoría","Proveedor"]

    opcion_busqueda = OptionMenu(ventana_generar_informe, criterio_busqueda, *opciones_busqueda)
    opcion_busqueda.grid(row=1, column=0)

    busqueda_entry = Entry(ventana_generar_informe, font=('Helvetica',15))
    busqueda_entry.grid(row=1, column=1)

    date_picker = DateEntry(ventana_generar_informe, width=12, background='darkblue', foreground='white', borderwidth=2)
    date_picker.grid(row=2, column=0)

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
            
            tree.column("#0", width=0, stretch=tk.NO)
            tree.heading("#1", text='Fecha',anchor=tk.CENTER) 
            tree.heading("#2", text="Producto", anchor=tk.CENTER)  # Centrar el encabezado 'Nombre'
            tree.heading("#3", text="Cantidad", anchor=tk.CENTER)
            tree.heading("#4", text="Precio Unitario", anchor=tk.CENTER)  
            tree.heading("#5", text="Total", anchor=tk.CENTER)
            tree.heading("#6", text="Categoria", anchor=tk.CENTER)   
            tree.heading("#7", text="Proveedor", anchor=tk.CENTER)  
             
            for i in range(1, 8):  
                tree.column(f"#{i}", anchor=tk.CENTER)

            for i in productos:

                tree.insert('', 'end', values=[i[1], i[2], i[3], i[4], i[5], i[6], i[7]])
                
            tree.grid(row=3, column=0, padx=10, pady=10, columnspan=3)

        base_datos.close()

    informes_buscar()   
    boton_ventas = Button(ventana_generar_informe, text='Buscar Ventas', command=informes_buscar, font=('Helvetica',15))
    boton_ventas.grid(row=2, columnspan=3, padx=5, pady=5)


    ventana_generar_informe.mainloop()
