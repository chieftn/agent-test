import asyncio
import os
from langchain_openai import AzureChatOpenAI
from dotenv import load_dotenv

from test_parser import get_test_suite_paths, get_test_suite, get_test_suite_configuration, TestSuiteParseError
from test_configuration import get_test_suite_configuration, TestConfigurationError
from test_runner import run_test_suite

load_dotenv()

azure_openai_api_key = os.environ.get('AZURE_OPENAI_KEY')
azure_openai_endpoint = os.environ.get('AZURE_OPENAI_ENDPOINT')
azure_openai_api_model = os.environ.get('AZURE_OPENAI_MODEL')
azure_openai_api_deployment = os.environ.get('AZURE_OPENAI_DEPLOYMENT')
azure_openai_api_version = os.environ.get('AZURE_OPENAI_VERSION')

async def main():
    try:
        llm = AzureChatOpenAI(
            model_name=azure_openai_api_model,
            openai_api_key=azure_openai_api_key,
            azure_endpoint=azure_openai_endpoint,
            deployment_name=azure_openai_api_deployment,
            api_version=azure_openai_api_version
        )

        test_suite_dir = './tests'
        test_config = get_test_suite_configuration(test_suite_dir)
        test_suite_paths = get_test_suite_paths(test_suite_dir)
        test_results = list()

        for test_suite_path in test_suite_paths:
            try:
                test_suite = get_test_suite(test_suite_path, test_config)
                test_suite_results = await run_test_suite(llm, test_suite)
                test_results.append(test_suite_results)

            except TestSuiteParseError as e:
                print(e)

    except TestConfigurationError as e:
        print(e)

    except Exception as e:
        print("A problem interrupted your test run:")
        print(e)

asyncio.run(main())