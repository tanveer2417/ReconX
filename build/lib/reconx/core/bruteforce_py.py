import os
import socket
from concurrent.futures import ThreadPoolExecutor

def load_wordlist(wordlist_path):
    if not os.path.isfile(wordlist_path):
        print(f"[!] Wordlist file not found at {wordlist_path}. Skipping brute-force.")
        return []
    with open(wordlist_path, "r") as file:
        return [line.strip() for line in file if line.strip()]

def check_subdomain(subdomain):
    try:
        socket.gethostbyname(subdomain)
        return subdomain
    except socket.gaierror:
        return None

def run(domain, wordlist_path="wordlist.txt", silent=False, verbose=False):
    wordlist = load_wordlist(wordlist_path)
    if not wordlist:
        return []

    if verbose and not silent:
        print(f"[*] Loaded {len(wordlist)} words from {wordlist_path} for brute-force enumeration")

    subdomains_to_check = [f"{word}.{domain}" for word in wordlist]

    if verbose and not silent:
        print(f"[*] Checking {len(subdomains_to_check)} brute-force subdomains...")

    live_subdomains = []
    with ThreadPoolExecutor(max_workers=50) as executor:
        results = executor.map(check_subdomain, subdomains_to_check)
        for result in results:
            if result:
                live_subdomains.append(result)

    if verbose and not silent:
        print(f"[+] Found {len(live_subdomains)} live brute-force subdomains")

    return live_subdomains
