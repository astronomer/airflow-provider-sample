"""Setup.py for the Astronomer sample Airflow provider package."""

import logging
import os
import sys
from os.path import dirname

from setuptools import find_packages, setup

logger = logging.getLogger(__name__)

version = '2020.10.29'

my_dir = dirname(__file__)


def do_setup(version_suffix_for_pypi=''):
    """Perform the package apache-airflow-backport-providers-datadog setup."""
    setup(
        name='airflow-astronomer-sample-provider',
        description='A sample provider for Astronomer.'
        'airflow-astronomer-sample-provider for Apache Airflow',
        long_description="Here is a long description for my sample provider",
        long_description_content_type='text/markdown',
        license='Apache License 2.0',
        version=version + version_suffix_for_pypi,
        packages=find_packages(include=['*']),
        zip_safe=False,
        install_requires=['apache-airflow~=1.10'],
        setup_requires=['setuptools', 'wheel'],
        extras_require={},
        classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Environment :: Console',
            'Environment :: Web Environment',
            'Intended Audience :: Developers',
            'Intended Audience :: System Administrators',
            'License :: OSI Approved :: Apache Software License',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Topic :: System :: Monitoring',
        ],
        author='Apache Software Foundation',
        author_email='dev@airflow.apache.org',
        url='http://airflow.apache.org/',
        download_url=('https://archive.apache.org/dist/airflow/backport-providers'),
        python_requires='~=3.6',
        project_urls={
            'Documentation': 'https://airflow.apache.org/docs/',
            'Bug Tracker': 'https://github.com/apache/airflow/issues',
            'Source Code': 'https://github.com/apache/airflow',
        },
    )


#
# Note that --version-suffix-for-pypi should only be used in case we generate RC packages for PyPI
# Those packages should have actual RC version in order to be published even if source version
# should be the final one.
#
if __name__ == "__main__":
    suffix = ''
    if len(sys.argv) > 1 and sys.argv[1] == "--version-suffix-for-pypi":
        if len(sys.argv) < 3:
            print("ERROR! --version-suffix-for-pypi needs parameter!", file=sys.stderr)
            sys.exit(1)
        suffix = sys.argv[2]
        sys.argv = [sys.argv[0]] + sys.argv[3:]
    do_setup(version_suffix_for_pypi=suffix)