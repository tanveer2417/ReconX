import argparse
from reconx.core import subdomains

def load_wordlist(path="wordlist.txt"):
    try:
        with open(path, "r") as f:
            return [line.strip() for line in f if line.strip()]
    except:
        return ["www", "mail", "ftp", "dev", "test", "admin"]

def run(args):
    wordlist = load_wordlist(args.wordlist)
    results = subdomains.run_subdomain_enum(args.domain, wordlist)

    print(f"\n[+] Subdomain enumeration completed for {args.domain}")
    for sub, data in results.items():
        print(f"\n{sub}")
        print("  DNS Records:", data["dns"])
        if data["tls"]:
            print("  TLS Certificate: Found")
        if data["takeover"]:
            print("  ⚠️ Potential Subdomain Takeover!")