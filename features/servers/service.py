from features.servers.upsert import upsert
from utils.limiter import limiter
from utils.clients import client

import asyncio

async def fetch_gameservers(token: str, server_id: str):
  headers = {"Authorization": f"Bearer {token}"}
  
  async with limiter:
    resp = await client.get(f"/services/{server_id}/gameservers", headers=headers)
  
  if resp.status_code == 200:
    return resp.json()["data"]["gameserver"]

async def fetch_servers(token: str, guild_id: str):
  headers = {"Authorization": f"Bearer {token}"}
  
  resp = await client.get("/services", headers=headers)
  
  if resp.status_code == 200:
    servers = []
    
    for server in resp.json()["data"]["services"]:
      if server.get("details", {}).get("folder_short") == "arkxb":
        servers.append(server)

    tasks = []
    for server in servers:
      tasks.append(fetch_gameservers(token, server["id"]))

    results = []
    for result in await asyncio.gather(*tasks):
      if result is not None:
        results.append(result)

    await upsert(results, guild_id)
    return results