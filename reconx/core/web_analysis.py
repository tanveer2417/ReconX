import requests
import re
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from colorama import Fore, init

init(autoreset=True)

def extract_urls(content, base_url):
    soup = BeautifulSoup(content, 'html.parser')
    urls = set()
    for tag in soup.find_all(['a', 'script', 'link', 'img']):
        attr = 'href' if tag.name != 'img' else 'src'
        if tag.has_attr(attr):
            full_url = urljoin(base_url, tag[attr])
            urls.add(full_url)
    return soup, urls

def analyze_js(js_url):
    try:
        r = requests.get(js_url, timeout=5)
        secrets = re.findall(
            r'(?:api|key|token|secret|pass)[\w-]*\s*[:=]\s*["\']?([A-Za-z0-9\-_]{8,})',
            r.text, re.IGNORECASE
        )
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

def check_security_headers(headers):
    print(Fore.YELLOW + "[+] Security Headers:")
    required = [
        "Content-Security-Policy", "Strict-Transport-Security",
        "X-Frame-Options", "X-Content-Type-Options"
    ]
    for h in required:
        if h in headers:
            print(Fore.GREEN + f"  {h}: {headers[h]}")
        else:
            print(Fore.RED + f"  {h} not set")

def fingerprint_tech(headers, content):
    print(Fore.YELLOW + "[+] Technology Stack Fingerprint:")
    server = headers.get("Server", "Unknown")
    x_powered = headers.get("X-Powered-By", "Unknown")
    print(Fore.CYAN + f"  Server: {server}")
    print(Fore.CYAN + f"  X-Powered-By: {x_powered}")
    if "google-analytics.com" in content or "UA-" in content:
        print(Fore.MAGENTA + "  Google Analytics Detected")
    if "googletagmanager.com" in content:
        print(Fore.MAGENTA + "  Google Tag Manager Detected")

def check_common_paths(base_url):
    print(Fore.YELLOW + "[+] Common Sensitive Paths Check:")
    common_paths = ["admin", "login", "config", ".git", ".env"]
    for path in common_paths:
        test_url = urljoin(base_url + "/", path)
        try:
            r = requests.get(test_url, timeout=3)
            if r.status_code == 200:
                print(Fore.RED + f"  [!] Accessible: {test_url}")
        except:
            pass

def detect_forms(soup):
    forms = soup.find_all("form")
    if forms:
        print(Fore.YELLOW + f"[+] Detected {len(forms)} forms:")
        for f in forms:
            print(Fore.GREEN + f"  Action: {f.get('action', 'N/A')}")
    else:
        print(Fore.BLUE + "[*] No forms detected.")

def check_broken_links(urls):
    print(Fore.YELLOW + "[+] Checking for Broken Links (Status 404):")
    for u in urls:
        try:
            r = requests.head(u, timeout=3)
            if r.status_code == 404:
                print(Fore.RED + f"  [!] Broken: {u}")
        except:
            pass

def web_analysis_main(args):
    url = f"http://{args.domain}"
    try:
        r = requests.get(url, timeout=5)
        print(Fore.GREEN + f"[+] Live site: {url} ({r.status_code})")
        fingerprint_tech(r.headers, r.text)
        check_security_headers(r.headers)
        print(Fore.CYAN + f"[+] CMS: {detect_cms(r.text)}")

        soup, urls = extract_urls(r.text, url)
        print(Fore.BLUE + f"[+] Found {len(urls)} URLs")

        js_urls = [u for u in urls if u.endswith('.js')]
        for js in js_urls:
            analyze_js(js)

        check_common_paths(url)
        detect_forms(soup)
        check_broken_links(urls)

    except Exception as e:
        print(Fore.RED + f"[-] Error: {e}")
