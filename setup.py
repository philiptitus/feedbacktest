from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='myproject',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    setup_requires=['wheel'],  # Add setup_requires parameter here
    entry_points={
        'console_scripts': [
            'manage.py = manage:main',
        ],
    },
)
