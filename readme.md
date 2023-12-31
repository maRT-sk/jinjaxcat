# JinjaXcat

![example workflow](https://github.com/maRT-sk/jinjaxcat/actions/workflows/test_workflow.yml/badge.svg)

JinjaXcat is a tool designed to simplify the process of creating text-based and Excel e-procurement catalogs.
It utilizes the power of the Jinja2 templating engine to dynamically generate catalog content, providing control through
an app based on the Streamlit framework. JinjaXcat can interpret input data from CSV, XLSX, JSON, and REST (API) files.

### Online Preview

You can preview the tool online at [jinjaxcat.foka.app](https://jinjaxcat.foka.app).
It is continuously and automatically deployed from this repository.

### Project Background and Motivation

JinjaXcat was developed in response to a need for a simple yet effective solution for generating e-procurement catalog
files.
The strength of this tool lies in its utilization of the Jinja2 templating engine and the flexibility to write custom
Python functions for enhancing catalog data, which makes it a versatile and robust solution for catalog generation.
The goal is to provide a fully customizable approach by utilizing premade templates to generate the desired output
catalog file.

Initially developed in 2021 as a Command Line Interface tool, it later evolved into an executable application with a
GUI. The first graphical interface was created using the Eel framework, further enhanced by Alpine.js, and styled with
Tailwind CSS. You can find it in the [legacy branch](https://github.com/maRT-sk/jinjaxcat/tree/legacy-eel).
Finally, the decision was made to transition the project to the Streamlit framework, primarily due to its advanced
built-in frontend capabilities and its resemblance to the existing Tailwind/Alpine.js GUI.

## Getting Started

### Prerequisites

- Python 3.10 or newer
- Git

Before you start with JinjaXcat, make sure Python and Git are already installed on your system.

### Installation

Follow the steps below to install JinjaXcat via the command line.

Clone the repository to your machine:

```
git clone https://github.com/maRT-sk/JinjaXcat.git
cd jinjaxcat
```

Within the project's root directory, create a new Python virtual environment named 'venv':

```
python -m venv venv
```

_**Note:** If 'python' is not registered as an environment variable, replace 'python' with the path to your Python
installation. The virtual environment's name 'venv' can be changed as per your preference. You can also choose to
create/activate the virtual environment at a different path._

Activate the virtual environment:

```
# Windows (PowerShell)
.\venv\Scripts\activate
# Unix
source ./venv/bin/activate
```

With the virtual environment activated, install the necessary dependencies:

```
pip install -r requirements.txt
```

Now, you are all set to run JinjaXcat:

```
streamlit run app\jinjaxcat.py
```

At this point, your default web browser should launch automatically.
If it doesn't, locate the URL in your command line interface and paste it into your browser manually.

## How to Render Input File Content to Template

JinjaXcat allows you to include input data from multiple file types into the template.
You can use different file types simultaneously to generate a comprehensive output based on the selected template.

### CSV input files

Any valid CSV file can be utilized; its encoding and delimiter will be detected automatically.  
To access the data from a CSV file in the template, use the file name as a variable.
For example, if you have an articles.csv, you can access respective columns in the template as follows:

```jinja
{% for article in articles_csv %}
{{ article['COLUMN_NAME'] }}
{% endfor %}
```

Replace 'COLUMN_NAME' with the actual column name from the respective CSV file that you want to include in the rendered
output.

### JSON Input Files

Similar to CSV files, each JSON file acts as an independent data source. In the template, the data from a JSON file can
be accessed by using the filename as a variable.

For example, if you have a data.json file, you can access its properties in the template as follows:

```jinja
{% for article in articles_csv %}
{{ article['PROPERTY_NAME'] }}
{% endfor %}
```

Replace 'PROPERTY_NAME' with the actual property name from the JSON file that you want to include in the rendered
output.

### REST Input Files

JinjaXcat also allows the uploading of basic .rest files that contain a GET request returning a JSON array of objects.
Here's an example of a GET request to obtain a JSON file as input data:

```http request
GET https://jsonplaceholder.typicode.com/todos
Accept: application/json
Accept-Encoding: gzip, deflate
```

Note: The referencing in the template is the same as for JSON inputs.

### Excel Input Files

You can also upload Excel files with multiple sheets, where each sheet represents a separate 2D data source starting
from the first cell. To access data from different sheets in the template, combine the sheet name, file name, and
extension using an underscore (_) as a separator.

For example, if you have a file named 'file.xlsx' with two sheets named 'Sheet1' and 'Sheet2', you can retrieve their
respective data in the text-based template as follows:

```jinja
{% for row in sheet1_file_xlsx %}
{{ row['COLUMN_NAME'] }}
{% endfor %}

{% for row in sheet1_file_xlsx %}
{{ row['COLUMN_NAME'] }}
{% endfor %}
```

Replace 'COLUMN_NAME' with the actual column name from the respective sheet that you want to include in the rendered
output.

## Template Files

JinjaXcat provides the flexibility to generate any text-based and XLSX output files.
You can define templates using the Jinja2 syntax and render data from your input files into the desired format.

### Text-based Templates

You can generate CSV, TXT, XML, CIF, JSON, or any other text-based file formats.
To create a template for a specific file format, define the structure and content using the appropriate syntax.
Customize the template to include placeholders and tags that will be replaced with the actual data during the rendering
process. Here's an example of a template for a CSV file:

```jinja
Supplier ID; Article ID; EAN Code; Description
{% for article in articles_json %}
Supplier123;{{ article['SUPPLIER_AID'] }};{{ article['EAN'] }};{{ article['DESCRIPTION_SHORT'] }}
{% endfor %}
```

In this example, each row in the CSV file represents an article, with columns corresponding to attributes such as
Supplier ID, Article ID, EAN Code, and Description.
With JinjaXcat, you have the flexibility to generate a wide range of text-based output files, allowing you to seamlessly
integrate the generated content into your workflows or applications.

### XLSX templates

When creating an XLSX template, it's necessary to use Jinja2 syntax in each cell where data is to be rendered.
The rendered values will populate all cells beneath, corresponding to the input's length, the first cell included.
To correctly shape the data, you must invoke the custom global variable {{split}}, which splits the data into new rows.

Here's an example of how to use Jinja2 syntax in a cell to get all SUPPLIER_AIDs:

```jinja
{% for article in articles_json %}
{{article['SUPPLIER_AID']}}
{{split}}
{% endfor %}
```

## Jinja2 Filters and Globals in Templates

JinjaXcat provides [builtin Jinja2 filters](https://jinja.palletsprojects.com/en/3.1.x/templates/#builtin-filters)  that
you can use to manipulate and format data within your templates. These filters are available and can be used out of the
box.

In addition to the default filters, JinjaXcat also includes prebuilt custom filters and globals.
These filters and variables are specifically designed to enhance the capabilities of the templating engine and provide
additional functionality to your templates
Some of the prebuilt filters and globals available in JinjaXcat include:

- remove_accents: A filter that removes accents from text, useful for normalizing and cleaning up strings.
- remove_leading_symbol: A filter that removes a specified leading symbol (e.g., a leading zero) from the beginning of a
  string.
- current_datetime: A global that returns the current date and time, providing you with real-time information within
  your templates.
- custom_date: A global that allows you to generate custom-formatted dates, giving you control over the date
  representation in your templates.
- get_status_code: A global that retrieves the status code of an HTTP request, useful for fetching status_code from
  external APIs or web services.
- get_groups_with_articles: A global that retrieves groups with associated articles, useful for BMEcat catalogs to
  filter out groups without any articles.

As a developer, you can add custom filters and globals to JinjaXcat.
Place your `.py` scripts in the `app/utils/jinja_extensions` directory. Function names within these scripts will
automatically be available as both globals and filters in your Jinja templates.
This allows you to enhance the templating engine to meet your specific needs and requirements.

The usage of filters and globals within a JinjaXcat template:

```jinja
{% for article in articles_csv %}
<ARTICLE>
    <SUPPLIER_AID>{{article['SUPPLIER_AID']}}</SUPPLIER_AID>
    <ARTICLE_DETAILS>
        <!-- Apply the custom 'remove_accents' filter to remove all accent marks from the current article  -->
        <DESCRIPTION_SHORT>{{article['DESCRIPTION_SHORT']|remove_accents }}</DESCRIPTION_SHORT>
        <!-- Display the first fifty characters of the current 'article' within the 'DESCRIPTION_LONG' tags. -->
        <DESCRIPTION_LONG>{{article['DESCRIPTION_LONG'][:50]}}</DESCRIPTION_LONG>
        <!-- Apply the 'int' filter to PRICE_QUANTITY, converting the value to an integer.  -->
        <PRICE_QUANTITY>{{article['PRICE_QUANTITY']|int}}</PRICE_QUANTITY>
        <!-- Apply the 'float' filter to PRICE_AMOUNT, converting the value to a float value.  -->
        <PRICE_AMOUNT>{{article['PRICE_AMOUNT']|float}}</PRICE_AMOUNT>
        <!-- Use the custom custom_date function to create a date with specific values. 
        Format the returned date object to a string in "YYYY-MM-DD". -->
        <VALID_FROM>{{ custom_date(2025, 1, 5).strftime("%Y-%m-%d") }}</VALID_FROM>
        <DELIVERY_TIME>{{article['DELIVERY_TIME']}}</DELIVERY_TIME>
        <!-- Begin iterating over each 'keyword' in the current 'article's 'KEYWORDS' attribute.
        The 'KEYWORDS' is a comma-separated string, which is split into individual keywords for the loop. -->
        {% for keyword in article['KEYWORDS'].split(',') %}
        <KEYWORD>{{keyword.strip()}}</KEYWORD>
        {% endfor %}
    </ARTICLE_DETAILS>
</ARTICLE>
{% endfor %}
```

## Command Line Interface

Running the entire application isn't necessary. Instead, you can use the CLI to run your configurations.
JinjaXcat's CLI functionality, accessible through run_cfg.py, enables users to create output files based on a specified
YAML configuration file.
This feature is beneficial for automating processes or integrating JinjaXcat with other tools and workflows.

The general usage via the command line is:

```
python app/jinjaxcat_cli.py path/to/config.yaml
```

This YAML configuration includes:

Mandatory Parameters:

- **input_files:** These are the paths to the input files, which JinjaXcat uses as the data source.
- **template_file:** The path to the template file that JinjaXcat uses to generate the output.
- **output_file:** This is the path to the file where JinjaXcat will write the generated output.

Optional Parameters:

- **beautify_output:** If this parameter is set to True, JinjaXcat will format the output file for better readability.
  If not provided, the default setting is False.
- **schema_file:** This parameter is the path to an XML schema file. If provided, JinjaXcat will validate the XML output
  against this schema, ensuring the output's structure and contents meet the defined requirements.

Example configuration file:

```yaml
input_files:
  - path/to/input1.csv
  - path/to/input2.json
template_file: path/to/template
beautify_output: True # Optional, defaults to False
schema_file: path/to/schema.xsd # Optional
output_file: path/to/output.csv
```

Please note that all paths are relative to the location from where the command is executed.

## JinjaXcat Automated Setup and Launch (Windows Only)

PowerShell script _init_jinjaxcat.ps1_ simplifies the setup and launch process of the JinjaXcat Python application.
Review the script contents before execution to ensure you understand its operations.

### Instructions:

1. Ensure that you're in the directory where you downloaded JinjaXcat from GitHub.
2. Right-click on the script file and select 'Run with PowerShell'.
3. If you don't have the necessary permissions, you can try running it via CLI using the following command:

```powershell
powershell -ExecutionPolicy Bypass -file ./init_jinjaxcat.ps1
```

### What Does The Script Do?

Upon execution, the script performs the following tasks:

1. Sets the current working directory to its location.
2. Checks if the desired version of Python (3.11.5) is installed.
3. If the required Python version is not found, it downloads and installs it.
4. Sets up a Python virtual environment in the script's directory.
5. Installs required dependencies from the requirements.txt file into the virtual environment.
6. Launches the JinjaXcat application using Streamlit.

## Development Status

Your feedback and contributions are greatly appreciated in helping to shape and enhance the JinjaXcat project.
Please be cautious when using JinjaXcat in production environments, as the project is still in the ongoing
development phase.
If you have any questions, suggestions, or would like to discuss the project, feel free to reach out through the
project's GitHub Discussions.

### TODO

- Introduce an option to select a delimiter, as the delimiter for CSV files is not always auto-detected correctly.
  object represents an item, are supported.
- Integrate XLS format support.
- Optimize the rendering process to reduce the time needed for output file creation.