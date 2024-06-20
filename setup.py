from setuptools import setup, find_packages
import os

# Function to recursively find all files in a directory
def find_recursive(directory):
    paths = []
    for root, _, files in os.walk(directory):
        for file in files:
            paths.append(os.path.relpath(os.path.join(root, file), start=directory))
    return paths

# Read the requirements file to install dependencies
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

# Define additional directories to include (besides 'myproject')
extra_directories = ['frontend', 'feedbackhub']  # Add more if needed

# Collect all package directories
package_dirs = ['frontend', 'feedbackhub','myproject']

# Collect all files in these directories
package_data = {}
for dir_name in package_dirs:
    package_data[dir_name] = find_recursive(dir_name)

setup(
    name='myproject',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    package_data=package_data,
    install_requires=requirements,
    setup_requires=['wheel'],
    entry_points={
        'console_scripts': [
            'manage.py = manage:main',  # Replace with your actual entry point if different
        ],
    },
)
