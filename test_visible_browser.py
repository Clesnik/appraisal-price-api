#!/usr/bin/env python3
"""
Simple test script to run browser visibly
"""

import asyncio
from playwright.async_api import async_playwright

async def main():
    print("Starting visible browser test...")
    print("Opening browser window - you should see it appear!")
    
    async with async_playwright() as p:
        # Try with different browser options
        try:
            # First try with Firefox which might be more stable
            print("Trying Firefox...")
            browser = await p.firefox.launch(headless=False)
        except Exception as e:
            print(f"Firefox failed: {e}")
            try:
                # Try Chromium with additional options
                print("Trying Chromium with additional options...")
                browser = await p.chromium.launch(
                    headless=False,
                    args=[
                        '--no-sandbox',
                        '--disable-dev-shm-usage',
                        '--disable-gpu',
                        '--disable-web-security',
                        '--disable-features=VizDisplayCompositor'
                    ]
                )
            except Exception as e2:
                print(f"Chromium also failed: {e2}")
                print("Trying WebKit...")
                browser = await p.webkit.launch(headless=False)
        
        page = await browser.new_page()
        
        try:
            print("Navigating to Nadlan valuation website...")
            await page.goto("https://nadlanvaluation.spurams.com/login.aspx")
            
            print("Waiting for page to load...")
            await page.wait_for_load_state("networkidle")
            
            print("Taking a screenshot...")
            await page.screenshot(path="visible_browser_screenshot.png")
            
            title = await page.title()
            print(f"Page title: {title}")
            
            # Wait a bit so you can see the page
            print("Waiting 10 seconds so you can see the page...")
            await page.wait_for_timeout(10000)
            
            print("Test completed successfully!")
            
        except Exception as e:
            print(f"Error during page navigation: {e}")
        
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
