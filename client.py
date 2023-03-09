import socket
import configparser
import time

config = configparser.ConfigParser()
config.read(r'client.conf')

HOST = (config.get('server', 'host'))
PORT = (config.get('server', 'port'))
PASSKEY = (config.get('server', 'passkey'))
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def verifyPasskey(Pksend, sock, PASSKEY):
    encReq = sock.recv(1024)
    Req = encReq.decode('utf-8')
    print(f"Req={Req}")
    if Req=="sendpasskey":
        pk = f"passkey={PASSKEY}"
        print(f"pk request confirmed. sending={pk}")
        encPk= bytes(pk, 'utf-8')
        sock.sendall(encPk)
        encOutcome = sock.recv(1024)
        outcome = encOutcome.decode('utf-8')
        print(f"outcome={outcome}")
        if outcome=='passkeyaccepted':
            print("accepted! sending acknowledgement")
            ack = bytes('approval acknowledged', 'utf-8')
            sock.sendall(ack)
            encReq = sock.recv(1024)
            Req = encReq.decode('utf-8')
            if Req=="sendpasskey":
                print("error: passkey requested again. exiting..")
                exit()
            if Req=='sendtask':
                print("requested to send task")
                #sendTask()

        else:
            print("rejected. exiting...")
            exit()
    else:
        print("request text does not match expectations!")

def main(sock):
    connectionSuccessful = False
    print("csucc=false")
    while not connectionSuccessful:
        try:
            print(f"trying to connect to: {HOST}:{PORT}")
            sock.connect((HOST, int(PORT)))    # Note: if execution gets here before the server starts up, this line will cause an error, hence the try-except
            print('socket connected')
            connectionSuccessful = True
        except:
            pass
        # end try
    # verify passkey!
    verifyPasskey(PASSKEY, sock, PASSKEY)
    # now send task:

main(sock)
    # here you put the task!