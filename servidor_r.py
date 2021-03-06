#!/usr/bin/python
from threading import Thread
from Tkinter import *
from PIL import Image, ImageTk
from math import floor
import socket
import binascii
import struct

#Clase genera hilo cada que hay un nuevo cliente
class Hilos(Thread):
    def __init__(self, socket2, direccion):
        Thread.__init__(self)
        self.socket2 = socket2
        self.datos = direccion[0]   
        
    def run(self):
        #corre el hilo y hace acciones de comandos que acepta
        while 1:
            msj, addr = self.socket2.recvfrom(4)
            comando = desempaqueto(msj)
            if comando[0] == "EXIT":
                self.socket2.close()
                print self.datos + " se desconecto"
                break
            if comando[0] == "GRIS":
                accion_grises()
            if comando[0] == "PROM":
                accion_promedio()
            if comando[0] == "ORIG":
                accion_original()
            if comando[0][0] == "U" and comando[0][1] == "M":
                valor = comando[0][2] + "." +comando[0][3]
                accion_umbral(float(valor))
            print "Cliente IP no. " + self.datos + " cambia a " + str(comando[0])

def desempaqueto(valores):
    #Desempaqueto los struct con 4 bytes en cadena string
    print valores
    paquete = struct.Struct('4s')
    obtener_valores = paquete.unpack(valores)
    print "\n"
    print "Cadena: ", paquete.format
    print "Uso: ", paquete.size
    print "Desempaquetado: ", obtener_valores
    print "\n"
    return obtener_valores

def poner_imagen(image):
    #pone imagen en ventana
    photo = ImageTk.PhotoImage(image)
    global label
    label = Label(image=photo)
    label.imagen = photo
    label.pack()

def cambiar_agrises(imagen):
    #Cambia a grises
    pixeles = imagen.load()
    x, y = imagen.size
    
    imagen_nueva = Image.new("RGB", (x, y))
    
    colores = []
    for a in range(x):
        for b in range(y):
            pixel_color = pixeles[a, b]
            promedio = sum(pixel_color)/3
            tupla_promedio = (promedio, promedio, promedio)
            colores.append(tupla_promedio)
            imagen_nueva.putpixel((a, b), tupla_promedio)
    
    return imagen_nueva

def cambiar_promedio(imagen):
    #Hace efecto borrado
    pixeles = imagen.load()
    x, y = imagen.size
    imagen_nueva_prom = Image.new("RGB", (x, y))
    
    colores = []
    for a in range(x):
        for b in range(y):
            pixel_color = pixeles[a, b]
            veces = 5
            suma = 0
            promedio = 0
            
            try:
                pixel_norte = pixeles[a-1,b]
            except IndexError:
                pixel_norte = (0, 0, 0)
                veces = veces - 1
            try:
                pixel_sur = pixeles[a+1, b]
            except IndexError:
                pixel_sur = (0, 0, 0)
                veces = veces - 1
            try:
                pixel_este = pixeles[a, b+1]
            except IndexError:
                pixel_este = (0, 0, 0)
                veces = veces - 1
            try:
                pixel_oeste = pixeles[a, b-1]
            except IndexError:
                pixel_oeste = (0, 0, 0)
                veces = veces - 1
            
            Rojos_suma = pixel_norte[0] + pixel_sur[0] + pixel_este[0] + pixel_oeste[0] + pixel_color[0]
            Verdes_suma = pixel_norte[1]+ pixel_sur[1] + pixel_este[1] + pixel_oeste[1] + pixel_color[1]
            Azul_suma = pixel_norte[2]+ pixel_sur[2] + pixel_este[2] + pixel_oeste[2] + pixel_color[2]
            
            Rojo_prom = Rojos_suma/veces
            Verdes_prom = Verdes_suma/veces
            Azul_prom = Azul_suma/veces
            
            tupla_promedio = (Rojo_prom, Verdes_prom, Azul_prom)
            colores.append(tupla_promedio)
            imagen_nueva_prom.putpixel((a, b), tupla_promedio)
    
    return imagen_nueva_prom

def cambiar_umbral(imagen, umbral_valor):
    #Binariza segun umnbral
    pixeles = imagen.load()
    x, y = imagen.size
    imagen_nueva = Image.new("RGB", (x, y))
    
    for a in range(x):
        for b in range(y):
            pixel_color = pixeles[a, b]
            valor_canal = float(pixel_color[0])
            color_nor = valor_canal/255.0
            if(color_nor>=umbral_valor):
                poner_pixel = 255
            else:
                poner_pixel = 0
            tupla_pixel = (poner_pixel, poner_pixel, poner_pixel)
            imagen_nueva.putpixel((a, b), tupla_pixel)
    
    return imagen_nueva

def obtener_original(path_imagen_original):
    imagen = Image.open(path_imagen_original)
    return imagen

#Acciones de comandos

def accion_grises():
    label.destroy()
    imagen_grises = cambiar_agrises(imagen_original.convert("RGB"))
    poner_imagen(imagen_grises)

def accion_original():
    label.destroy()
    imagen_original = obtener_original(path_imagen_original)
    poner_imagen(imagen_original)

def accion_promedio():
    label.destroy()
    imagen_grises = cambiar_agrises(imagen_original.convert("RGB"))
    imagen_prom = cambiar_promedio(imagen_grises.convert("RGB"))
    poner_imagen(imagen_prom)

def accion_umbral(umbral_valor):
    label.destroy()
    imagen_grises = cambiar_agrises(imagen_original.convert("RGB"))
    imagen_umb = cambiar_umbral(imagen_grises.convert("RGB"), umbral_valor)
    poner_imagen(imagen_umb)


def main():
    socket1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    socket1.bind(("localhost", 6699))
    print "Haz iniciado satisfactoriamente el editor de imagenes colaborativo\nmuestro los mensajes."
    clientes = []
    
    root = Tk()
    root.title('Filtros')
    path_imagen_original = "paris.gif"
    frame = Frame()
    frame.pack(padx=5,pady=5)
    global imagen_original
    imagen_original = obtener_original(path_imagen_original)
    poner_imagen(imagen_original)
    numero = int(raw_input("Cuantos van a colaborar: "))
    
    while (1):
        print "1) Acepta conexiones"
        socket2, direccion = socket1.recvfrom(4)
        print "2) Mensaje conectado"
        print direccion[0] + " conectado."
        print "3) Genera hilos"
        hilo = Hilos(socket1, direccion)
        print "4) Empieza hilo"
        hilo.start()
        print "5) Agrega cliente"
        clientes.append(hilo)
        if len(clientes) == numero:
            break
        else:
            print "Esperando cliente . . . . "

    print "6) Actualizo GUI"
    root.mainloop(0)
    print "cerrando"
    socket1.close()

path_imagen_original = "paris.gif"
main()