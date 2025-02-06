from langchain_openai import AzureChatOpenAI
from browser_use import Agent, Browser
from dotenv import load_dotenv
import os

load_dotenv()

import asyncio

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

    sensitive_data = {'x_name': os.getenv('SO_USERNAME'), 'x_password': os.getenv('SO_PASSWORD')}

    browser = Browser()
    agent = Agent(
        task="""
            1. go to stackoverflow.com
            1. log in with username x_name and password x_password
        """,
        llm=llm,
        browser=browser,
        sensitive_data=sensitive_data
    )
    await agent.run()

    browser.close()
    # print(result)
    # print(result.screenshots())

asyncio.run(main())