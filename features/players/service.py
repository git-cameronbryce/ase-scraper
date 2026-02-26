from features.players.upsert import upsert
from utils.limiter import limiter
from utils.clients import client

async def fetch_players(token: str, guild_id: str, server_id: str):
  headers = {"Authorization": f"Bearer {token}"}
    
  async with limiter:
    resp = await client.get(f"/services/{server_id}/gameservers/games/players", headers=headers)
  
  if resp.status_code == 200:
    results = resp.json()["data"]["players"]
    await upsert(results, guild_id, server_id)