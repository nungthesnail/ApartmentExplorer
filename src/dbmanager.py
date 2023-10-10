import utils
import config
import sqlalchemy as sql
import sqlalchemy_utils as sql_utils
import datetime


engine = sql.create_engine(config.db_path)
if not sql_utils.database_exists(engine.url):
    sql_utils.create_database(engine.url)

metadata = sql.MetaData()

tables = {
    "avito_apartments": sql.Table(
        "avito_apartments", metadata,
        sql.Column("id", sql.Integer, primary_key=True),
        sql.Column("url", sql.Integer, nullable=False),
        sql.Column("name", sql.Text, nullable=False),
        sql.Column("price", sql.Integer, nullable=False),
        sql.Column("update_time", sql.Text, nullable=False)
        ),
    "avito_average_prices": sql.Table(
        "avito_average_prices", metadata,
        sql.Column("id", sql.Integer, primary_key=True),
        sql.Column("date_time", sql.Text, nullable=False),
        sql.Column("average_price", sql.REAL, nullable=False)
        ),

    "cian_apartments": sql.Table(
        "cian_apartments", metadata,
        sql.Column("id", sql.Integer, primary_key=True),
        sql.Column("url", sql.Integer, nullable=False),
        sql.Column("name", sql.Text, nullable=False),
        sql.Column("price", sql.Integer, nullable=False),
        sql.Column("update_time", sql.Text, nullable=False)
        ),

    "cian_average_prices": sql.Table(
        "cian_average_prices", metadata,
        sql.Column("id", sql.Integer, primary_key=True),
        sql.Column("date_time", sql.Text, nullable=False),
        sql.Column("average_price", sql.REAL, nullable=False)
        )
}
metadata.create_all(engine)


class ShopData:
    @staticmethod
    def add_articles(values):
        raise NotImplementedError

    @staticmethod
    def get_articles(price=None):
        raise NotImplementedError

    @staticmethod
    def add_average(avg: float, dt: datetime):
        raise NotImplementedError

    @staticmethod
    def get_averages():
        raise NotImplementedError


class CianData(ShopData):
    @staticmethod
    def add_articles(values):
        if not values:
            return

        connection = engine.connect()
        query = tables["cian_apartments"].insert().values(values)
        connection.execute(query)
        connection.commit()
        connection.close()

    @staticmethod
    def get_articles(price=None):
        connection = engine.connect()
        query: sql.Select

        if not price:
            query = tables["cian_apartments"].select()
        else:
            if price == 0:
                query = tables["cian_apartments"].select().where(
                    tables["cian_apartments"].c.price <= 2000000
                )
            elif price == 1:
                query = tables["cian_apartments"].select().where(
                    (tables["cian_apartments"].c.price >= 2000000)
                    & (tables["cian_apartments"].c.price <= 4000000)
                )
            elif price == 2:
                query = tables["cian_apartments"].select().where(
                    (tables["cian_apartments"].c.price >= 4000000)
                    & (tables["cian_apartments"].c.price <= 7000000)
                )
            elif price == 3:
                query = tables["cian_apartments"].select().where(
                    tables["cian_apartments"].c.price >= 7000000
                )
            else:
                query = tables["cian_apartments"].select()

        result = connection.execute(query)
        connection.close()
        return result.fetchall()

    @staticmethod
    def add_average(avg: float, dt: datetime):
        connection = engine.connect()
        query = tables["cian_average_prices"].insert().values({
            "date_time": utils.format_datetime(dt), "average_price": avg})
        connection.execute(query)
        connection.commit()
        connection.close()

    @staticmethod
    def get_averages():
        connection = engine.connect()
        query = tables["cian_average_prices"].select()
        result = connection.execute(query)
        connection.close()
        return result.fetchall()


class AvitoData(ShopData):
    @staticmethod
    def add_articles(values):
        if not values:
            return

        connection = engine.connect()
        query = tables["avito_apartments"].insert().values(values)
        connection.execute(query)
        connection.commit()
        connection.close()

    @staticmethod
    def get_articles(price=None):
        connection = engine.connect()
        query: sql.Select

        if price is None:
            query = tables["avito_apartments"].select()
        else:
            if price == 0:
                query = tables["avito_apartments"].select().where(
                    (tables["avito_apartments"].c.price < 2000000)
                )
            elif price == 1:
                query = tables["avito_apartments"].select().where(
                    (tables["avito_apartments"].c.price >= 2000000)
                    & (tables["avito_apartments"].c.price <= 4000000)
                )
            elif price == 2:
                query = tables["avito_apartments"].select().where(
                    (tables["avito_apartments"].c.price >= 4000000)
                    & (tables["avito_apartments"].c.price <= 7000000)
                )
            elif price == 3:
                query = tables["avito_apartments"].select().where(
                    (tables["avito_apartments"].c.price >= 7000000)
                )
            else:
                query = tables["avito_apartments"].select()

        result = connection.execute(query)
        connection.close()
        return result.fetchall()

    @staticmethod
    def add_average(avg: float, dt: datetime):
        connection = engine.connect()
        query = tables["avito_average_prices"].insert().values({
            "date_time": utils.format_datetime(dt), "average_price": avg})
        connection.execute(query)
        connection.commit()
        connection.close()

    @staticmethod
    def get_averages():
        connection = engine.connect()
        query = tables["avito_average_prices"].select()
        result = connection.execute(query)
        connection.close()
        return result.fetchall()


def upload_articles_avito(items):
    old_items = [row.url for row in AvitoData.get_articles()]
    new_items = []

    for item in items:
        if item.url in old_items:
            continue

        new_items.append({
            "url": item.url,
            "name": item.name,
            "price": item.price,
            "update_time": utils.format_datetime(datetime.datetime.now())
        })

    AvitoData.add_articles(new_items)


def update_average_avito():
    def get_average_price() -> float:
        prices = [row.price for row in AvitoData.get_articles()]
        return sum(prices) / len(prices)

    AvitoData.add_average(get_average_price(), datetime.datetime.now())


def upload_articles_cian(items):
    old_items = [row.url for row in CianData.get_articles()]
    new_items = []

    for item in items:
        if item.url in old_items:
            continue

        new_items.append({
            "url": item.url,
            "name": item.name,
            "price": item.price,
            "update_time": utils.format_datetime(datetime.datetime.now())
        })

    CianData.add_articles(new_items)


def update_average_cian():
    def get_average_price() -> float:
        prices = [row.price for row in CianData.get_articles()]
        return sum(prices) / len(prices)

    CianData.add_average(get_average_price(), datetime.datetime.now())


def get_articles_avito(price):
    return AvitoData.get_articles(price)


def get_articles_cian(price):
    return CianData.get_articles(price)


def get_averages_avito():
    return AvitoData.get_averages()


def get_averages_cian():
    return CianData.get_averages()
