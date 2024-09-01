import sys, os
sys.path.append('..')

from zeus import *

if __name__ == "__main__":

    os.system("cls||clear")

    ip = str(input("Enter the host to stress: "))

    ns = NetworkStress(ip, 80)
    print("Stressing " + ip)
    ns.udp(threads=16,count=1000000, Bytes=512,packet_count=10)
    print("Done")
