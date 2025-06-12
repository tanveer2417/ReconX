import requests
import whois
from googlesearch import search
import re

# -------------------------
# 1. GOOGLE DORKS
# -------------------------
def google_dorks(domain):
    dorks = [
        f"site:{domain} intitle:index.of",
        f"site:{domain} inurl:admin",
        f"site:{domain} filetype:sql",
        f"site:{domain} ext:php",
        f"site:{domain} inurl:login"
    ]
    print(f"\n[+] Google Dorks for {domain}")
    for dork in dorks:
        print(f"\n[>] Searching: {dork}")
        try:
            results = search(dork, num_results=5)
            for result in results:
                print(f"  - {result}")
        except Exception as e:
            print(f"[!] Error during search: {e}")

# -------------------------
# 2. GITHUB DORKS (REAL)
# -------------------------
def github_dorks(domain):
    print(f"\n[+] GitHub Dorks for {domain}")
    dorks = [
        f"site:github.com {domain} password",
        f"site:github.com {domain} API_KEY",
        f"site:github.com {domain} token"
    ]
    for dork in dorks:
        print(f"\n[>] Searching: {dork}")
        try:
            results = search(dork, num_results=3)
            for result in results:
                print(f"  - {result}")
        except Exception as e:
            print(f"[!] Error during search: {e}")

def github_repos(domain):
    print(f"\n[+] GitHub Repositories for {domain}")
    try:
        query = f"{domain} in:name"
        results = search(f"site:github.com {query}", num_results=5)
        for result in results:
            print(f"  - {result}")
    except Exception as e:
        print(f"[!] Error during search: {e}")

# -------------------------
# 3. FIND EMAILS (REAL)
# -------------------------
def get_email_accounts(domain):
    print(f"\n[+] Finding email accounts for {domain}")
    try:
        results = search(f"@{domain}", num_results=10)
        emails = set()
        for url in results:
            try:
                page = requests.get(url, timeout=5).text
                found = re.findall(rf"[\w\.-]+@{re.escape(domain)}", page)
                for email in found:
                    emails.add(email)
            except:
                continue
        if emails:
            for email in emails:
                print(f"  - {email}")
        else:
            print("  [-] No emails found.")
    except Exception as e:
        print(f"[!] Error during email search: {e}")

# -------------------------
# 4. DOMAIN INFO (WHOIS)
# -------------------------
def domain_info(domain):
    print(f"\n[+] Domain Info for {domain}")
    try:
        info = whois.whois(domain)
        for key in ["domain_name", "registrar", "creation_date", "expiration_date", "emails"]:
            print(f"{key}: {info.get(key)}")
    except Exception as e:
        print(f"[!] Error fetching WHOIS data: {e}")

# -------------------------
# 5. API LEAKS (Mocked)
# -------------------------
def check_api_leaks(domain):
    print(f"\n[+] Checking API leaks for {domain} (placeholder)")

# -------------------------
# 6. IP INFO (API)
# -------------------------
def ip_info(ip):
    print(f"\n[+] IP Info for {ip}")
    try:
        res = requests.get(f"http://ip-api.com/json/{ip}")
        data = res.json()
        for key in ["query", "country", "regionName", "city", "isp", "org", "timezone"]:
            print(f"{key}: {data.get(key)}")
    except Exception as e:
        print(f"[!] Error fetching IP info: {e}")

# -------------------------
# 7. METADATA (Placeholder)
# -------------------------
def extract_metadata(file_path):
    print(f"\n[+] Extracting metadata from {file_path} (placeholder)")
