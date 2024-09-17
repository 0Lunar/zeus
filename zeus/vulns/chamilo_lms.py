import requests
import logging


# CVE-2023-4220 - https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-4220

def chamilo_lms(url: str, verify: bool = True, timeout: int | float = 10) -> bool:
    try:
        target_url = url + "/main/inc/lib/javascript/bigupload/files/"
        response = requests.get(target_url, verify=verify, timeout=timeout)

        if response.status_code == 200:
            return True
        
        else:
            False
    
    except Exception as e:
        logging.error(e)