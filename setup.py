from setuptools import setup, find_packages

# Read the requirements file to install dependencies
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='myproject',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        '': ['*.*'],  # Include all files in the wheel
    },
    install_requires=requirements,
    setup_requires=['wheel'],  # Ensures wheel is available during setup
    entry_points={
        'console_scripts': [
            'manage.py = manage:main',  # Replace with your actual entry point if different
        ],
    },
)
