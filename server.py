import socket
from DHE import DH_Endpoint
import sqlite3

#function descrypt
def decryptAndSave(server,path):
    #conectar a la base de datos o crearla si no existe
    con = sqlite3.connect("decrypts")
    cursor = con.cursor()
    
    #try por si la base ya ha sido creada
    query = "CREATE TABLE decrypt(id INT, text VARCHAR(61));"
    try:
        cursor.execute(query)
    except:
        print("La tabla ya ha sido creada.")
    
    #abrir archivo
    encrypt = open(path,"r")
    
    for i in range(4020):
        text = encrypt.readline()
        print("Decrypting "+text+"...")
        textDecrypt= server.decrypt_message(text)
        query = "INSERT INTO decrypt VALUES(" + str(i) + ",'"+textDecrypt+ "');"
        cursor.execute(query)
    
    encrypt.close()
    con.commit()
    con.close()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind the socket to the port
server_address = ('localhost', 10000)
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)
# Listen for incoming connections
sock.listen(1)
empezar =True

while empezar:
    # Wait for a connection
    print('waiting for a request')
    connection, client_address = sock.accept()
    try:
        print('connection from', client_address)
        
        c_public = connection.recv(16)
        if c_public:
            print('received public key: {!r}'.format(c_public))
            c_public = int(c_public)
            s_private=53
            s_public=59 

            print('sending public key to the enctypter')
            connection.sendall( str(s_public))
            
            #create server object 
            server = DH_Endpoint(c_public, s_public, s_private)
            
            #create partials key
            s_partial=server.generate_partial_key()
            print("server partial key: {!r}".format(s_partial))

            #recibir partial key
            c_partial = connection.recv(16)
            print("client partial key: "+c_partial)
            c_partial = int(c_partial)
            
            #enviar partial key
            connection.sendall(str(s_partial))
            
            #create the full key
            s_full=server.generate_full_key(c_partial)
            print("server full key: {!r}".format(s_full))
            
            #received the path
            path = connection.recv(16)
            print("path received: "+path)
            
            #decrypt the file
            decryptAndSave(server,path)

            empezar=False
        else:
            print('no request from', client_address)

    finally:
        connection.close()