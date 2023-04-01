# ygCloud Kyrios - MAIN
# Kyrios, or kurios, is a Greek word which is usually translated as "lord" or "master".
# https://github.com/yoav33

print("--------------")
print("ygCloud-Kyrios")

import configparser
import socket
import os
from datetime import datetime
import time

# connected device class: basically for managing if a device is approved or not (passkey correct, or remembered)
class connectedDevice:
    ipadd = ""
    cert = ""
    approved = False

config = configparser.ConfigParser()
config.read(r'kyrios.conf')

cindex = 1

HOST = "0.0.0.0"
PORT = (config.get('server', 'port'))
PASSKEY = (config.get('server', 'passkey'))

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(("0.0.0.0", int(PORT)))

def main():
    print("--------------")
    print(f"listening on {HOST}:{PORT}")
    sock.listen()
    print('waiting for client connection...')
    conn, addr = sock.accept()      # Note: execution waits here until the client calls sock.connect()
    print('client connected, waiting for passkey')
    passkeymessage = 'sendpasskey'
    print(f"sending: {passkeymessage}")
    verifyPasskey(passkeymessage, conn, PASSKEY)

def stratussend(sock):
    ssack = bytes("stratussend acknowledged", 'utf-8')
    sock.sendall(ssack)
    # first get client hostname to know what to put it under
    clientname = socket.gethostname()
    print("-------------------")
    print("ygCloud StratusSend")
    print("-------------------")
    print()
    print(f"client name: {clientname}")
    if (os.path.isdir(clientname)):
        print("client folder exists")
    else:
        os.mkdir(clientname)
        print("client folder just created")
    print("receiving file name..")
    incomingfilename = sock.recv(1024).decode('utf-8')
    print(f"incoming file name: {incomingfilename}")
    print("sending acknowledgement.")
    sock.sendall(bytes("acknowledged", 'utf-8'))
    # begin receiving file
    BUFFER_SIZE = 4096 # default buffer size for kyrios: 4096B
    os.chdir(clientname)
    print(f"receiving new file from {clientname}: {incomingfilename}")
    with open('testfile', "wb") as f:
        while True:
            bytes_read = sock.recv(BUFFER_SIZE)
            if not bytes_read:
                os.chdir('..')
                print("file received. closing socket and breaking...")
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                sock.close()
                print("-----------")
                break
            f.write(bytes_read)



def verifyPasskey(send, sock, PASSKEY):
    encReq = bytes(send, 'utf-8') #encReq = encoded request
    sock.sendall(encReq)
    encPK = sock.recv(1024) #encodedPasskey
    Pkin = encPK.decode('utf-8')
    print(f"Pkin={Pkin}")
    expectedPkin = f"passkey={PASSKEY}"
    print(f"expectedPkin={expectedPkin}")
    if Pkin==expectedPkin:
        print("passkey verified! sending accepted message")
        encAcc = bytes("passkeyaccepted", 'utf-8')
        sock.sendall(encAcc)
        encAck = sock.recv(1024)
        Ack = encAck.decode('utf-8')
        if Ack=="approval acknowledged":
            print("approval acknowledged! sending request of task.")
            encReq = bytes('sendtask', 'utf-8')  # encReq = encoded request
            sock.sendall(encReq)
            encTask = sock.recv(1024)
            task = encTask.decode('utf-8')
            print(f"task={task}")
            if task=="stratussend":
                stratussend(sock)
            if task=="raindropsend":
                raindropsend(sock)
            if task=="raindroplistener":
                raindroplistener(sock)
    else:
        print("passkey verified! sending accepted message")
        encAcc = bytes("passkeyrejected", 'utf-8')
        sock.sendall(encAcc)
        print("passkey declined! sending rejection message and restarting")

rdlist = []

def raindropsend(sock):
    print("raindrop sender ------------------")
    count = len(rdlist)
    print(f"sending '{count}' for count in rdlist")
    msg = bytes(f"{count}", 'utf-8')
    sock.sendall(msg)
    for x in rdlist:
        print(f"sending data for {x.username}...")
        msg = bytes(f"localip={x.localip}", 'utf-8')
        sock.sendall(msg)
        msg = bytes(f"port={x.port}", 'utf-8')
        sock.sendall(msg)
        msg = bytes(f"username={x.username}", 'utf-8')
        sock.sendall(msg)
        msg = bytes(f"time={x.time}", 'utf-8')
        sock.sendall(msg)
        print("sent. moving on")
    print("done with rdlist")

    #encack = sock.recv(1024)
    #ack = encack.decode('utf-8')
    #print(f"ack = {ack}")

def raindroplistener(sock):
    msg = bytes('sendlocalip', 'utf-8')
    sock.sendall(msg)
    enclip = sock.recv(1024)
    localip = enclip.decode('utf-8')
    msg = bytes('sendport', 'utf-8')
    sock.sendall(msg)
    encport = sock.recv(1024)
    port = encport.decode('utf-8')
    msg = bytes('sendname', 'utf-8')
    sock.sendall(msg)
    encport = sock.recv(1024)
    username1 = encport.decode('utf-8')
    print(f"received client info: {username1}, {localip}:{port}")
    name = RainDropUser()
    name.username = username1
    name.localip = localip
    name.port = port
    name.time = datetime.now().strftime("%H:%M")
    rdlist.append(name)
    maxcount = (config.get('raindrop', 'maxlisteners'))
    print(f"count of rdlist: {len(rdlist)} (maximum: {maxcount})")
    if not maxcount == "n":
        if len(rdlist) >= int(maxcount):
            print("rdlist user count exceeded max. removing 0th.")
            del rdlist[0]
    print("going through rdlist: --------------------")
    for x in rdlist:
        print(f"{x.username}, {x.localip}:{x.port} at {x.time}")
class RainDropUser:
    index = 1
    name = ""
    localip = ""
    port = 0000

while True:
    try:
        main()
    except KeyboardInterrupt:
        print("keyboardinterrupt. closing socket")
        sock.close()