import dbmanager
import config
from . import pageprocessor
from .. import config
import time


def get_articles():
    return {
        "avito": pageprocessor.AvitoParser.get_items(
            pageprocessor.get_page_selenium(config.avito_url)),
        "cian": pageprocessor.CianParser.get_items(
            pageprocessor.get_page(config.cian_url))
    }


def upload_articles(articles):
    dbmanager.upload_articles_cian(articles["cian"])
    dbmanager.upload_articles_avito(articles["avito"])


def update_averages():
    dbmanager.update_average_cian()
    dbmanager.update_average_avito()


def update():
    articles = get_articles()
    upload_articles(articles)
    update_averages()


def main():
    while True:
        try:
            update()
        except:
            pass
        finally:
            time.sleep(config.day_length * config.update_rate)
