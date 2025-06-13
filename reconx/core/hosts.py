import requests
import socket
import json
from colorama import Fore


def get_ip_info(ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}")
        return response.json()
    except:
        return {}

def detect_cdn(ip_info):
    cdn_providers = ['Cloudflare', 'Akamai', 'Fastly', 'Incapsula']
    if ip_info.get("org"):
        for cdn in cdn_providers:
            if cdn.lower() in ip_info["org"].lower():
                return cdn
    return "No CDN Detected"

def detect_waf(domain):
    try:
        headers = requests.get(f"http://{domain}", timeout=5).headers
        for k, v in headers.items():
            if 'waf' in k.lower() or 'waf' in v.lower():
                return f"WAF Detected: {k}: {v}"
        return "No obvious WAF"
    except:
        return "Error detecting WAF"

def hosts_main(args):
    ip = socket.gethostbyname(args.domain)
    print(Fore.GREEN + f"[+] Resolved IP: {ip}")

    info = get_ip_info(ip)
    print(Fore.YELLOW + json.dumps(info, indent=2))

    cdn = detect_cdn(info)
    print(Fore.CYAN + f"[+] CDN: {cdn}")

    waf = detect_waf(args.domain)
    print(Fore.MAGENTA + f"[+] WAF: {waf}")