import filecmp
import os
from unittest.mock import mock_open, patch

import yaml

from ..app import jinjaxcat_cli
from .helpers import get_file_path


# This test ensures that the creation of a CustomUploadedFile object
def test_custom_uploaded_file():
    file_path = get_file_path('test_data/articles.csv')
    file = jinjaxcat_cli.CustomUploadedFile(file_path)  # Create a CustomUploadedFile object
    assert file.file_path == file_path
    assert file.name == os.path.basename(file_path)
    assert file.type == os.path.splitext(file_path)[1]
    assert file.size == os.path.getsize(file_path)


# This test checks whether the function load_config correctly loads a config file
def test_load_config():
    config_path = get_file_path('test_data/demo_config.yml')
    config = jinjaxcat_cli.load_config(config_path)
    assert config == {
        'input_files': ['test_data/articles.csv', 'test_data/groups.csv'],
        'template_file': 'test_data/template.xml',
        'schema_file': 'test_data/schema.xsd',
        'beautify_output': True,
        'output_file': 'test_data/output.xml'
    }


# This test validates whether prepare_files function correctly prepares file paths
def test_prepare_files():
    file_paths = [get_file_path('test_data/groups.csv'), get_file_path('test_data/articles.csv')]
    files = jinjaxcat_cli.prepare_files(file_paths)  # Prepare the files
    assert len(files) == len(file_paths)
    for file, file_path in zip(files, file_paths):
        assert isinstance(file, jinjaxcat_cli.CustomUploadedFile)
        assert file.file_path == file_path


# This test checks whether the write_output function writes the correct output content to the file
@patch("builtins.open", new_callable=mock_open)
def test_write_output(mock_open):
    output_content = 'test output'
    file_path = 'temp_output.txt'
    jinjaxcat_cli.write_output(output_content, file_path)  # Write the output
    mock_open.assert_called_with(file_path, 'w')  # Assert that the file was written to
    mock_open().write.assert_called_once_with(output_content)  # Assert that the correct content was written to the file


# This test ensures that the run_jinaxcat function generates the correct output
def test_run_jinaxcat():
    config_path = get_file_path('test_data/demo_config.yml')
    expected_output_file = get_file_path('test_data/output.xml')
    # Get the script directory and set it as the current working directory
    script_dir = os.path.dirname(os.path.realpath(__file__))
    os.chdir(script_dir)
    jinjaxcat_cli.run_jinaxcat(config_path)  # Run the jinaxcat function
    with open(config_path) as file:  # Load the output file path from the config
        config = yaml.safe_load(file)
    output_file = config['output_file']

    # Compare the content of the expected output file and the actual output file
    assert filecmp.cmp(expected_output_file, output_file, shallow=False)
