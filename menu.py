from tkinter import *
from PIL import Image, ImageTk  
from agregarProducto import ventana_agregar_producto
from buscarProducto import buscar_producto
from generarInformes import generar_informe
from buscarProveedores import buscar_proveedores

ventana = Tk()

ventana.resizable(width=False, height=False)
ventana.title('Textil La Jardinera')
ventana.iconbitmap("icon.ico")
imagen_presentacion = Image.open("Control de Stock.png")
imagen_presentacion = imagen_presentacion.resize((600, 400))  # Ajusta el tamaño de la imagen

imagen_tk = ImageTk.PhotoImage(imagen_presentacion) # Convierte la imagen en un formato que Tkinter puede manejar

imagen_label = Label(ventana, image=imagen_tk)
imagen_label.grid(row=0, column=0, columnspan=3)

boton_agregar = Button(ventana, text='Agregar Productos', command=lambda: ventana_agregar_producto(ventana), font=('Helvetica', 15))
boton_agregar.grid(row=1, column=0)

boton_mostrar_productos = Button(ventana, text='Consultar Productos', command=lambda: buscar_producto(ventana), font=('Helvetica', 15))
boton_mostrar_productos.grid(row=1, column=1)

boton_buscar = Button(ventana, text='Consultar Informes', command=lambda: generar_informe(ventana), font=('Helvetica', 15))
boton_buscar.grid(row=1, column=2)

boton_proveedores = Button(ventana, text='Consultar Proveedores', command=lambda:buscar_proveedores(ventana), font=('Helvetica', 15))
boton_proveedores.grid(row=2, column=0)

boton_compraproveedores = Button(ventana, text= "Compra a Proveedores")
boton_compraproveedores.grid(row=2, column= 1)

ventana.mainloop()
