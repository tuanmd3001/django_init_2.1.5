# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    # }
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'hcc',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '3306'
    },
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
        "KEY_PREFIX": "dev:vnpost:web:cache",
    },
    "session": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "KEY_PREFIX": "dev:vnpost:web:client:session",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "locMemCache": {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    },
}
# CACHES = {
#     'default': {
#         "OPTIONS": {
#             "CLIENT_CLASS": "django_redis.client.DefaultClient",
#         },
#
#         # "KEY_PREFIX": "vnpost:web:client",
#         "KEY_PREFIX": "dev:vnpost:web:cache",
#         'BACKEND': 'redis_cache.RedisClusterCache',
#         "LOCATION": [
#             "redis://redis.106.emoney.vnpost.vn:7000/0",
#             "redis://redis.106.emoney.vnpost.vn:7001/0",
#             "redis://redis.106.emoney.vnpost.vn:7002/0",
#             "redis://redis.106.emoney.vnpost.vn:7003/0",
#             "redis://redis.106.emoney.vnpost.vn:7004/0",
#             "redis://redis.106.emoney.vnpost.vn:7005/0",
#             "redis://redis.107.emoney.vnpost.vn:7000/0",
#             "redis://redis.107.emoney.vnpost.vn:7001/0",
#             "redis://redis.107.emoney.vnpost.vn:7002/0",
#             "redis://redis.107.emoney.vnpost.vn:7003/0",
#             "redis://redis.107.emoney.vnpost.vn:7004/0",
#             "redis://redis.107.emoney.vnpost.vn:7005/0"
#         ]
#     },
#     'session': {
#         "OPTIONS": {
#             "CLIENT_CLASS": "django_redis.client.DefaultClient",
#         },
#         'BACKEND': 'redis_cache.RedisClusterCache',
#         "LOCATION": [
#             "redis://redis.106.emoney.vnpost.vn:7000/0",
#             "redis://redis.106.emoney.vnpost.vn:7001/0",
#             "redis://redis.106.emoney.vnpost.vn:7002/0",
#             "redis://redis.106.emoney.vnpost.vn:7003/0",
#             "redis://redis.106.emoney.vnpost.vn:7004/0",
#             "redis://redis.106.emoney.vnpost.vn:7005/0",
#             "redis://redis.107.emoney.vnpost.vn:7000/0",
#             "redis://redis.107.emoney.vnpost.vn:7001/0",
#             "redis://redis.107.emoney.vnpost.vn:7002/0",
#             "redis://redis.107.emoney.vnpost.vn:7003/0",
#             "redis://redis.107.emoney.vnpost.vn:7004/0",
#             "redis://redis.107.emoney.vnpost.vn:7005/0"
#         ]
#     },
#     "locMemCache": {
#         'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
#     }
# }
