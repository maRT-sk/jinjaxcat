# This script is for quick debugging of Jinja2 templates. To execute this script and see the output, run:
# .\venv\Scripts\python.exe .\jinja_debug\jinja_render.py

from jinja2 import Environment, FileSystemLoader

# Define a sample data structure that mimics the expected shape of data that we use in JinjaXcat
context = {'products':
    [
        {'Name': 'Laptop', 'Price': 1200},
        {'Name': 'Smartphone', 'Price': 800},
        {'Name': 'Headphones', 'Price': 150},
        {'Name': 'Tablet', 'Price': 400},
        {'Name': 'Smartwatch', 'Price': 250}
    ]
}

# Set up a Jinja2 environment optimized for clean template rendering
env = Environment(loader=FileSystemLoader('jinja_debug'),
                  trim_blocks=True,
                  lstrip_blocks=True,
                  )

template = env.get_template('render_demo_input.txt')  # Load the template file named 'render_demo_input.txt'
rendered_string = template.render(context)  # Render the template using the 'context' defined above.
print(rendered_string)  # Print the rendered string to the console.
# Save the rendered string to an output file named 'render_demo_output.txt'.
with open('jinja_debug/render_demo_output.txt', 'w') as output_file:
    output_file.write(rendered_string)