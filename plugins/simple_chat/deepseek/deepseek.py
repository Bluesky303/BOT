from openai import OpenAI
from pathlib import Path
import json

path = Path(__file__).parent / "apikey.json"
api_key = json.load(open(path))['key']
client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")