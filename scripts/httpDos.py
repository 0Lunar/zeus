import sys, os
sys.path.append('..')

from zeus import *

if __name__ == "__main__":

    os.system("cls||clear")

    ip = str(input("Enter the url to stress: "))

    ns = NetworkStress(ip)
    print("Stressing " + ip)
    ns.http(threads=16,count=10000, method="GET")
    print("Done")
