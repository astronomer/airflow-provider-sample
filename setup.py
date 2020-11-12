"""Setup.py for the Astronomer sample Airflow provider package. Built from datadog provider package for now."""

from setuptools import find_packages, setup

setup(
    name='kairflow-sample_provider',
    description='A sample provider for Astronomer. airflow-sample_provider for Apache Airflow',
    long_description="Here is a long description for my sample provider",
    long_description_content_type='text/markdown',
    license='Apache License 2.0',
    version='0.0.1',
    packages=find_packages(),
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
