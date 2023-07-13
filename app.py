# Third party imports
import streamlit as st
from streamlit_option_menu import option_menu

# Import necessary utilities and functions from local modules
from utils.help_texts import help_dict
from utils.interface import (
    display_input_files,
    display_template,
    display_xlsx_frame,
    load_css,
    run_output_procedure,
    select_xml_validation_file,
    show_beautify_option,
)

# Set the configuration for the Streamlit page
st.set_page_config(
    page_title="JinjaXcat",
    page_icon=":cat",
    layout="wide",
    initial_sidebar_state='auto',
    menu_items={"Get help": "https://github.com/maRT-sk/jinjaxcat"}
)

# Load custom CSS, and set the title and description for the Streamlit app
st.markdown(load_css("utils/style.css"), unsafe_allow_html=True)
st.title("JinjaXcat", anchor=False)  #
st.markdown("Generate any excel and text based e-catalog with the power of Jinja templating!")

# Initialize session state variables
st.session_state.setdefault('key_mapping', {})
st.session_state.setdefault('xml_validation', False)
st.session_state.setdefault('menu_index', "Input files")
st.session_state.setdefault('output_state', set())

# Define the sidebar elements for file uploading, settings configuration, and user interaction
with st.sidebar:
    input_files = st.file_uploader(
        "Select Input Files:", accept_multiple_files=True, type=["csv", "xlsx", "json", "rest"],
        help=help_dict["input_files"])
    template_file = st.file_uploader(
        "Select Jinja2 Template:", help=help_dict["template_file"])

    if template_file:
        validation_file = select_xml_validation_file(template_file)
        beautify_output = show_beautify_option(template_file)

    output_filename = st.text_input('Optional Output Filename:', placeholder='Output',
                                    help=help_dict["output_filename"])
    if template_file and input_files:
        if st.button('Generate Output', use_container_width=True):
            st.session_state['menu_index'] = "Output"
            run_output_procedure(input_files, template_file, output_filename, validation_file, beautify_output)
    else:
        st.button('Generate Output', disabled=True, use_container_width=True)

# Define the main menu to allow the user navigation through input files, templates, and output sections
main_menu = option_menu(
    menu_title=None,
    options=["Input Files", "Template", "Output"],
    orientation="horizontal",
    manual_select=2 if st.session_state['menu_index'] == "Output" else None,
    styles={"container": {"padding": "0", "max-width": "100%"},
            "icon": {"display": "none"},
            "nav-link": {"margin": "0px", "white-space:": "nowrap"},
            "nav-link-selected": {"font-weight": "normal"}})

# Display content and manage interactions based on user's selection from the main navigation menu
if main_menu == "Input Files":
    if not input_files:
        st.info("No **Input Files** selected. Please choose input files using the sidebar on the left.", icon="ℹ️")

    if input_files:
        display_input_files(input_files)

elif main_menu == "Template":
    if not template_file:
        st.info("No **Template** selected. Please choose a template using the sidebar on the left.", icon="ℹ️")
    elif template_file:
        display_template(template_file)

elif main_menu == "Output":
    if not st.session_state['output_state']:
        st.info(
            "Output has not been generated yet. Please use the **Generate Output** button in the sidebar on the left "
            "to initiate the generation process.", icon="ℹ️")
    if st.session_state['output_state']:
        output, extension, validation_status, beautify_output, prettified_status = st.session_state['output_state']
        if output and extension != '.xlsx':
            st.success("**Success**:\n The output hss been generated successfully.")
            st.info("**Info**: Previewing output file and displaying the first 35000 characters.")
            if validation_status:
                if validation_status.type == 'KO':
                    st.error(f"**{validation_status.msg}**:\n\n {validation_status.log}")
                else:
                    st.success(f"**{validation_status.msg}**:\n {validation_status.log}")
            if beautify_output:
                if prettified_status:
                    st.success("**Success**:\n The output has been beautified successfully.")
                else:
                    st.error("**Error**:\n The output could not be beautified. The original output remains unchanged.")
            if len(output) > 35000:
                output = output[:35000] + "..."
            st.code(output, language=extension[1:], line_numbers=True)
        elif output and extension == '.xlsx':
            st.success("**Success**:\n The output has been generated successfully.")
            st.info("**Info**: Previewing outputfile and displaying the first 250 rows.")
            display_xlsx_frame(output)
