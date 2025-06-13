import requests
import whois
from googlesearch import search
from termcolor import colored
from tabulate import tabulate
import re
from bs4 import BeautifulSoup
import urllib.request
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# -------------------------
# 1. GOOGLE DORKS
# -------------------------
def google_dorks(domain):
    dorks = [
        f"site:{domain} intitle:index.of",
        f"site:{domain} inurl:admin",
        f"site:{domain} filetype:sql",
        f"site:{domain} ext:php",
        f"site:{domain} inurl:login",
        f"site:{domain} ext:env",
        f"site:{domain} ext:log",
        f"site:{domain} ext:json"
    ]
    print(colored(f"\n[+] Google Dorks for {domain}", "cyan"))
    for dork in dorks:
        print(colored(f"\n[>] Searching: {dork}", "yellow"))
        try:
            results = search(dork, num_results=5)
            for result in results:
                print(colored(f"  - {result}", "green"))
        except Exception as e:
            print(colored(f"[!] Error during search: {e}", "red"))

# -------------------------
# 2. GITHUB DORKS (Live via Google)
# -------------------------
def github_dorks(domain):
    dork = f"site:github.com {domain} password"
    print(colored(f"\n[+] GitHub Dorks for {domain}", "cyan"))
    try:
        results = search(dork, num_results=5)
        for result in results:
            print(colored(f"  - {result}", "green"))
    except Exception as e:
        print(colored(f"[!] Error: {e}", "red"))

def github_repos(domain):
    dork = f"site:github.com {domain}"
    print(colored(f"\n[+] GitHub Repositories for {domain}", "cyan"))
    try:
        results = search(dork, num_results=5)
        for result in results:
            print(colored(f"  - {result}", "green"))
    except Exception as e:
        print(colored(f"[!] Error: {e}", "red"))

# -------------------------
# 3. FIND EMAILS
# -------------------------
def get_email_accounts(domain):
    print(colored(f"\n[+] Finding email accounts for {domain}", "cyan"))
    dork = f"{domain} email contact"
    try:
        results = search(dork, num_results=3)
        found_emails = set()
        for url in results:
            try:
                html = urllib.request.urlopen(url).read().decode("utf-8", errors="ignore")
                emails = re.findall(r"[\w\.-]+@[\w\.-]+", html)
                found_emails.update(emails)
            except:
                continue
        if found_emails:
            print(tabulate([[e] for e in found_emails], headers=["Emails"], tablefmt="fancy_grid"))
        else:
            print(colored("No emails found.", "yellow"))
    except Exception as e:
        print(colored(f"[!] Error: {e}", "red"))

# -------------------------
# 4. DOMAIN INFO (WHOIS)
# -------------------------
def domain_info(domain):
    print(colored(f"\n[+] Domain Info for {domain}", "cyan"))
    try:
        info = whois.whois(domain)
        data = [(key, info.get(key)) for key in ["domain_name", "registrar", "creation_date", "expiration_date", "emails"]]
        print(tabulate(data, headers=["Field", "Value"], tablefmt="fancy_grid"))
    except Exception as e:
        print(colored(f"[!] Error fetching WHOIS data: {e}", "red"))

# -------------------------
# 5. API LEAKS DORKS
# -------------------------
def check_api_leaks(domain):
    print(colored(f"\n[+] Checking API leaks for {domain}", "cyan"))
    dorks = [
        f"site:pastebin.com {domain} api_key",
        f"site:trello.com {domain} password",
        f"site:gitlab.com {domain} token"
    ]
    for dork in dorks:
        print(colored(f"\n[>] Searching: {dork}", "yellow"))
        try:
            results = search(dork, num_results=5)
            for result in results:
                print(colored(f"  - {result}", "green"))
        except Exception as e:
            print(colored(f"[!] Error during API dork search: {e}", "red"))

# -------------------------
# 6. IP INFO (API)
# -------------------------
def ip_info(ip):
    print(colored(f"\n[+] IP Info for {ip}", "cyan"))
    try:
        res = requests.get(f"http://ip-api.com/json/{ip}")
        data = res.json()
        table = [(k, data.get(k)) for k in ["query", "country", "regionName", "city", "isp", "org", "timezone"]]
        print(tabulate(table, headers=["Field", "Value"], tablefmt="fancy_grid"))
    except Exception as e:
        print(colored(f"[!] Error fetching IP info: {e}", "red"))

# -------------------------
# 7. SCREENSHOT SAVING (SEPARATE DIR)
# -------------------------
def save_screenshot(domain):
    print(colored(f"\n[+] Saving screenshot of {domain}", "cyan"))
    try:
        options = Options()
        options.headless = True
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(options=options)
        url = f"http://{domain}"
        driver.set_window_size(1920, 1080)
        driver.get(url)
        os.makedirs("screenshots", exist_ok=True)
        filepath = f"screenshots/{domain}.png"
        driver.save_screenshot(filepath)
        print(colored(f"[+] Screenshot saved to {filepath}", "green"))
        driver.quit()
    except Exception as e:
        print(colored(f"[!] Error saving screenshot: {e}", "red"))

# -------------------------
# 8. SHODAN API (Dynamic key passed in)
# -------------------------
def shodan_lookup(ip, shodan_key):
    print(colored(f"\n[+] Shodan Lookup for {ip}", "cyan"))
    try:
        url = f"https://api.shodan.io/shodan/host/{ip}?key={shodan_key}"
        res = requests.get(url)
        data = res.json()
        fields = ["ip_str", "org", "os", "isp", "country_name", "city", "last_update"]
        table = [(k, data.get(k)) for k in fields if k in data]
        print(tabulate(table, headers=["Field", "Value"], tablefmt="fancy_grid"))
    except Exception as e:
        print(colored(f"[!] Error fetching Shodan data: {e}", "red"))

# -------------------------
# 9. METADATA (Placeholder)
# -------------------------
def extract_metadata(file_path):
    print(colored(f"\n[+] Extracting metadata from {file_path} (placeholder)", "cyan"))
