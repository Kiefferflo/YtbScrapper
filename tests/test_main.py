import sys
sys.path.append("../")
from scrapper import *
import requests
from bs4 import BeautifulSoup

page = requests.get("https://www.youtube.com/watch?v=yxCMsQtVev8")
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