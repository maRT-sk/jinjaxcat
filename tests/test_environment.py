import datetime

import pytest

from ..app.utils import jinja_environment


# Creating a pytest fixture for the custom environment. This fixture will be available across all tests in the session
@pytest.fixture(scope='session')
def env():
    return jinja_environment.create_environment()


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


# Test case for current datetime. This test case checks if the current date is rendered correctly
def test_current_datetime(env):
    template = env.from_string('{{ current_datetime().strftime("%Y-%m-%d") }}')
    rendered_output = template.render()
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    assert rendered_output == today


# Test case for custom date. This test case checks if a custom date is rendered correctly
def test_custom_date(env):
    template = env.from_string('{{ custom_date(2025, 1, 5).strftime("%Y-%m-%d") }}')
    rendered_output = template.render()
    date_test = datetime.date(2025, 1, 5).strftime("%Y-%m-%d")
    assert rendered_output == date_test


# Test case for log filter. This test case checks if the log message is being output correctly
def test_log_filter(env, capfd):
    template = env.from_string("{{ log('Test log message!') }}")
    template.render()  # This line is necessary to actually render the template
    out, _ = capfd.readouterr()
    assert out.strip() == 'Test log message!'
