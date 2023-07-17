import argparse
import io
import os

import yaml

from utils.procesor import generate_output, validate_xml, prettify_output


class CustomUploadedFile(io.BytesIO):
    """
     A custom file object extending io.BytesIO to store additional file metadata.
     """

    def __init__(self, file_path):
        """
        Initializes the object, loading the file content and metadata.
        """
        with open(file_path, 'rb') as file:
            super().__init__(file.read())
        self.file_path = file_path
        self.name = os.path.basename(file_path)
        self.type = os.path.splitext(file_path)[1]
        self.size = os.path.getsize(file_path)


def load_config(config_path):
    """
    Load the configuration from a YAML file. Checks for mandatory keys and reports if any are missing.
    """
    mandatory_keys = ['input_files', 'template_file', 'output_file']
    with open(config_path, 'r') as stream:
        try:
            cfg = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(f"Failed to load the YAML configuration: {exc}")
            return None
        missing_keys = [key for key in mandatory_keys if key not in cfg]
        if missing_keys:
            print(f"Missing mandatory key(s) in configuration: {', '.join(missing_keys)}")
            return None
        return cfg


def prepare_files(file_paths):
    """
    Prepare a list of CustomUploadedFile objects from the given file paths.
    """
    return [CustomUploadedFile(file_path) for file_path in file_paths]


def write_output(output_content, file_path):
    """
    Writes the given output to the specified file path.
    """
    with open(file_path, 'w') as f:
        f.write(output_content)


if __name__ == '__main__':
    # Set up argument parsing for command line usage
    parser = argparse.ArgumentParser(description="Process input and template files according to the config file")
    parser.add_argument('config', type=str, help="Path to the configuration yaml file")
    args = parser.parse_args()

    # Load config file
    config = load_config(args.config)
    if not config:
        exit("Failed to load the configuration file.")

    # Prepare the input files and template file
    input_files = prepare_files(config['input_files'])
    template_file = CustomUploadedFile(config['template_file'])

    # Generate the output, optionally beautify it, and validate it against the schema if provided
    output = generate_output(input_files, template_file, key_mapping={})
    if config.get('beautify_output', False):
        extension = template_file.name[template_file.name.rfind("."):]
        output = prettify_output(output, extension)
    if schema_path := config.get('schema_file'):
        validate_xml(output.encode(), schema_path)

    # Write the output to file
    write_output(output, config['output_file'])
