import urllib3
from urllib.parse import urlencode
import socket
from concurrent.futures import ThreadPoolExecutor
import threading
import os
import logging


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:116.0) Gecko/20100101 Firefox/116.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}


class NetworkStress:
    def __init__(self, host: str, port: int = None):
        self.host = host
        self.port = port
        self.sent = 0
        self.lock = threading.Lock()

    def _sendUdp(self, count: int, Bytes: int, packet_count: int):
        """ Send UDP packets until it reaches the maximum number of packets set """

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        while True:
            with self.lock:
                if self.sent >= count:
                    break
                self.sent += 1
                current_sent = self.sent

            s.sendto(os.urandom(Bytes), (self.host, self.port))

            if packet_count > 0 and current_sent % packet_count == 0:
                print(f"Packet sent: {current_sent}")


    def udp(self, threads: int = 16, count: int = 10000, Bytes: int = 64, packet_count : int = -1):
        """ Start the UDP stress process """

        with ThreadPoolExecutor(max_workers=threads) as executor:
            for _ in range(threads):
                executor.submit(self._sendUdp, count, Bytes, packet_count)
        

    def _sendTcp(self, count: int, Bytes: int, packet_count: int):
        """ send TCP packets until it reaches the maximum number of packets set """

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(10)

        try:
            s.connect((self.host, self.port))

            while self.sent < count:
                s.send(os.urandom(Bytes))
                self.sent += 1

                if packet_count > 0 and self.sent % packet_count == 0:
                    print("Packet sent: " + str(self.sent))
            
            self.sent = 0
        
        except socket.gaierror:
            logging.error("Name or service not known")
        
        except TimeoutError:
            logging.error("TimeoutError")
        
        except OSError:
            logging.error("Network is unreachable")
        
    def tcp(self, threads : int = 16, count: int = 10000, Bytes: int = 64, packet_count: int = -1):
        """ Start the TCP stress process """

        with ThreadPoolExecutor(max_workers=threads) as executor:
            for _ in range(threads):
                executor.submit(self._sendTcp, count, Bytes, packet_count)


    def _checkUrl(self):
        """ Check if the url is valid checking the protocol (http:// or https://) """

        if self.host.startswith("https://") == False and self.host.startswith("http://") == False:
            return False
        
        try:
            hostname = self.host.split("://")[1].split("/")[0]
            socket.gethostbyname(hostname)
            
            return True

        except socket.gaierror:
            return False
        
        except Exception as e:
            logging.ERROR(e)


    @staticmethod
    def _checkContentType(ContentType: str, body):
        """ Check if the Content-Type is valid """

        dataTypes = {'application/json': dict, 'application/x-www-form-urlencoded': str, 'text/plain': bytes}

        if ContentType not in dataTypes:
            return False
    
        if type(body) != dataTypes[ContentType]:
            if dataTypes[ContentType] == "application/x-www-form-urlencoded" and type(body) == dict:
                body = urlencode(body)
            
            else:
                return False

        return body

    
    def _sendHttp(self, body, count: int, method: str, packet_count: int, ContentType: str):
        """ send HTTP requests until it reaches the maximum number of packets set """

        http = urllib3.PoolManager()

        try:
            while self.sent < count:

                if body != None:
                    url = self.host + ":" + str(self.port)
                    http.request(method, url, headers=headers, body=body)

                else:
                    http.request(method, self.host, headers=headers)

                self.sent += 1

                if packet_count > 0 and self.sent % packet_count == 0:
                    print("Packet sent: " + str(self.sent))

        except urllib3.exceptions.NewConnectionError as e:
            logging.error("Failed to establish a new connection:", e)

        except urllib3.exceptions.TimeoutError as e:
            logging.error("Connection timed out:", e)
        
        except urllib3.exceptions.ConnectionError as e:
            logging.error("A connection error occurred:", e)

        except urllib3.exceptions.SSLError as e:
            logging.error("Error validating the SSL/TLS certificate: ", e)


    def http(self, ContentType: str = "application/json", body = None, threads : int = 16, count: int = 10000, method: str = "GET", packet_count: int = -1):
        """ Start the HTTP stress process """

        if body != None:
            body = self._checkContentType(ContentType, body)

        if body == False:
            logging.error("Body/Content-Type Error")

        elif self._checkUrl() == False:
            logging.error("Invalid URL")

        else:
            if self.port == None:
                if self.host.startswith("http://"):
                    self.port = 80
                else:
                    self.port = 443

            with ThreadPoolExecutor(max_workers=threads) as executor:
                for _ in range(threads):
                    executor.submit(self._sendHttp, body, count, method, packet_count, ContentType)