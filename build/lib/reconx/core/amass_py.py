import requests
from bs4 import BeautifulSoup
from colorama import Fore

PUBLIC_SOURCES = [
    ("mozilla", "https://monitor.firefox.com/domain/{d}"),
    ("archive", "https://web.archive.org/cite/{d}"),
]

def run(domain, silent=False, verbose=False):
    subs = set()
    
    for name, url_tpl in PUBLIC_SOURCES:
        if verbose and not silent:
            print(Fore.BLUE + f"[*] Checking {name} ...")
        
        try:
            r = requests.get(url_tpl.format(d=domain), timeout=10)
            if r.ok:
                soup = BeautifulSoup(r.text, 'html.parser')
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    if href.endswith(f".{domain}"):
                        subs.add(href)
        except Exception as e:
            if verbose and not silent:
                print(Fore.RED + f"[!] Error fetching from {name}: {e}")

    return sorted(subs)
