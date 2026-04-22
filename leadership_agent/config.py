import os
import sys
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

REQUIRED = [
    "GMAIL_ADDRESS",
    "GMAIL_APP_PASSWORD",
    "TO_EMAIL",
    "ANTHROPIC_API_KEY",
]


@dataclass
class Config:
    gmail_address: str
    gmail_app_password: str
    to_email: str
    anthropic_api_key: str


def load_config() -> Config:
    missing = [k for k in REQUIRED if not os.getenv(k)]
    if missing:
        print("Missing required environment variables:")
        for k in missing:
            print(f"  {k}")
        print("\nCopy .env.example to .env and fill in your credentials.")
        sys.exit(1)

    return Config(
        gmail_address=os.environ["GMAIL_ADDRESS"],
        gmail_app_password=os.environ["GMAIL_APP_PASSWORD"],
        to_email=os.environ["TO_EMAIL"],
        anthropic_api_key=os.environ["ANTHROPIC_API_KEY"],
    )
