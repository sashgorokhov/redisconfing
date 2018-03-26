import time

import aioredis
import redis


class RedisConfig:
    timeout = 60

    def __init__(self):
        self._cache = dict()
        self._redis = self._init_redis()

    def _redis_settings(self):
        return {
            'host': 'localhost',
            'port': '6379',
            'db': 0
        }

    def _init_redis(self):
        return redis.Redis(**self._redis_settings())

    def _check_cache(self, name):
        if name not in self._cache:
            return
        value, ttl = self._cache.get(name)
        if time.time() - ttl > self.timeout:
            return
        return value

    def _set_cache(self, name, value):
        self._cache[name] = (value, time.time())

    def _get_redis_setting(self, name):
        return self._redis.get(name) or None

    def _set_redis_setting(self, name, value):
        return self._redis.set(name, value)

    def get_setting(self, name, default=None):
        value = self._check_cache(name)
        if value is not None:
            return value
        value = self._get_redis_setting(name)
        if value is not None:
            value = value.decode()
            self._set_cache(name, value)
            return value
        self._set_redis_setting(name, default)
        self._set_cache(name, default)
        return default


class AsyncRedisConfig(RedisConfig):
    def _redis_settings(self):
        return {
            'address': 'localhost',
            'port': '6379',
            'db': 0
        }

    def _init_redis(self):
        return aioredis.create_redis(**self._redis_settings())

    async def _get_redis_setting(self, name):
        return await self._redis.get(f'redisconfig.{name}')

    async def _set_redis_setting(self, name, value):
        return await self._redis.set(f'redisconfig.{name}', value)

    async def get_setting(self, name, default=None):
        value = self._check_cache(name)
        if value is not None:
            return value
        value = await self._get_redis_setting(name)
        if value is not None:
            self._set_cache(name, value)
            return value
        await self._set_redis_setting(name, value)
        self._set_cache(name, value)
        return default
