from features.servers.service import fetch_servers
from features.players.service import fetch_players
from utils.firebase import db
import asyncio

async def main():
  while True:
    docs = db.collection("guilds").stream()

    async for doc in docs:
      data = doc.to_dict()

      token = data.get("token")

      servers = await fetch_servers(token, doc.id)

      tasks = []
      for server in servers:
        service_id = server.get("service_id")

        tasks.append(fetch_players(token, doc.id, str(service_id)))

      if tasks:
        await asyncio.gather(*tasks)
        
    await asyncio.sleep(60)

asyncio.run(main())