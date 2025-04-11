from dotenv import dotenv_values
from typing import Optional
import sys
from pydantic import BaseModel, ValidationError


class Config(BaseModel):
    CLIENT_ID: str
    CLIENT_SECRET: str
    SERVER_PASS: Optional[str] = None    


env = dotenv_values()

try:
    CONFIG = Config(**env)  # type: ignore
except ValidationError as errors:
    for error in errors.errors():
        print(f"FATAL: Missing environment variable: {error['loc'][0]}")
    sys.exit(1)