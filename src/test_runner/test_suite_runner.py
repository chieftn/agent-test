from langchain_openai import AzureChatOpenAI
from browser_use.agent.service import Agent
from browser_use.browser.browser import Browser
from browser_use.browser.context import BrowserContextConfig, BrowserContext

from test_parser import Test
from test_parser import Test, TestSeries, TestSuite
from .test_result import TestResult

async def run_test_suite(llm: AzureChatOpenAI, test_suite: TestSuite) -> list[TestResult]:
    suite_results = list()
    for test_series in test_suite.series:
        series_results = await run_test_series(llm, test_series)
        suite_results.extend(series_results)

async def run_test_series(llm: AzureChatOpenAI, suite_name: str, test_series: TestSeries) -> list[TestResult]:
    browser = Browser()
    series_results = list()

    async with await browser.new_context(
        config=BrowserContextConfig(trace_path='../tmp/traces/')
    ) as context:
        for test in test_series.tests:
            result = await run_test(llm, context, suite_name, test_series.name, test)
            series_results.append(result)

    await browser.close()
    return series_results

async def run_test(llm: AzureChatOpenAI, context: BrowserContext, suite_name: str, series_name: str, test: Test) -> TestResult:
    task = """
        You are an E2E tester expected to perform following script and report a result.
        {act}

        # RULES
        You report 'pass' if:
            1. you successfully perform actions
            1. and these criteria are met: {expect}
        You report 'fail' with a reason if:
            1. you cannot perform the action
            2. an error occurs

    """.format(
        act=test.act,
        name=test.name,
        expect=test.expect
    )

    agent = Agent(
        task=task,
        llm=llm,
        browser_context=context
    )

    history = await agent.run()
    result = history.final_result()



    print("-----------------------------------------------")
    print(result)
