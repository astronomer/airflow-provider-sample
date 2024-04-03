__version__ = "1.0.0"

## This is needed to allow Airflow to pick up specific metadata fields it needs for certain features.
def get_provider_info():
    return {
        "package-name": "airflow-provider-greenplum",  # Required
        "name": "Greenplum",  # Required
        "description": "A sample template for Apache Airflow providers.",  # Required
        "connection-types": [
            {
                "connection-type": "greenplum",
                "hook-class-name": "greenplum_provider.hooks.sample.GreenplumHook"
            }
        ],
        # "extra-links": ["greenplum_provider.operators.sample.GreenplumOperatorExtraLink"],
        "versions": [__version__],  # Required
    }
