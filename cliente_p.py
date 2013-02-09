#!/usr/bin/python
import socket  
  
envio = socket.socket() #creo un socket  
envio.connect(("localhost", 6699))  #conecto

print "Haz entrado satisfactoriamente al chat, para salir escribe <<salir>> ;)"

while (1):  
      texto = raw_input("Escribe aqui: ")
      envio.send(texto)
      if texto == "salir":  
         break  
    
envio.close() #cierro socket
