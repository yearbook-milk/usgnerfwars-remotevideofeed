import socket
import time

signaling_port = 10007
udp_port = 0

TCP_SOCKET = None
TCP_CONNECTION = None
UDP_SOCKET = None
TCP_REMOTE_PEER = None

def sendTo(protocol, sock, message, destiny = None):
    global udp_port
    print(destiny)
    message = bytes(message, "ascii")
    try:
        if protocol == "TCP":
            sock.sendall(message)
        else:
            assert destiny != None
            sock.sendto(message, (destiny, udp_port))
        return None
    except (ConnectionResetError, OSError, BrokenPipeError) as e:
        print(f"[net] Cx Error {e}! Recx logic disabled.")
        #initConnection()

def readFrom(protocol, sock, bufSize = 1024):
    global TCP_REMOTE_PEER
    try:
        assert bufSize > 1
        if protocol == "TCP":
            try:
                return sock.recv(bufSize)
            except:
                return None
        elif protocol == "UDP":
            assert bufSize < 65535
            try:
                return sock.recv(bufSize)
            except Exception:
                return None
    except (ConnectionResetError, OSError, BrokenPipeError):
        print("Cx Error! Recx logic disabled.")
        #init_connection(TCP_REMOTE_PEER[0])

def setupParameters(tcpport = 10007, udpport = 10009):
    global signaling_port, udp_port
    signaling_port = tcpport
    #udp_port = udpport
    # the UDP port number is determined by the drone and is negotiated over TCP, so it does not make
    # any sense for the user to be able to set this number when it will be overwritten later

def init_connection(addr):
    global TCP_SOCKET, UDP_SOCKET, udp_port, signaling_port, TCP_REMOTE_PEER
    print("Waiting to connect again...")
    if TCP_SOCKET:
        TCP_SOCKET.close()
        TCP_SOCKET = None
        print("Closed TCP socket.")
    if UDP_SOCKET:
        UDP_SOCKET = None
        print("Closed UDP socket.")
        
    TCP_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #TCP_SOCKET.setblocking(0)
    TCP_REMOTE_PEER = addr
    TCP_SOCKET.connect( (addr, signaling_port) )
    global TCP_CONNECTION
    TCP_CONNECTION = TCP_SOCKET
    TCP_SOCKET.setblocking(0)
    # on the other program, conn is the connected state of socket, but in this case both names refer to the same socket that we want to send to

    # now we have to wait for the UDP port number the remote wants
    while True:
        try:
            udp_port = int(str(TCP_SOCKET.recv(1024), "ascii"))
            print(f"Success! The remote peer has decided that the UDP will be over port {udp_port}")
            break
        except Exception as e:
            print(f"Remote peer send an invalid negotiated UDP port number back [{udp_port}: {e}], unable to establish receiver for UDP packets.")

    UDP_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    UDP_SOCKET.setblocking(0)
    #UDP_SOCKET.settimeout(1.0)   
    UDP_SOCKET.bind( ("0.0.0.0", udp_port) )

    
# 192.168.137.1

