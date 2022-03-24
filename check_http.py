#!/usr/bin/python

import warnings
import sqlite3
import csv

warnings.filterwarnings('ignore', message='Unverified HTTPS request')

from requests_html import HTMLSession
import requests
import subprocess
import sys, re, os


def write_list2csv(data, fname):
    with open(fname, 'a') as f:
        writer = csv.writer(f)
        writer.writerow([data])


def check_urls(dom):
    #dom = 'lankapage.com'
    #url = 'https://' + dom
    url = dom.replace('http', 'https')
    is_https = 0
    code = 999
    content_text = ""
    tout = 30

    try:
        #url = 'https://' + dom
        #Ref: https://stackoverflow.com/questions/56691190/requests-html-httpsconnectionpoolread-timed-out
        session = HTMLSession(verify=False)
        r = session.get(url, timeout=tout)
        #if r.status_code == 200:
        if int(str(r.status_code)[:1]) < 4:
            is_https = 1
            code = r.status_code
            content_text = r.html.html
    except Exception as e:
        print(str(e))
        pass

    if is_https == 0:
        try:
            #url = 'http://' + dom
            url = dom
            session = HTMLSession(verify=False)
            r = session.get(url, timeout=tout)
            is_https = 0
            code = r.status_code
            content_text = r.html.html

            print(f"[{url}] is in http, not secure!")
            write_list2csv(url, 'http_insecure_sites.csv')
        except Exception as e:
            #print(str(e))
            pass
    # return {'is_https': is_https, 'code': code, 'content': content_text, 'url': url}
    return [url, is_https, code, content_text]

def main():

    conn = sqlite3.connect('./virusTotal/global.sqlite')
    sql  = 'SELECT site_url, country, continent FROM site_visits'
    cursor = conn.cursor()
    cursor = cursor.execute(sql)
    with open('site_urls.csv', 'w') as f:
        writer = csv.writer(f)
        for row in cursor:
            if row[0].startswith('"'):
                row[0] = row[0][1:-1]
            writer.writerow(row)


    url_list = []
    with open('site_urls.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            url_list.append(row[0])

    for row in url_list:
        url = row.strip()
        result = check_urls(url)
        write_list2csv(result, 'rough_http_result.csv')


if __name__ == "__main__":
    main()   