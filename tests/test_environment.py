import datetime

import pandas as pd
import pytest

from ..app.utils import environment
from .helpers import get_file_path


# Creating a pytest fixture for the custom environment. This fixture will be available across all tests in the session
@pytest.fixture(scope='session')
def env():
    return environment.CustomEnvironment()


# Parametrized test case for remove accents filter. This test case ensures that the remove accents filter works
@pytest.mark.parametrize("input_text, expected", [
    ("héllo123", "hello123"),
    ("ľščťžýá", "lsctzya"),
    ("ĽŠČŤŽÝÁ", "LSCTZYA"),
    ("", ""),
    ("año pâté français café", "ano pate francais cafe")
])
def test_remove_accents_filter(env, input_text, expected):
    template = env.from_string(f'{{{{ "{input_text}"|remove_accents }}}}')
    assert template.render() == expected
    assert environment.remove_accents(input_text) == expected


# Parametrized test case for remove leading symbol filter. This test case ensures that the filter works
@pytest.mark.parametrize("input_text, symbol, expected", [
    ('0000012345', '0', '12345'),
    ('000009990', '0', '9990'),
    ('#hello', '#', 'hello'),
    ('####hello', '#', 'hello'),
    ('#hello#', '#', 'hello#'),
    ('###', '#', ''),
    ('', '#', ''),
    ('0', '0', '')])
def test_remove_leading_symbol(env, input_text, symbol, expected):
    template = env.from_string(f'{{{{ "{input_text}"|remove_leading_symbol("{symbol}") }}}}')
    assert template.render() == expected
    assert environment.remove_leading_symbol(input_text, symbol) == expected


# Test case for current datetime. This test case checks if the current date is rendered correctly
def test_current_datetime(env):
    template = env.from_string('{{ current_datetime().strftime("%Y-%m-%d") }}')
    rendered_output = template.render()
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    assert rendered_output == today
    assert environment.current_datetime().strftime("%Y-%m-%d") == today


# Test case for custom date. This test case checks if a custom date is rendered correctly
def test_custom_date(env):
    template = env.from_string('{{ custom_date(2025, 1, 5).strftime("%Y-%m-%d") }}')
    rendered_output = template.render()
    date_test = datetime.date(2025, 1, 5).strftime("%Y-%m-%d")
    assert rendered_output == date_test
    assert environment.custom_date(2025, 1, 5).strftime("%Y-%m-%d") == date_test


# Test case for log filter. This test case checks if the log message is being output correctly
def test_log_filter(env, capfd):
    template = env.from_string("{{ log('Test log message!') }}")
    template.render()  # This line is necessary to actually render the template
    out, _ = capfd.readouterr()
    assert out.strip() == 'Test log message!'


# This test case checks if the correct status code is returned for valid and invalid URLs
def test_get_status_code(requests_mock):
    url_ok = 'https://www.google.com'
    expected_status_ok = 200
    requests_mock.get(url_ok, status_code=expected_status_ok)
    assert environment.get_status_code(url_ok) == expected_status_ok
    url_ko = 'http://thisurldoesnotexist.xyz'
    expected_status_ko = None
    requests_mock.get(url_ko, status_code=expected_status_ko)
    assert environment.get_status_code(url_ko) == expected_status_ko


#  This test case checks if the function returns the correct groups that have articles
def test_get_groups_with_articles():
    groups_file = get_file_path('test_data/groups.csv')
    articles_file = get_file_path('test_data/articles.csv')
    groups = pd.read_csv(groups_file, dtype=str, quoting=3, sep=None, engine="python",
                         encoding='utf-8-sig').to_dict('records')
    articles = pd.read_csv(articles_file, dtype=str, quoting=3, sep=None, engine="python",
                           encoding='utf-8-sig').to_dict('records')
    expected_output = {'3', '0', '1', '2', '201', '202', '203', '301', '302', '303', '201201'}
    assert set(environment.get_groups_with_articles(articles, groups)) == expected_output
