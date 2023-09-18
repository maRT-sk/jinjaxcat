import unicodedata
from datetime import date, datetime

import requests

from .decorators import cached_input_files

# Third party imports


def remove_accents(input_str: str) -> str:
    """
    Removes accents from a string.
    :param input_str: String that may contain accents.
    :return: String without accents.
    """
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    only_ascii = nfkd_form.encode('ASCII', 'ignore')
    return only_ascii.decode()


def remove_leading_symbol(input_string: str, leading_symbol: str) -> str:
    """
    Removes a specified leading symbol from the beginning of a string.
    :param input_string: The input string from which the leading symbol will be removed.
    :param leading_symbol: The symbol to be removed from the beginning of the input string.
    :return: A new string with the specified leading symbol removed from the beginning, if found.
    """
    return input_string.lstrip(leading_symbol)


def current_datetime() -> datetime:
    """
    Gets the current timestamp.
    :return: Current datetime object.
    """
    return datetime.now()


def custom_date(year, month, day) -> date:
    """
    Creates a custom date object.
    :param year: Year for the date.
    :param month: Month for the date.
    :param day: Day for the date.
    :return: Custom date object.
    """
    return date(year, month, day)


def log(message: str) -> str:
    """
    Log the input to console.
    :param message: Message to be logged.
    :return: Empty string.

    """
    print(message)
    return ''


def get_status_code(url: str) -> int | None:
    """
    Get the HTTP status code of a web page.

    :param url: URL of a web page.
    :return: HTTP status code or None if the request fails.
    """
    try:
        response = requests.get(url)
        return response.status_code
    except:  # NOQA E722 *this serves as an example of how to create a custom function.
        return None


@cached_input_files
def remove_inactive_products(data: list) -> list:
    """
    This method removes inactive products from the given list of data records.
    """
    data = [record for record in data if record.get('Status') != 'Inactive']
    return data
