import os
import pytest
import asyncio
from playwright.async_api import async_playwright
from dotenv import load_dotenv

load_dotenv()

@pytest.mark.asyncio
async def test_ping_command():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()

        # Buscar as variáveis de ambiente
        discord_email = os.getenv("DISCORD_EMAIL")
        discord_password = os.getenv("DISCORD_PASSWORD")
        discord_channel_url = "https://discord.com/channels/1081985248969105558/1081985250923651229"

        if not discord_email or not discord_password or not discord_channel_url:
            raise ValueError("Variáveis de ambiente não definidas. Verifique as variáveis DISCORD_EMAIL, DISCORD_PASSWORD e DISCORD_CHANNEL_URL.")

        # Substitua pela URL de login do Discord
        discord_login_url = "https://discord.com/login"

        page = await context.new_page()
        
        # Navegar para a página de login do Discord
        await page.goto(discord_login_url)

        # Fazer login no Discord
        await page.fill('input[name="email"]', discord_email)
        await page.fill('input[name="password"]', discord_password)
        await page.click('button[type="submit"]')

        # Aguarde até que a navegação esteja completa
        await page.wait_for_url('https://discord.com/channels/@me')

        # Navegar para o canal específico
        await page.goto(discord_channel_url)
        
        text_area_selector = 'div[role="textbox"]'

        # Enviar o comando ping
        await page.fill(text_area_selector, '/ping')
        await page.press(text_area_selector, 'Enter')

        # Adicionar uma pausa para garantir que o bot tenha tempo de responder
        await asyncio.sleep(3)  # Aguarde 3 segundos

        # Verificar a resposta do bot
        response = await page.inner_text('text=O ping é')
        assert 'O ping é' in response

        await browser.close()
