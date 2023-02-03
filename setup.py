"""Setup.py for the Astronomer sample Airflow provider package. Built from datadog provider package for now."""

from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

__version__ = "1.0.0"

"""Perform the package airflow-provider-sample setup."""
setup(
    name="airflow-provider-sample",
    version=__version__,
    description="A sample Apache Airflow provider package built by Astronomer.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    entry_points={"apache_airflow_provider": ["provider_info=sample_provider.__init__:get_provider_info"]},
    license="Apache License 2.0",
    packages=find_packages(exclude=["*tests.*", "*tests"]),
    install_requires=["apache-airflow>=2.3"],
    setup_requires=["setuptools", "wheel"],
    author="Pete DeJoy",
    author_email="pete@astronomer.io",
    url="https://astronomer.io/",
    classifiers=[
        "Framework :: Apache Airflow",
        "Framework :: Apache Airflow :: Provider",
    ],
    python_requires="~=3.8",
)
