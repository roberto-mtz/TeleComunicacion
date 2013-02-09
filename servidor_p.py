#!/usr/bin/python
from threading import Thread
from Tkinter import *
from PIL import Image, ImageTk
from math import floor
import socket
import Queue

acciones = Queue.Queue()

class Hilos(Thread):
      def __init__(self, socket2, direccion):
            Thread.__init__(self)
            self.socket2 = socket2
            self.datos = direccion[0]   

      def run(self):
            while 1:
                  msj = self.socket2.recv(1024)
                  if msj == "salir":
                        self.socket2.close()
                        print self.datos + " se desconecto"
                        break
                  acciones.put(msj)
                  print self.datos + " dijo: " + msj
                  return


class GUI:
      def __init__(self, root, path_imagen_original):
            self.path_imagen_original = "paris.gif"
            self.frame = Frame()
            self.frame.pack(padx=5,pady=5)
            self.poner_imagen(self.obtener_original(self.path_imagen_original))
            

      def poner_imagen(self, image):
            photo = ImageTk.PhotoImage(image)
            global label
            label = Label(image=photo)
            label.imagen = photo
            label.pack()

      def cambiar_agrises(self):
            imagen = Image.open(path_imagen_original).convert("RGB")
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

      def cambiar_promedio(self, imagen):
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

      def cambiar_umbral(self, imagen, umbral_valor):
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

      def obtener_original(self, path_imagen_original):
            imagen = Image.open(path_imagen_original)
            return imagen

      def accion_grises():
            label.destroy()
            imagen_grises = cambiar_agrises(path_imagen_original)
            poner_imagen(imagen_grises)

      def accion_original():
            label.destroy()
            imagen_original = obtener_original(path_imagen_original)
            poner_imagen(imagen_original)

      def accion_promedio():
            label.destroy()
            imagen_grises = cambiar_agrises(path_imagen_original)
            imagen_prom = cambiar_promedio(imagen_grises.convert("RGB"))
            poner_imagen(imagen_prom)

      def accion_umbral():
            label.destroy()
            umbral_valor = 0.8
            imagen_grises = cambiar_agrises(path_imagen_original)
            imagen_umb = cambiar_umbral(imagen_grises.convert("RGB"), umbral_valor)
            poner_imagen(imagen_umb)



def main():
      socket1 = socket.socket()  
      socket1.bind(("localhost", 6699))  
      print "Haz iniciado satisfactoriamente el chat\nmuestro los mensajes."
      socket1.listen(1)  
      clientes = []
    
      root = Tk()
      root.title('Filtros')
      path_imagen_original = "paris.gif"
      gui = GUI(root, path_imagen_original)
    
      while (1):
            socket2, direccion = socket1.accept()
            print direccion[0] + " conectado."
            hilo = Hilos(socket2, direccion)
            hilo.start()
            clientes.append(hilo)
            mensajito = acciones.get()
            print "Este es el msjito = " + mensajito
            #root.after(10*1000, root.quit)
            #root.mainloop()
            
            
      print "cerrando"
      socket1.close()

main()
