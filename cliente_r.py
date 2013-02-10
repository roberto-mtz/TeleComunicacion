#!/usr/bin/python
from Tkinter import *
import socket  
import binascii
import struct

envio = socket.socket() #creo un socket
envio.connect(("localhost", 6699))  #conecto
paquete = struct.Struct('4s')

valor_slider = 0

def ventana():
    global root
    root = Tk()
    root.title('Controlador')
    frame = Frame()
    frame.pack(padx=5,pady=5)
    b1 = Button(text='Original', command = boton_original).pack(in_=frame, side=LEFT)
    b2 = Button(text='Grises', command = boton_grises).pack(in_=frame, side=LEFT)
    b3 = Button(text='Promedio', command = boton_promedio).pack(in_=frame, side=LEFT)
    b4 = Button(text='Umbral', command = boton_slider).pack(in_=frame, side=LEFT)
    b5 = Button(text='Salir', command = boton_salir).pack(in_=frame, side=LEFT)
    root.mainloop()

def boton_grises():
    texto = "GRIS"
    valores = (texto)
    empaquetado = paquete.pack(valores)
    print "\n"
    print "Cadena: ", paquete.format
    print "Uso: ", paquete.size
    print "Empaquetado: ", binascii.hexlify(empaquetado)
    print "\n"
    envio.send(empaquetado)

def boton_original():
    texto = "ORIG"
    valores = (texto)
    empaquetado = paquete.pack(valores)
    print "\n"
    print "Cadena: ", paquete.format
    print "Uso: ", paquete.size
    print "Empaquetado: ", binascii.hexlify(empaquetado)
    print "\n"
    envio.send(empaquetado)

def boton_promedio():
    texto = "PROM"
    valores = (texto)
    empaquetado = paquete.pack(valores)
    print "\n"
    print "Cadena: ", paquete.format
    print "Uso: ", paquete.size
    print "Empaquetado: ", binascii.hexlify(empaquetado)
    print "\n"
    envio.send(empaquetado)

def boton_umbral():
    global valor_slider
    valor = valor_slider
    divi = str(float(valor)/100.0)
    texto = "UM" + divi[0] + divi[2]
    valores = (texto)
    empaquetado = paquete.pack(valores)
    print "\n"
    print "Cadena: ", paquete.format
    print "Uso: ", paquete.size
    print "Empaquetado: ", binascii.hexlify(empaquetado)
    print "\n"
    envio.send(empaquetado)

def valores_slider(value):
    global valor_slider 
    valor_slider = value
    print valor_slider


def boton_slider():
    ventanita = Tk()
    slider = Scale(ventanita, orient=HORIZONTAL,from_=0, to=100, command=valores_slider)
    b6 = Button(ventanita, text='Enviar', command = boton_umbral).pack(side=LEFT)
    slider.pack()


def boton_salir():
    valores = ("EXIT")
    empaquetado = paquete.pack(valores)
    envio.send(empaquetado)
    envio.close()
    root.destroy()

ventana()



