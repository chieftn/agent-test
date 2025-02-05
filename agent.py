from langchain_openai import ChatOpenAI
from browser_use import Agent, Browser
from dotenv import load_dotenv
import os

load_dotenv()

import asyncio

llm = ChatOpenAI(model="gpt-4o")

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