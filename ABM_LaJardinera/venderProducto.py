import sqlite3
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import tkinter as tk

from comandosSQL import *

def vender_producto():
    ventana_vender_producto = Tk()
    ventana_vender_producto.resizable(width=None, height=None)

    vender_titulo = Label(ventana_vender_producto, text='Vender Producto')
    vender_titulo.grid(row=0, column=0, columnspan=2)

    producto_label = Label(ventana_vender_producto, text='Producto: ')
    producto_label.grid(row=1, column=0)

    producto_nombre_label = Label(ventana_vender_producto, text='')
    producto_nombre_label.grid(row=1, column=1)

    precio_label = Label(ventana_vender_producto, text='Precio por Metro: ')
    precio_label.grid(row=2, column=0)

    producto_precio_label = Label(ventana_vender_producto, text='')
    producto_precio_label.grid(row=2, column=1)

    stock_label = Label(ventana_vender_producto, text='')