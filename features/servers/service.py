from features.servers.upsert import upsert
from utils.limiter import limiter
from utils.clients import client

import asyncio

async def fetch_gameservers(token: str, server_id: str):
  headers = {"Authorization": f"Bearer {token}"}
  
  async with limiter:
    resp = await client.get(f"/services/{server_id}/gameservers", headers=headers)
    body = resp.json()

  if resp.status_code == 200:
    return body.get("data", {}).get("gameserver", {})

async def fetch_servers(token: str, guild_id: str):
  headers = {"Authorization": f"Bearer {token}"}
  
  resp = await client.get("/services", headers=headers)
  
  if resp.status_code != 200:
    return

  body = resp.json()
  services = body.get("data", {}).get("services", [])

  servers = []
  for service in services:
    if service.get("details", {}).get("folder_short") == "arkxb":
      servers.append(service)

  tasks = []
  for server in servers:
    tasks.append(fetch_gameservers(token, server.get("id")))

  results = []
  for result in await asyncio.gather(*tasks):
    results.append(result)

  await upsert(results, guild_id)
  return results