import requests
import re
from bs4 import BeautifulSoup
from colorama import Fore

def assetfinder_py(domain):
    print(Fore.BLUE + "[*] Scraping homepage for subdomains…")
    result = set()
    try:
        r = requests.get(f"https://{domain}", timeout=5)
        urls = re.findall(r"[a-zA-Z0-9.-]+\\." + re.escape(domain), r.text)
        result.update(urls)
    except:
        pass
    return sorted(result)
