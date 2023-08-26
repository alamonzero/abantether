import redis
from django.conf import settings

from utils.singleton import Singleton

class RedisManager(metaclass=Singleton):

    def __init__(self):
        super(RedisManager, self).__init__()
        self.client = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)
