import requests, dns.resolver, socket, ssl, re
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

def passive_enum_crt(domain):
    url = f"https://crt.sh/?q=%25.{domain}&output=json"
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200 and resp.text.strip():
            try:
                return sorted({entry['name_value'] for entry in resp.json()})
            except ValueError:
                print(f"[!] crt.sh returned invalid JSON for {domain}")
                return []
        else:
            print(f"[!] crt.sh returned empty or invalid response for {domain}")
            return []
    except requests.exceptions.Timeout:
        print(f"[!] crt.sh request timed out for {domain}")
    except requests.exceptions.RequestException as e:
        print(f"[!] crt.sh error: {e}")
    return []

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
    except Exception:
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
            found.update(re.findall(rf"([\w.-]+\.{re.escape(domain)})", src))
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
    subs = set(passive_enum_crt(domain))
    for _ in range(depth):
        new_subs = set()
        for sub in subs.copy():
            if sub != domain and domain in sub:
                new_subs.update(passive_enum_crt(sub))
        subs.update(new_subs)
    return list(subs)

def run_subdomain_enum(domain, wordlist):
    print(f"[+] Starting subdomain enumeration for {domain}")
    subs = set()

    subs.update(passive_enum_crt(domain))
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
