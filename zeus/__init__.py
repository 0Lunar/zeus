
__version__ = "0.1.0"

from .Botnet import *
from .Bruteforce import Bruteforce
from .Fuzzer import Fuzzer
from .NetworkScanner import NetworkScan
from .NetworkStress import NetworkStress
#from .VulnScanner import VulnScanner	(under development)


def print_version():
    print(f"Zeus version: {__version__}")
