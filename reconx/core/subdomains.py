import requests, dns.resolver, socket, ssl, re
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

def passive_enum_all(domain):
    crtsh_subs = set()
    certspotter_subs = set()

    # --- Fetch from crt.sh ---
    try:
        print("[*] Fetching from crt.sh...")
        url = f"https://crt.sh/?q=%25.{domain}&output=json"
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            for entry in data:
                name = entry.get('name_value')
                if name:
                    crtsh_subs.update(name.splitlines())
        else:
            print(f"[!] crt.sh returned status code {resp.status_code}")
    except Exception as e:
        print(f"[!] crt.sh error: {e}")

    # --- Fetch from Certspotter ---
    try:
        print("[*] Fetching from Certspotter...")
        url = f"https://api.certspotter.com/v1/issuances?domain={domain}&include_subdomains=true&expand=dns_names"
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            for entry in data:
                dns_names = entry.get("dns_names", [])
                certspotter_subs.update(dns_names)
        else:
            print(f"[!] Certspotter returned status code {resp.status_code}")
    except Exception as e:
        print(f"[!] Certspotter error: {e}")

    all_subdomains = crtsh_subs.union(certspotter_subs)
    clean_subdomains = {sub.lower().strip() for sub in all_subdomains if domain in sub.lower()}
    
    return sorted(clean_subdomains)


def dns_noerror_enum(domain, wordlist):
    found = []
    for sub in wordlist:
        subdomain = f"{sub}.{domain}"
        try:
            socket.gethostbyname(subdomain)
            found.append(subdomain)
        except socket.gaierror:
            continue
    return found

def bruteforce_enum(domain, wordlist):
    return dns_noerror_enum(domain, wordlist)

def resolve_dns(subdomain):
    records = {}
    try:
        for rtype in ['A', 'AAAA', 'MX', 'TXT', 'NS']:
            answers = dns.resolver.resolve(subdomain, rtype, lifetime=2)
            records[rtype] = [str(r.to_text()) for r in answers]
    except:
        pass
    return records

def tls_handshake_enum(subdomain):
    context = ssl.create_default_context()
    try:
        with socket.create_connection((subdomain, 443), timeout=3) as sock:
            with context.wrap_socket(sock, server_hostname=subdomain) as ssock:
                return ssock.getpeercert()
    except:
        return None

def extract_subs_from_html(domain):
    found = set()
    try:
        resp = requests.get(f"https://{domain}", timeout=5)
        soup = BeautifulSoup(resp.text, "html.parser")
        scripts = soup.find_all("script", {"src": True})
        for tag in scripts:
            src = tag['src']
            found.update(re.findall(rf"([\w.-]+\.{domain})", src))
    except:
        pass
    return list(found)

def zone_transfer_check(domain):
    try:
        ns = dns.resolver.resolve(domain, 'NS')
        for server in ns:
            try:
                zt = dns.query.xfr(str(server), domain)
                return [str(r) for r in zt]
            except:
                continue
    except:
        return []

def subdomain_takeover_check(subdomain):
    try:
        r = requests.get(f"http://{subdomain}", timeout=4)
        if "There is no such app" in r.text or "NoSuchBucket" in r.text:
            return True
    except:
        pass
    return False

def recursive_search(domain, wordlist, depth=1):
    subs = set(passive_enum_all(domain))
    for _ in range(depth):
        new_subs = set()
        for sub in subs:
            new_subs.update(passive_enum_all(sub))
        subs.update(new_subs)
    return list(subs)

def run_subdomain_enum(domain, wordlist):
    print(f"[+] Starting subdomain enumeration for {domain}")
    subs = set()

    subs.update(passive_enum_all(domain))
    subs.update(bruteforce_enum(domain, wordlist))
    subs.update(extract_subs_from_html(domain))
    subs.update(recursive_search(domain, wordlist, depth=1))

    detailed_results = {}

    with ThreadPoolExecutor(max_workers=20) as executor:
        future_to_sub = {executor.submit(resolve_dns, sub): sub for sub in subs}
        for future in future_to_sub:
            sub = future_to_sub[future]
            records = future.result()
            if records:
                detailed_results[sub] = {
                    "dns": records,
                    "tls": tls_handshake_enum(sub),
                    "takeover": subdomain_takeover_check(sub)
                }

    return detailed_results
