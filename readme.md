# JinjaXcat

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

Before you start with JinjaXcat, make sure Python and Git are already installed on your system.

### Installation

Follow the steps below to install JinjaXcat via the command line.

Clone the repository to your local machine:

```
git clone https://github.com/maRT-sk/JinjaXcat.git
cd JinjaXcat
```

Set up a new Python virtual environment:

```
$ python3 -m venv venv
```

Activate the virtual environment:

```
# Windows
$ path\to\venv\Scripts\activate.bat
# Unix
$ source path/to/venv//bin/activate
```

Install the required dependencies:

```
pip install -r requirements.txt
```

Now, you are all set to run JinjaXcat:

```
streamlit run app.py
```

At this point, your default web browser should launch automatically.
If it doesn't, locate the URL in your command line interface and paste it into your browser manually.

## How to Render Input File Content to Template

JinjaXcat allows you to include input data from multiple file types into the template.
You can use different file types simultaneously to generate a comprehensive output based on the selected template.

### CSV input files

Any valid CSV file can be utilized; its encoding and delimiter will be detected automatically.  
To access the data from a CSV file in the template, use the file name (without the suffix) as a variable.
For example, if you have an articles.csv, you can access respective columns in the template as follows:

```
{% for article in articles_csv %}
{{ article['COLUMN_NAME'] }}
{% endfor %}
```

Replace 'COLUMN_NAME' with the actual column name from the respective CSV file that you want to include in the rendered
output.

### JSON Input Files

Similar to CSV files, each JSON file acts as an independent data source. In the template, the data from a JSON file can
be accessed by using the filename (without the extension) as a variable.

For example, if you have a data.json file, you can access its properties in the template as follows:

```
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

```
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

```csv
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

```
{% for article in articles_json %}{{article['SUPPLIER_AID']}}{{split}}{% endfor %}
```

## Jinja2 Filters in Templates

JinjaXcat provides [builtin Jinja2 filters](https://jinja.palletsprojects.com/en/3.1.x/templates/#builtin-filters)  that
you can use to manipulate and format data within your templates. These filters are available and can be used out of the
box.

In addition to the default filters, JinjaXcat also includes prebuilt custom filters and globals.
These filters and variables are specifically designed to enhance the capabilities of the templating engine and provide
additional functionality to your templates
Some of the prebuilt filters and globals available in JinjaXcat include:

- remove_accents: A filter that removes accents from text, useful for normalizing and cleaning up strings.
- current_datetime: A global that returns the current date and time, providing you with real-time information within
  your templates.
- custom_date: A global that allows you to generate custom-formatted dates, giving you control over the date
  representation in your templates.
- get_status_code: A global that retrieves the status code of an HTTP request, useful for fetching status_code from
  external APIs or web services.
- get_groups_with_articles: A global that retrieves groups with associated articles, useful for BMEcat catalogs to
  filter out groups without any articles.

As a developer, you can add custom filters and globals to JinjaXcat.
Simply define and register them within the CustomEnvironment class in the `.\utils\environment.py` file.
This allows you to enhance the templating engine to meet your specific needs and requirements.

The usage of filters and globals within a JinjaXcat template:

```XML
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
        The 'KEYWORDS' attribute is a comma-separated string, which is split into individual keywords for the loop. -->
        {% for keyword in article['KEYWORDS'].split(',') %}
        <KEYWORD>{{keyword.strip()}}</KEYWORD>
        {% endfor %}
    </ARTICLE_DETAILS>
</ARTICLE>{% endfor %}
```

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