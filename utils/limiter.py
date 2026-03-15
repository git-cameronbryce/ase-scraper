from aiolimiter import AsyncLimiter

xbox_limiter = AsyncLimiter(1, 1)
limiter = AsyncLimiter(25, 1)