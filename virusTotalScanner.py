
import os
import sqlite3
import time

import requests
import argparse
import json
import csv

INTERVAL = 10


api_key='f09885ff6f29eafcac68736694840afd89db409df9babe0c55c26fc6f838f442'

def distinct_countries(conn):
    sql = 'SELECT DISTINCT(country) FROM site_visits'
    cursor = conn.cursor()
    cursor.execute(sql)

    countries = []
    for row in cursor:
      countries.append(row[0])
    return countries

def connect_database(db_file):
    conn = sqlite3.connect(db_file)
    return conn


def excute_statement(conn, sql):
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    return cursor


def load_urls(conn, c):
    cursor = conn.cursor()
    sql = f"SELECT  DISTINCT(site_url) FROM site_visits WHERE country='{c}'"
    # print(sql)
    cursor.execute(sql)
    conn.commit()

    urls = []
    for row in cursor:
        urls.append(row[0])

    return urls


def scan(url):
    scan_server = 'https://www.virustotal.com/vtapi/v2/url/scan'
    print(f'Scanning: {url}')
    id = ''
    try:
        params = {'apikey': api_key, 'url': url }
        response = requests.post(scan_server, data=params)
        if response.status_code == 200:
            id = response.json()['scan_id']
    except ValueError as e:
        print(f"[SCAN] Rate limit detected: {e}")
    except Exception:
        print("[SCAN] Error detected.....")

    return id


def download_report(id):
    report_server = 'https://www.virustotal.com/vtapi/v2/url/report'
    report_list = []
    try:
        params = {'apikey': api_key, 'resource': id }
        response = requests.get(report_server, params=params)
        status_code = response.status_code
    except ValueError as e:
        print(f"[Report] Rate limit detected: {e}")
    
    return response, status_code


def parse_report(response):
    result = response.json()
    scans = result['scans']
    virus = []
    for key in scans:
        items = scans[key]
        if items['detected'] == True or items['result']!='clean site':
            virus.append(key)

    return virus


def inspect_one_country(urls, malicious_sites, c, cont):
    for url in urls:
        id = scan(url)
        time.sleep(INTERVAL)
        report, status = download_report(id)
        time.sleep(INTERVAL)
        if status == 200:
            result = parse_report(report)
            if len(result)>0:
                malicious_sites[url] = [len(result), c, cont]
                print(f'{url} is identified as malicious')
        else:
          print(f'url={url}, report status={status}')

    return malicious_sites


def main():
    dir = './VirusTotalScan/'
    # continents = ['Africa', 'Asia', 'NorthAmerica', 'Europe', 'LatinAmerica', 'aw']
    continents = ['Africa']
    for cont in continents:
        print(f'----{cont}----')
        malicious_sites = {}
        conn = connect_database(dir + cont + '.sqlite')
        countries = distinct_countries(conn)
        for c in countries:
          print(f'----Checking country = {c}----')
          urls = load_urls(conn, c)
          malicious_sites = inspect_one_country(urls, malicious_sites, c, cont)

        with open(cont+'_malicious.csv', 'w') as file:
            writer = csv.writer(file)
            for key, values in malicious_sites:
              writer.writerow([key, values[0], values[1], values[2]])

    print('Scan Complete. Well done!!!''')


if __name__ == '__main__':
    main()
