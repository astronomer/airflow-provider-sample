<p align="center">
  <a href="https://www.airflow.apache.org">
    <img alt="Airflow" src="https://cwiki.apache.org/confluence/download/attachments/145723561/airflow_transparent.png?api=v2" width="60" />
  </a>
</p>
<h1 align="center">
  Airflow Sample Provider
</h1>
  <h3 align="center">
  Guidelines on building, deploying, and maintaining provider packages that will help Airflow users interface with external systems. Maintained with ❤️ by Astronomer.
</h3>

<br/>

This repository provides best practices for building, structuring, and deploying Airflow provider packages as independent python modules available on PyPI.

Provider repositories must be public on Github and follow the structural and technical guidelines laid out in this Readme. Ensure that all of these requirements have been met before submitting a provider package for community review.

Here, you'll find information on requirements and best practices for key aspects of your project:

- File formatting
- Development
- Airflow integration
- Documentation
- Testing

## Formatting Standards

Before writing and testing the functionality of your provider package, ensure that your project follows these formatting conventions.

### Package name

The highest level directory in the provider package should be named in the following format:

```
airflow-provider-<provider-name>
```

### Repository structure

All provider packages must adhere to the following file structure:

```bash
├── LICENSE # A license is required, MIT or Apache is preferred.
├── README.md
├── sample_provider # Your package import directory. This will contain all Airflow modules and example DAGs.
│   ├── __init__.py
│   ├── example_dags
│   │   └── sample.py
│   ├── hooks
│   │   ├── __init__.py
│   │   └── sample.py
│   ├── operators
│   │   ├── __init__.py
│   │   └── sample.py
│   └── sensors
│       ├── __init__.py
│       └── sample.py
├── setup.py # A setup.py file to define dependencies and how the package is built and shipped. If you'd like to use setup.cfg, that is fine as well.
└── tests # Unit tests for each module.
    ├── __init__.py
    ├── hooks
    │   ├── __init__.py
    │   └── test_sample_hook.py
    ├── operators
    │   ├── __init__.py
    │   └── test_sample_operator.py
    └── sensors
        ├── __init__.py
        └── test_sample_sensor.py
```


## Development Standards

If you followed the formatting guidelines above, you're now ready to start editing files to include standard package functionality.

### Python Packaging Scripts

Your `setup.py` file should contain all of the appropriate metadata and dependencies required to build your package. Use the [sample `setup.py` file](https://github.com/astronomer/airflow-provider-sample/blob/main/setup.py) in this repository as a starting point for your own project.

If some of the options for building your package are variables or user-defined, you can specify a `setup.cfg` file instead.

To improve discoverability of your provider package on PyPI, it is recommended to [add classifiers](https://packaging.python.org/en/latest/tutorials/packaging-projects/#configuring-metadata) to the package's metadata. The following standard classifiers should be used in addition to any others you may choose to include:

- Framework :: Apache Airflow
- Framework :: Apache Airflow :: Provider

### Managing Dependencies

When building providers, these guidelines will help you avoid potential for dependency conflicts:

- It is important that the providers do not include dependencies that conflict with the underlying dependencies for a particular Airflow version. All of the default dependencies included in the core Airflow project can be found in the Airflow [setup.py file](https://github.com/apache/airflow/blob/master/setup.py#L705).
- Keep all dependencies relaxed at the upper bound. At the lower bound, specify minor versions (for example, `depx >=2.0.0, <3`).

### Versioning

Use standard semantic versioning for releasing your package. When cutting a new release, be sure to update all of the relevant metadata fields in your setup file.

### Building Modules

All modules must follow a specific set of best practices to optimize their performance with Airflow:

- **All classes should always be able to run without access to the internet.** The Airflow Scheduler parses DAGs on a regular schedule. Every time that parse happens, Airflow will execute whatever is contained in the `init` method of your class. If that `init` method contains network requests, such as calls to a third party API, there will be problems due to repeated network calls.
- **Init methods should never call functions which return valid objects only at runtime**. This will cause a fatal import error when trying to import a module into a DAG. A common best practice for referencing connectors and variables within DAGs is to use [Jinja Templating](https://airflow.apache.org/docs/apache-airflow/stable/concepts.html#jinja-templating).
- **All operator modules need an `execute` method.** This method defines the logic that the operator will implement.

Modules should also take advantage of native Airflow features that allow your provider to:

- Register custom connection types, which improve the user experience when connecting to your tool.
- Include `extra-links` that link your provider back to its page on the Astronomer Registry. This provides users easy access to documentation and example DAGs.

Refer to the `Airflow Integration Standards` section for more information on how to build in these extra features.

### Unit testing

Your top-level `tests/` folder should include unit tests for all modules that exist in the repository. You can write tests in the framework of your choice, but the Astronomer team and Airflow community typically use [pytest](https://docs.pytest.org/en/stable/).

You can test this package by running: `python3 -m unittest` from the top-level of the directory.

## Airflow Integration Standards

Airflow exposes a number of plugins to interface from your provider package. We highly encourage provider maintainers to add these plugins because they significantly improve the user experience when connecting to a provider.

### Defining an entrypoint

To enable custom connections, you first need to define an `apache_airflow_provider ` entrypoint in your `setup.py` or `setup.cfg` file:

```
entry_points={
  "apache_airflow_provider": [
      "provider_info=sample_provider.__init__:get_provider_info"
        ]
    }
```

Next, you need to add a `get_provider_info` method to the `__init__` file in your top-level provider folder. This function needs to return certain metadata associated with your package in order for Airflow to use it at runtime:

```python
def get_provider_info():
    return {
        "name": "Sample Apache Airflow Provider",  # Required
        "description": "A sample template for Apache Airflow providers.",  # Required
        "connection-types": [
            {"connection-type": "sample", "hook-class-name": "sample_provider.hooks.sample.SampleHook"}
        ],
        "versions": ["1.0.0"] # Required
    }
```

Once you define the entrypoint, you can use native Airflow features to expose custom connection types in the Airflow UI, as well as additional links to relevant documentation.

### Adding Custom Connection Forms

Airflow enables custom connection forms through discoverable hooks. The following is an example of a custom connection form for the Fivetran provider:

<img src="https://user-images.githubusercontent.com/63181127/112921463-d07b2880-90d8-11eb-871b-fc4e1c6cade9.png" width="600" />

Add code to the hook class to initiate a discoverable hook and create a custom connection form. The following code defines a hook and a custom connection form:

```python
class ExampleHook(BaseHook):
    """ExampleHook docstring..."""

    conn_name_attr = 'example_conn_id'
    default_conn_name = 'example_default'
    conn_type = 'example'
    hook_name = 'Example'

    @staticmethod
    def get_connection_form_widgets() -> Dict[str, Any]:
        """Returns connection widgets to add to connection form"""
        from flask_appbuilder.fieldwidgets import BS3PasswordFieldWidget, BS3TextFieldWidget
        from flask_babel import lazy_gettext
        from wtforms import PasswordField, StringField, BooleanField

        return {
            "bool": BooleanField(lazy_gettext('Example Boolean')),
            "account": StringField(
                lazy_gettext('Account'), widget=BS3TextFieldWidget()
            ),
            "secret_key": PasswordField(
                lazy_gettext('Secret Key'), widget=BS3PasswordFieldWidget()
            ),
        }

    @staticmethod
    def get_ui_field_behaviour() -> Dict:
        """Returns custom field behaviour"""
        import json

        return {
            "hidden_fields": ['port'],
            "relabeling": {},
            "placeholders": {
                'extra': json.dumps(
                    {
                        "example_parameter": "parameter",
                    },
                    indent=4,
                ),
                'host': 'example hostname',
                'schema': 'example schema',
                'login': 'example username',
                'password': 'example password',
                'account': 'example account name',
                'secret_key': 'example secret key',
            },
        }
 ```

Some notes about using custom connections:

- `get_connection_form_widgets()` creates extra fields using flask_appbuilder. A variety of field types can be created using this function, such as strings, passwords, booleans, and integers.

- `get_ui_field_behaviour()` is a JSON schema describing the form field behavior. Fields can be hidden, relabeled, and given placeholder values.

- To connect a form to Airflow, add the hook class name and connection type of a discoverable hook to `"connection-types"` in the `get_provider_info` method as mentioned in `Defining an entrypoint`.

### Adding Custom Links

Operators can add custom links that users can click to reach an external source when interacting with an operator in the Airflow UI. This link can be created dynamically based on the context of the operator. The following code example shows how to initiate an extra link within an operator:

```python
from airflow.models import BaseOperator, BaseOperatorLink

class ExampleLink(BaseOperatorLink):
    """Link for ExmpleOperator"""

    name = 'Example Link'

    def get_link(self, operator: BaseOperator, *, ti_key=None):
        """Get link to registry page."""

        registry_link = "https://{example}.com"
        return registry_link.format(example='example')

class ExampleOperator(BaseOperator):
    """ExampleOperator docstring..."""

    operator_extra_links = (Example_Link(),)
```

To connect custom links to Airflow, add the operator class name to `"extra-links"` in the `get_provider_info` method mentioned above.

## Documentation Standards

Creating excellent documentation is essential for explaining the purpose of your provider package and how to use it.

### Inline Module Documentation

Every Python module, including all hooks, operators, sensors, and transfers, should be documented inline via [sphinx-templated docstrings](https://pythonhosted.org/an_example_pypi_project/sphinx.html). These docstrings should be included at the top of each module file and contain three sections separated by blank lines:
- A one-sentence description explaining what the module does.
- A longer description explaining how the module works. This can include details such as code blocks or blockquotes. For more information Sphinx markdown directives, read the [Sphinx documentation](https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html#directive-code-block).
- A declarative definition of parameters that you can pass to the module, templated per the example below.

For a full example of inline module documentation, see the [example operator in this repository](https://github.com/astronomer/airflow-provider-sample/blob/main/sample_provider/operators/sample_operator.py#L11).

### README

The README for your provider package should give users an overview of what your provider package does. Specifically, it should include:

- High-level documentation about the provider's service.
- Steps for building a connection to the service from Airflow.
- What modules exist within the package.
- An exact set of dependencies and versions that your provider has been tested with.
- Guidance for contributing to the provider package.

## Functional Testing Standards

To build your repo into a python wheel that can be tested, follow the steps below:

1. Clone the provider repo.
2. `cd` into provider directory.
3. Run `python3 -m pip install build`.
4. Run `python3 -m build` to build the wheel.
5. Find the .whl file in `/dist/*.whl`.
6. Download the [Astro CLI](https://github.com/astronomer/astro-cli).
7. Create a new project directory, cd into it, and run `astro dev init` to initialize a new astro project.
8. Ensure the Dockerfile contains the Airflow 2.0 image:

   ```
   FROM quay.io/astronomer/ap-airflow:2.0.0-buster-onbuild
   ```

9. Copy the `.whl` file to the top level of your project directory.
10. Install `.whl` in your containerized environment by adding the following to your Dockerfile:

   ```
   RUN pip install --user airflow_provider_<PROVIDER_NAME>-0.0.1-py3-none-any.whl
   ```

11. Copy your sample DAG to the `dags/` folder of your astro project directory.
12. Run `astro dev start` to build the containers and run Airflow locally (you'll need Docker on your machine).
13. When you're done, run `astro dev stop` to wind down the deployment. Run `astro dev kill` to kill the containers and remove the local Docker volume. You can also use `astro dev kill` to stop the environment before rebuilding with a new `.whl` file.

> Note: If you are having trouble accessing the Airflow webserver locally, there could be a bug in your wheel setup. To debug, run `docker ps`, grab the container ID of the scheduler, and run `docker logs <scheduler-container-id>` to inspect the logs.

## Publishing your Provider repository for the Astronomer Registry

If you have never submitted your Provider repository for publication to the Astronomer Registry, [create a new release/tag for your repository](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository) on the `main` branch. Ultimately, the backend of the Astronomer Registry will check for new tags for a Provider repository to trigger adding the new version of the Provider on the Registry.

> **NOTE:** Tags for the repository must follow typical [semantic versioning](https://semver.org/).

Now that you've created a release/tag, head over to the [Astronomer Registry](https://registry.astronomer.io) and [fill out the form](https://registry.astronomer.io/publish) with your shiny new Provider repo details!

If your Provider is currently on the Astronomer Registry, simply create a new release/tag will trigger an update to the Registry and the new version will be published.
