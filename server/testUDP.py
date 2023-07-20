import remote, time, random

remote.setupParameters()
try: remote.initConnection()
except Exception as e:
    print(f"Could not establish connection with other peer: {e}")


while True:
    msg = bytes(str(random.randint(0,1000)))
    remote.sendTo("UDP", remote.UDP_SOCKET, msg)
    print(f"I just sent something to the remote ({msg})")
    time.sleep(0.5)

    r = readFrom("TCP", remote.TCP_CONNECTION, 2048):
    if r:
        print(f"The remote just sent something to me: {r}")
