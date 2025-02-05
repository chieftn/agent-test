from langchain_openai import ChatOpenAI
from browser_use import Agent, Browser
from dotenv import load_dotenv, dotenv_values

load_dotenv()

import asyncio

llm = ChatOpenAI(model="gpt-4o")

async def main():
    sensitive_data = {'x_name': dotenv_values("USERNAME"), 'x_password': dotenv_values("PASSWORD")}

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