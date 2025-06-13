import requests
import re
from bs4 import BeautifulSoup
from colorama import Fore

def run(domain, silent=False, verbose=False):
    result = set()
    
    if verbose and not silent:
        print(Fore.BLUE + "[*] Scraping homepage for subdomains via assetfinder_py…")

    try:
        r = requests.get(f"https://{domain}", timeout=5)
        urls = re.findall(r"[a-zA-Z0-9.-]+\." + re.escape(domain), r.text)
        result.update(urls)
    except Exception as e:
        if verbose and not silent:
            print(Fore.RED + f"[!] assetfinder_py error: {e}")
    
    return sorted(result)
