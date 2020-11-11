<p align="center">
  <a href="https://www.airflow.apache.org">
    <img alt="Airflow" src="https://cwiki.apache.org/confluence/download/attachments/145723561/airflow_transparent.png?api=v2" width="60" />
  </a>
</p>
<h1 align="center">
  Airflow Sample Provider
</h1>
  <h3 align="center">
  Guildelines on building, deploying, and maintaining provider packages that will help Airflow users interface with external systems. Maintained with ❤️ by Astronomer.
</h3>

<br/>

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

### Building Modules

All modules built should follow a specific set of best practices that optimize for how they will run in the context of Airflow.
- **All classes should run without access to the internet.** This is because the Airflow scheduler parses DAGs on a regular schedule; every time that parse happens, Airflow will execute whatever is contained in the `init` method of your class. If that `init` method contains network requests, such as calls to a third party API, there will be problems due to how frequently Airflow parses the DAG file.
- **All operator modules will need an `execute` method.** This method will define the logic that will be implemented by the operator.

### Writing Tests

Information on writing tests for modules here.

### Managing Dependencies

When building providers, a few rules should be followed to remove potential for dependency conflicts.

1. It is important that the providers do not include dependencies that conflict with the underlying dependencies for a particular Airflow version. [All of the default dependencies included in the core Airflow project can be found here.](https://github.com/apache/airflow/blob/master/setup.py#L705)
2. Keep all dependencies upper-bound relaxed; at least allow minor versions, ie. `depx >=2.0.0, <3`. Publish a contraint file with the exact set of dependencies that your provider package has been tested with.

### Versioning

Maintainers should use standard semantic versioning for releasing their packages.

## Building Your Package

To build your repo into a python wheel that can then be deployed to [PyPi](https://pypi.org), we use [setuptools](https://pypi.org/project/setuptools/).

Once your `setup.py` file is set up, you can run the following command to build a local version of your wheel off of your project directory:

```bash
python setup.py bdist_wheel
```

Once you have the local wheel built, you can deploy it to PyPi for broader distribution.

### Automated Builds

Add section on automatically building and deploying package with CI here.