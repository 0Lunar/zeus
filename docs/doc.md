# ZEUS

Zeus is a python framework wich help you performing penetration test.
it allows you to easly perform various attacks like Network Scan with nmap, Bruteforce attacks 
with http/https, ssh and ftp protocols, and Network Stress with TCP/IP, UDP and HTTP/HTTPS.


# Quickstart

First, make sure you have installer the requirements:
- colorama
- python-nmap
- requests
- urllib3
- paramiko
- ftplib

Let’s get started with some simple examples.:
- [Network Scan](#network-scan)
- [Bruteforce](#bruteforce)
- [Network Stress](#network-stress)

## Network Scan

First import NetowkScan from zeus

```python
from zeus import NetworkScan
```

Create a variable with the host you want to scan, for example `192.168.1.1`

```python
ns = NetworkScan("192.168.1.1")
```

Start a standard scan

```python
ns.standardScan()
```

Now let's get the open ports

```python
open_ports = ns.ports()
```

This function will return all the open ports in json:

```json
{port: {"status": "open/filtered/closed", "name": "Service Name"}}
```

We can also get all the hostnames scanned, in this case the router hostname:

```python
hostnames = ns.all_hostnames()
```

This function will return all the hostnames in a list:

`hostnames -> ['exampleRouter-1.0.0']`

If you need the ip address associated with the hostname you can use the funcion `all_hosts()`

```python
hosts = ns.all_hosts()
```

This function will return all the hosts ip with their hostname in json
example:

`hosts -> {"192.168.1.1": "exampleRouter-1.0.0"}`

This is an example of a port scanning on a local network:

```python
from zeus import NetworkScan


if __name__ == "__main__":

    os.system("clear||cls")

    scanner = NetworkScan("192.168.1.1")
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

```

## Bruteforce

First import Bruteforce from zeus

```python
from zeus import Bruteforce
```

Create a variable with the host you want to attack, the usernames and the wordlist

```python
users = open("users.txt", "rt").read().splitlines()
wordlist = open("wordlist.txt", "rt").read().splitlines()

br = Bruteforce("example.com", users, wordlists)
```

You can also use one single username but you have to use a list:

```python
user = ['anonymous']
wordlist = open("wordlist.txt", "rt").read().splitlines()

br = Bruteforce("example.com", user, wordlists)
```

Now you can chose the attack protocol:
- [SSH](#ssh-attack)
- [FTP](#ftp-attack)
- [HTTP/HTTPS](#http-attack)

*note: if you have to perform a http brutefroce you have to put the protocol on the host*

example:

```python
br = Bruteforce("https://example.com", users, wordlist)
```
---
### ssh attack

```python3
result = br.ssh()
```

### ftp attack

```python3
result = br.ftp()
```

### http attack

```python3
result = br.http()
```
---

You can choose to wait the results in json or you can print immediately the results using the pram `printSuccess = True`

```python3
br.http(printSuccess=True)
```

## Network Stress

First import NetworkStress from zeus

```python3
from zeus import NetworkStress
```

create a variable with the host and port wou want to stress

```python3
ns = NetworkStress("192.168.1.1", 53) # 53 is a open port on the modem for dns
```

*Note: if you have to perform a HTTP/HTTPS stress, you have to put the protocol con the host and you can avoid inserting the port*

example:

```python3
ns = NetworkStress("http://192.168.1.1") # NetworkStress will directly set the port to 80
```

Now you can chose the attack protocol:
- [UDP](#udp-stress)
- [TCP/IP](#tcpip-stress)
- [HTTP/HTTPS](#http-stress)

---

### UDP Stress

*Note: count is used to specify how many packets to send; packet count is used to print every 1000 packet the number of packet sent, if you use -1 it will not print the packet sent but only perform the stress*


```python
ns.udp(count=100000, packet_count=1000)
```

### TCP/IP Stress

```python
ns.tcp(count=100000, packet_count=1000)
```

### HTTP Stress

```python
ns.http(count=100000, packet_count=1000)
```