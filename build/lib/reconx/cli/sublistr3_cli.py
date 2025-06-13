import requests
import re
from bs4 import BeautifulSoup


def run(domain):
    print(f"[*] Gathering subdomains using Sublister logic for {domain}")
    found_subdomains = set()

    # 1. DNSDumpster (simulate a request like sublister does)
    try:
        response = requests.get(f"https://dnsdumpster.com", timeout=10)
        if response.status_code == 200:
            csrf_token = re.search(r'name="csrfmiddlewaretoken" value="(.*?)"', response.text).group(1)
            cookies = response.cookies
            headers = {
                'Referer': 'https://dnsdumpster.com/'
            }
            data = {
                'csrfmiddlewaretoken': csrf_token,
                'targetip': domain
            }
            post_resp = requests.post("https://dnsdumpster.com/", data=data, cookies=cookies, headers=headers)
            if post_resp.status_code == 200:
                subdomains = re.findall(r"\b(?:[a-zA-Z0-9_\-]+\.)+" + re.escape(domain) + r"\b", post_resp.text)
                found_subdomains.update(subdomains)
    except Exception as e:
        print(f"[!] DNSDumpster failed: {e}")

    # 2. Search engines (simple Google dorking simulation)
    try:
        query = f"site:{domain} -www"
        google_url = f"https://www.google.com/search?q={query}"
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        res = requests.get(google_url, headers=headers, timeout=10)
        links = re.findall(r"https?://([a-zA-Z0-9_\-.]+\.{domain})", res.text)
        found_subdomains.update(links)
    except Exception as e:
        print(f"[!] Google scraping failed: {e}")

    # 3. Netcraft
    try:
        netcraft_url = f"https://searchdns.netcraft.com/?restriction=site+contains&host={domain}&position=limited"
        res = requests.get(netcraft_url, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        links = soup.find_all("a", href=True)
        for link in links:
            href = link['href']
            if domain in href and not href.startswith("/"):
                sub = href.split("/")[2]
                found_subdomains.add(sub)
    except Exception as e:
        print(f"[!] Netcraft scraping failed: {e}")

    return found_subdomains
