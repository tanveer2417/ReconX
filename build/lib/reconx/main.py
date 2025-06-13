from reconx.cli import subdomain_cli, osint_cli, hosts_cli, web_cli
import argparse

def main():
    parser = argparse.ArgumentParser(description="ReconX: Automated Recon Tool")
    subparsers = parser.add_subparsers(dest="command")

    # Subdomain Module
    subdomain_parser = subparsers.add_parser("subdomain", help="Run Subdomain Enum module")
    subdomain_parser.add_argument("--domain", required=True, help="Target domain")
    subdomain_parser.add_argument("--wordlist", help="Custom wordlist path", default="wordlist.txt")
    subdomain_parser.set_defaults(func=subdomain_cli.run)

    # OSINT Module
    osint_parser = subparsers.add_parser("osint", help="Run OSINT module")
    osint_parser.add_argument("--domain", help="Target domain (e.g., example.com)")
    osint_parser.add_argument("--ip", help="Target IP address (e.g., 8.8.8.8)")
    osint_parser.add_argument("--file", help="File path for metadata extraction (optional)")
    osint_parser.set_defaults(func=osint_cli.run_osint)

    # Hosts Module
    hosts_parser = subparsers.add_parser("hosts", help="Run Hosts module")
    hosts_parser.add_argument("--domain", required=True, help="Target domain")
    hosts_parser.set_defaults(func=hosts_cli.run)

    # Web Analysis Module
    web_parser = subparsers.add_parser("web", help="Run Web Analysis module")
    web_parser.add_argument("--domain", required=True, help="Target domain")
    web_parser.set_defaults(func=web_cli.run)

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()
