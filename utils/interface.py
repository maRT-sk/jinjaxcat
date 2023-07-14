import io
import os

import pandas as pd
import streamlit as st
from lxml import etree
from streamlit.runtime.scriptrunner import get_script_run_ctx

from utils.help_texts import help_dict
from utils.procesor import generate_output, load_data, prettify_output, validate_xml


@st.cache_data
def load_css(file_name):
    """
    Loads the contents of a CSS file and returns it as a string wrapped within '<style>' HTML tags.

    :param file_name: String containing the path to the CSS file
    :return: A string containing the CSS file content.
    """
    with open(file_name) as file_css:
        style = f'<style>{file_css.read()}</style>'
        return style


def display_input_files(input_files):
    """
    For every input file, load its data and display it in a Streamlit app. Also provides an interface to
    rename the dataframes in accordance with variable names used in a Jinja2 template.

    :param input_files: A list of input files to be displayed.
    """
    data_dict = load_data(input_files)
    for name, data in data_dict.items():
        dict_key_mapping = st.session_state['key_mapping']
        if dict_key_mapping.get(name):
            fixed_name = dict_key_mapping[name]
        else:
            fixed_name = name
        changed_filename = st.text_input(label=f"**📄 {name}**", value=fixed_name,
                                         help=f""" Please rename this dataframe to match the variable name in your 
                                         Jinja2 template. By default, you can access data from the dataframe below 
                                         using the variable name **{fixed_name.strip()}** in your template.""", )
        file_type = name.split('_')[-1]
        if file_type.lower() in ['json', 'rest']:
            st.json(data)
        else:
            st.dataframe(pd.DataFrame(data), use_container_width=True)
        dict_key_mapping[name] = changed_filename


def display_template(template_file):
    """
    Reads the provided template file and displays its contents in a Streamlit app.
    In case of XML files, also checks for XML syntax errors.

    :param template_file: A template file to be displayed.
    """
    template_error = None
    if template_file.name.endswith(".xml"):
        try:
            etree.fromstring(template_file.getvalue())
        except etree.XMLSyntaxError as e:
            template_error = f"**{e.__class__.__name__}**: {e}"
    if template_file.name.endswith(".xlsx"):
        display_xlsx_frame(io.BytesIO(template_file.getvalue()))
    else:
        file_contents = template_file.read()
        file_text = file_contents.decode()
        if template_error: st.error(template_error, icon="🚨")  # noqa:E701
        st.code(file_text, language="jinja2", line_numbers=False)


@st.cache_data
def generate_excel_columns():
    """
    Generate a list of Excel-style column names. Starting from "A" to "Z", then "AA" to "AZ", "BA" to "BZ" and so on.

    :return: A list of Excel-style column names.
    """
    columns = []
    for num in range(1, 703):
        column_name = ""
        while num > 0:
            remainder = (num - 1) % 26
            column_name = chr(65 + remainder) + column_name
            num = (num - 1) // 26
        columns.append(column_name)
    return columns


@st.cache_data
def save_file(file, folder):
    """
    Creates a copy of a given  file to a specified folder on the disk.

    :param file: The temporary file to save.
    :param folder: The folder to save the temporary file in.
    :return: The file path of the saved file.
    """

    file_path = os.path.join(folder, file.name)
    with open(file_path, "wb") as f:
        f.write(file.read())
    return file_path


def select_xml_validation_file(template_file):
    """
    For XML templates, provides an interface to upload XSD/DTD validation files.
    This function also creates a temporary copy of the validation file on disk.

    :param template_file: An XML template file.
    :return: String specifying the path of the validation file, or None if no validation file was selected.
    """

    if template_file.name.endswith(".xml"):
        etree.fromstring(template_file.getvalue())
        validation_files = st.file_uploader("Optional XML Validation (XSD/DTD):", type=["xsd", "dtd"],
                                            accept_multiple_files=True, help=help_dict["optional_xml_validation"])
        if validation_files:
            session_id = get_script_run_ctx().session_id
            temp_folder = "temp/" + str(session_id) + "/"
            if not os.path.exists(temp_folder):
                os.makedirs(temp_folder)
            validation_filepaths = []
            temp_file = None
            for file in validation_files:
                temp_file = save_file(file, temp_folder)
                validation_filepaths.append(file.name)

            if len(validation_files) == 1:
                return temp_file
            else:
                choose_validation_file = st.selectbox('Select the primary validation file.', validation_filepaths)
                return temp_folder + choose_validation_file


def show_beautify_option(template_file):
    """
    Displays a checkbox to allow the user to choose to beautify the output file.
    This function is only applicable for XML and CSV template files.

    :param template_file: The template file to beautify.
    :return: The state of the checkbox (True if checked, False otherwise), or None if the file type is not supported.
    """
    if template_file.name.endswith(".xml") or template_file.name.endswith(".csv"):
        st.subheader("Optional Output Settings:")
        return st.checkbox('Beautify Output File', help=help_dict["beautify_output"])
    else:
        return None


@st.cache_data
def display_xlsx_frame(xlsx_file):
    """
    Reads an Excel file and displays the content of its sheets in a Streamlit app.
    The displayed content includes up to 250 rows from each sheet and uses Excel-style column names.

    :param xlsx_file: The Excel file which content need to be displayed.
    """
    excel_data = pd.read_excel(xlsx_file, sheet_name=None, header=None, dtype=str)
    excel_sheet_names = list(excel_data.keys())  # Get the sheet names
    excel_columns = generate_excel_columns()  # Generate a list of letters corresponding to the number of columns

    # Iterate over each sheet
    for sheet_name in excel_sheet_names:
        st.markdown(f"📗 **{sheet_name}:**")
        excel_df = excel_data[sheet_name].head(250)
        excel_df = excel_df.fillna('')
        excel_df.index = excel_df.index + 1
        excel_df.columns = excel_columns[:len(excel_df.columns)]  # Assign the letters as column names
        st.dataframe(excel_df, use_container_width=True)


def run_output_procedure(input_files, template_file, output_filename, validation_file, beautify_output):
    """
    Processes the provided input data using the given template, validates the output (if a validation file is
    provided), beautifies the output (if specified), and then creates a download button in the Streamlit application
    that allows users to download the resulting output.

    :param input_files: List of input files that hold the data to be processed.
    :param template_file: File that provides the template for processing the input data.
    :param output_filename: String representing the desired name for the output file.
    :param validation_file: File that provides the schema for validating the output. If no validation is required,
                            this should be None.
    :param beautify_output: Boolean indicating whether the output should be beautified. If True, applies beautification
                            to the output.

    :return: None. The function's main effect is its side effect of processing data and creating a download button
             in the Streamlit application.
    """
    prettified_status = None
    validation_status = None

    st.session_state['output_state'] = (None, None, None, beautify_output, False)
    if not output_filename: output_filename = "output"  # noqa
    extension = template_file.name[template_file.name.rfind("."):]

    output = generate_output(input_files, template_file, st.session_state['key_mapping'])

    if beautify_output:
        prettified_output = prettify_output(output, extension)
        if prettified_output:
            output = prettified_output
            prettified_status = True
    if validation_file:
        validation_status = validate_xml(output.encode(), validation_file)

    st.session_state['menu_index'] = "Output"
    st.session_state['output_state'] = (output, extension, validation_status, beautify_output, prettified_status)

    st.download_button(
        label=f"Download as {output_filename}{extension}",
        data=output,
        file_name=output_filename + extension,
        use_container_width=True)
