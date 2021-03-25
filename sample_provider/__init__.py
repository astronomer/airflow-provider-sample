## This is needed to allow Airflow to pick up specific metadata fields it needs for certain features. We recognize it's a bit unclean to define these in multiple places, but at this point it's the only workaround if you'd like your custom conn type to show up in the Airflow UI.
def get_provider_info():
    return {
        "package-name": "airflow-provider-sample",
        "name": "Sample Airflow Provider",
        "description": "A sample templat for airflow providers.",
        "hook-class-names": ["sample_provider.hooks.sample_hook.SampleHook"]
    }