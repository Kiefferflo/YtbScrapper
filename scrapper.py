import requests
import sys
import re
import json
from bs4 import BeautifulSoup

URL = "https://www.youtube.com/watch?v="

def scrap_main(id: str):
    res: dict = {}
    page: request = requests.get(URL + id)
    soup: BeautifulSoup = BeautifulSoup(page.content, "html.parser")
    res["title"] = scrap_title(soup)
    res["channel"] = scrap_name_chnl(soup)
    res["like"] = scrap_nb_like(soup)
    res["desc"] = scrap_desc(soup)
    res["links"] = scrap_desc_links(soup)
    res["id"] = id
    res["comm"] = scrap_comm(soup)
    return res

def scrap_title(soup: BeautifulSoup):
    result: BeautifulSoup = soup.find("meta", itemprop="name")
    return result['content']

def scrap_name_chnl(soup: BeautifulSoup):
    result: BeautifulSoup = soup.find("link", itemprop="name")
    return result['content']

def scrap_nb_like(soup: BeautifulSoup):
    results: BeautifulSoup = soup.find_all("script")
    pattern = re.compile(r'([0-9]*.?[0-9]*[0-9]).?clics')
    nb = "0"
    for result in results:
        match = pattern.search(str(result))
        if match:
            nb = match.group(1)
            break
    return "".join(x for x in nb if x.isdigit())

def scrap_desc(soup: BeautifulSoup):
    results: BeautifulSoup = soup.find_all("script")
    pattern = re.compile(r'"shortDescription":"(.*)","isCrawlable":')
    tmp = pattern.search(str(results))
    res = ""
    if tmp:
        res = tmp.group(1).replace('\\n', '\n')
    return res

def scrap_desc_links(soup: BeautifulSoup):
    results: BeautifulSoup = soup.find_all("script")
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
                texts = [(x[0].encode().decode('unicode-escape'), x[1].encode().decode('unicode-escape')) for x in texts if x[0] != '']
                break
    res = []
    for text in texts:
        tmp = text[0]
        if text[1]=="WEB_PAGE_TYPE_WATCH":
            tmp = "https://www.youtube.com" + text[0]
        res.append(tmp)
    return res

def scrap_comm(soup: BeautifulSoup):
    results: BeautifulSoup = soup.find_all("script")
    pattern = re.compile(r',"teaserContent":{"simpleText":"((?:[^\\"]|\\"|\\)*)"},"trackingParams":')
    tmp = pattern.search(str(results))
    res = ""
    if tmp:
        res = tmp.group(1)
    return res

def vars():
    args=sys.argv[1:]
    int_cpt=len(args)
    if int_cpt == 0:
        input_file = "input.json"
        output_file = "output.json"
    elif int_cpt == 4 :
        if (args[0]!="--input" and args[0]!="--output" and args[2]!="--input" and args[2]!="--output"):
            raise Exception("Arguments error flag allowed : --input; --output")
        if args[0] == "--input":
            input_file = args[1]
        else:
            output_file = args[1]
        if args[2] == "--input":
            input_file = args[1]
        else:
            output_file = args[1]   
    else:
        raise Exception("Arguments error, please run the command python3 scrapper.py --input input_file.json --output output_file.json")
    return [input_file,output_file]


if __name__ == '__main__':
    try:
        input_file,output_file=vars()
        with open(input_file) as mon_fichier:
            data: dict = json.load(mon_fichier)
        IdVideos: list = data['videos_id']
        NbrVideos: int = len(IdVideos)
    except Exception as e:
        print(e)
    for i in range(NbrVideos):
        donnees: dict = scrap_main(IdVideos[i])
        try:
            with open(output_file, "a") as file:
                json.dump(donnees, file)
                file.write("\n")
        except Exception as e:
            print(e)