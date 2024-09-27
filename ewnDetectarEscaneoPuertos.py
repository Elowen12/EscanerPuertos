#Importamos las librerias correspondientes
#Libreria para comunicacion de red
import socket
#libreria para controlar tiempo
import time


#Clase que me va a detectar si alguien esta escanando puertos
class Guardian():
    def __init__(self,ip, puertos):
        
        #Le decimos que tenga un atributo donde alamacenaremos los puertos que queremos que monitore
        self.puertos = puertos
        self.ip = ip

    
    #funcion que estara monitoreando posibles escaneos
    def monitorear(self):

        while True:

            #Creamos una variable para almacenar los puertos escuchados
            solicitudes = 1

            #almacenamos al solicitante de la conexion
            solicitante = ""

            for puerto in self.puertos:

                server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
                
                #Agregamos la ip del servidor y su puerto
                direccion = (self.ip,puerto)
                server.bind(direccion)

                #Ponemos a escuchar al servidor
                server.listen(2)
                print("Monitoreando conexiones...")

                try:
                     #Obtenemos la conexion
                    cliente, direccion = server.accept()
                    print("Conexion establecida con: "+str(direccion) + " Puerto: "+ str(puerto))
                    solicitante = direccion

                    #opcional
                    #Recibimos los datos enviados por el cliente
                    datos = cliente.recv(1024).decode("utf-8").strip()

                    print("Datos recibidos: " + datos )
                
                    #Cerramos las conexiones
                    cliente.close()
                    server.close()
                    print("conexion terminada...")

                    #aumentamos el contador de solicitudes
                    solicitudes = solicitudes + 1

                except server.timeout:
                    print("tiempo de monitoreo agotado..")
                    print("Reiniciando servidor...")
                    server.close()
                    break


                
            #Validamos que las solicitudes 
            if solicitudes >= len(self.puertos):
                print("La ip "+ str(solicitante) +" esta realizando un escaneo de puertos")


if __name__ == "__main__":
    puertos = [21,80,100]
    monitor = Guardian("192.168.1.20",puertos)
    monitor.monitorear()

