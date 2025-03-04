import asyncio
from langchain_openai import AzureChatOpenAI
from dotenv import load_dotenv

from test_parser import get_test_suite_paths, get_test_suite, TestSuiteParseError
from test_parameters import get_test_parameters, TestParametersError
from test_secrets import get_test_secrets, TestSecretsError
from test_settings import get_test_settings, TestSettingsError
from test_runner import run_test_suite

load_dotenv()

async def main():
    try:
        test_suite_dir = './tests'
        test_secrets = get_test_secrets(test_suite_dir)
        test_parameters = get_test_parameters(test_suite_dir)
        test_suite_paths = get_test_suite_paths(test_suite_dir)
        test_settings = get_test_settings(test_suite_dir, test_secrets)
        test_results = list()

        model_settings = test_settings.model_settings
        llm = AzureChatOpenAI(
            model_name=model_settings.model,
            openai_api_key=model_settings.key,
            azure_endpoint=model_settings.endpoint,
            deployment_name=model_settings.deployment,
            api_version=model_settings.version
        )

        for test_suite_path in test_suite_paths:
            try:
                test_suite = get_test_suite(test_suite_path, test_parameters)
                test_suite_results = await run_test_suite(
                    llm=llm,
                    sensitive_data=test_secrets.sensitive_data,
                    test_suite=test_suite)

                test_results.append(test_suite_results)

            except TestSuiteParseError as e:
                print(e)

    except (TestParametersError, TestSecretsError, TestSettingsError, Exception) as e:
        print("A problem interrupted your test run:")
        print(e)

asyncio.run(main())