import csv
import requests
from bs4 import BeautifulSoup

def crawl_hospitals(continent, count):
    sites_list = []
    total = 0
    for index in range(count):
        url = 'https://hospitals.webometrics.info/en/' + continent
        if index != 0:
            url = url + '?page=' + str(index)
        print(url)
        html_doc = requests.get(url).text
        tmp_list = parse_html(html_doc)
        sites_list.extend(tmp_list)

    with open(continent + '.csv', "w") as f:
        writer = csv.writer(f)
        writer.writerows(sites_list)
        total = len(sites_list)
        print(f'{continent} has {total} hospitals')


def parse_html(html_doc):
    my_list = []

    soup = BeautifulSoup(html_doc, 'html.parser')
    trs = soup.table.find_all('tr')
    for tr in trs:
        hosp_row = []
        tds = tr.find_all('td')
        for td in tds:
            a = td.find('a', href=True, target='_blank')
            if a and a.text:
                # url
                hosp_row.append(a['href'])
                hosp_row.append(a.text)
                continue
            img = td.find('img', alt="bandera")
            if img:
                img_name = img['src'].split('/')[-1]
                country = img_name.split('.')[0]
                hosp_row.append(country)

            if hosp_row:
                my_list.append(hosp_row)
                print(hosp_row)
                break

    return my_list

if __name__ == '__main__':
    tabs = {
        'North_america': 46, 'Latin_America': 14, 'Europe': 64,
        'Asia': 37, 'Africa':3, 'aw': 3, 'Oceania':3
    }
    for continent in tabs:
        count = tabs[continent]
        crawl_hospitals(continent, count)