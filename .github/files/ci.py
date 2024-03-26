import action_lib

env = action_lib.OCIEnvIntegrationTest(
    envs=[
        {
            "env_file": "standalone.compose.env",
            "run_tests": False,
            "db_restore": None,
        }
    ]
)
