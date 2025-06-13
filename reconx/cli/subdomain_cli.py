import os
import socket
from colorama import Fore
from reconx.core import subfinder_py, amass_py, assetfinder_py, dnsx_py, sublister_py

def load_wordlist(path="wordlist.txt"):
    try:
        with open(path, "r") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"[!] Wordlist file not found at {path}, using default list.")
        return ["www", "mail", "ftp", "dev", "test", "admin"]

def resolve_domain(subdomain):
    try:
        socket.gethostbyname(subdomain)
        return True
    except socket.error:
        return False

def run(args):
    domain = args.domain
    print(f"{Fore.CYAN}[+] Starting subdomain enumeration for {domain}{Fore.RESET}\n")

    wordlist = load_wordlist(args.wordlist)
    subdomains = set()

    print(f"{Fore.YELLOW}[*] Using internal subfinder logic...{Fore.RESET}")
    subdomains.update(subfinder_py.run(domain))

    print(f"{Fore.YELLOW}[*] Using internal amass logic...{Fore.RESET}")
    subdomains.update(amass_py.run(domain))

    print(f"{Fore.YELLOW}[*] Using internal assetfinder logic...{Fore.RESET}")
    subdomains.update(assetfinder_py.run(domain))

    print(f"{Fore.YELLOW}[*] Using internal sublister logic...{Fore.RESET}")
    subdomains.update(sublister_py.run(domain))

    print(f"{Fore.YELLOW}[*] Generating brute-force subdomains...{Fore.RESET}")
    for prefix in wordlist:
        subdomains.add(f"{prefix}.{domain}")

    print(f"{Fore.YELLOW}[*] Probing live subdomains using DNSX logic...{Fore.RESET}")
    live_subs = dnsx_py.probe(subdomains)

    print(f"\n{Fore.GREEN}[+] Subdomain enumeration completed for {domain} — {len(live_subs)} live subdomains found.{Fore.RESET}")
    for sub in sorted(live_subs):
        print(sub)
