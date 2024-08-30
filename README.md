![Logo](./img/output.png)

# Zeus

**Zeus** is a penetration testing framework written in Python, designed to facilitate security testing activities such as network scanning and brute force attacks. The project is currently under active development, with plans to continuously expand the available features.

## Features

- **Network Scanning:** Uses `python-nmap` to perform network scans, identifying active hosts, open ports, and running services.
- **Bruteforce:** Implements brute force attacks on various protocols and services, leveraging libraries like `paramiko` for SSH and `ftplib` for FTP.
- **Network Stress:** Implements Network Stress attacks on Various protocols using the socket library for TCP/IP and UDP, and urllib3 for HTTP/HTTPS 

## Libraries Used

Zeus leverages the following Python libraries:

- [python-nmap](https://pypi.org/project/python-nmap/): A wrapper for Nmap, useful for performing network scans.
- [requests](https://pypi.org/project/requests/): A simple and powerful HTTP library used for making web requests.
- [colorama](https://pypi.org/project/colorama/): Provides terminal text coloring support, improving user interface readability.
- [paramiko](https://pypi.org/project/paramiko/): A Python SSHv2 implementation, used for secure remote server access.
- [ftplib](https://docs.python.org/3/library/ftplib.html): A standard Python library for interacting with FTP servers.

## Project Status

The framework is currently in the **development** phase. It currently includes basic functionality for network scanning, brute force attacks and network stressing, with plans to significantly expand the feature set in the future.

## Requirements

Ensure you have Python 3.6 or higher installed. You can install the necessary dependencies by running:

```bash
pip install -r requirements.txt
```

## Installation

1. Clone the repository

```bash
git clone https://github.com/0luna/zeus.git
```

2. Navigate to the project directory:

```bash
cd zeus
```

3. Install the dependencies:

```bash
pip install -r requirements.txt
```

*Note: Zeus is intended for educational and research purposes in security. The authors are not responsible for any misuse of this tool. Use Zeus only on systems for which you have legal authorization to test.*