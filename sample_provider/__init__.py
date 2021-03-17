def get_provider_info():
    return {
        "package-name": "airflow-provider-sample",
        "name": "Sample Airflow Provider",
        "description": "A sample templat for airflow providers.",
        "hook-class-names": ["sample_provider.hooks.sample_hook.SampleHook"]
    }