import asyncio
from pathlib import Path
import toml
import os
from langchain_openai import AzureChatOpenAI
from browser_use.agent.service import Agent
from browser_use.browser.browser import Browser
from browser_use.browser.context import BrowserContextConfig, BrowserContext
from dotenv import load_dotenv

class Test:
    def __init__(self, name, act):
        self.name = name
        self.act = act

class TestSeries:
    def __init__(self, name, tests: list[Test]):
        self.name = name
        self.tests = tests

class TestSuite:
    def __init__(self, name: str, test_series: list[TestSeries]):
        self.name = name
        self.series = test_series


def get_test_suites(directory: str):
    path = Path(directory)
    file_extension = '.toml'

    path_list = list(path.rglob(f'*{file_extension}'))
    return list(map(get_test_suite, path_list))

def get_test_suite(path: Path):
    with open(path, 'r') as f:
        config = toml.load(f)

    test_series = [TestSeries]
    for index in range(len(config['describe'])):
        series_content = config['describe'][index]

        series_name = series_content['name']
        test_list = [Test]

        for index in range(len(series_content['it'])):
            test_content = series_content['it'][index]

            test_name = test_content['name']
            test_act = test_content['act']

            test_list.append(Test(test_name, test_act))

        test_series.append(TestSeries(series_name, test_list))

    return TestSuite(path.name, test_series)

async def run_test_suite(test_suite: TestSuite):
    for test_series in test_suite.series:
        print(dir(test_series))
        await run_test_series(test_series)

async def run_test_series(test_series: TestSeries):
    browser = Browser()

    async with await browser.new_context(
        config=BrowserContextConfig(trace_path='./tmp/traces/')
    ) as context:
        print(dir(test_series))
        # for test in test_series.tests:
        #     await run_test(context, test)

    await browser.close()

async def run_test(context: BrowserContext, test: Test):
    agent = Agent(
        task=test.act,
        llm=llm,
        context=context
    )

    print(agent)
    # await agent.run()

load_dotenv()
azure_openai_api_key = os.environ.get('AZURE_OPENAI_KEY')
azure_openai_endpoint = os.environ.get('AZURE_OPENAI_ENDPOINT')
azure_openai_api_model = os.environ.get('AZURE_OPENAI_MODEL')
azure_openai_api_deployment = os.environ.get('AZURE_OPENAI_DEPLOYMENT')
azure_openai_api_version = os.environ.get('AZURE_OPENAI_VERSION')

llm = AzureChatOpenAI(
    model_name=azure_openai_api_model,
    openai_api_key=azure_openai_api_key,
    azure_endpoint=azure_openai_endpoint,
    deployment_name=azure_openai_api_deployment,
    api_version=azure_openai_api_version
)

async def main():
    test_suites = get_test_suites('../sample/tests')

    for test_suite in test_suites:
        await run_test_suite(test_suite)



asyncio.run(main())