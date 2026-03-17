from utils.xuid import fetch_xuid
from utils.firebase import db


async def upsert(results, guild_id, server_id):
  for player in results:

    if not player.get("online"):
      continue

    player_id = player.get("id")
    gamertag = player.get("name")

    xuid = await fetch_xuid(gamertag)
    
    guild_ref = db.collection("guilds").document(str(guild_id))
    server_ref = guild_ref.collection("servers").document(str(server_id))
    player_ref = server_ref.collection("players").document(str(player_id))

    await player_ref.set({
      "gamertag": gamertag,
      "last_online": player.get("last_online"),
      "is_online": player.get("online"),
      "xuid": xuid,
    })