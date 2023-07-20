import socket

signaling_port = 10008
data_channel_port = 10009

def readFrom(protocol, sock, bufSize = 1024):
    assert bufSize > 1
    if protocol == "TCP":
        try:
            return sock.recv(bufSize)
        except:
            return None
    elif protocol == "UDP":
        assert bufSize < 65535
        try:
            return sock.recvFrom(bufSize)
        except:
            return None


def sendTo(protocol, sock, message):
    sock.send(bytes(message))
    return None

def setupParameters(tcpport = 10008, udpport = 10009):
    global signaling_port, data_channel_port
    signaling_port = tcpport
    data_channel_port = udppport
    
def initConnection():
    global TCP_SOCKET, UDP_SOCKET, TCP_REMOTE_PEER, signaling_port
    # if we're breaking up with the current pair, we close() the sockets in preparation for a nwe partner
    if TCP_SOCKET:
        TCP_SOCKET.close()
        TCP_SOCKET = None
    if UDP_SOCKET:
        UDP_SOCKET = None

    TCP_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # the program will block until someone else connects to the thing
    TCP_SOCKET.setblocking(0)
    # get a better name

    TCP_SOCKET.bind(("0.0.0.0", signaling_port))
    print(f"<signalerTCP> Listening on TCP port {signaling_port}")
    TCP_SOCKET.listen()
    while True:
        try:
            conn, addr = TCP_SOCKET.accept()
            break
        except:
            # do nothing, because there is no connection

    print(f"<signalerTCP> Remote peer has connected: {addr}")

    # now that everything is set up, we can set global objects that can be read from
    TCP_CONNECTION = conn
    TCP_REMOTE_PEER = addr
    UDP_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    UDP_SOCKET.bind( (addr[0], 10008) )
