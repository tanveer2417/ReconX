import requests
import re
from bs4 import BeautifulSoup
from colorama import Fore

def find_from_ct(domain):
    subs = set()
    url = f"https://crt.sh/?q=%25.{domain}"
    r = requests.get(url, timeout=10)
    if r.ok:
        soup = BeautifulSoup(r.text, 'html.parser')
        for td in soup.select('td[colspan="2"]'):
            text = td.text.strip()
            if text.endswith(f'.{domain}'):
                subs.add(text)
    return subs

def subfinder_py(domain):
    print(Fore.BLUE + "[*] Running Certificate Transparency search...")
    return sorted(find_from_ct(domain))
