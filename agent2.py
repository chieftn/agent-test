import os
import sys

from langchain_openai import AzureChatOpenAI

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import asyncio

from browser_use.agent.service import Agent
from browser_use.browser.browser import Browser
from browser_use.browser.context import BrowserContextConfig

azure_openai_api_key = os.environ.get('AZURE_OPENAI_KEY')
azure_openai_endpoint = os.environ.get('AZURE_OPENAI_ENDPOINT')
azure_openai_api_model = os.environ.get('AZURE_OPENAI_MODEL')
azure_openai_api_deployment = os.environ.get('AZURE_OPENAI_DEPLOYMENT')
azure_openai_api_version = os.environ.get('AZURE_OPENAI_VERSION')

# Initialize the Azure OpenAI client
llm = AzureChatOpenAI(
    model_name=azure_openai_api_model,
    openai_api_key=azure_openai_api_key,
    azure_endpoint=azure_openai_endpoint,
    deployment_name=azure_openai_api_deployment,
    api_version=azure_openai_api_version
)

async def main():
    browser = Browser()

    async with await browser.new_context(
        config=BrowserContextConfig(trace_path='./tmp/traces/')
    ) as context:
        agent = Agent(
            task='Go to hackernews, then go to apple.com and return all titles of open tabs',
            llm=llm,
            browser_context=context,
        )
        await agent.run()

        agent2 = Agent(
            task="Go to hackernews",
            llm=llm,
            browser_context=context
        )

        await agent2.run()

    await browser.close()


asyncio.run(main())