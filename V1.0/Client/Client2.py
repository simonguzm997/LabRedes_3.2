import socket
import hashlib
import datetime
from datetime import datetime
#TransferInfo
TCP_IP = '192.168.0.5'
TCP_PORT = 50000
BUFFER_SIZE = 1024



numBytes2Get = 1024;

destination         = (TCP_IP, TCP_PORT);

clientInfo = "Cliente 1"


#For logs
testDate = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
print (testDate)
#Take inputs
cantClientes = input("Input numer of conections: ")
numCliente = input("Input client number: ")
fileName = "Cliente"+numCliente+'-Prueba-'+cantClientes+".txt"
hash = ""

# Log file Creation
logFile = open ("./logs/"+testDate+"-log.txt", "w")
logFile.write("Date of the test: "+ testDate+"\n")
logFile.write("Name connection amount: "+ cantClientes+"\n")
logFile.write("Client Number: "+ numCliente+"\n")
logFile.write("------------------------------------------\n")


#Hash Creation
Sha256Hash = hashlib.sha256()

def getFileHash ():
    f2 = open(fileName,'rb')
    while True:
        l2 = f2.read(BUFFER_SIZE)
        if not l2:
            break
        Sha256Hash.update(l2)


udpClientSocket     = socket.socket(socket.AF_INET, socket.SOCK_DGRAM);
print ("KAKAKAAK")
print (udpClientSocket)
logFile.write("My connection info: "+"\n")



sentBytesCount      = udpClientSocket.sendto(clientInfo.encode(), destination);


with open(fileName, 'wb') as f:
    tIniTransm = 0
    tFinTransm = 0
    boolTransEx = False
    numPaquetes = 0
    print ('Ready to receive')
    hash = udpClientSocket.recvfrom(numBytes2Get)[0]
    clientInfo = str(udpClientSocket.recvfrom(numBytes2Get)[0].decode('utf8')).split(":")

    logFile.write("My Ip: "+clientInfo[0] +"\n")
    logFile.write("My Port: "+clientInfo[1] +"\n")
    logFile.write("------------------------------------------\n")
    tIniTransm = datetime.now()
    while True:
        #print('receiving data...')
        data = udpClientSocket.recvfrom(numBytes2Get)[0]
        print ("PRINTDATA",data)
        numPaquetes = numPaquetes +1
        print (numPaquetes)
        if data == "Xd4Xa".encode():
            tFinTransm = datetime.now()
            boolTransEx = True
            transferTime = tFinTransm- tIniTransm
            ##TODO logFile.write("Client ip: "+ self.ip+" port: "+ str(self.port)+ "\n")
            logFile.write("Successfull delivery: "+ str(boolTransEx) +"\n")
            logFile.write("Transfer time: "+ str(transferTime) + "\n")
            logFile.write("Packet Number: "+ str(numPaquetes) + "\n")
            f.close()
            print ('File received successfully')
            break
        # write data to a file
        f.write(data)

#Integirty verification with Hash
getFileHash()
print ("The hash value received by the server is: ")
print (hash.decode())
print ("The hash calculated from the received file is: ")
print (Sha256Hash.hexdigest())

if hash.decode() == Sha256Hash.hexdigest():
    print ("Hash verified")
    logFile.write("Hash Verification: VERIFIED \n")
else:
    print ("Hash NOT verified")
    logFile.write("Hash Verification: NOT VERIFIED \n")

print('Data saved ')

print('connection ended')
