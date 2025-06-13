import socket
from colorama import Fore

def run(subs):
    live = []
    for s in subs:
        try:
            socket.gethostbyname(s)
            live.append(s)
        except:
            continue
    print(Fore.GREEN + f"[+] {len(live)} live subdomains found.")
    return sorted(live)
