import sys
import socket


target = socket.gethostbyname('localhost')
try:
    for port in range(8079, 8085):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(1)
        result = s.connect_ex((target, port))
        print(f'on scan port {port}')
        if result == 0:
            print("Port {} is open".format(port))
        s.close()
except KeyboardInterrupt:
    print("\n Exiting Program !!!!")
except socket.gaierror:
    print("\n Hostname Could Not Be Resolved !!!!")
except socket.error:
    print("\ Server not responding !!!!")
except Exception as err:
    print(err)
sys.exit()