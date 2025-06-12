import argparse
from reconx.cli.osint_cli import run_osint

def main():
    print("Running main.py")
    parser = argparse.ArgumentParser(
        prog='reconx',
        description='ReconX - OSINT & Recon Automation Tool'
    )

    parser.add_argument("-m", "--module", help="Module to run: osint", required=True)
    parser.add_argument("--domain", help="Target domain (e.g., example.com)")
    parser.add_argument("--ip", help="Target IP address (e.g., 8.8.8.8)")
    parser.add_argument("--file", help="File path for metadata extraction (optional)")

    args = parser.parse_args()
    print(f"Args received: {args}")
    print("Calling run_osint...")

    if args.module == "osint":
        if not (args.domain or args.ip or args.file):
            parser.error("For module 'osint', provide at least one of --domain, --ip, or --file")
        run_osint(args)
    else:
        print(f"Unknown module: {args.module}")
        parser.print_help()
