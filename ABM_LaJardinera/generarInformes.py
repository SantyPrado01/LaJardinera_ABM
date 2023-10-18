import sqlite3
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from editarProducto import *
from venderProducto import *
from comandosSQL import *

def generar_informe():

    ventana_generar_informe = Tk()
    ventana_generar_informe.resizable(width=False, height=False)
    ventana_generar_informe.title('Generar Informes')
    
    titulo = Label(ventana_generar_informe, text='Buscar Informe', font=65)
    titulo.grid(row=0, columnspan=3, padx=10, pady=10)

    criterio_busqueda = StringVar()
    criterio_busqueda.set("Seleccionar Criterio")
    opciones_busqueda = ["Seleccionar Criterio","Nombre", "Categoría","Proveedor"]

    opcion_busqueda = OptionMenu(ventana_generar_informe, criterio_busqueda, *opciones_busqueda)
    opcion_busqueda.grid(row=1, column=0)

    busqueda_entry = Entry(ventana_generar_informe, font=45)
    busqueda_entry.grid(row=1, column=1)

    def informes_buscar():

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
            cursor.execute('''
                SELECT ventas.id_venta, ventas.fecha, producto.nombre, ventas.cantidad, ventas.precio_unitario, 
                    (ventas.cantidad * ventas.precio_unitario) as total_venta, categoria.nombre as categoria, 
                    proveedor.razon_social as proveedor
                FROM ventas
                INNER JOIN producto ON ventas.id_producto = producto.id_producto
                LEFT JOIN categoria ON producto.id_categoria = categoria.id_categoria
                LEFT JOIN proveedor ON producto.id_proveedor = proveedor.id_proveedor
            ''')

        productos = cursor.fetchall()
        
        if not productos:

            messagebox.showerror('Error', f'{valor_busqueda} No Encontrado' )

        else:
            # Muestra los resultados 
            global tree
            tree = ttk.Treeview(ventana_generar_informe, columns=('ID',"Fecha","Producto","Cantidad","Precio Unitario","Total","Categoria","Proveedor"))
            
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
    boton_buscar = Button(ventana_generar_informe, text='Buscar Producto', command=informes_buscar, font=45)
    boton_buscar.grid(row=2, columnspan=3, padx=5, pady=5)

    ventana_generar_informe.mainloop()
generar_informe()