# Python's built-in libraries
import unicodedata
from datetime import date, datetime

# Third party imports
import eel
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


def log(message: str, is_alert = False) -> str:
    """
    Log the input to console.
    :param message: Message to be logged.
    :return: Empty string.
    """
    eel.updateLog(message, is_alert) # noqa
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
    except:
        return None


def get_groups_with_articles(articles, groups, delimiter=',', CATALOG_STRUCTURE='CATALOG_STRUCTURE',
                             GROUP_ID='GROUP_ID', PARENT_ID='PARENT_ID') -> set:
    """
    Generates a set of group IDs associated with the given articles.
    :param articles: List of articles (name of your CSV file or Excel sheet)
    :param groups: List of groups/BME categories  (name of your CSV file or Excel sheet)
    :param delimiter: Delimiter for multiple catalog groups within an article cell.
    :param CATALOG_STRUCTURE: Column name for the BME hierarchy structure type.
    :param GROUP_ID: Column name for the group ID in the BME hierarchy structure.
    :param PARENT_ID: Column name for the parent ID in the BME hierarchy structure.
    :return: Set of group IDs associated with the given articles.
    """

    groups_with_articles = set()  # Initialize an empty set to store group IDs

    # Find all related groups for each group
    for group in groups:
        related_groups = []
        if group[CATALOG_STRUCTURE] == 'root':
            related_groups.append(group[GROUP_ID])  # Add the root group ID to the list of related groups
            continue
        parent = group[PARENT_ID]
        related_groups.append(parent)  # Add the parent group ID to the list of related groups
        while parent:
            for _group in groups:
                if _group[GROUP_ID] == parent:
                    if _group[CATALOG_STRUCTURE] in ['leaf', 'node']:
                        parent = _group[PARENT_ID]  # Update the parent ID to the next level in the hierarchy
                    else:
                        parent = None   # Stop traversing the hierarchy if it's not a leaf or node group
        group['all_related_groups'] = related_groups  # Store the list of related groups in the group object

    # Find all groups associated with each article
    for row in articles:
        for articles_group_id in row['CATALOG_GROUP_ID'].split(delimiter):
            for _group in groups:
                if articles_group_id == _group[GROUP_ID]:
                    groups_with_articles.add(_group[GROUP_ID])    # Add the group ID to the set of groups with article
                    groups_with_articles.update(_group['all_related_groups'])    # Add the related group IDs
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
        # Add more filters and globals if needed
