import redis
r = redis.Redis()
r.set('x',1)
print(r.get('x'))
