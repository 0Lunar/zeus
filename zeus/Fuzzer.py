import requests
import socket
import threading
import os
import logging
import json


class Fuzzer:
    def __init__(self) -> None:
        self.lock = threading.Lock()
        self.event = threading.Event()
        self.wordlist = None
        self.found = []
    

    def urlFuzzer(self, url: str, wordlist: str, method: str = "GET", responses: list = [200], fsize: int = None, threads: int = 16, proxies: dict = None, timeout: int | float = 10, verify: bool = True):

        self.found.clear()

        if url.startswith("https://") == False and url.startswith("http://") == False:
            raise ValueError(f"Invalid url: {url}")
        
        if os.path.isfile(wordlist):
            self.wordlist = open(wordlist, "rt")
        
        else:
            raise FileNotFoundError(f"Word list not found: {wordlist}")

        for i in range(threads):
            th = threading.Thread(target=self._fuzzURL, args=(url, method, responses, fsize, proxies, timeout))
            th.start()

        self.event.wait()
        self.event.clear()
        self.wordlist.close()
        
        return self.found

    
    def _fuzzURL(self, url: str, method: str = "GET", responses: list = [200], fsize: int = None, proxies: dict = None, timeout: int | float = 10, verify: bool = True):
        word = None
        
        while word != "":
            self.lock.acquire()
            word = self.wordlist.readline()[:-1]
            self.lock.release()

            try:
                r = requests.request(method, url + "/" + word, proxies=proxies, timeout=timeout, verify=verify)

            except Exception as e:
                logging.error(e)

            if r.status_code in responses:
                self.lock.acquire()
                if fsize:
                    if fsize != len(r.content):
                        self.found.append(word)
                
                else:
                    self.found.append(word)
                
                self.lock.release()

        self.event.set()

    
    def subdomainFuzzer(self, domain: str, wordlist: str, threads: int = 16):
        self.found.clear()

        #check if the domain exist
        socket.gethostbyname(domain)

        if os.path.isfile(wordlist):
            self.wordlist = open(wordlist, "rt")

        else:
            raise FileNotFoundError(f"Wordlist not found: {wordlist}")

        for i in range(threads):
            th = threading.Thread(target=self._fuzzSub, args=(domain,))
            th.start()

        self.event.wait()
        self.event.clear()
        self.wordlist.close()
        
        return self.found

    
    def _fuzzSub(self, domain: str):
        word = None
        
        while word != "":
            self.lock.acquire()
            word = self.wordlist.readline()[:-1]
            self.lock.release()

            if word != "":
                try:
                    socket.gethostbyname(word + "." + domain)
                    self.found.append(word + "." + domain)

                except socket.gaierror:
                    pass
                
                except Exception as e:
                    logging.error(e)
            
        self.event.set()
    

    def headerFuzzer(self, url: str, wordlist: str, headers: dict, replacer: str = "FUZZ", method: str = "GET", responses: list = [200], fsize: int = None, threads: int = 16, proxies: dict = None, timeout: int | float = 10, verify: bool = True):

        self.found.clear()

        if os.path.isfile(wordlist):
            self.wordlist = open(wordlist, "rt")
        
        else:
            raise FileNotFoundError(f"Wordlist not found: {wordlist}")
        
        #for i in range(threads):
        #    th = threading.Thread(target=self._fuzzHeader, args=(url, headers, replacer, method, responses, fsize, proxies, timeout,))
        #    th.start(url, headers, replacer, method, responses, fsize, proxies, timeout)

        self._fuzzHeader(url, headers, replacer, method, responses, fsize, proxies, timeout)

        self.event.wait()
        self.event.clear()
        self.wordlist.close()

        return self.found
        

    def _fuzzHeader(self, url, headers: dict, replacer: str = "FUZZ", method: str = "GET", responses: list = [200], fsize: int = None, proxies: dict = None, timeout: int | float = 10, verify: bool = True):
        word = None

        while word != "":
            self.lock.acquire()
            word = self.wordlist.readline()[:-1]
            self.lock.release()

            newHeader = json.loads(json.dumps(headers).replace(replacer, word))

            try:
                response = requests.request(method, url, headers=newHeader, proxies=proxies, timeout=timeout, verify=verify)

            except Exception as e:
                logging.error(e)

            if response.status_code in responses:
                if fsize:
                    if len(response.content) in fsize:
                        self.found.append(newHeader)
                
                else:
                    self.found.append(newHeader)

        self.event.set()