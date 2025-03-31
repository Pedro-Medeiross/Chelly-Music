# Import required modules
import os  # For environment variable access
import pytest  # Testing framework
import asyncio  # Async operations support
from playwright.async_api import async_playwright  # Browser automation
from dotenv import load_dotenv  # Environment loader

# Load environment variables from .env file
load_dotenv()  # Expects DISCORD_EMAIL, DISCORD_PASSWORD

@pytest.mark.asyncio
async def test_ping_command():
    """End-to-end test for Discord bot's ping command using browser automation."""
    
    async with async_playwright() as p:
        # Launch headless Chromium browser (no GUI)
        browser = await p.chromium.launch(headless=True)
        
        # Create isolated browser context (prevents cookie sharing between tests)
        context = await browser.new_context()

        # Retrieve sensitive credentials from environment
        discord_email = os.getenv("DISCORD_EMAIL")
        discord_password = os.getenv("DISCORD_PASSWORD")
        discord_channel_url = "https://discord.com/channels/1081985248969105558/1081985250923651229"

        # Validate environment configuration
        if not all([discord_email, discord_password, discord_channel_url]):
            missing = [var for var in ["DISCORD_EMAIL", "DISCORD_PASSWORD"] if not os.getenv(var)]
            raise ValueError(f"Missing environment variables: {', '.join(missing)}")

        # Create new browser tab
        page = await context.new_page()
        
        # --- Discord Login Flow ---
        await page.goto("https://discord.com/login")
        
        # Fill login form using CSS selectors
        await page.fill('input[name="email"]', discord_email)  # Email input
        await page.fill('input[name="password"]', discord_password)  # Password input
        await page.click('button[type="submit"]')  # Submit button
        
        # Wait for login completion (redirect to home)
        await page.wait_for_url('https://discord.com/channels/@me', timeout=15000)

        # --- Test Execution ---
        await page.goto(discord_channel_url)
        
        # Discord message input selector (role-based accessibility selector)
        text_area_selector = 'div[role="textbox"]'
        
        # Send ping command to bot
        await page.fill(text_area_selector, 'c!ping')  # Type command
        await page.press(text_area_selector, 'Enter')  # Simulate Enter key
        
        # Wait for bot response (consider using Playwright's wait_for_selector instead)
        await asyncio.sleep(3)  # Flaky - better to wait for specific element

        # --- Assertions ---
        response = await page.inner_text('text=O ping é')  # Get response text
        assert 'O ping é' in response  # Verify bot responded correctly

        # Cleanup
        await browser.close()  # Close browser and release resources