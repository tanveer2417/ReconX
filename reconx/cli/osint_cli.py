from reconx.core import osint

def run_osint(args):
    print("[DEBUG] Inside run_osint()")  # <-- ADD THIS
    domain = getattr(args, "domain", None)
    ip = getattr(args, "ip", None)
    file = getattr(args, "file", None)

    print(f"[DEBUG] domain: {domain}, ip: {ip}, file: {file}")  # <-- ADD THIS

    if domain and not ip:
        print("[DEBUG] Calling domain-related OSINT functions")  # <-- ADD THIS
        osint.google_dorks(domain)
        osint.github_dorks(domain)
        osint.github_repos(domain)
        osint.get_email_accounts(domain)
        osint.domain_info(domain)
        osint.check_api_leaks(domain)

    if ip and not domain:
        print("[DEBUG] Calling IP info")  # <-- ADD THIS
        osint.ip_info(ip)

    if file:
        print("[DEBUG] Calling metadata extractor")  # <-- ADD THIS
        osint.extract_metadata(file)
