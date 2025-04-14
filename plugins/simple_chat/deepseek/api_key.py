from pathlib import Path
import json

path = Path(__file__).parent / "apikey.json"

API_KEY= json.load(open(path))['key']