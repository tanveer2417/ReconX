import requests
import re
from bs4 import BeautifulSoup

def run(domain):
    subdomains = set()

    # ---------- Source 1: ThreatCrowd ----------
    try:
        print("[*] Collecting from ThreatCrowd...")
        r = requests.get(f"https://www.threatcrowd.org/searchApi/v2/domain/report/?domain={domain}", timeout=10)
        if r.status_code == 200:
            data = r.json()
            if "subdomains" in data:
                subdomains.update(data["subdomains"])
    except Exception as e:
        print(f"[!] ThreatCrowd error: {e}")

    # ---------- Source 2: Netcraft ----------
    try:
        print("[*] Collecting from Netcraft...")
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        r = requests.get(f"https://searchdns.netcraft.com/?host={domain}", headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        for link in soup.find_all("a", href=True):
            if domain in link.text and link.text != domain:
                subdomains.add(link.text.strip())
    except Exception as e:
        print(f"[!] Netcraft error: {e}")

    # ---------- Source 3: crt.sh ----------
    try:
        print("[*] Collecting from crt.sh...")
        r = requests.get(f"https://crt.sh/?q=%25.{domain}&output=json", timeout=10)
        if r.status_code == 200:
            entries = r.json()
            for entry in entries:
                name = entry.get("name_value")
                if name and domain in name:
                    for sub in name.split("\n"):
                        sub = sub.strip()
                        if "*" not in sub and sub != domain:
                            subdomains.add(sub)
    except Exception as e:
        print(f"[!] crt.sh error: {e}")

    return list(subdomains)
