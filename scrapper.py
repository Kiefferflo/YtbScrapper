import requests
import re
import json
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
    res["Title"] = scrap_title(soup)
    res["like"] = scrap_nb_like(soup)
    res["desc"] = scrap_desc(soup)
    res["links"] = scrap_desc_links(soup)
    res["id"] = id
    res["comm"] = scrap_comm(soup)
    
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
    return pattern.search(str(results)).group(1).replace('\\n', '\n')

def scrap_desc_links(soup: BeautifulSoup):
    results = soup.find_all("script")
    pattern = re.compile(r'"description":{"runs":\[(.*)\]},"subscribeButton":')
    all_desc = ""
    texts = []
    for result in results:
        match = pattern.search(str(result))
        if match:
            all_desc = match.group(1)
            pattern2 = re.compile(r'(?:"url":"((?:[^\\"]|\\"|\\)*)"[^}]*,"webPageType":"((?:[^\\"]|\\"|\\)*)")*')
            texts = pattern2.findall(all_desc)
            if texts:
                texts = [ (x[0].encode().decode('unicode-escape'), x[1].encode().decode('unicode-escape')) for x in texts if x[0] != '']
                break
    res = []
    for text in texts:
        tmp = text[0]
        if text[1]=="WEB_PAGE_TYPE_WATCH":
            tmp = "https://www.youtube.com" + text[0]
        res.append(tmp)
    return res

def scrap_comm(soup: BeautifulSoup):
    results = soup.find_all("script")
    pattern = re.compile(r',"teaserContent":{"simpleText":"((?:[^\\"]|\\"|\\)*)"},"trackingParams":')
    return pattern.search(str(results)).group(1)

def main():
    with open('input.json') as mon_fichier:
        data : dict = json.load(mon_fichier)

    IdVideos : list = data['videos_id']
    NbrVideos : int = len(IdVideos)

    for i in range (NbrVideos):
        donnees : dict = scrap_main(i)
        with open("output.json", "a") as file:
            json.dump(donnees, file)
            file.write("\n")