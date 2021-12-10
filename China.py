'''
Author: Xiufen Yu
'''

from bs4 import BeautifulSoup
import requests, lxml.html, json

headers = {
    "User-Agent":
    "Mozilla/5.0 (Linux; Android 10; HD1913) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.105 Mobile Safari/537.36 EdgA/46.1.2.5140"
}

def get_organic_results():
    html = requests.get('https://www.baidu.com/s?&tn=baidu&wd=中日医院',headers=headers)
    soup = BeautifulSoup(html.text, 'lxml')

    baidu_data = []

    for result in soup.select('.result.c-container.new-pmd'):
      title = result.select_one('.t').text
      link = result.select_one('.t').a['href']
      displayed_link = result.select_one('.c-showurl').text
      snippet = result.select_one('.c-abstract').text
      try:
        sitelink_title = result.select_one('.op-se-listen-recommend').text
      except:
        sitelink_title = None
      try:
        sitelink_link = result.select_one('.op-se-listen-recommend')['herf']
      except:
        sitelink_link = None

      baidu_data.append({
        'title': title,
        'link': link,
        'displayed_link': displayed_link,
        'snippet': snippet,
        'sitelinks': {'title': sitelink_title, 'link': sitelink_link},
      })

    print(json.dumps(baidu_data, indent=2, ensure_ascii=False))

# get_organic_results()


header2 = {
    'User-Agent': 'My User Agent 1.0',
    'From': 'youremail@domain.com'  # This is another valid field
}
def crawl_one_province(province):
    response = requests.get('http://www.haodf.com/yiyuan/' + province + '/list.htm',headers=header2)
    root_node = lxml.html.fromstring(response.text)
    nodes = root_node.xpath("//div[contains(@class, 'm_ctt_green')]/ul/li/a")
    with open(province.strip()+".txt", "a") as province_file:
        for name in nodes:
            print(name.text)
            province_file.write(name.text+"\n")

crawl_one_province('beijing')



def count_hospitals():
    with open("provinces.txt", "r") as provinces:
        for p in provinces:
            count = 0
            f = open('./Hospitals/' + p.strip() + '.txt', 'r')
            for line in f:
                count = count + 1
            #print(p.strip() + "-NOK : ", count)
            f.close()

            count2 = 0
            f2 = open('./Websites/website_' + p.strip() + '.txt', 'r')
            for line in f2:
                count2 = count2 + 1
            # print(f'{p}: sum={count+count2}, OK={count2},  NOK={count}')
            print(f'{p}: sum={count + count2}, OK={count2}')
            f2.close()

count_hospitals()

def count_clinics():
    clinics = ['诊所', '服务所', '卫生院', '卫生室', '服务中心', '社区', '镇']
    with open("provinces.txt", "r") as provinces:
        for p in provinces:
            count = 0
            f = open('./Hospitals/' + p.strip() + '.txt', 'r')
            for line in f:
                for clinic in clinics:
                    if clinic in line:
                        count = count + 1

            print(p + ':', count)
            f.close()

# count_clinics()