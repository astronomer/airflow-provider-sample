"""Setup.py for the Astronomer sample Airflow provider package. Built from datadog provider package for now."""

from setuptools import find_packages, setup

version = '2020.10.29'

with open("README.md", "r") as fh:
    long_description = fh.read()

"""Perform the package airflow-sample_provider setup."""
setup(
    name='airflow-sample_provider',
    version="0.0.1",
    description='A sample provider for Astronomer.'
    'airflow-sample_provider for Apache Airflow',
    long_description=long_description,
    long_description_content_type='text/markdown',
    entry_points={
        "apache_airflow_provider": [
            "provider_info=sample_provider.__init__:get_provider_info"
        ]
    },
    license='Apache License 2.0',
    packages=find_packages(include=['*']),
    zip_safe=False,
    install_requires=['apache-airflow>=2.0'],
    setup_requires=['setuptools', 'wheel'],
    author='Pete DeJoy',
    author_email='pete@astronomer.io',
    url='http://astronomer.io/',
    python_requires='~=3.7',
)
