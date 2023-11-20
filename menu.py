from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk  
from buscarProducto import buscar_productos, nuevo_producto, buscar_proveedor, nuevo_proveedor, buscar_informes


ventana = Tk()

ventana.state('zoomed')
ventana.config(bg='white')
ventana.title('Textil La Jardinera')
ventana.iconbitmap("icon.ico")
imagen_presentacion = Image.open("Control de Stock.png")
imagen_presentacion = imagen_presentacion.resize((1200, 220))  # Ajusta el tamaño de la imagen

imagen_tk = ImageTk.PhotoImage(imagen_presentacion)# Convierte la imagen 

frame_menu = Frame(ventana, bg='white')

frame_imagen = Frame(frame_menu, bg='white')

imagen_label = Label(frame_imagen, image=imagen_tk)
imagen_label.pack()
frame_imagen.grid(row=0, column=0, columnspan=2, pady=15)

frame_botones = Frame(frame_menu, bg= 'white')

estilos_botones = ttk.Style()

estilos_botones.configure('BotonMenu.TButton', foreground='black', background='white', font=('Helvetica', 20), padding=(10,10), relief='groove')

boton_nuevo_prodcuto = ttk.Button(frame_botones, text='Nuevo Producto', command=lambda:nuevo_producto(frame_menu), style='BotonMenu.TButton')
boton_nuevo_prodcuto.grid(row=1, column=0, columnspan=2, pady=20)

boton_mostrar_productos = ttk.Button(frame_botones, text='Buscar Productos', command=lambda: buscar_productos(frame_menu), style='BotonMenu.TButton')
boton_mostrar_productos.grid(row=2, column=0, columnspan=2, pady=20)

boton_buscar = ttk.Button(frame_botones, text='Consultar Informes', command=lambda: buscar_informes(frame_menu), style='BotonMenu.TButton')
boton_buscar.grid(row=3, column=0, columnspan=2, pady=20)

boton_nuevo_proveedores = ttk.Button(frame_botones, text='Nuevo Proveedor', command=lambda:nuevo_proveedor(frame_menu), style='BotonMenu.TButton')
boton_nuevo_proveedores.grid(row=4, column=0, columnspan=2, pady=20)

boton_proveedores = ttk.Button(frame_botones, text='Buscar Proveedores', command=lambda:buscar_proveedor(frame_menu), style='BotonMenu.TButton')
boton_proveedores.grid(row=5, column=0, columnspan=2, pady=20)

boton_compraproveedores = ttk.Button(frame_botones, text= "Compra a Proveedores", command='', style='BotonMenu.TButton')
boton_compraproveedores.grid(row=6, column= 0, columnspan=2, pady=20)

frame_botones.grid(row=1, column=0, padx=15)
frame_menu.pack()

buscar_productos(frame_menu)

ventana.mainloop()
