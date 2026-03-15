from utils.xuid import fetch_xuid
from utils.firebase import db

player_set = set()

async def upsert(results, guild_id, server_id):
  for player in results:
    player_id = player.get("id")

    if player_id is None:
      continue

    if player_id in player_set:
      print("Player already in set()")
      continue

    player_set.add(player_id)

    gamertag = player.get("name")
    
    xuid = None
    if gamertag:
      xuid = await fetch_xuid(gamertag)

    print(f"{xuid} - {player_id}")

    guild_ref = db.collection("guilds").document(str(guild_id))
    server_ref = guild_ref.collection("servers").document(str(server_id))
    player_ref = server_ref.collection("players").document(str(player_id))

    await player_ref.set({
      "gamertag": gamertag,
      "last_online": player.get("last_online"),
      "is_online": player.get("online"),
      "xuid": xuid,
    })