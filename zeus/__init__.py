
__version__ = "0.1.0"

from .NetworkScanner import NetworkScan
from .bruteforce import Bruteforce
from .NetworkStress import NetworkStress
from .Botnet import *
from .VulnScanner import VulnScanner


def print_version():
    print(f"Zeus version: {__version__}")