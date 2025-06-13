import requests
from bs4 import BeautifulSoup
from colorama import Fore

def find_from_ct(domain):
    subs = set()
    url = f"https://crt.sh/?q=%25.{domain}"
    try:
        r = requests.get(url, timeout=50)  # ⬅️ Increased timeout from 10 to 20
        if r.ok:
            soup = BeautifulSoup(r.text, 'html.parser')
            for td in soup.select('td[colspan="2"]'):
                text = td.text.strip()
                if text.endswith(f'.{domain}'):
                    subs.add(text)
    except requests.exceptions.ReadTimeout:
        print(Fore.RED + f"[!] Timeout while connecting to crt.sh for {domain}")
    except Exception as e:
        print(Fore.RED + f"[!] Error in crt.sh request: {e}")
    return subs

def run(domain):
    print(Fore.BLUE + "[*] Running Certificate Transparency search...")
    return sorted(find_from_ct(domain))
