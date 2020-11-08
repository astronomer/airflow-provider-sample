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

## Readme Structure

Readmes will need to be structured in a way that is logical and compliant.

## Module Documentation

Modules will be documented via docstrings at the top of each module.py file. These will include a high-level overview of the operator purpose and the available params.