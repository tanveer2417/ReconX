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


def check_tech_stack(headers):
    print(Fore.CYAN + "[+] Technology Stack Fingerprint:")
    server = headers.get('Server', 'Unknown')
    powered = headers.get('X-Powered-By', 'Unknown')
    print(Fore.YELLOW + f"  Server: {server}")
    print(Fore.YELLOW + f"  X-Powered-By: {powered}")


def check_security_headers(headers):
    print(Fore.CYAN + "[+] Security Headers:")
    if 'Content-Security-Policy' not in headers:
        print(Fore.RED + "  Content-Security-Policy not set")
    if 'Strict-Transport-Security' not in headers:
        print(Fore.RED + "  Strict-Transport-Security not set")


def check_forms(content):
    soup = BeautifulSoup(content, 'html.parser')
    forms = soup.find_all('form')
    print(Fore.CYAN + f"[+] Detected {len(forms)} forms:")
    for f in forms:
        action = f.get('action', 'N/A')
        print(Fore.YELLOW + f"  Action: {action}")


def check_common_paths(base_url):
    paths = ["/admin", "/login", "/.git", "/config", "/phpinfo.php"]
    print(Fore.CYAN + "[+] Common Sensitive Paths Check:")
    for path in paths:
        full_url = urljoin(base_url, path)
        try:
            r = requests.get(full_url, timeout=3)
            if r.status_code in [200, 403]:
                print(Fore.YELLOW + f"  [!] {path} ({r.status_code})")
        except:
            continue


def check_broken_links(urls):
    print(Fore.CYAN + "[+] Checking for Broken Links (Status 404):")
    for u in urls:
        try:
            r = requests.head(u, timeout=5, allow_redirects=True)
            if r.status_code == 404:
                print(Fore.RED + f"  [!] Broken: {u}")
        except:
            continue


def web_analysis_main(args):
    url = f"http://{args.domain}"
    try:
        r = requests.get(url, timeout=5)
        print(Fore.GREEN + f"[+] Live site: {url} ({r.status_code})")

        check_tech_stack(r.headers)
        check_security_headers(r.headers)

        print(Fore.CYAN + f"[+] CMS: {detect_cms(r.text)}")

        urls = extract_urls(r.text, url)
        print(Fore.CYAN + f"[+] Found {len(urls)} URLs:")
        for u in urls:
            print(Fore.YELLOW + f"  - {u}")

        js_urls = [u for u in urls if u.endswith('.js')]
        for js in js_urls:
            analyze_js(js)

        check_common_paths(url)
        check_forms(r.text)
        check_broken_links(urls)

    except Exception as e:
        print(Fore.RED + f"[-] Error: {e}")
