import os

def load_wordlist(path="wordlist.txt"):
    try:
        with open(path, "r") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"[!] Wordlist file not found at {path}, using default list.")
        return ["www", "mail", "ftp", "dev", "test", "admin"]

def run(args):
    # 🔄 Delayed import to avoid circular import error
    from reconx.core import subdomains

    wordlist = load_wordlist(args.wordlist)
    results = subdomains.run_subdomain_enum(args.domain, wordlist)

    print(f"\n[+] Subdomain enumeration completed for {args.domain}")
    for sub, data in results.items():
        print(f"\n{sub}")
        print("  DNS Records:", data.get("dns", {}))
        if data.get("tls"):
            print("  TLS Certificate: Found")
        if data.get("takeover"):
            print("  ⚠️ Potential Subdomain Takeover!")
