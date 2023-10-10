class Item:
    url: str = ""
    name: str = ""
    price: int = 0

    def __init__(self, url="", name="", price=0):
        self.url = url
        self.name = name
        self.price = price

    def __str__(self):
        return f"Item: {self.name} - {self.price} - {self.url}"

    def __repr__(self):
        return f"Item: {self.name} - {self.price} - {self.url}"
