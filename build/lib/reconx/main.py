import argparse
import sys
from reconx.cli import subdomain_cli, osint_cli, hosts_cli, web_cli
from colorama import Fore, init
import pyfiglet

# Initialize colorama
init(autoreset=True)

def print_banner():
    banner = pyfiglet.figlet_format("ReconX")
    print(Fore.CYAN + banner)
    print(Fore.GREEN + "Automated OSINT and Recon Tool")
    print(Fore.YELLOW + "Developed by: Mariya Fareed, Ruheena Begum, Tanveer Fatima\n")

def main():
    # Check for --silent before parsing
    silent_mode = "--silent" in sys.argv
    if silent_mode:
        sys.argv.remove("--silent")
    else:
        print_banner()

    parser = argparse.ArgumentParser(
        description="ReconX - A modular recon and OSINT CLI framework",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""Examples:
  reconx subdomain --domain example.com
  reconx osint --domain example.com --ip 8.8.8.8
  reconx hosts --domain example.com
  reconx web --domain example.com
  reconx --silent subdomain --domain example.com
"""
    )

    parser.add_argument(
        "--silent",
        action="store_true",
        help="Suppress banner and informational output"
    )

    subparsers = parser.add_subparsers(dest="command", title="Modules")

    # Subdomain Module
    subdomain_parser = subparsers.add_parser("subdomain", help="Enumerate subdomains using multiple sources")
    subdomain_parser.add_argument("--domain", required=True, help="Target domain for subdomain enumeration")
    subdomain_parser.add_argument("--wordlist", help="Custom wordlist path", default="wordlist.txt")
    subdomain_parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
    subdomain_parser.set_defaults(func=subdomain_cli.run)

    # OSINT Module
    osint_parser = subparsers.add_parser("osint", help="Gather OSINT information from domain/IP/file")
    osint_parser.add_argument("--domain", help="Target domain (e.g., example.com)")
    osint_parser.add_argument("--ip", help="Target IP address (e.g., 8.8.8.8)")
    osint_parser.add_argument("--file", help="File path for metadata extraction")
    osint_parser.set_defaults(func=osint_cli.run_osint)

    # Hosts Module
    hosts_parser = subparsers.add_parser("hosts", help="Enumerate DNS/hosts")
    hosts_parser.add_argument("--domain", required=True, help="Target domain")
    hosts_parser.set_defaults(func=hosts_cli.run)

    # Web Analysis Module
    web_parser = subparsers.add_parser("web", help="Analyze web technologies used by the target")
    web_parser.add_argument("--domain", required=True, help="Target domain")
    web_parser.set_defaults(func=web_cli.run)

    args = parser.parse_args()

    # Add silent and verbose flags to args for use in modules
    setattr(args, "silent", silent_mode)

    if not hasattr(args, "verbose"):
        setattr(args, "verbose", False)

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()
