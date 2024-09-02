
__version__ = "0.1.0"

from .banner import banner
from .NetworkScanner import NetworkScan
from .bruteforce import Bruteforce
from .NetworkStress import NetworkStress
from .Botnet import *


def print_version():
    print(f"Zeus version: {__version__}")