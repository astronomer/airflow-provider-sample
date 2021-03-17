"""Setup.py for the Astronomer sample Airflow provider package. Built from datadog provider package for now."""

from setuptools import find_packages, setup

setup(
    name='airflow-provider-sample',
    description='A sample provider for Apache Airflow',
    long_description=
    long_description_content_type='text/markdown',
    license='Apache License 2.0',
    version='0.0.1',
    ## This is needed to allow Airflow to pick up specific metadata fields it needs for certain features
    entry_points='''
        [apache_airflow_provider]
        provider_info=sample_provider.__init__:get_provider_info
    ''',
    packages=find_packages(),
    zip_safe=False,
    install_requires=['apache-airflow~=1.10'],
    setup_requires=['setuptools', 'wheel'],
    extras_require={},
    author='Pete DeJoy',
    author_email='pete@astronomer.io',
    url='http://astronomer.io/',
    python_requires='~=3.6',
)
