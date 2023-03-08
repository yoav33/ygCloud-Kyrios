# ygCloud Kyrios - MAIN
# Kyrios, or kurios, is a Greek word which is usually translated as "lord" or "master".
# ygCloud Kyrios: the "host" of ygCloud - the backend.
# https://github.com/yoav33

import configparser
import socket

# connected device class: basically for managing if a device is approved or not (passkey correct, or remembered)
class connectedDevice:
    ipadd = ""
    cert = ""
    approved = False

config = configparser.ConfigParser()
config.read(r'kyrios.conf')

host = ''
port = int(config.get('server', 'port'))
passkey = (config.get('server', 'passkey'))
connections = (config.get('server', 'connections'))
s = socket.socket()

#if ((config.get('server', 'approveallconnections')) == "y"):
    #devaccepted = True
#else:
    #devaccepted = False

# this verifies connections - asks for passkey. name: ip:port of connected client. default: whether the client got accepted or not. usually should start with n.
# default is later checked again. default is boolean.
def verifyConnection():
    con, addr = s.accept()
    data = con.recv(1024)
    # real quick grab name
    passin = data.decode()
    print("passin: " + passin)
    expected = (f"passkey={passkey}")
    print("expected: " + expected)
    global devaccepted
    if passin==expected:
        print("now setting yes..")
        devaccepted = True
        print(devaccepted)
        return devaccepted
    else:
        if ((config.get('server', 'approveallconnections')) == "y"):
            devaccepted = True
        else:
            devaccepted = False
        return devaccepted

# s.listen(int(connections))
s.bind((host, port))
s.listen(5)
print("listening for connections.")

def sendTextViaSocket(message):
    s.bind((hostname.ipadd), )
    encodedMessage = bytes(message, 'utf-8')
    s.sendall(encodedMessage)
    encodedAckText = sock.recv(1024)
    ackText = encodedAckText.decode('utf-8')
    print(f"acktext={ackText}")

# forever loop!
while True:
    verifyConnection()
    print(f"accepted: {devaccepted}")
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    print(hostname)
    print(ip_address)
    hostname = connectedDevice()
    hostname.ipadd = (f"{ip_address}")
    hostname.approved = devaccepted
    hostname.cert = "Y21ES"
    print(hostname.cert)
    print()
    print("device details class:")
    print(f"IP={hostname.ipadd}, approved={hostname.approved}")
    print("now trying function...")
    sendTextViaSocket("MESSAGE!@2")
