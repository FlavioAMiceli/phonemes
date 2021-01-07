import pyppeteer
import asyncio
from bs4 import BeautifulSoup

async def main():
	browser = await pyppeteer.launch()
	page = await browser.newPage()

	await page.goto('https://nl.wikipedia.org/wiki/Hoofdpagina')
	await page.type('[id=searchInput]', "filosofie")
	await page.keyboard.press('Enter')
	await page.waitForNavigation()

	urls = await page.evaluate('''
		() => {
			const links = document.querySelectorAll('.mw-search-results a')
			const urls = Array.from(links).map(link => link.href)
			return urls
		}
	''')

	print(urls[0])

	await page.goto(urls[0])

	data = 	urls = await page.evaluate('''
		() => {
			const contents = document.querySelectorAll('.mw-parser-output p')
			const ps = Array.from(contents).map(para => para.innerHTML)
			return ps
		}
	''')

	allData = ' '.join(data)

	soup = BeautifulSoup(allData, features="html.parser")
	text = soup.get_text().strip()

	print(text)

	await browser.close()

asyncio.get_event_loop().run_until_complete(main())
