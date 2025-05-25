from robot.api import logger
from robot.api.deco import keyword

from Browser.base.librarycomponent import LibraryComponent
from Browser.generated.playwright_pb2 import Request
from robot.libraries.BuiltIn import BuiltIn 

from playwright.sync_api import sync_playwright

from alumnium import Alumni
import os


class AlumniumPlugin(LibraryComponent):

    @keyword
    def new_ai_browser(
        self, 
        browser: str,
        headless: bool = True,
        port: int = 9222,
        ai_provider: str = None,    
        ai_model: str = None,
        api_key: str = None,
        api_base: str = None
        ) -> dict:
        
        self.pw = None
        if ai_provider:
            os.environ["ALUMNIUM_AI_PROVIDER"] = ai_provider
        if ai_model:
            os.environ["ALUMNIUM_AI_MODEL"] = ai_model
        if api_key:
            if ai_provider == "openai":
                os.environ["OPENAI_API_KEY"] = api_key
            elif ai_provider == "anthropic":
                os.environ["ANTHROPIC_API_KEY"] = api_key
            elif ai_provider == "google":
                os.environ["GOOGLE_API_KEY"] = api_key
            elif ai_provider == "deepseek":
                os.environ["DEEPSEEK_API_KEY"] = api_key
        if api_base:
            os.environ["ALUMNIUM_API_BASE"] = api_base

        self.pw = sync_playwright().start()
        if browser == "chrome" or browser == "chromium":
            self.sync_browser = self.pw.chromium.launch(headless=headless, args=["--remote-debugging-port=" + str(port)])
        elif browser == "firefox":
            self.sync_browser = self.pw.firefox.launch(headless=headless)
        elif browser == "webkit":
            self.sync_browser = self.pw.webkit.launch(headless=headless)
        else:
            raise ValueError(f"Unsupported Playwright browser: {browser}")

        self.browserlib = BuiltIn().get_library_instance("Browser")
        # connect to the sync browser
        self.browserlib.connect_to_browser(wsEndpoint="http://127.0.0.1:" + str(port), use_cdp=True)  

    @keyword
    def new_ai_page(self, url, port: int = 9222) -> Alumni:
        if not self.pw:
            raise RuntimeError("Playwright is not initialized. Please call new_ai_browser first.")
        page = self.sync_browser.new_page()
        self.al = Alumni(page)
        page.goto(url)

    @keyword
    def ai_do(self, command):
        """Run a natural language command.

        | =Arguments= | =Description= |
        | ``command`` | Instruction to the AI |

        Example:
        | `AI Do`  Calculate "2 + 2, multiply the result by 12 and then divide by 6"
        | `AI Do`  Switch currency to EUR
        | `AI Do`  Fill address form fields with "ELABIT, Beach Road 541, 44444 Miami, USA"
        """
        try:
            self.al.do(command)
        except Exception as e:
            raise

    @keyword
    def ai_check(self, command):
        """Run a verification.

        | =Arguments= | =Description= |
        | ``command`` | Instruction to the AI |

        Example:
        | `AI Check`  Price is below 300 EUR
        | `AI Check`  Price is below 300 EUR
        """        
        try:
            self.al.check(command)
        except Exception as e:
            raise

    @keyword
    def ai_get(self, command):
        """Run a get command with error handling."""
        try:
            return self.al.get(command)
        except Exception as e:
            raise
