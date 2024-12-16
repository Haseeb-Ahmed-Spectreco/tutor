# -*- coding: utf-8 -*-
import os
from cms.envs.devstack import *

LMS_BASE = "local.edly.io:8000"
LMS_ROOT_URL = "http://" + LMS_BASE

CMS_BASE = "studio.local.edly.io:8001"
CMS_ROOT_URL = "http://" + CMS_BASE

# Authentication
SOCIAL_AUTH_EDX_OAUTH2_KEY = "cms-sso-dev"
SOCIAL_AUTH_EDX_OAUTH2_PUBLIC_URL_ROOT = LMS_ROOT_URL

FEATURES["PREVIEW_LMS_BASE"] = "preview.local.edly.io:8000"

####### Settings common to LMS and CMS
import json
import os

from xmodule.modulestore.modulestore_settings import update_module_store_settings

# Mongodb connection parameters: simply modify `mongodb_parameters` to affect all connections to MongoDb.
mongodb_parameters = {
    "db": "openedx",
    "host": "mongodb",
    "port": 27017,
    "user": None,
    "password": None,
    # Connection/Authentication
    "connect": False,
    "ssl": False,
    "authsource": "admin",
    "replicaSet": None,
    
}
DOC_STORE_CONFIG = mongodb_parameters
CONTENTSTORE = {
    "ENGINE": "xmodule.contentstore.mongo.MongoContentStore",
    "ADDITIONAL_OPTIONS": {},
    "DOC_STORE_CONFIG": DOC_STORE_CONFIG
}
# Load module store settings from config files
update_module_store_settings(MODULESTORE, doc_store_settings=DOC_STORE_CONFIG)
DATA_DIR = "/openedx/data/modulestore"

for store in MODULESTORE["default"]["OPTIONS"]["stores"]:
   store["OPTIONS"]["fs_root"] = DATA_DIR

# Behave like memcache when it comes to connection errors
DJANGO_REDIS_IGNORE_EXCEPTIONS = True

# Elasticsearch connection parameters
ELASTIC_SEARCH_CONFIG = [{
  
  "host": "elasticsearch",
  "port": 9200,
}]

# Common cache config
CACHES = {
    "default": {
        "KEY_PREFIX": "default",
        "VERSION": "1",
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://@redis:6379/1",
    },
    "general": {
        "KEY_PREFIX": "general",
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://@redis:6379/1",
    },
    "mongo_metadata_inheritance": {
        "KEY_PREFIX": "mongo_metadata_inheritance",
        "TIMEOUT": 300,
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://@redis:6379/1",
    },
    "configuration": {
        "KEY_PREFIX": "configuration",
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://@redis:6379/1",
    },
    "celery": {
        "KEY_PREFIX": "celery",
        "TIMEOUT": 7200,
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://@redis:6379/1",
    },
    "course_structure_cache": {
        "KEY_PREFIX": "course_structure",
        "TIMEOUT": 604800, # 1 week
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://@redis:6379/1",
    },
    "ora2-storage": {
        "KEY_PREFIX": "ora2-storage",
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://@redis:6379/1",
    }
}

# The default Django contrib site is the one associated to the LMS domain name. 1 is
# usually "example.com", so it's the next available integer.
SITE_ID = 2

# Contact addresses
CONTACT_MAILING_ADDRESS = "The Transition Academy - http://local.edly.io"
DEFAULT_FROM_EMAIL = ENV_TOKENS.get("DEFAULT_FROM_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
DEFAULT_FEEDBACK_EMAIL = ENV_TOKENS.get("DEFAULT_FEEDBACK_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
SERVER_EMAIL = ENV_TOKENS.get("SERVER_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
TECH_SUPPORT_EMAIL = ENV_TOKENS.get("TECH_SUPPORT_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
CONTACT_EMAIL = ENV_TOKENS.get("CONTACT_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
BUGS_EMAIL = ENV_TOKENS.get("BUGS_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
UNIVERSITY_EMAIL = ENV_TOKENS.get("UNIVERSITY_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
PRESS_EMAIL = ENV_TOKENS.get("PRESS_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
PAYMENT_SUPPORT_EMAIL = ENV_TOKENS.get("PAYMENT_SUPPORT_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
BULK_EMAIL_DEFAULT_FROM_EMAIL = ENV_TOKENS.get("BULK_EMAIL_DEFAULT_FROM_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
API_ACCESS_MANAGER_EMAIL = ENV_TOKENS.get("API_ACCESS_MANAGER_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
API_ACCESS_FROM_EMAIL = ENV_TOKENS.get("API_ACCESS_FROM_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])

# Get rid completely of coursewarehistoryextended, as we do not use the CSMH database
INSTALLED_APPS.remove("lms.djangoapps.coursewarehistoryextended")
DATABASE_ROUTERS.remove(
    "openedx.core.lib.django_courseware_routers.StudentModuleHistoryExtendedRouter"
)

# Set uploaded media file path
MEDIA_ROOT = "/openedx/media/"

# Video settings
VIDEO_IMAGE_SETTINGS["STORAGE_KWARGS"]["location"] = MEDIA_ROOT
VIDEO_TRANSCRIPTS_SETTINGS["STORAGE_KWARGS"]["location"] = MEDIA_ROOT

GRADES_DOWNLOAD = {
    "STORAGE_TYPE": "",
    "STORAGE_KWARGS": {
        "base_url": "/media/grades/",
        "location": "/openedx/media/grades",
    },
}

# ORA2
ORA2_FILEUPLOAD_BACKEND = "filesystem"
ORA2_FILEUPLOAD_ROOT = "/openedx/data/ora2"
FILE_UPLOAD_STORAGE_BUCKET_NAME = "openedxuploads"
ORA2_FILEUPLOAD_CACHE_NAME = "ora2-storage"

# Change syslog-based loggers which don't work inside docker containers
LOGGING["handlers"]["local"] = {
    "class": "logging.handlers.WatchedFileHandler",
    "filename": os.path.join(LOG_DIR, "all.log"),
    "formatter": "standard",
}
LOGGING["handlers"]["tracking"] = {
    "level": "DEBUG",
    "class": "logging.handlers.WatchedFileHandler",
    "filename": os.path.join(LOG_DIR, "tracking.log"),
    "formatter": "standard",
}
LOGGING["loggers"]["tracking"]["handlers"] = ["console", "local", "tracking"]

# Silence some loggers (note: we must attempt to get rid of these when upgrading from one release to the next)
LOGGING["loggers"]["blockstore.apps.bundles.storage"] = {"handlers": ["console"], "level": "WARNING"}

# These warnings are visible in simple commands and init tasks
import warnings

try:
    from django.utils.deprecation import RemovedInDjango50Warning, RemovedInDjango51Warning
    warnings.filterwarnings("ignore", category=RemovedInDjango50Warning)
    warnings.filterwarnings("ignore", category=RemovedInDjango51Warning)
except ImportError:
    # REMOVE-AFTER-V18:
    # In Quince, edx-platform uses Django 5. But on master, edx-platform still uses Django 3.
    # So, Tutor v17 needs to silence these warnings, whereas Tutor v17-nightly fails to import them.
    # Once edx-platform master is upgraded to Django 5, the try-except wrapper can be removed.
    pass

warnings.filterwarnings("ignore", category=DeprecationWarning, module="wiki.plugins.links.wiki_plugin")
warnings.filterwarnings("ignore", category=DeprecationWarning, module="boto.plugin")
warnings.filterwarnings("ignore", category=DeprecationWarning, module="botocore.vendored.requests.packages.urllib3._collections")
warnings.filterwarnings("ignore", category=DeprecationWarning, module="pkg_resources")
warnings.filterwarnings("ignore", category=DeprecationWarning, module="fs")
warnings.filterwarnings("ignore", category=DeprecationWarning, module="fs.opener")
SILENCED_SYSTEM_CHECKS = ["2_0.W001", "fields.W903"]

# Email
EMAIL_USE_SSL = False
# Forward all emails from edX's Automated Communication Engine (ACE) to django.
ACE_ENABLED_CHANNELS = ["django_email"]
ACE_CHANNEL_DEFAULT_EMAIL = "django_email"
ACE_CHANNEL_TRANSACTIONAL_EMAIL = "django_email"
EMAIL_FILE_PATH = "/tmp/openedx/emails"

# Language/locales
LANGUAGE_COOKIE_NAME = "openedx-language-preference"

# Allow the platform to include itself in an iframe
X_FRAME_OPTIONS = "SAMEORIGIN"


JWT_AUTH["JWT_ISSUER"] = "http://local.edly.io/oauth2"
JWT_AUTH["JWT_AUDIENCE"] = "openedx"
JWT_AUTH["JWT_SECRET_KEY"] = "rzvIJZtAE87VrKD7E0VK8n6N"
JWT_AUTH["JWT_PRIVATE_SIGNING_JWK"] = json.dumps(
    {
        "kid": "openedx",
        "kty": "RSA",
        "e": "AQAB",
        "d": "A0dwvEtYcXrqLUvYprjqg8ss5USb_Q1wQ-TkAGLsY9l6EMHBQ7Ps9AFWJbkvuXjOa8VfJ3ntFUBYK_kZ79fAKivqS5aXws2y8CwH20WDTIGkpgrco1vuFtx2alEzqBFI21FYCnKs-aCath8HbPh4QaC6dXRN6XwhmCJ__34sbJUT_7cN_L1F6kpUfLs2oi0ghgrFX1ayyBOikOO9yZA6_U3vtJipdsGId9ejhe6BmlXMNOS2_bbcdXUElysDytiwSdUMQApHikenX4jeNvLyCWsH4KmP7bWkUoiC9MVz4MPzSYYEWQufUXwIJ9YYgq5FwU7cNOHgt1nAiVNCHicqIQ",
        "n": "vL7Me78Gi6TUTKUF6NcZiORWskkhtvUuvu1ITRq0wUVcblNTQ0VVvv01LD2cgqgomgDJQ8KVPUka3B5dnlkKIe_qj3T2_8AFsDzoI2Io7QD3YqDRy9XtOhHCsmAIw-OvUgQ5YnMeU1q4V4CCJugOmsj3DB7SV3EMtxuW1gZnymHS-iIFoe82oyb9tD6_GE48Re-Kf6l-B23U_4PhgWYhyGUf_lCzdXKmifapumMEx6QXUNdl0XYqOFPVvALyykWuU2pKXb3WcHEtTR4ArW8FXp1Oz9qH6rabL7VrBn9svacY66BDtw3K9tqbslqf2WnbE8F95UJ9Z40ynE7nuDyhjw",
        "p": "2EN824IYbnSdgMsiwMy0rKFVLNsGBaKGKe09uP4g5-dzWpTqD3ZNYOdfWxJFs1ZBJv1odkqahbmPtuVyc7MQFMpufNCvx16kTBdXjjvLYjgWzrtzjf0vaOkd2zePXMym70zaAp244yGYpq4Eao9zPJYyD5jtle0OpHiE4R7AqSk",
        "q": "32zqrQeHjeKMluHaau93zkWe7hikR0Sw2tAZ317HD6YFIzZPoPrPXRhSEdpYI5QVNsVyTVm61zz4-uK7AC6MlW9fSyd_3BCh6pQ4JUR5Vn5cESPyLpOPF0FUWiK-lEr5-85nqAft2HzQyAOCZGVITL3rd_4Axk-ayErkz5z8c_c",
        "dq": "TUBXlCQ6VnCys6i74KWUAxpHbYPPqWSy0bWKfJVEtsBsnlQ1DDAsar_yAIJCX2rgOuPiNaSE2c8XN4gVqGZv7Wtow4-QwgJuObGuCBS475MZOkP3hOs4Wo4YIGJLCvMxpEMlzA-RyXy-o6my-AudCAvS0tZcZjU4C3D51F8vWtk",
        "dp": "kugtXdOfExFmmMHlBsFIDmi9um3CRnuj1cFSB2OiKMaCBstXwE8luykRDoV4EZ4LPhgwKQL-us5VwPFWcR_3UZg9u83rSmyRARtuH7GgtETTwXV2xsJxvTt2S58PZQOkdrRm-BX6LVh6IOffGh_-MO76bLv-0LSrGLDB20cPqxk",
        "qi": "saaSjQPjiYlJsRnF0t5LGowx_wKJXO50CM7syCc0v3al3fe0vSdnGFekkK6o5MB8f9J5jk2N3y-JgIU0FW4SmxqEjBv_gQKW_CCMl03fvespZ-kTruxC1ExOxjvW4K8X9F7MVurbvuG368sj-fSUq2i-X8L_BsUXcFGMLlPDB_U",
    }
)
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

# Enable/Disable some features globally
FEATURES["ENABLE_DISCUSSION_SERVICE"] = False
FEATURES["PREVENT_CONCURRENT_LOGINS"] = False
FEATURES["ENABLE_CORS_HEADERS"] = True

# CORS
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = False
CORS_ALLOW_INSECURE = True
# Note: CORS_ALLOW_HEADERS is intentionally not defined here, because it should
# be consistent across deployments, and is therefore set in edx-platform.

# Add your MFE and third-party app domains here
CORS_ORIGIN_WHITELIST = []

# Disable codejail support
# explicitely configuring python is necessary to prevent unsafe calls
import codejail.jail_code
codejail.jail_code.configure("python", "nonexistingpythonbinary", user=None)
# another configuration entry is required to override prod/dev settings
CODE_JAIL = {
    "python_bin": "nonexistingpythonbinary",
    "user": None,
}


FEATURES['ENABLE_COURSE_DISCOVERY'] = True
FEATURES['ENABLE_COURSEWARE_SEARCH'] = True
FEATURES['ENABLE_DASHBOARD_SEARCH'] = True

FEATURES['ENABLE_COURSEWARE_INDEX'] = True
FEATURES['ENABLE_LIBRARY_INDEX'] = True

######## End of settings common to LMS and CMS

######## Common CMS settings
STUDIO_NAME = "The Transition Academy - Studio"

CACHES["staticfiles"] = {
    "KEY_PREFIX": "staticfiles_cms",
    "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    "LOCATION": "staticfiles_cms",
}

# Authentication
SOCIAL_AUTH_EDX_OAUTH2_SECRET = "HxOmcJJT8NEPz0qe09BB2JIl"
SOCIAL_AUTH_EDX_OAUTH2_URL_ROOT = "http://lms:8000"
SOCIAL_AUTH_REDIRECT_IS_HTTPS = False  # scheme is correctly included in redirect_uri
SESSION_COOKIE_NAME = "studio_session_id"

MAX_ASSET_UPLOAD_FILE_SIZE_IN_MB = 100

FRONTEND_LOGIN_URL = LMS_ROOT_URL + '/login'
FRONTEND_REGISTER_URL = LMS_ROOT_URL + '/register'

# Create folders if necessary
for folder in [LOG_DIR, MEDIA_ROOT, STATIC_ROOT, ORA2_FILEUPLOAD_ROOT]:
    if not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)



######## End of common CMS settings

# Setup correct webpack configuration file for development
WEBPACK_CONFIG_PATH = "webpack.dev.config.js"


# MFE-specific settings

COURSE_AUTHORING_MICROFRONTEND_URL = "http://apps.local.edly.io:2001/course-authoring"
CORS_ORIGIN_WHITELIST.append("http://apps.local.edly.io:2001")
LOGIN_REDIRECT_WHITELIST.append("apps.local.edly.io:2001")
CSRF_TRUSTED_ORIGINS.append("http://apps.local.edly.io:2001")
