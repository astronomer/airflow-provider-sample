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

This repository demonstrates best practices for building, structuring, and deploying Airflow provider packages as independent python modules available on PyPI.

## Requirements

Provider repositories must be public on Github and follow the structural and technical guidelines laid out in this Readme.

The package must be named as `airflow-provider-<provider-name>`.

> Note: If the provider repo sits inside an organization the `provider-name` should be the same as the organization name.

## Repository Structure

You'll need this package structure to construct a provider package repo:

```bash
├── LICENSE # A license is required, MIT or Apache is preferred.
├── README.md
├── sample_provider # Your package import directory. This will contain all Airflow modules and example DAGs.
│   ├── __init__.py
│   ├── example_dags
│   │   ├── __init__.py
│   │   └── sample-dag.py
│   ├── hooks
│   │   ├── __init__.py
│   │   └── sample_hook.py
│   ├── operators
│   │   ├── __init__.py
│   │   └── sample_operator.py
│   └── sensors
│       ├── __init__.py
│       └── sample_sensor.py
├── setup.py # A setup.py file to define dependencies and how the package is built and shipped. If you'd like to use setup.cfg, that is fine as well.
└── tests # Unit tests for each module.
    ├── hooks
    │   └── sample_hook_test.py
    ├── operators
    │   └── sample_operator_test.py
    └── sensors
        └── sample_sensor_test.py
```


## Development Standards

### Building Provider Package

Most of what you need is included in `setup.py` and ready to customize. You may use `setup.cfg` as a valid alternative.

### Provider Readmes

Readmes should contain top-level documentation about the provider's service, how to build a connection to the service from Airflow, what modules exist within the package, what dependency versions the provider has been tested with, and how the repository maintainers would like folks to contribute.

#### Managing Dependencies

When building providers, these guidelines will help you avoid potential for dependency conflicts.

1. It is important that the providers do not include dependencies that conflict with the underlying dependencies for a particular Airflow version. [All of the default dependencies included in the core Airflow project can be found here.](https://github.com/apache/airflow/blob/master/setup.py#L705)
2. Keep all dependencies upper-bound relaxed; at least allow minor versions, ie. `depx >=2.0.0, <3`. Please include a section in your Readme with the exact set of dependencies that your provider package has been tested with.

#### Versioning

Maintainers should use standard semantic versioning for releasing their packages. They should be sure to update all of the relevant metadata fields before cutting a new release.

### Building Modules

All modules should follow a specific set of best practices that optimize for how they will run in the context of Airflow.
- **All classes should run without access to the internet.** The Airflow scheduler parses DAGs on a regular schedule. Every time that parse happens, Airflow will execute whatever is contained in the `init` method of your class. If that `init` method contains network requests, such as calls to a third party API, there will be problems due to repeated network calls.
- **Init methods should not call functions which only return valid objects at runtime**. This will cause a fatal import error when trying to import a module into a DAG. A common pattern to reference connectors and variables within DAGs is to use [Jinja Templating](https://airflow.apache.org/docs/apache-airflow/stable/concepts.html#jinja-templating).
- **All operator modules will need an `execute` method.** This method defines the logic that the operator will implement.

Modules should also take advantage of native Airflow features that allow your provider to:
- Register custom conn types for a great UX around connecting to your tool.
- Include `extra-links` that link your provider back to its page on the Astronomer Registry for easy user access to documentation and example DAGs.

See the `Airflow Integration` section below for more information on how to build for these extra features.

### Testing Modules

The provider should contain a top-level `tests/` folder that contains unit tests for all modules that exist in the repository. Maintainers may write tests in the framework of their choice- the Astronomer team and Airflow community typically uses [pytest](https://docs.pytest.org/en/stable/).

### Module Documentation

Provider modules, including all hooks, operators, sensors, and transfers, should be documented via [sphinx-templated docstrings](https://pythonhosted.org/an_example_pypi_project/sphinx.html) at the top of each of their respective python file. These docstrings should include three things, all separated by blank lines in the docstring:
1. A one-sentence description explaining *what* the module does.
2. A long description explaining *how* the module works. This can include more verbose language or documentation, including code blocks or blockquotes. You can read about available Sphinx markdown directives [here](https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html#directive-code-block).
3. A declarative definition of parameters that you can pass to the module, templated per the example below.

[See here for an active example](https://github.com/astronomer/airflow-sample_provider/blob/main/modules/operators/sample_operator.py#L11).

## Integrating with Airflow

Airflow exposes a number of plugins to interface from your provider package in case you care to do so. We *highly* encourage provider maintainers to add these bits, as they improve the UX of a provider significantly.

To start, you'll need to define an `apache_airflow_provider ` entrypoint in your `setup.py` or `setup.cfg` file:

```    
entry_points={
  "apache_airflow_provider": [
      "provider_info=sample_provider.__init__:get_provider_info"
        ]
    }
```

Next, you'll need to add a `get_provider_info` method to [the `__init__` file in your top-level provider folder](./sample_provider/__init__.py). This function needs to return certain metadata associated with your package in order for Airflow to be able to pick it up. We are aware it's not completely ideal to define some of this metadata in a location separate from your `setup.py` file, but Airflow needs this function at runtime for its plugins to pick up the necessary information:

```python
def get_provider_info():
    return {
        "package-name": "airflow-provider-sample",
        "name": "Sample Airflow Provider", # Required
        "description": "A sample template for airflow providers.", # Required
        "hook-class-names": ["sample_provider.hooks.sample_hook.SampleHook"],
        "extra-links": ["sample_provider.operators.sample_operator.ExtraLink"]
        "versions": ["0.0.1"] # Required
    }
```

Once you define the entrypoint, you can leverage Airflow's native features to expose custom connection types in the Airflow UI and additional links to relevant pages of documentation and information.

### Adding Custom Connections

Airflow allows for custom connection forms through discoverable hooks. Below is an example of a custom connection form for the Fivetran provider.

<img src="https://user-images.githubusercontent.com/63181127/112665235-36458700-8e31-11eb-8fb5-ecf26e8a8323.png" width="600" />

Add code to the hook class to initiate a discoverable hook and create a custom connection form. The following is an example of this code.

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
            "extra__example__bool": BooleanField(lazy_gettext('Example Boolean')),
            "extra__example__account": StringField(
                lazy_gettext('Account'), widget=BS3TextFieldWidget()
            ),
            "extra__example__secret_key": PasswordField(
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
                    indent=1,
                ),
                'host': 'example hostname',
                'schema': 'example schema',
                'login': 'example username',
                'password': 'example password',
                'extra__example__account': 'example account name',
                'extra__example__secret_key': 'example secret key',
            },
        }
 ```

`get_connection_form_widgets()` creates extra fields using flask_appbuilder. A field created this way must be named `extra__<conn_type>__<field_name>`. A veriety of field types can be created such as text, password, boolian, intiger, etc..

`get_ui_field_behaviour()` is a JSON schema describing the form field behavior. Fields can be hidden, relabeled, and be given placeholders.

Add the hook class name of a discoverable hook to `"hook-class-names"` in the `get_provider_info` method mentioned above.
 
### Adding Extra Links

Operators can have extra links that users can use to reach an external source from the Airflow UI when interacting with an operator. This link can be created dynamically based on the context of the operator. The following code example shows how to initiate an extra link within an operator.

```python
class ExampleLink(BaseOperatorLink):
    """Link for ExmpleOperator"""

    name = 'Example Link'

    def get_link(self, operator, dttm):
        """Get link to registry page."""

        registry_link = "https://{example}.com"
        return registry_link.format(example='example')

class ExampleOperator(BaseOperator):
    """ExampleOperator docstring..."""

    operator_extra_links = (Example Link(),)
```

Add the operator class name to `"extra-links"` in the `get_provider_info` method mentioned above to initiate the extra link.

## Testing Your Package

To build your repo into a python wheel that can be tested, follow the steps below:

1. Clone the provider repo
2. cd into provider directory
3. Run `python3 -m pip install build`
4. Run `python3 -m build` to build the wheel
5. Find the .whl file in `/dist/*.whl`
6. Download the [Astro CLI](https://github.com/astronomer/astro-cli)
7. Create a new project directory, cd into it, and run `astro dev init` to initialize a new astro project
8. Ensure the Dockerfile contains Airflow 2.0: `FROM quay.io/astronomer/ap-airflow:2.0.0-buster-onbuild`
9. Copy `.whl` file to the top-level of your Astro project
10. Add the `.whl` file to the Dockerfile: `RUN pip install --user airflow_provider_<PROVIDER_NAME>-0.0.1-py3-none-any.whl` to install the wheel into the containerized operating environment.
11. Copy your sample DAG to the `dags/` folder of your astro project directory.
12. Run `astro dev start` to build the containers and run Airflow locally (you'll need Docker on your machine).
13. When you're done, run `astro dev stop` to wind down the deployment. Run `astro dev kill` to kill the containers and remove the local Docker volumes- use this command if you need to rebuild the environment with a new `.whl` file.

> Note: If you are having trouble accessing the Airflow webserver locally, there could be a bug in your wheel setup. To debug, run `docker ps`, grab the container ID of the scheduler, and run `docker logs <scheduler-container-id>` to see the issue.

Once you have the local wheel built and tested, you're ready to [send us your repo](https://registry.astronomer.io/publish-rovider) to be published on [The Astronomer Registry](https://registry.astronomer.io).

