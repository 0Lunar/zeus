import sys, os
sys.path.append('..')

from zeus import NetworkScan


if __name__ == "__main__":

    os.system("clear||cls")

    ip = input("Enter the ip to scan => ")

    scanner = NetworkScan(ip)
    scanner.fastScan()

    hosts = scanner.all_hosts()

    for host in hosts:
        print("\n\n\n" + hosts[host] + " (" + host + ")\n\n")
        
        ports = scanner.ports(host)

        if ports:
            for port in ports:
                print("Port: " + str(port) + "\tStatus: " + ports[port]['status'] + "\tService Name: " + ports[port]['name'])

        else:
            print("Port: Not found")
