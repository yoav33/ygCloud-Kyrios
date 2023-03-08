import socket
import configparser
import time

def authenticate(sendpass):
    s.send(f'passkey={sendpass}'.encode())

s = socket.socket()
print ("Socket created successfully.")
config = configparser.ConfigParser()
config.read(r'client.conf')

host = config.get('server', 'host')
port = int(config.get('server', 'port'))

s.connect((host, port))
print('Connection Established.')

# first attempt authentication.
authenticate(config.get('server', 'passkey'))

def receiveTextViaSocket():
    # get the text via the scoket
    encodedMessage = s.recv(1024)

    # if we didn't get anything, log an error and bail
    if not encodedMessage:
        print('error: encodedMessage was received as None')
        return None
    # end if

    # decode the received text message
    message = encodedMessage.decode('utf-8')
    print(f"message={message}")

    # now time to send the acknowledgement
    # encode the acknowledgement text
    encodedAckText = bytes(ACK_TEXT, 'utf-8')
    # send the encoded acknowledgement text
    s.sendall(encodedAckText)
    print("send acktext")

while True:
    receiveTextViaSocket()
