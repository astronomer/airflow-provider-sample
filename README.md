# Airflow Sample Provider

This repository is intended to demonstrate a well-defined set of rules and best practices for building, structuring, and deploying Airflow provider packages as independent python modules available on pypi.

## Naming Convention

All provider repositories must be public on github and must follow the naming convention `airflow-provider_name`. The package must be named the same way such that a user can `pip install airflow-provider_name` to make the provider package available to the user.

## Repository Structure

In building out a provider package repo, there are a few structural elements that you need. 

```bash
├── LICENSE # A license is required, MIT or Apache is preferred
├── README.md # A clear and descriptive readme that follows the standards defined below
├── examples # A directory for example DAGs using this provider in context
│   └── sample-dag.py
├── modules # A modules directory that contains all Airflow hooks, operators, sensors, transfers, etc.
│   ├── hooks
│   │   ├── __init__.py
│   │   └── sample_hook.py
│   ├── operators
│   │   ├── __init__.py
│   │   └── sample_operator.py
│   └── sensors
│       ├── __init__.py
│       └── sample_sensor.py
├── setup.cfg # A setup.cfg file
└── setup.py # A setup.py file to define dependencies and how the package is built and shipped
```

## Provider Readmes

Readmes will need to be structured in a way that is logical and compliant. This is a bit confusing since _this_ Readme is not compliant with it's own rules, but [there is a sample readme that demonstrates correct structure here](./SAMPLE_README.md).They will adhere to the following standards:
- H1 at the top of the markdown file should read `<Provider Name> Airflow Provider
- Under the H1 must be a short overview of the provider's tool and what it does.
- There must be an H2 `Modules` section that lists and links to the available modules in the repository with a short description.
- There must be an H2 `Compatibility` section with a table that demonstrates compatibility with Airflow versions.

## Module Documentation

Provider modules, including all hooks, operators, sensors, and transfers, will be documented via docstrings at the top of each of their respective python file. These will include a high-level overview of the operator purpose and the available params- [see here for an example of what that should look like](https://github.com/astronomer/airflow-sample_provider/blob/main/modules/operators/sample_operator.py#L11).

## Development Standards

### Managing Dependencies

[All of the default dependencies included in the core Airflow project can be found here.](https://github.com/apache/airflow/blob/master/setup.py#L705) When building providers, defined compatibility with specific Airflow versions is required. It's important that the providers do not include dependencies that conflict with the underlying dependencies for a particular Airflow version.

Additionally, there are a few rules to adhere to when considering adding dependencies to your provider package in your `setup.py` file. These rules are intended to avoid conflicts between various provider packages that may be imported and used in the same Airflow instance:
1. Rule 1
2. Rule 2
3. Rule 3

### Writing Tests

Information on writing tests for modules here.


## Building Your Package

To build your repo into a python wheel that can then be deployed to [PyPi](https://pypi.org), we use [setuptools](https://pypi.org/project/setuptools/).

Once your `setup.py` file is set up, you can run the following command to build a local version of your wheel off of your project directory:

```bash
python setup.py bdist_wheel
```

Once you have the local wheel built, you can deploy it to PyPi for broader distribution.