import requests
import re
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from colorama import Fore


def extract_urls(content, base_url):
    soup = BeautifulSoup(content, 'html.parser')
    urls = set()
    for tag in soup.find_all(['a', 'script', 'link', 'img']):
        attr = 'href' if tag.name != 'img' else 'src'
        if tag.has_attr(attr):
            full_url = urljoin(base_url, tag[attr])
            urls.add(full_url)
    return urls

def analyze_js(js_url):
    try:
        r = requests.get(js_url, timeout=5)
        secrets = re.findall(r'(?:api|key|token|secret|pass)[\w-]*\s*[:=]\s*["\']?([A-Za-z0-9\-_]{8,})', r.text)
        if secrets:
            print(Fore.YELLOW + f"  [!] Secrets in {js_url}:")
            for s in secrets:
                print(Fore.RED + f"    - {s}")
    except:
        pass

def detect_cms(content):
    if "wp-content" in content:
        return "WordPress"
    if "Joomla" in content:
        return "Joomla"
    if "Drupal" in content:
        return "Drupal"
    return "Unknown"

def web_analysis_main(args):
    url = f"http://{args.domain}"
    try:
        r = requests.get(url, timeout=5)
        print(Fore.GREEN + f"[+] Live site: {url} ({r.status_code})")
        print(Fore.CYAN + f"[+] CMS: {detect_cms(r.text)}")
        urls = extract_urls(r.text, url)
        print(Fore.BLUE + f"[+] Found {len(urls)} URLs")
        js_urls = [u for u in urls if u.endswith('.js')]
        for js in js_urls:
            analyze_js(js)
    except Exception as e:
        print(Fore.RED + f"[-] Error: {e}")