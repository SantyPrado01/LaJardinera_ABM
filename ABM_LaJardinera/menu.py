from tkinter import *
from comandosSQL import *
from funciones import * 

ventana = Tk()
ventana.resizable(width=False, height=False)
ventana.title('Textil La Jardinera')

tiutlo = Label(ventana, text='Gestion de Stock', font=60)
tiutlo.grid(row=0, columnspan=3, padx=10, pady=10)

boton_agregar = Button(ventana, text='Agregar Productos', command=pantallaAgregar, font=45)
boton_agregar.grid(row=1, column=0, padx=10, pady=10)

boton_mostrar_productos = Button(ventana, text='Consultar Productos', command=pantallaBuscar, font=45)
boton_mostrar_productos.grid(row=1, column=1, padx=10, pady=10)

boton_buscar = Button(ventana, text='Consultar Informes', command="", font=45)
boton_buscar.grid(row=1, column=2, padx=10, pady=10)

ventana.mainloop()