from utils.limiter import xbox_limiter
from utils.clients import xbox_client
import json

with open("config/config.json") as f:
  token = json.load(f)["openxbl"]["api_key"]

async def fetch_xuid(gamertag: str):
  headers = {"X-Authorization": token}

  async with xbox_limiter:
    resp = await xbox_client.get(f"https://xbl.io/api/v2/search/{gamertag}", headers=headers)

  if resp.status_code != 200:
    return

  data = resp.json()
  people = data.get("people", [])
  for account in people:
    return account.get("xuid")