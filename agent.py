from langchain_openai import ChatOpenAI
from browser_use import Agent
from dotenv import load_dotenv
load_dotenv()

import asyncio

llm = ChatOpenAI(model="gpt-4o")

async def main():
    agent = Agent(
        task="""
            1. visit wikipedia.com.
            1. search tensors
            1. summarize results of first article
        """,
        llm=llm,
    )
    result = await agent.run()
    print(result)
    print(result.screenshots())

asyncio.run(main())