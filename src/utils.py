import re
import datetime


regex: dict = {
    "digits": re.compile("\d+")
}


def digits_from_str(s: str) -> str | None:
    return "".join(regex["digits"].findall(s))


def format_datetime(dt: datetime.datetime) -> str:
    return "{0}.{1}.{2} {3}:{4}:{5}.000".format(
        dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)
