from utils.redis import client
import json

async def upsert(results, guild_id, server_id):
  players = []

  for result in results:
    if result is None:
      continue
    if not result["online"]:
      continue

    players.append({
      "id": result["id"],
      "gamertag": result["name"],
      "is_online": result["online"],
      "last_online": result["last_online"]
    })

  key = f"guild:{guild_id}:server:{server_id}:players"
  await client.set(key, json.dumps(players))
  print(key)