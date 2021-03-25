"""Setup.py for the Astronomer sample Airflow provider package. Built from datadog provider package for now."""

from setuptools import find_packages, setup

<<<<<<< HEAD
logger = logging.getLogger(__name__)

version = '2020.10.29'

my_dir = dirname(__file__)

with open("README.md", "r") as fh:
    long_description = fh.read()

def do_setup(version_suffix_for_pypi=''):
    """Perform the package airflow-sample_provider setup."""
    setup(
        name='airflow-sample_provider',
        description='A sample provider for Astronomer.'
        'airflow-sample_provider for Apache Airflow',
        long_description=long_description,
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
        author='Pete DeJoy',
        author_email='pete@astronomer.io',
        url='http://astronomer.io/',
        python_requires='~=3.6',
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
=======
setup(
    name='airflow-provider-sample',
    description='A sample provider for Apache Airflow',
    long_description=
    long_description_content_type='text/markdown',
    license='Apache License 2.0',
    version='0.0.1',
    entry_points={
        "apache_airflow_provider": [
            "provider_info=sample_provider.__init__:get_provider_info"
        ]
    },
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
>>>>>>> 3dde2708ae9e3ad4b74dc5696361cae28fbf69bc
