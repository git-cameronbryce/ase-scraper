from features.servers.service import fetch_servers
from features.players.service import fetch_players
from utils.firebase import db
import asyncio

async def main():
  while True:
    docs = db.collection("guilds").stream()

    async for doc in docs:
      data = doc.to_dict()
      if data is None:
        continue

      token = data.get("token")
      if token is None:
        continue

      servers = await fetch_servers(token, doc.id)
      if not servers:
        continue

      tasks = []
      for server in servers:
        tasks.append(fetch_players(token, doc.id, str(server["service_id"])))
        
      await asyncio.gather(*tasks)
    await asyncio.sleep(60)

asyncio.run(main())