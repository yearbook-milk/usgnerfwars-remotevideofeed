import remote

remote.setupParameters()
try:
    remote.init_connection(input("Addr? "))
except Exception as e:
    print(f"Failed to establish a connection to the remote: {e}")

fn = 0
while True:
    print("I am doing something while also listening to the remote.")
    r = remote.readFrom("UDP", remote.UDP_SOCKET, 2048)
    if r:
        print(r)
        
    if fn % 25 == 0:
        remote.sendTo("TCP", remote.TCP_SOCKET, f"Just received frame #{fn}")
        
        
    fn += 1
