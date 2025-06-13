import socket
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore

def is_alive(domain):
    try:
        socket.gethostbyname(domain)
        return domain
    except:
        return None

def probe(subdomains, silent=False, verbose=False):
    if verbose and not silent:
        print(Fore.BLUE + f"[*] Probing {len(subdomains)} subdomains for liveness...")

    live = []
    with ThreadPoolExecutor(max_workers=50) as executor:
        results = executor.map(is_alive, subdomains)
        for result in results:
            if result:
                live.append(result)

    if not silent:
        print(Fore.GREEN + f"[+] {len(live)} live subdomains found.\n")

    return live
