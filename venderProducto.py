from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import datetime
import sqlite3

def ventana_vender_producto(tree, a):

    def calcular_venta(*args):
        try:
            cantidad = int(cantidad_var.get())
            precio = float(datos[2])  # Convertir el precio a float si no es entero
            total = cantidad * precio
            producto_total_var.set(total)
        except ValueError:
            producto_total_var.set("Invalido")

    item_seleccionado = tree.selection()

    if item_seleccionado:
        fila_seleccionada = tree.item(item_seleccionado)
        datos = fila_seleccionada['values']

        ventana_vender_producto = Toplevel(a)
        ventana_vender_producto.iconbitmap("icon.ico")
        ventana_vender_producto.resizable(width=None, height=None)

        vender_titulo = Label(ventana_vender_producto, text='Vender Producto', font=('Helvetica',60))
        vender_titulo.grid(row=0, column=0, columnspan=2)

        producto_label = Label(ventana_vender_producto, text='Producto: ', font=('Helvetica',15))
        producto_label.grid(row=1, column=0)

        producto_nombre_entry = Entry(ventana_vender_producto)
        producto_nombre_entry.grid(row=1, column=1)
        producto_nombre_entry.insert(0, datos[1])
        producto_nombre_entry.config(state="readonly")

        precio_label = Label(ventana_vender_producto, text='Precio por Metro: ', font=('Helvetica',15))
        precio_label.grid(row=2, column=0)

        producto_precio_entry = Entry(ventana_vender_producto)
        producto_precio_entry.grid(row=2, column=1)
        producto_precio_entry.insert(0, datos[2])
        producto_precio_entry.config(state="readonly")

        stock_label = Label(ventana_vender_producto, text='Metro/Kilos/Unidades', font=('Helvetica',15))
        stock_label.grid(row=3, column=0)

        producto_stock_entry = Entry(ventana_vender_producto)
        producto_stock_entry.grid(row=3, column=1)
        producto_stock_entry.insert(0, datos[3])
        producto_stock_entry.config(state="readonly")

        cantidad_vender_label = Label(ventana_vender_producto, text='Unidades a vender: ', font=('Helvetica',15))
        cantidad_vender_label.grid(row=4, column=0)

        cantidad_var = StringVar()
        cantidad_vender_entry = Entry(ventana_vender_producto, textvariable=cantidad_var)
        cantidad_vender_entry.grid(row=4, column=1)
        cantidad_var.trace_add("write", calcular_venta)

        total_label = Label(ventana_vender_producto, text="Total: ", font=('Helvetica',15))
        total_label.grid(row=5, column=0)

        producto_total_var = StringVar()
        producto_total_entry = Entry(ventana_vender_producto, textvariable=producto_total_var)
        producto_total_entry.grid(row=5, column=1)
        producto_total_entry.config(state= "readonly")

        def vender_producto():
            cantidad = float(cantidad_vender_entry.get())
            stock = float(producto_stock_entry.get())
            if cantidad <= stock:
                precio = float(producto_precio_entry.get())
                stock_actualizado = stock - cantidad

                fecha_actual = datetime.date.today()
                base_datos = sqlite3.connect('LaJardinera.bd')
                cursor = base_datos.cursor()

                cursor.execute('INSERT INTO ventas(id_producto, cantidad, precio_unitario, fecha) VALUES (?,?,?,?)',
                            (datos[0], cantidad, precio, fecha_actual))
                
                cursor.execute('UPDATE producto SET cantidad=? WHERE id_producto=?', 
                            (stock_actualizado, datos[0]))
                
                base_datos.commit()
                messagebox.showinfo('Completado','La venta se ha realizado con éxito.')
                ventana_vender_producto.destroy()

            else:
                messagebox.showerror('Error','Stock Insuficiente' )

            

        boton_vender = Button(ventana_vender_producto, text='Realizar Venta', command=vender_producto, font=('Helvetica',15))
        boton_vender.grid(row=6, column=0, columnspan=2)
