#!/usr/bin/python
from threading import Thread
import socket

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
                        print self.datos + " se desconeto"
                        break

                  print self.datos + " dijo: " + msj
            
def main():  
      socket1 = socket.socket()  
      socket1.bind(("localhost", 6699))  
      print "Haz iniciado satisfactoriamente el chat\nmuestro los mensajes."
      socket1.listen(1)  
      clientes = []
      
      while (1):
            socket2, direccion = socket1.accept()
            print direccion[0] + " conectado."
            hilo = Hilos(socket2, direccion)
            hilo.start()
            clientes.append(hilo)
            
      print "cerando"
      socket1.close()
        

main()
