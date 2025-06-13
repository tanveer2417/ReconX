# reconx/cli/subdomain_cli.py

import os
from reconx.core import subfinder_py, amass_py, assetfinder_py, sublister_py, bruteforce_py, dnsx_py
from colorama import Fore

def run(args):
    domain = args.domain
    wordlist = args.wordlist
    verbose = args.verbose

    def vprint(msg):
        if verbose:
            print(msg)

    print(Fore.CYAN + f"[+] Starting subdomain enumeration for {domain}\n")

    # Subdomain set
    subdomains = set()

    # Subfinder logic
    vprint("[*] Using internal subfinder logic...")
    vprint("[*] Running Certificate Transparency search via subfinder_py…")
    subdomains.update(subfinder_py.run(domain))

    # Amass logic
    vprint("[*] Using internal amass logic...")
    subdomains.update(amass_py.amass_py(domain))

    # Assetfinder logic
    vprint("[*] Using internal assetfinder logic...")
    vprint("[*] Scraping homepage for subdomains via assetfinder_py…")
    subdomains.update(assetfinder_py.assetfinder_py(domain))

    # Sublister logic
    vprint("[*] Using internal sublister logic...")
    subdomains.update(sublister_py.run(domain))

    # Brute-force
    vprint("[*] Generating brute-force subdomains...")
    subdomains.update(bruteforce_py.bruteforce(domain, wordlist))

    # Probe
    vprint("[*] Probing live subdomains using DNSX logic...")
    live_subs = dnsx_py.probe(subdomains)

    print(Fore.GREEN + f"\n[+] Subdomain enumeration completed for {domain} — {len(live_subs)} live subdomains found.")
    for sub in live_subs:
        print(sub)
