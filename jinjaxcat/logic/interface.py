# Standard library imports
import json
import os
from tkinter import Tk, filedialog

# Third party imports
import eel

# Local application/library specific imports
from jinjaxcat.logic.processor import (
    create_environment,
    load_data,
    render_template,
    validate_output,
)


@eel.expose
def execute_rendering_workflow(input_files: list, template_name: str, output_file_name: str,
                               is_prettify_output: bool,validation_type: str,
                               validate_against: str | None = None) -> bool:
    """
    Orchestrates the complete rendering workflow. Loads data, renders the template, and validates the output.
    :param input_files: A list of input files.
    :param template_name: The name of the template file.
    :param output_file_name: The name of the output file.
    :param is_prettify_output: A flag to specify if the output should be pretty-printed.
    :param validation_type: The type of validation to perform on the output (XML or JSON).
    :param validate_against: The validation schema file. Optional and defaults to None.
    :return: True if the rendering and validation (if applicable) are successful. False otherwise.
    """
    data_dict = load_data(input_files)  # Load data from the input files
    environment = create_environment()  # Set up Jinja2 environment

    # Use the loaded data and environment to render the template
    output_file = render_template(data_dict, environment, template_name, output_file_name, is_prettify_output)
    if not output_file:
        return False

    # If a validation type is not None, validate the output file
    if str(validation_type) != 'None':
        if validate_output(output_file, validation_type, validate_against):
            return True
        else:
            return False
    return True


def setup_user_interface():
    """
    Set up the User Interface and expose the required functions to Eel for interaction with the front-end.
    """
    HOME_DIR = os.path.expanduser("~")
    PRESET_FOLDER = os.path.join(HOME_DIR, 'jinjaxcat')
    PRESET_FILE = os.path.join(PRESET_FOLDER, 'presets.json')

    def choose_files(operation='askopenfilename', title="Select Files", filetypes=tuple()):
        """
        Opens a file dialog to allow user to select file(s).
        :param operation: The type of file dialog to open. Default is 'askopenfilename'.
        :param title: The title for the file dialog. Default is "Select Files".
        :param filetypes: The file types to be displayed in the file dialog. Default is an empty tuple.
        :return: The selected file(s) or None if no file is selected.
        """
        root = Tk()  # Create a Tk root widget and hide it (we don't want the full GUI)
        root.wm_attributes("-topmost", 1)  # Ensure dialog is displayed on top
        root.withdraw()

        # Open the file dialog
        if operation == 'saveasfilename':
            files = filedialog.asksaveasfilename(title=title, filetypes=filetypes)
        elif operation == 'openfilenames':
            files = filedialog.askopenfilenames(title=title, filetypes=filetypes)
        else:
            files = filedialog.askopenfilename(title=title, filetypes=filetypes)
        root.destroy()  # Destroy the root widget
        return files or None  # Return the selected files

    @eel.expose
    def choose_input_files(current_files):
        """
        Open a dialog allowing the user to select input files, and return the selected files.
        """
        new_files = choose_files(operation='openfilenames', title="Select Input Files")

        if current_files and new_files:
            return list(new_files) + list(current_files)  # Concatenate new files with the existing files
        elif new_files in ['', None]:
            return current_files
        else:
            return new_files

    @eel.expose
    def choose_template():
        """
        Open a dialog allowing the user to select a template file, and return the selected file.
        """
        return choose_files(title="Select Template File")

    @eel.expose
    def choose_xml_validation_file():
        """
        Open a dialog allowing the user to select a validation file, and return the selected file.
        """
        return choose_files(title="Select Validation File",
                            filetypes=(('Definition files', '*.dtd *.xsd'), ('All Files', '*.*')))

    @eel.expose
    def choose_output_file():
        """
        Open a dialog allowing the user to select an output file, and return the selected file.
        """
        return choose_files(operation='saveasfilename', title="Select Output File")

    @eel.expose
    def save_preset(preset_name: str, preset: list) -> None:
        """
        Save a new preset, adding it to the existing presets in the presets file.
        """
        os.makedirs(PRESET_FOLDER, exist_ok=True)  # Ensure the preset folder exists

        # Load existing presets and append the new one
        existing_presets = load_presets()
        existing_presets.append({"name": preset_name, "data": preset})

        # Save the updated presets back to the file
        with open(PRESET_FILE, 'w') as f:
            json.dump(existing_presets, f, indent=2)

        eel.updateLog(f"Preset successfully saved: {preset_name} ")  # noqa
        return get_preset_names()

    @eel.expose
    def load_presets() -> list:
        """
        Load and return the presets from the presets file. Returns an empty list if the file does not exist.
        """
        if not os.path.exists(PRESET_FILE):  # Check if the preset file exists before trying to load it
            return []

        with open(PRESET_FILE) as f:   # Load and return the presets
            return json.load(f)

    @eel.expose
    def get_preset_names() -> list:
        """
        Load the presets and extract their names. Returns the list of preset names.
        """
        return [preset['name'] for preset in load_presets()]

    @eel.expose
    def get_preset_data(preset_name):
        """
        Find and return the data for the preset with the given name, if it exists
        """
        for preset in load_presets():  # Loop over presets to find the one with the specified name
            if preset['name'] == preset_name:
                eel.updateLog(f"Preset loaded successfully: {preset_name} ")  # noqa
                return preset['data']
        return None

    @eel.expose
    def delete_preset(preset_name):
        """
        Load presets and remove the specified one Deletes the specified preset.
        """
        presets = load_presets()
        presets = [preset for preset in presets if preset['name'] != preset_name]

        # Save the updated presets back to the file
        if preset_name is not None:
            with open(PRESET_FILE, 'w') as f:
                json.dump(presets, f)
                eel.updateLog(f"Preset successfully removed: {preset_name}", True)   # noqa

    @eel.expose
    def validation_types():
        """
        Returns the list of available validation types.
        """
        return [{'text': 'Enable XSD/DTD validation for XML', 'value': 'xml'},
                {'text': 'Basic JSON validation', 'value': 'json'}, ]
