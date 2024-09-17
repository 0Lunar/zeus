![Logo](./img/output.png)

# Zeus

**Zeus** is a penetration testing framework written in Python, designed to facilitate security testing activities such as network scanning and brute force attacks. The project is currently under active development, with plans to continuously expand the available features.

## Features

- **Botnet**
- **Bruteforce**
- **Fuzzer**
- **Network Scanner**
- **Network Stresser**
- **Vulnerability Scanner**

## Libraries Used

Zeus leverages the following Python libraries:

- [python-nmap](https://pypi.org/project/python-nmap/): A wrapper for Nmap, useful for performing network scans.
- [requests](https://pypi.org/project/requests/): A simple and powerful HTTP library used for making web requests.
- [colorama](https://pypi.org/project/colorama/): Provides terminal text coloring support, improving user interface readability.
- [paramiko](https://pypi.org/project/paramiko/): A Python SSHv2 implementation, used for secure remote server access.
- [ftplib](https://docs.python.org/3/library/ftplib.html): A standard Python library for interacting with FTP servers.

## Project Status

The framework is currently in the **development** phase. It currently includes basic functionality.

## Requirements

Ensure you have Python 3.8 or higher installed. You can install the necessary dependencies by running:

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

4. run the setup

```bash
python3 setup.py install
```

*Note: Zeus is intended for educational and research purposes in security. The authors are not responsible for any misuse of this tool. Use Zeus only on systems for which you have legal authorization to test.*