#!/usr/bin/python
import socket  
import binascii
import struct

envio = socket.socket() #creo un socket  
envio.connect(("localhost", 6699))  #conecto

print "Haz entrado satisfactoriamente al cambio de imagen, para salir escribe <<salir>> ;)"
print "Escribe <<grises>> para poner a escala de grises"
print "Escribe <<umbral numero>> para poner un umbral"
print "Escribe <<blurr>> para sacar el promedio de cada pixel"
print "Escribe <<original>> para poner la imagen en su estado original"

paquete = struct.Struct('2s f')


while (1):
      texto = raw_input("Escribe aqui: ")
      if texto == "grises":
            texto = "GR"
      elif texto == "umbral":
            texto = "UM"
      elif texto == "blurr":
            texto == "PR"
      elif texto == "original":
            texto = "OR"
      valores = (texto, 0.5)
      empaquetado = paquete.pack(*valores)
      print "\n"
      print "Cadena: ", paquete.format
      print "Uso: ", paquete.size
      print "Empaquetado: ", binascii.hexlify(empaquetado)
      print "\n"
      envio.send(empaquetado)
      if texto == "salir":
         valores = ("EX", 0.5)
         empaquetado = paquete.pack(*valores)
         envio.send(empaquetado)
         break  
      

envio.close() #cierro socket


