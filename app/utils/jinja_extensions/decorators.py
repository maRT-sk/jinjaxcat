"""
This module provides decorators to enhance and customize the behavior of custom jinja2 extensions for JinjaXcat.
Currently, it offers caching functionalities using cachetools.
"""


import cachetools


def cached_input_files(maxsize=100):
    """
    A decorator to cache the results of functions (jinja2 extensions) used on input file data.
    This decorator utilizes an LRU (Least Recently Used) caching mechanism provided by cachetools.
    It caches the result of the function based on the hashed input file data.

    :param maxsize: Maximum number of items to be stored in the cache. Defaults to 100.
    :return: A wrapped function with caching capabilities.

    Usage:
    -----
    @cached_input_files(maxsize=50)
    def process_files(data):
        # expensive computation
        return processed_data
    """
    return cachetools.cached(cachetools.LRUCache(maxsize=maxsize),
                             key=lambda data: hash(frozenset(tuple(d.items()) for d in data)))
