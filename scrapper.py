import requests
import re
from bs4 import BeautifulSoup

URL = "https://www.youtube.com/watch?v="

def scrap_all(id: str):
    page = requests.get(URL + id)
    soup = BeautifulSoup(page.content, "html.parser")
    tests = open("rsc/results", "w")
    tests.write(soup.prettify())
    tests.close()
    return []

def scrap_main(id: str):
    res = []
    page = requests.get(URL + id)
    soup = BeautifulSoup(page.content, "html.parser")
    res.append(scrap_title(soup))
    res.append(scrap_nb_like(soup))
    res.append(scrap_desc(soup))
    return []

def scrap_title(soup: BeautifulSoup):
    result = soup.find("meta", itemprop="name")
    return result['content']

def scrap_name_chnl(soup: BeautifulSoup):
    result = soup.find("link", itemprop="name")
    return result['content']

def scrap_nb_like(soup: BeautifulSoup):
    results = soup.find_all("script")
    pattern = re.compile(r'([0-9]*.?[0-9]*[0-9]).?clics')
    nb = "0"
    for result in results:
        match = pattern.search(str(result))
        if match:
            nb = match.group(1)
            break
    return "".join(x for x in nb if x.isdigit())

def scrap_desc(soup: BeautifulSoup):
    results = soup.find_all("script")
    pattern = re.compile(r'"shortDescription":"(.*)","isCrawlable":')
    print(pattern.search(str(results)).group(1).replace('\\n', '\n'))
    return pattern.search(str(results)).group(1).replace('\\n', '\n')

def scrap_desc_links(soup: BeautifulSoup):
    results = soup.find_all("script")
    pattern = re.compile(r'"description":{"runs":\[(.*)\]},"subscribeButton":')
    all_desc = ""
    for result in results:
        match = pattern.search(str(result))
        if match:
            all_desc = match.group(1)
            pattern2 = re.compile(r'(?:{"text":"((?:[^\\"]|\\"|\\)*)"[^}]*})*')
            texts = pattern2.findall(all_desc)
            if texts:
                texts = "".join(x for x in texts if x != "")
                break
    return texts

scrap_main("yxCMsQtVev8")