# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import os.path
from bs4 import BeautifulSoup
import requests, lxml.html, json

headers = {
    'User-Agent': 'My User Agent 1.0',
    'From': 'youremail@domain.com'  # This is another valid field
}


def crawl_hospital_names():
    with open("provinces.txt", "r") as provinces:
        for province in provinces:
            response = requests.get('https://www.haodf.com/yiyuan/'+province.strip()+'/list.htm',headers=headers)
            root_node = lxml.html.fromstring(response.text)
            nodes = root_node.xpath("//div[contains(@class, 'm_ctt_green')]/ul/li/a")
            with open(province.strip()+".txt", "a") as province_file:
                print(province.strip())
                for name in nodes:
                    province_file.write(name.text+"\n")


hospitals_dict= {}
def load_hospitals():
    with open("provinces.txt", "r") as provinces:
        os.chdir('./Hospitals')
        # print("Current working directory: {0}".format(os.getcwd()))
        for province in provinces:
            hospitals = []
            with open(province.strip()+".txt", "r") as file:
                for line in file:
                    hospitals.append(line.strip())
            hospitals_dict[province.strip()] = hospitals
            # print(province.strip() + ": " , len(hospitals))
    os.chdir('../')
    print("Current working directory: {0}".format(os.getcwd()))


headers2 = {
    "User-Agent":
    "Mozilla/5.0 (Linux; Android 10; HD1913) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.105 Mobile Safari/537.36 EdgA/46.1.2.5140"
}
def crawl_hospital_url(name):
    html = requests.get('https://www.baidu.com/s?&tn=baidu&wd='+name, headers=headers2)
    print("status_code: ", html.status_code)
    soup = BeautifulSoup(html.text, 'lxml')

    for result in soup.select('.result.c-container.new-pmd'):
        dl = result.select_one('.c-showurl')
        t = result.select_one('.t')
        if t is None or dl is None:
            continue
        title = t.text
        displayed_link = dl.text
        if '官方' in title:
            print(name + ": " + displayed_link)
            return displayed_link

# crawl_hospital_url('中日医院')


def get_all_hospital_urls():
    for province in hospitals_dict:
        success = 0
        failed = 0
        ok_urls = []
        nok_names = []
        print(province + ": ", len(hospitals_dict[province]))
        for hospital in hospitals_dict[province]:
            url = crawl_hospital_url(hospital)
            if url:
                ok_urls.append(url + "\n")
                success = success + 1
            else:
                nok_names.append(hospital + "\n")
                failed = failed + 1
                print('Cannot find url for: ' + hospital)
        print(province + ": success:%d, failed=%d", success, failed)
        write_file("website_" + province + '.txt', ok_urls)
        write_file("failed_" + province + '.txt', nok_names)


def write_file(file_name, lines):
    file= open(file_name, 'a')
    try:
        file.write("".join(lines))
    finally:
        file.close()


if __name__ == "__main__":
    print(__name__)
    #load_hospitals()
    # get_all_hospital_urls()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
