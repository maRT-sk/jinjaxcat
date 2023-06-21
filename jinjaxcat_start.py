# Standard library imports
import argparse
import sys

# Third party imports
import eel

# Local application/library specific imports
from jinjaxcat.logic.interface import execute_rendering_workflow, setup_user_interface

# Initialize Eel with the 'jinjaxcat' folder
eel.init('jinjaxcat')


# Call the function to set up the user interface
def start_application():
    """
    Function to set up and start the user interface application.
    Uses the Eel library to establish communication between Python and HTML/JS.
    """
    setup_user_interface()  # Call the function to set up the user interface
    eel.updateLog("Application started.")  # noqa | Log the application's start message via the JavaScript function

    # Start the Eel application, pointing it to 'main.html' as the starting page
    # The size of the application window is set to 1680x1050, with a shutdown delay of 30 seconds.
    # The application uses a random open port (port=0)
    eel.start('gui/main.html', size=(1680, 1050), shutdown_delay=30, port=0)


#  Parse the command-line arguments for the script.
def parse_cli_arguments():
    """
    Parses command-line arguments provided to the script.
    """
    # Instantiate the parser object
    parser = argparse.ArgumentParser(description="Render a template with data and optionally validate output.")
    # Define the command-line arguments that the script accepts
    parser.add_argument('--input_files', required=True, nargs='+',
                        help='Provide one or more input files. These files contain data for the template.')
    parser.add_argument('--template_name', required=True,
                        help='Path to the template file. Defines how input data will be structured.')
    parser.add_argument('--output_file_name', required=True,
                        help='Specify the path to the output file. The rendered template will be written to this file.')
    parser.add_argument('--is_prettify_output', default=False, type=bool,
                        help='Optional. Set this flag to True if you want the output to be formatted for readability.')
    parser.add_argument('--validation_type', default=None,
                        help='Optional. Set the output validation type. Use "xml" or "json" for output validation.')
    parser.add_argument('--validation_file', default=None,
                        help='Optional. If validation needed, give path to the schema for output validation.')
    return parser.parse_args()  # Parse and return the command-line arguments


if __name__ == '__main__':
    """
    Main entry point of the application.
    Runs as a GUI application if no command line arguments are provided.
    If command-line arguments are provided, runs the application in CLI mode.
    """
    if len(sys.argv) == 1:
        start_application()
    else:
        args = parse_cli_arguments()
        execute_rendering_workflow(args.input_files, args.template_name, args.output_file_name, args.is_prettify_output,
                                   args.validation_type, args.validation_file)
