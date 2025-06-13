import socket
from colorama import Fore

def dnsx_py(subs):
    live = []
    for s in subs:
        try:
            socket.gethostbyname(s)
            live.append(s)
        except:
            continue
    return sorted(live)
