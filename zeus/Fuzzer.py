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
    

    def urlFuzzer(self, url: str, wordlist: str, headers: dict = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:130.0) Gecko/20100101 Firefox/130.0"}, method: str = "GET", responses: list = [200], fsize: int = None, threads: int = 16, proxies: dict = None, timeout: int | float = 10, verify: bool = True, errorLogging: bool = True) -> list:

        self.found.clear()

        if url.startswith("https://") == False and url.startswith("http://") == False:
            raise ValueError(f"Invalid url: {url}")
        
        if os.path.isfile(wordlist):
            self.wordlist = open(wordlist, "rt")
        
        else:
            raise FileNotFoundError(f"Word list not found: {wordlist}")

        for i in range(threads):
            th = threading.Thread(target=self._fuzzURL, args=(url, method, responses, fsize, proxies, timeout, errorLogging))
            th.start()

        self.event.wait()
        self.event.clear()
        self.wordlist.close()
        
        return self.found

    
    def _fuzzURL(self, url: str, headers: dict, method: str = "GET", responses: list = [200], fsize: int = None, proxies: dict = None, timeout: int | float = 10, verify: bool = True, errorLogging: bool = False) -> None:
        word = None
        
        while word != "":
            self.lock.acquire()
            word = self.wordlist.readline()[:-1]
            self.lock.release()

            try:
                r = requests.request(method, url + "/" + word, headers=headers, proxies=proxies, timeout=timeout, verify=verify)

            except Exception as e:
                if errorLogging:
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

    
    def subdomainFuzzer(self, domain: str, wordlist: str, threads: int = 16, errorLogging: bool = False) -> list:
        self.found.clear()

        #check if the domain exist
        socket.gethostbyname(domain)

        if os.path.isfile(wordlist):
            self.wordlist = open(wordlist, "rt")

        else:
            raise FileNotFoundError(f"Wordlist not found: {wordlist}")

        for i in range(threads):
            th = threading.Thread(target=self._fuzzSub, args=(domain, errorLogging,))
            th.start()

        self.event.wait()
        self.event.clear()
        self.wordlist.close()
        
        return self.found

    
    def _fuzzSub(self, domain: str, errorLogging: bool = False) -> None:
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
                    if errorLogging:
                        logging.error(e)
            
        self.event.set()
    

    def headerFuzzer(self, url: str, wordlist: str, headers: dict, replacer: str = "FUZZ", method: str = "GET", responses: list = [200], fsize: int = None, threads: int = 16, proxies: dict = None, timeout: int | float = 10, verify: bool = True, errorLogging: bool = False) -> list:

        self.found.clear()

        if os.path.isfile(wordlist):
            self.wordlist = open(wordlist, "rt")
        
        else:
            raise FileNotFoundError(f"Wordlist not found: {wordlist}")
        
        for i in range(threads):
            th = threading.Thread(target=self._fuzzHeader, args=(url, headers, replacer, method, responses, fsize, proxies, timeout, errorLogging,))
            th.start()

        self.event.wait()
        self.event.clear()
        self.wordlist.close()

        return self.found
        

    def _fuzzHeader(self, url, headers: dict, replacer: str = "FUZZ", method: str = "GET", responses: list = [200], fsize: int = None, proxies: dict = None, timeout: int | float = 10, verify: bool = True, errorLogging: bool = False) -> None:
        word = None

        while word != "":
            self.lock.acquire()
            word = self.wordlist.readline()[:-1]
            self.lock.release()

            newHeader = json.loads(json.dumps(headers).replace(replacer, word))

            try:
                response = requests.request(method, url, headers=newHeader, proxies=proxies, timeout=timeout, verify=verify)

                if response.status_code in responses:
                    if fsize:
                        if len(response.content) in fsize:
                            self.found.append(newHeader)

                    else:
                        self.found.append(newHeader)

            except ConnectionError as e:
                if errorLogging:
                    logging.error(e)

        self.event.set()
    

    def parameterFuzzer(self, url: str, wordlist: str, param: str, headers: dict = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:130.0) Gecko/20100101 Firefox/130.0", "Content-Type": "application/json"}, replacer: str = "FUZZ", method: str = "GET", responses: list = [200], fsize: int = None, threads: int = 16, proxies: dict = None, timeout: int | float = 10, verify: bool = True, errorLogging: bool = True) -> None:

        self.found.clear()

        if os.path.isfile(wordlist):
            self.wordlist = open(wordlist, "rt")
        
        else:
            raise FileNotFoundError(f"Wordlist not found: {wordlist}")
        
        for i in range(threads):
            th = threading.Thread(target=self._fuzzParam, args=(url, param, headers, replacer, method, responses, fsize, proxies, timeout, verify, errorLogging))
            th.start()

        self.event.wait()
        self.event.clear()
        self.wordlist.close()

        return self.found
        
    
    def _fuzzParam(self, url: str, param: str | dict, headers: dict, replacer: str = "FUZZ", method: str = "GET", responses: list = [200], fsize: int = None, proxies: dict = None, timeout: int | float = 10, verify: bool = True, errorLogging: bool = False) -> None:
        word = None

        while word != "":
            self.lock.acquire()
            word = self.wordlist.readline()[:-1]
            self.lock.release()

            if type(param) == dict:
                newParam = json.dumps(param).replace(replacer, word)
            
            elif type(param) == str:
                newParam = param.replace(replacer, word)
            
            try:
                response = requests.request(method, url, data=newParam, headers=headers, verify=verify, proxies=proxies, timeout=timeout)

                if response.status_code in responses:
                    if fsize:
                        if len(response.content) == fsize:
                            self.found.append(newParam)
                    
                    else:
                        self.found.append(newParam)
            
            except Exception as e:
                if errorLogging:
                    logging.error(e)
        
        self.event.set()