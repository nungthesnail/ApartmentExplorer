from bs4 import BeautifulSoup
from selenium import webdriver
from . import models
import utils
import requests
import re


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5 (.NET CLR 3.5.30729)",
    "Accept": "text/html,application/xhtml+xml,application/xml"
}


def get_page(url: str) -> str | None:
    try:
        source = requests.get(url, headers=HEADERS).text
        return source
    except:
        return None


def get_page_selenium(url: str) -> str | None:
    driver = webdriver.Chrome()
    driver.get(url)
    source = driver.page_source
    driver.close()
    return source


class ShopParser:
    @staticmethod
    def get_items(source):
        raise NotImplementedError


class AvitoParser(ShopParser):
    @staticmethod
    def get_items(source):
        items = []
        soup = BeautifulSoup(source, "lxml")
        for i in soup.find_all("div", {"class": re.compile(".*item-body.*")}):
            try:
                title_attrs = i.find_next("a", {"data-marker": "item-title"}).attrs
                name = title_attrs["title"]
                url = "https://www.avito.ru" + title_attrs["href"]
                price = utils.digits_from_str(
                    i.find_next("p", {"data-marker": "item-price"}).text
                )

                items.append(models.Item(url, name, int(price)))

            except Exception as e:
                print(f"exception: {e}, {i}")
                continue

        return items


class CianParser(ShopParser):
    @staticmethod
    def get_items(source):
        items = []
        soup = BeautifulSoup(source, "lxml")
        for i in soup.find_all("article", {"data-name": "CardComponent"}):
            url = i.find_next("a").attrs["href"]
            name = i.find_next("span", {"data-mark": "OfferTitle"}).text
            price = utils.digits_from_str(
                i.find_next("span", {"data-mark": "MainPrice"}).text
            )

            items.append(models.Item(url, name, int(price)))

        return items
