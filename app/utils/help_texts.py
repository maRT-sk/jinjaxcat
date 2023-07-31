help_dict = {
    "input_files":
        """
        Multiple input files in various formats can be uploaded.
        - **CSV:** Upload any comma-separated files. The delimiter is automatically detected.
        - **XLSX:** Upload workbooks with sheets containing 2D arrays starting from the first cell.
        - **JSON:** Upload JSON files for structured data representation, suitable for various applications.
        - **REST:** Upload basic REST files with a GET request returning a JSON array of objects are valid.\n
        Check out the example input files in the [documentation](https://github.com/maRT-sk/jinjaxcat/tree/main/examples) for further understanding.
        """,
    "template_file":
        """
        Upload your Jinja2 template file for rendering. This template acts as a blueprint to generate dynamic content with the provided data. 
        JinjaXCat features built-in Jinja2 filters for data manipulation and formatting in your templates. 
        Alongside the default filters, JinjaXCat comes with prebuilt custom filters and globals to enhance template engine capabilities and provide extra functionality.
        - **Text-based templates:** Upload any templates like .xml, .csv, .json, .txt that follow the Jinja2 conventions.
        - **XLSX templates:** Upload template fulfill JinjaXCat's custom Jinja2 requirements for parsing XLSX files.
        
        Check out the example Jinja2 templates in the [documentation](https://github.com/maRT-sk/jinjaxcat/tree/main/examples) for further understanding.
        """,
    "output_filename":
        """Specify the desired output filename **without the extension**.  
        If left blank, the default filename will be "output" and the extension will be copied from the 
        template file.""",
    "optional_xml_validation":
        """
        If you select an XML Jinja2 template, you have the option to enable XML validation using either:
        - **XSD** (XML Schema Definition) 
        - **DTD** (Document Type Definition)  

        If you choose not to use this feature, JinjaXCat will generate the XML file as per the template provided without any validation checks.
        Note: If validation fails, the process will stop, and an error detailing the validation issue will be displayed.
        
        Please find example XSD and DTD files in the [documentation](https://github.com/maRT-sk/jinjaxcat/tree/main/examples) for reference.
        """,
    "beautify_output":
        """
        The optional 'Beautify Output' feature allows you to prettify XML and CSV files, making them visually more appealing and easier to read.
        When enabled, the output files will be formatted with indentation, line breaks, and proper spacing, resulting in a cleaner and more organized structure..
        """,
}
