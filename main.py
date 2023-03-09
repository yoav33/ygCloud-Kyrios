# ygCloud Kyrios - MAIN
# Kyrios, or kurios, is a Greek word which is usually translated as "lord" or "master".
# https://github.com/yoav33

print("--------------")
print("ygCloud-Kyrios")
print("--------------")

import configparser
import socket
import os

# connected device class: basically for managing if a device is approved or not (passkey correct, or remembered)
class connectedDevice:
    ipadd = ""
    cert = ""
    approved = False

config = configparser.ConfigParser()
config.read(r'kyrios.conf')

#import socket
import select
import time

HOST = '0.0.0.0'
PORT = (config.get('server', 'port'))
PASSKEY = (config.get('server', 'passkey'))

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, int(PORT)))
    sock.listen()
    print()
    print('waiting for client connection...')
    print(f"listening on: {HOST}:{PORT}")
    conn, addr = sock.accept()      # Note: execution waits here until the client calls sock.connect()
    print('client connected, waiting for passkey')
    passkeymessage = 'sendpasskey'
    print(f"sending: {passkeymessage}")
    verifyPasskey(passkeymessage, conn, PASSKEY)

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
    else:
        print("passkey verified! sending accepted message")
        encAcc = bytes("passkeyrejected", 'utf-8')
        sock.sendall(encAcc)
        print("passkey declined! sending rejection message and restarting")

while True:
    main()