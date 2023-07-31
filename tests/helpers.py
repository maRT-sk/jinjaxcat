import os


def get_file_path(filename):
    """Returns the full path to a test data file in the same directory as the current script."""
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
