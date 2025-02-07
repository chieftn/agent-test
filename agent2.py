import os
import sys
import asyncio

from langchain_openai import AzureChatOpenAI
from browser_use.agent.service import Agent
from browser_use.browser.browser import Browser, BrowserConfig
from browser_use.browser.context import BrowserContextConfig
from dotenv import load_dotenv
from playwright.async_api import async_playwright

from keyVaultClient import get_secret

load_dotenv()

azure_openai_api_key = os.environ.get('AZURE_OPENAI_KEY')
azure_openai_endpoint = os.environ.get('AZURE_OPENAI_ENDPOINT')
azure_openai_api_model = os.environ.get('AZURE_OPENAI_MODEL')
azure_openai_api_deployment = os.environ.get('AZURE_OPENAI_DEPLOYMENT')
azure_openai_api_version = os.environ.get('AZURE_OPENAI_VERSION')

subscription = os.environ.get('AZURE_SUBSCRIPTION')
keyVaultName = os.environ.get('KEY_VAULT_NAME')
kv_uri = f"https://{keyVaultName}.vault.azure.net"
secretName = os.environ.get('KV_SECRET_NAME')
e2eUserEmail = os.environ.get('E2E_USER_EMAIL')

# Initialize the Azure OpenAI client
llm = AzureChatOpenAI(
    model_name=azure_openai_api_model,
    openai_api_key=azure_openai_api_key,
    azure_endpoint=azure_openai_endpoint,
    deployment_name=azure_openai_api_deployment,
    api_version=azure_openai_api_version
)

async def main():
    browser = Browser(
        config=BrowserConfig(
            headless=True
        )
    )

    print(f'Getting test user secret {secretName}...')

    e2eUserPassword = get_secret(subscription, keyVaultName, kv_uri, secretName)

    if (e2eUserPassword == None):
        print(f'Failed to get secret {secretName}')
        return
    
    print(f'Got test user password {secretName} from keyvault.')

    async with async_playwright() as p:
        # playwrightBrowser = await p.chromium.launch(headless=False)
        # context
        browserContext = await browser.new_context()
        page = await browserContext.new_page()
        await page.goto('https://aka.ms/doe-ppe')

        await page.getByPlaceholder('Email or phone').fill(e2eUserEmail)
        await page.getByRole('button', name='Next').click()

        


    # async with await browser.new_context(
    #     config=BrowserContextConfig(trace_path='./tmp/traces/')
    # ) as context:
    #     # agent = Agent(
    #     #     task='Go to hackernews, then go to apple.com and return all titles of open tabs',
    #     #     llm=llm,
    #     #     browser_context=context,
    #     # )
    #     # await agent.run()

    #     sensitive_data = {
    #         'e2eUserEmail': e2eUserEmail,
    #         'e2eUserPassword': e2eUserPassword
    #     }
    #     task = """
    #         Navigate to https://aka.ms/doe-ppe and login with the username e2eUserEmail and password e2eUserPassword. 
    #         Once the login flow is complete, confirm the text Welcome to Azure IoT Operations is visible. 
    #         If you see a message saying you need to reauthorize, open the browser console and watch for console errors or network errors. Continue with next instructions.
    #         If you get into a loop where you can't reauthorize, click the three dots to logout and try logging in again.
    #         If logging out doesn't work after the first try, clear the browser cookies and cache and try again.
    #         End the test if you run into the loop more than 3 times, after trying to clear site data.
    #     """

    #     agent2 = Agent(
    #         task=task,
    #         llm=llm,
    #         browser_context=context,
    #         sensitive_data=sensitive_data
    #     )

    #     await agent2.run()

    await browser.close()
    
# async def main():
#     browser = Browser(
#         config=BrowserConfig(
#             headless=True
#         )
#     )

#     print(f'Getting test user secret {secretName}...')

#     e2eUserPassword = get_secret(subscription, keyVaultName, kv_uri, secretName)

#     if (e2eUserPassword == None):
#         print(f'Failed to get secret {secretName}')
#         return
    
#     print(f'Got test user password {secretName} from keyvault.')

#     # async with await browser.new_context(
#     #     config=BrowserContextConfig(trace_path='./tmp/traces/')
#     # ) as context:
#     #     # agent = Agent(
#     #     #     task='Go to hackernews, then go to apple.com and return all titles of open tabs',
#     #     #     llm=llm,
#     #     #     browser_context=context,
#     #     # )
#     #     # await agent.run()

#     #     sensitive_data = {
#     #         'e2eUserEmail': e2eUserEmail,
#     #         'e2eUserPassword': e2eUserPassword
#     #     }
#     #     task = """
#     #         Navigate to https://aka.ms/doe-ppe and login with the username e2eUserEmail and password e2eUserPassword. 
#     #         Once the login flow is complete, confirm the text Welcome to Azure IoT Operations is visible. 
#     #         If you see a message saying you need to reauthorize, open the browser console and watch for console errors or network errors. Continue with next instructions.
#     #         If you get into a loop where you can't reauthorize, click the three dots to logout and try logging in again.
#     #         If logging out doesn't work after the first try, clear the browser cookies and cache and try again.
#     #         End the test if you run into the loop more than 3 times, after trying to clear site data.
#     #     """

#     #     agent2 = Agent(
#     #         task=task,
#     #         llm=llm,
#     #         browser_context=context,
#     #         sensitive_data=sensitive_data
#     #     )

#     #     await agent2.run()

#     await browser.close()


asyncio.run(main())