import importlib
import inspect
import os

from jinja2 import FileSystemLoader
from jinja2.sandbox import SandboxedEnvironment


def _load_jinja_extensions_from_directory(directory: str) -> dict:
    """
    Load functions from Python modules within the specified directory and return as a dictionary.
    :param directory: Path to the directory containing Jinja2 extension modules.
    :return: Dictionary containing functions from the modules.
    """
    extensions = {}

    for filename in os.listdir(directory):
        root, ext = os.path.splitext(filename)

        if ext == ".py" and root != "__init__":
            module = importlib.import_module(f"utils.jinja_extensions.{root}")

            # Extract functions from the loaded module that are defined within the module
            functions_from_module = {
                name: obj for name, obj in inspect.getmembers(module)
                if inspect.isfunction(obj) and obj.__module__ == module.__name__
            }
            extensions.update(functions_from_module)
    return extensions


def create_environment() -> SandboxedEnvironment:
    """
    Create a custom Jinja2 environment.
    :return: SandboxedEnvironment object with custom filters and globals.
    """
    env = SandboxedEnvironment(
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=False,
        autoescape=True,
        loader=FileSystemLoader(''),
    )

    # Directory containing the Jinja2 extension modules
    extensions_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'jinja_extensions')

    # Load functions from the extensions directory
    extensions = _load_jinja_extensions_from_directory(extensions_directory)
    env.filters.update(extensions)
    env.globals.update(extensions)

    # Add additional "static" globals
    env.globals['split'] = '##'  # This global variable stores the separator used for Excel templates

    return env