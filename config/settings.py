import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Settings:
    api_base_url: str = os.getenv("API_BASE_URL", "[restful-booker.herokuapp.com](https://restful-booker.herokuapp.com)")
    ui_base_url: str = os.getenv("UI_BASE_URL", "[automationintesting.online](https://automationintesting.online)")
    request_timeout: int = int(os.getenv("REQUEST_TIMEOUT", "10"))
    headless: bool = os.getenv("HEADLESS", "true").lower() == "true"

settings = Settings()
