import redis.asyncio as redis

client = redis.Redis(host="...", port=000, password="...",decode_responses=True)