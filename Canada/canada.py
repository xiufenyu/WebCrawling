from bs4 import BeautifulSoup
import requests, lxml.html, json

hospitals_dict = {}

def load_ca_hosipitals():
    fpath = './Canadas/canada.txt'
    province = 'Alberta'
    with open(fpath, 'r') as file:
        for line in file:
            if line.startswith('=='):
                province = line.split('==')[1]
                hospitals_dict[province] = []
            elif line:
                line = line.split('\n')[0]
                hospitals_dict[province].append(line)

    # for key in hospitals_dict:
    #     print(f'---{key}----')
    #     print(hospitals_dict[key])

headers = {
    "User-Agent":
        "Mozilla/5.0 (Linux; Android 10; HD1913) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.105 Mobile Safari/537.36 EdgA/46.1.2.5140"
}

def crawl_urls():
    for key in hospitals_dict:
        print(f'==={key}===')
        for hospital in hospitals_dict[key]:
            html = requests.get('https://en.wikipedia.org/wiki/' + hospital, headers=headers)
            soup = BeautifulSoup(html.text, 'lxml')
            result = soup.find('a',{'rel': True})['href']
            if not result:
                print(f'Cannot find url for {hospital}')
            else:
                print(result)

def count_canada_urls():
    path = './Canada/website_canada.txt'
    count = 0
    file = open(path, 'r')
    for line in file:
        if line.startswith('http'):
            count = count + 1
    file.close()
    print(f'There are {count} websites in the file') # count = 198

if __name__ == '__main__':
    # load_ca_hosipitals()
    # crawl_urls()
    count_canada_urls()