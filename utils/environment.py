# Python's built-in libraries
import unicodedata
from datetime import date, datetime

# Third party imports
import pandas as pd
import requests
from jinja2 import Environment


def remove_accents(input_str: str) -> str:
    """
    Removes accents from a string.
    :param input_str: String that may contain accents.
    :return: String without accents.
    """
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    only_ascii = nfkd_form.encode('ASCII', 'ignore')
    return only_ascii.decode()


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


def get_groups_with_articles(articles, groups, delimiter=',', CATALOG_STRUCTURE='CATALOG_STRUCTURE',
                             GROUP_ID='GROUP_ID', PARENT_ID='PARENT_ID', CATALOG_GROUP_ID='CATALOG_GROUP_ID'):
    """
    This function is used to generate a set of group IDs associated with articles.
    Its purpose is to exclude BME categories that do not include any  articles.

    :param articles: This is the input dataframe containing article data.
    :param groups: This is the dataframe containing BME group data.
    :param delimiter: Delimiter used when multiple catalog groups are present within an article cell. Default - ','.
    :param CATALOG_STRUCTURE: The column name for the BME hierarchy within the dataframe. Default - 'CATALOG_STRUCTURE'.
    :param GROUP_ID: The column name for the group ID within the BME hierarchy dataframe. Default - 'GROUP_ID'.
    :param PARENT_ID: The column name for the parent ID within the BME hierarchy dataframe. Default -  'PARENT_ID'.
    :param CATALOG_GROUP_ID: The column name for the catalog group within the articles df. Default - 'CATALOG_GROUP_ID'.
    :return: Set of group IDs associated with the given articles.
    """

    # Convert raw data to pandas dataframes
    groups_df = pd.DataFrame(groups)
    articles_df = pd.DataFrame(articles)

    # Extract and process catalog group IDs
    group_ids = articles_df[CATALOG_GROUP_ID]
    unique_catalog_group_ids = group_ids.str.split(delimiter).explode().unique()

    # Identify leaf categories in groups data
    leaf_categories = groups_df[
        (groups_df[GROUP_ID].isin(unique_catalog_group_ids)) &
        (groups_df[CATALOG_STRUCTURE] == 'leaf')]

    # Convert GROUP_IDs of leaf categories to list
    leaf_ids = leaf_categories[GROUP_ID].to_list()
    # Identify parent categories of the leaf categories
    parent_ids = set()
    for group_id in leaf_ids:
        while group_id:
            matching_row = groups_df.loc[groups_df[GROUP_ID] == group_id]
            group_id = matching_row[PARENT_ID].values[0]
            structure = matching_row[CATALOG_STRUCTURE].values[0]
            parent_ids.add(group_id)

            if group_id in [0, "0"] or structure == "root":
                break

    groups_with_articles = list(parent_ids) + leaf_ids
    return groups_with_articles


class CustomEnvironment(Environment):
    """
    Custom Jinja2 environment with custom filters and global variables.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Add custom filters to the environment
        self.filters['remove_accents'] = remove_accents
        # Add custom global variables to the environment
        self.globals['current_datetime'] = current_datetime
        self.globals['custom_date'] = custom_date
        self.globals['log'] = log
        self.globals['get_status_code'] = get_status_code
        self.globals['get_groups_with_articles'] = get_groups_with_articles
        self.globals['split'] = '##'
        # Add more filters and globals if needed
