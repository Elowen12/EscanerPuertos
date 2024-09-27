#Importamos las librerias correspondientes para el modulo

#Realizar conexiones de red y transmitir datos
import socket
#Ejecutar comandos del sistema operativo
import subprocess
#Manejo de tiempos
import time

#Clase princpial para manejar la manipulacion de la red
class Red():

    #Constructor vacio de la clase
    def __init__(self) -> None:
        pass

    #Funcion que identifica los dispositivos conectados a una red
    def identificarDispositivosEnRed(self,red,inicio,fin):

        #Creamos una lista para almacenear las ips encontradas
        ips = []

        #Checamos que dispositivos estan conectados a una red
        for i in range(inicio,fin + 1):

            #Creamos una ip personalizada apartir del indice del bucle
            ip = f"{red}.{i}"

            print("Escaneando ip: "+ ip)


            #Verificamos si el dispositivo esta conectado a la red
            dispositivo = self.comunicar(ip=ip)

            #Si lo encontramos lo almacenamos en la lista
            if dispositivo:
                ips.append(ip)
        
        #Retornamos la lista encontrada
        return ips


        
    #Funcion para enviar un ping a un dispositivo conectado a la red
    def comunicar(self,ip):

        #Corremos el comaando ping para checar si la ip existe
        output = subprocess.run(["ping","-c","4",ip],capture_output=True,text=True)

        #Formateamos la respuesta a string para poderla leer
        respuesta = str(output)
        
        #Checamos si en la respuesta tememos este mensaje que nos indica de ping exitoso
        if "4 packets transmitted, 4 received, 0% packet loss," in respuesta:
            
            #Retornamos un true si el ping fue exitoso
            return True
        else: 

            #Retornamos un false si el ping fue exitoso
            return False
    
    def escanaerPuertos(self,ip,inicial,final):
        
        #Creamos una lista que almacene los puertos abiertos de la ip
        puertos = []

        #Recorremos los puertos que establecimos como inicio y final
        for puerto in range(inicial,final + 1):

            
            #Creamos un socket de conexion
            sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            sock.settimeout(5)

            direccion = (ip, puerto)

            #Establecemos la conexion con la ip
            respuesta = sock.connect_ex(direccion)

            #Checamos que la conexion sea exitosa
            if respuesta == 0:

                try:
                    # le enviamos algo de informacion para que nos retorne el banner del servicio corriendo
                    #sock.send(b"/r/n")

                    #Optenemos el banner del puerto, lo desencriptamos y formateamos para que sea mas legible
                    banner = sock.recv(1024).decode().strip()
                    
                    #Imprimimos un mensaje del puerto abierto
                    print(ip + "Puerto: " + str(puerto) + "abierto")
                    print(banner)

                    #Almacenamos el puerto y el banner en la lista
                    puertos.append({"puerto":puerto,"banner":banner})

                except:

                    #Imprimimos un mensaje si el puerto esta cerrado
                    print("No se pudo revisar el puerto")
                    
                    #Almacenamos el puerto y el banner en la lista
                    puertos.append({"puerto":puerto})
            
            else:
                   #Imprimimos un mensaje si el puerto esta cerrado
                    print(ip + " Puerto: " + str(puerto) + " cerrado") 
            
            #Cerramos la conexion
            sock.close()
        
        #Retornamos la lista de puertos abiertos
        return puertos
        

if __name__ == "__main__":
    
    
    ips = Red().identificarDispositivosEnRed("192.168.1",1,254)

    for ip in ips:

        red = Red()
        print(red.escanaerPuertos(ip,1,100))