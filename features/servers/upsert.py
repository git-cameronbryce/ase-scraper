from utils.firebase import db

async def upsert(results, guild_id):
  batch = db.batch()

  for result in results:
    if result is None:
      continue

    game_specific = result.get("game_specific") or {}

    ref = db.collection("guilds").document(str(guild_id)).collection("servers").document(str(result["service_id"]))
    batch.set(ref, {
      "game": {
        "status": result["status"],
        "path": game_specific.get("path")
      },
      "network": {
        "ip": result["ip"],
        "port": result["port"]
      }
    })

  await batch.commit()