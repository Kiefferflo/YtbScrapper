import sys
sys.path.append("../")
import pytest
from scrapper import *
import requests
from bs4 import BeautifulSoup
id = "yxCMsQtVev8"
page = requests.get("https://www.youtube.com/watch?v=" + id)
soup = BeautifulSoup(page.content, "html.parser")


def test_title():
    assert scrap_title(soup) == "Soulstone Survivors, Fabular & l'actu | IndieMag l'hebdo #227 - 13/11/2022"

def test_chnl():
    assert scrap_name_chnl(soup) == "Seldell"

def test_nb_like():
    assert int(scrap_nb_like(soup)) >= 293

def test_desc():
    tmp = scrap_desc(soup)
    assert "(EA) = Early Access" in tmp and "#Actualités" in tmp

def test_links():
    assert scrap_desc_links(soup)[0] == "https://www.youtube.com/watch?v=yxCMsQtVev8&t=0s"

def test_comm():
    assert scrap_comm(soup) == "Je ne trouve pas à quelle jeux correspond l'image du milieu de la miniature. L'illustration est incroyable !"

def test_vars():
    with pytest.raises(Exception) as e:
        vars()

def test_scrap_main():
    title = "Soulstone Survivors, Fabular & l'actu | IndieMag l'hebdo #227 - 13/11/2022"
    chnl = "Seldell"
    like = 293
    desc = "(EA) = Early Access"
    link = "https://www.youtube.com/watch?v=yxCMsQtVev8&t=0s"
    comm = "Je ne trouve pas à quelle jeux correspond l'image du milieu de la miniature. L'illustration est incroyable !"
    tmp = scrap_main(id)
    assert tmp["title"] == title and tmp["channel"] == chnl and int(tmp["like"]) >= like and desc in tmp["desc"] and tmp["links"][0] == link and tmp["id"] == id and tmp["comm"] == comm