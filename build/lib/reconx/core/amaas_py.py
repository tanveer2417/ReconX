import requests
from bs4 import BeautifulSoup
from colorama import Fore

PUBLIC_SOURCES = [
    ("mozilla", "https://monitor.firefox.com/domain/{d}"),
    ("archive", "https://web.archive.org/cite/{d}"),
]

def amass_py(domain):
    subs = set()
    for name, url_tpl in PUBLIC_SOURCES:
        print(Fore.BLUE + f"[*] Checking {name} ...")
        try:
            r = requests.get(url_tpl.format(d=domain), timeout=10)
            if r.ok:
                for link in BeautifulSoup(r.text, 'html.parser').find_all('a', href=True):
                    href = link['href']
                    if href.endswith(f".{domain}"):
                        subs.add(href)
        except:
            pass
    return sorted(subs)
