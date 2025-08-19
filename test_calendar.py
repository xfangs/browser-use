import pytest
from dotenv import load_dotenv
from playwright.async_api import async_playwright
from browser_use import Agent
from browser_use.llm import ChatOllama
import asyncio

# 加载环境变量
load_dotenv()

@pytest.mark.asyncio
async def test_calendar():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto("https://helpingtesters53.github.io/helpingtesters-basic-demo-website/")
        
        agent = Agent(
            task=("Log in to the application, and then log out."),
            llm=ChatOllama(model="qwen2.5:7b", host="http://127.0.0.1:11434"),
            context=context,
            page=page
        )
        
        await asyncio.sleep(5)
        await agent.run()
        await browser.close()

if __name__ == "__main__":
    asyncio.run(test_calendar())
