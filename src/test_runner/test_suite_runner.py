import json

from langchain_openai import AzureChatOpenAI
from browser_use.agent.service import Agent
from browser_use.browser.browser import Browser
from browser_use.browser.context import BrowserContextConfig, BrowserContext

from test_parser import Test
from test_parser import Test, TestSeries, TestSuite
from .test_result import TestResult
from .test_prompt import TEST_PROMPT

async def run_test_suite(llm: AzureChatOpenAI, test_suite: TestSuite) -> list[TestResult]:
    suite_results = list()
    for test_series in test_suite.series:
        series_results = await run_test_series(
            llm=llm,
            suite_name=test_suite.name,
            test_series=test_series
        )
        suite_results.extend(series_results)

async def run_test_series(llm: AzureChatOpenAI, suite_name: str, test_series: TestSeries) -> list[TestResult]:
    series_results = list()
    browser = Browser()

    async with await browser.new_context(
        config=BrowserContextConfig(
            trace_path='../tmp/traces/',
            save_recording_path='../tmp/traces/',
            cookies_file='../tmp/cookies.json',
            disable_security=False,
        )
    ) as context:
        for test in test_series.tests:
            result = await run_test(
                llm=llm,
                context=context,
                suite_name=suite_name,
                series_name=test_series.name,
                test=test
            )
            series_results.append(result)

    await browser.close()
    return series_results

async def run_test(llm: AzureChatOpenAI, context: BrowserContext, suite_name: str, series_name: str, test: Test) -> TestResult:
    try:
        task = TEST_PROMPT.format(act=test.act, expect=test.expect)
        agent = Agent(
            task=task,
            llm=llm,
            browser_context=context,
            sensitive_data={}
        )

        history = await agent.run()
        result = history.final_result()

        result_parsed = json.load(result)

        return TestResult(
            suite_name=suite_name,
            series_name=series_name,
            name=test.name,
            result=result_parsed["result"],
            message=result_parsed["message"]
        )

    except Exception as e:
        return TestResult(
            suite_name=suite_name,
            series_name=series_name,
            name=test.name,
            result="fail",
            message=e
        )
