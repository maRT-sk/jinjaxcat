import os
import sys

# This ensures that when we import modules, Python will look in the app directory first.
app_directory = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'app')
sys.path.insert(0, app_directory)