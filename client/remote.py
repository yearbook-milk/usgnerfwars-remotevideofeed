import socket

signaling_port = 10008
udp_port = 0

TCP_SOCKET = None
UDP_SOCKET = None

def sendTo(protocol, sock, message):
    sock.send(bytes(message))
    return None

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

def setupParameters(tcpport = 10008, udpport = 10009):
    global signaling_port, udp_port
    signaling_port = tcpport
    udp_port = udpport

def init_connection(addr):
    global TCP_SOCKET, UDP_SOCKET, udp_port, signaling_port
    TCP_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    TCP_REMOTE_PEER = addr
    TCP_SOCKET.connect( (addr, signaling_port) )
    # on the other program, conn is the connected state of socket, but in this case both names refer to the same socket that we want to send to

    # now we have to wait for the UDP port number the remote wants
    try: udp_port = int(str(TCP_SOCKET.recv(1024)))
    except:
        print("Remote peer send an invalid negotiated UDP port number back, unable to establish receiver for UDP packets.")
        input("<ENTER> to exit.")
        exit()

    UDP_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    UDP_SOCKET.bind( (addr, udp_port) )

    
