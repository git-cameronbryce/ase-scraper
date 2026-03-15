import httpx

client = httpx.AsyncClient(base_url="https://api.nitrado.net", timeout=60)
xbox_client = httpx.AsyncClient(timeout=60)