import datetime
import dbmanager
import config
from .res import replicas


class ResultGenerator:
    @staticmethod
    def answer(data):
        raise NotImplementedError

    @staticmethod
    def process_data(data):
        raise NotImplementedError


class PlatformAverage(ResultGenerator):
    @staticmethod
    def answer(data):
        averages = PlatformAverage.process_data(data)
        result = replicas.get_replica("result_average_by_platform")
        return result.format(
            int(averages["avito"].average_price),
            int(averages["cian"].average_price)
        )

    @staticmethod
    def process_data(data):
        averages = {
            "cian": dbmanager.get_averages_cian()[-1],
            "avito": dbmanager.get_averages_avito()[-1]
        }

        return averages


class TimeAverage(ResultGenerator):
    @staticmethod
    def answer(data):
        averages = TimeAverage.process_data(data)
        result = replicas.get_replica("result_average_by_time")

        return result.format(
            datetime.datetime.strptime(averages["old"]["avito"].date_time, "%Y.%m.%d %H:%M:%S.%f").date(),
            # Date of old average price Avito

            int(averages["old"]["avito"].average_price),  # Old average price Avito
            int(averages["current"]["avito"].average_price),  # Current average price Avito
            int(averages["current"]["avito"].average_price / averages["old"]["avito"].average_price * 100),  # Change by percent Avito

            datetime.datetime.strptime(averages["old"]["cian"].date_time, "%Y.%m.%d %H:%M:%S.%f").date(),
            # Date of old average price Cian

            int(averages["old"]["cian"].average_price),  # Old average price Cian
            int(averages["current"]["cian"].average_price),  # Current average price Cian
            int(averages["current"]["cian"].average_price / averages["old"]["cian"].average_price * 100)  # Change by percent Cian
        )

    @staticmethod
    def process_data(data):
        all_averages = {
            "avito": dbmanager.get_averages_avito(),
            "cian": dbmanager.get_averages_cian()
        }
        current_averages = {
            "avito": all_averages["avito"][-1],
            "cian": all_averages["avito"][-1]
        }

        old_averages = {}
        step = int(config.day_length * config.result_avg_time_change
                / (config.day_length * config.update_rate))

        if len(all_averages["avito"]) < step or len(all_averages["cian"]) < step:
            old_averages["avito"] = all_averages["avito"][0]
            old_averages["cian"] = all_averages["cian"][0]
        else:
            old_averages["avito"] = all_averages["avito"][-step]
            old_averages["cian"] = all_averages["cian"][-step]

        return {"old": old_averages, "current": current_averages}


class ApartmentView(ResultGenerator):
    @staticmethod
    def answer(data):
        articles = ApartmentView.process_data(data)
        result = replicas.get_replica("result_apartments_view").format(
            data["platform"], "".join(articles)
        )
        return result

    @staticmethod
    def process_data(data):
        count = config.result_apartment_view_count
        articles = []
        if data["platform"] == "Авито":
            articles = dbmanager.get_articles_avito(data["price"])[-count:]
        elif data["platform"] == "Циан":
            articles = dbmanager.get_articles_cian(data["price"])[-count:]

        return [
            replicas.get_template("apartment_article").format(
                article.name,
                article.price,
                article.url
            )
            for article in articles
        ]


def answer(data):
    if data["action"] == 0:
        return PlatformAverage.answer(data)
    elif data["action"] == 1:
        return TimeAverage.answer(data)
    elif data["action"] == 2:
        return ApartmentView.answer(data)
    else:
        return replicas.get_replica("error")
