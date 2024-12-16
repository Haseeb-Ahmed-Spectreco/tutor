from ..devstack import *

SECRET_KEY = "1PNnsfMW3kb6fwBiD4mB"
ALLOWED_HOSTS = [
    "discovery",
    "discovery.local.edly.io"
]

PLATFORM_NAME = "The Transition Academy"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "discovery",
        "USER": "discovery",
        "PASSWORD": "sORxCDMx",
        "HOST": "mysql",
        "PORT": "3306",
        "OPTIONS": {
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

ELASTICSEARCH_DSL['default'].update({
    'hosts': "http://elasticsearch:9200/"
})



CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "KEY_PREFIX": "discovery",
        "LOCATION": "redis://@redis:6379/1",
    }
}

# Some openedx language codes are not standard, such as zh-cn
LANGUAGE_CODE = {
    "zh-cn": "zh-hans",
    "zh-hk": "zh-hant",
    "zh-tw": "zh-hant",
}.get("en", "en")
PARLER_DEFAULT_LANGUAGE_CODE = LANGUAGE_CODE
PARLER_LANGUAGES[1][0]["code"] = LANGUAGE_CODE
PARLER_LANGUAGES["default"]["fallbacks"] = [PARLER_DEFAULT_LANGUAGE_CODE]

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
DEFAULT_PRODUCT_SOURCE_SLUG = "edx"
EMAIL_HOST = "smtp"
EMAIL_PORT = "8025"
EMAIL_HOST_USER = ""
EMAIL_HOST_PASSWORD = ""
EMAIL_USE_TLS = False

# Get rid of the "local" handler
LOGGING["handlers"].pop("local")
for logger in LOGGING["loggers"].values():
    if "local" in logger["handlers"]:
        logger["handlers"].remove("local")
# Decrease verbosity of algolia logger
LOGGING["loggers"]["algoliasearch_django"] = {"level": "WARNING"}

OAUTH_API_TIMEOUT = 5

import json
JWT_AUTH["JWT_ISSUER"] = "http://local.edly.io/oauth2"
JWT_AUTH["JWT_AUDIENCE"] = "openedx"
JWT_AUTH["JWT_SECRET_KEY"] = "rzvIJZtAE87VrKD7E0VK8n6N"
# TODO assign a discovery-specific public key
JWT_AUTH["JWT_PUBLIC_SIGNING_JWK_SET"] = json.dumps(
    {
        "keys": [
            {
                "kid": "openedx",
                "kty": "RSA",
                "e": "AQAB",
                "n": "vL7Me78Gi6TUTKUF6NcZiORWskkhtvUuvu1ITRq0wUVcblNTQ0VVvv01LD2cgqgomgDJQ8KVPUka3B5dnlkKIe_qj3T2_8AFsDzoI2Io7QD3YqDRy9XtOhHCsmAIw-OvUgQ5YnMeU1q4V4CCJugOmsj3DB7SV3EMtxuW1gZnymHS-iIFoe82oyb9tD6_GE48Re-Kf6l-B23U_4PhgWYhyGUf_lCzdXKmifapumMEx6QXUNdl0XYqOFPVvALyykWuU2pKXb3WcHEtTR4ArW8FXp1Oz9qH6rabL7VrBn9svacY66BDtw3K9tqbslqf2WnbE8F95UJ9Z40ynE7nuDyhjw",
            }
        ]
    }
)
JWT_AUTH["JWT_ISSUERS"] = [
    {
        "ISSUER": "http://local.edly.io/oauth2",
        "AUDIENCE": "openedx",
        "SECRET_KEY": "rzvIJZtAE87VrKD7E0VK8n6N"
    }
]

EDX_DRF_EXTENSIONS = {
    'OAUTH2_USER_INFO_URL': 'http://local.edly.io/oauth2/user_info',
}



BACKEND_SERVICE_EDX_OAUTH2_KEY = "discovery-dev"
BACKEND_SERVICE_EDX_OAUTH2_SECRET = "HXLBOFQw"
BACKEND_SERVICE_EDX_OAUTH2_PROVIDER_URL = "http://lms:8000/oauth2"

SOCIAL_AUTH_EDX_OAUTH2_KEY = "discovery-sso-dev"
SOCIAL_AUTH_EDX_OAUTH2_SECRET = "eHGqZpFW"
SOCIAL_AUTH_EDX_OAUTH2_ISSUER = "http://local.edly.io:8000"
SOCIAL_AUTH_EDX_OAUTH2_URL_ROOT = SOCIAL_AUTH_EDX_OAUTH2_ISSUER
SOCIAL_AUTH_EDX_OAUTH2_PUBLIC_URL_ROOT = SOCIAL_AUTH_EDX_OAUTH2_ISSUER
SOCIAL_AUTH_EDX_OAUTH2_LOGOUT_URL = SOCIAL_AUTH_EDX_OAUTH2_ISSUER + "/logout"

# Disable API caching, which makes it a pain to troubleshoot issues
USE_API_CACHING = False

DISCOVERY_BASE_URL = "http://discovery.local.edly.io:8381"
MEDIA_URL = DISCOVERY_BASE_URL + "/media/"

