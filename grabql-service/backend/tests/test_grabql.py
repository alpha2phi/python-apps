import unittest
from playwright.sync_api import sync_playwright


class TestClass(unittest.TestCase):
    """Test case docstring."""
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_grab(self):
        with sync_playwright() as p:
            # for browser_type in [p.chromium, p.firefox, p.webkit]:
            for browser_type in [p.chromium]:
                browser = browser_type.launch()
                page = browser.new_page()
                page.set_viewport_size({"width": 640, "height": 480})
                page.goto('http://whatsmyuseragent.org/')
                page.screenshot(path=f'example-{browser_type.name}.png')
                browser.close()
