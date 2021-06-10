import re
import json
from requests_html import HTMLSession

URL = "https://www.investing.com/equities/google-inc-c-balance-sheet"

session = HTMLSession()
response = session.get(URL)

response.html.render(keep_page=True, timeout=60)


async def run():

    # Click on Annual button and wait for results
    await response.html.page.click("a[data-ptype='Annual']")
    await response.html.page.waitForSelector("table[class='genTbl reportTbl']")

    elements = await response.html.page.xpath(
        "//*[@id='rrtable']/table//*[@id='header_row']/th/span")
    for element in elements:
        text = await response.html.page.evaluate('(e) => e.textContent',
                                                 element)
        match = re.search(r"\d\d\d\d", text.strip())
        if match:
            print(match.string)

    print("Completed...")


try:
    session.loop.run_until_complete(run())
finally:
    session.close()
