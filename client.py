import socket
import os
import time
import bcrypt
from DHE import DH_Endpoint

# === Cackeo de archivos ===
# === Cackeo de archivos ===
# === Cackeo de archivos ===
print("Empezando crackeo del archivo 1.")
os.system(".\hashcat.exe --stdout .\diccionario_2.dict -r rules/best64.rule | .\hashcat.exe -m 0 -a 0 -O .\Hashes\archivo_1 -o cracked1.txt")
time.sleep(1)

print("Empezando crackeo del archivo 2.")
os.system(".\hashcat.exe --stdout .\diccionario_2.dict -r rules/best64.rule | .\hashcat.exe -m 10 -a 0 -O .\Hashes\archivo_2 -o cracked2.txt")
time.sleep(1)

print("Empezando crackeo del archivo 3.")
os.system(".\hashcat.exe --stdout .\diccionario_2.dict -r rules/best64.rule | .\hashcat.exe -m 10 -a 0 -O .\Hashes\archivo_3 -o cracked3.txt")
time.sleep(1)

print("Empezando crackeo del archivo 4.")
os.system(".\hashcat.exe --stdout .\diccionario_2.dict -r rules/best64.rule | .\hashcat.exe -m 1000 -a 0 -O .\Hashes\archivo_4 -o cracked4.txt")
time.sleep(1)

print("Empezando crackeo del archivo 5.")
os.system(".\hashcat.exe --stdout .\diccionario_2.dict -r rules/best64.rule | .\hashcat.exe -m 1800 -a 0 -O -w 3 .\Hashes\archivo_5 -o cracked5.txt")


# === hashear los archivos ===
# === hashear los archivos ===
# === hashear los archivos ===

# archivo 1
archivo = open('cracked1.txt', 'r')
salida = open('hash1.txt','w')
print("Hasheando archivo1...")
for i in range(1000):
    lineText = archivo.readline()
    largo = len(lineText)
    lineText = lineText[33:largo]
    print("Hasheando el texto: "+lineText)
    salida.write( bcrypt.hashpw(lineText, bcrypt.gensalt() ) +'\n')

archivo.close()
salida.close()
print("======================")

# archivo 2
archivo2 = open('cracked2.txt', 'r')
salida2 = open('hash2.txt','w')
print("Hasheando archivo2...")
for i in range(1000):
    lineText = archivo2.readline()
    largo = len(lineText)
    lineText = lineText[50:largo]
    print("Hasheando el texto: "+lineText)
    salida2.write( bcrypt.hashpw(lineText, bcrypt.gensalt() ) +'\n')

archivo2.close()
salida2.close()

print("======================")
# archivo 3
archivo3 = open('cracked3.txt', 'r')
salida3 = open('hash3.txt','w')
print("Hasheando archivo3...")
for i in range(1000):
    lineText = archivo3.readline()
    largo = len(lineText)
    lineText = lineText[50:largo]
    print("Hasheando el texto: "+lineText)
    salida3.write( bcrypt.hashpw(lineText, bcrypt.gensalt() ) +'\n')

archivo3.close()
salida3.close()

print("======================")
# archivo 4
archivo4 = open('cracked4.txt', 'r')
salida4 = open('hash4.txt','w')
print("Hasheando archivo4...")
for i in range(1000):
    lineText = archivo4.readline()
    largo = len(lineText)
    lineText = lineText[33:largo]
    print("Hasheando el texto: "+lineText)
    salida4.write( bcrypt.hashpw(lineText, bcrypt.gensalt() ) +'\n')

archivo4.close()
salida4.close()

print("======================")
# archivo 5
archivo5 = open('cracked5.txt', 'r')
salida5 = open('hash5.txt','w')
print("Hasheando archivo5...")
for i in range(20):
    lineText = archivo5.readline()
    lineText = lineText.split(":")
    print("Hasheando el texto: "+lineText[1])
    salida5.write( bcrypt.hashpw(lineText[1], bcrypt.gensalt() ) +'\n')

archivo5.close()
salida5.close()

#========== function encrypt ===========
#========== function encrypt ===========
#========== function encrypt ===========
def encyptFile(client):

    hashing1 = open("hash1.txt", "r")
    hashing2 = open("hash2.txt", "r")
    hashing3 = open("hash3.txt", "r")
    hashing4 = open("hash4.txt", "r")
    hashing5 = open("hash5.txt", "r")
    encrypt = open("encrypts.txt","w")

    for i in range(1000):
        text = hashing1.readline()
        print("Encrypting "+text+" ...")
        encrypt.write( client.encrypt_message(text) + "\n" )

        text = hashing2.readline()
        print("Encrypting "+text+" ...")
        encrypt.write( client.encrypt_message(text) + "\n" )

        text = hashing3.readline()
        print("Encrypting "+text+" ...")
        encrypt.write( client.encrypt_message(text) + "\n" )

        text = hashing4.readline()
        print("Encrypting "+text+" ...")
        encrypt.write( client.encrypt_message(text) + "\n" )

    for i in range(20):
        text = hashing5.readline()
        print("Encrypting "+text+" ...")
        encrypt.write( client.encrypt_message(text) + "\n" )

    hashing1.close()
    hashing2.close()
    hashing3.close()
    hashing4.close()
    hashing5.close()
    encrypt.close()

# =============== Connect to the descrypter file python ===============
# =============== Connect to the descrypter file python ===============
# =============== Connect to the descrypter file python ===============

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connect the socket to the port where the server is listening
server_address = ('localhost', 10000)
print('connecting to {} port {}'.format(*server_address))
sock.connect(server_address)

try:
    #crear llaves, enviar y recibir llaves publicas
    c_public=97
    c_private=91

    # requerir y enviar llave publica
    #message = input('Press Enter to request the public key')
    sock.sendall(str(c_public))
    print('Key public request is send.')

    # recibir llave publica
    s_public = sock.recv(16)
    print('received server public key: {!r}'.format(s_public))
    #transformar a int
    s_public = int(s_public)

    #create client object 
    client = DH_Endpoint(c_public, s_public, c_private)

    #create partials key
    c_partial = client.generate_partial_key()
    print("client partial key: {!r}".format(c_partial))

    #request partials key of server 
    sock.sendall(str(c_partial))
    print("Request the server partial key")

    #recibir partial key
    s_partial = sock.recv(16)
    s_partial = int(s_partial)
    print("received server partial key: {!r}".format(s_partial))

    #create the full key
    c_full=client.generate_full_key(s_partial)
    print("client full key: {!r}".format(c_full))

    #encrypt the hashs
    encyptFile(client)

    #sending the path
    sock.sendall("encrypts.txt")

finally:
    print('closing encypter socket')
    sock.close()