# -*- coding: utf-8 -*-
from __future__ import absolute_import

from celery.schedules import crontab
from configurations import values
from froide.settings import Base
from froide.settings import ThemeBase
from froide.settings import os_env
import os
import re


rec = lambda x: re.compile(x, re.I | re.U)


class UipaOrgThemeBase(ThemeBase):
    FROIDE_THEME = 'uipa_org.theme'

    SITE_NAME = "UIPA.org"
    SITE_EMAIL = "info@example.com"
    SITE_URL = 'http://localhost:8000'

    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    STATIC_ROOT = os.path.abspath(os.path.join(PROJECT_ROOT, "..", "public"))

    FIXTURE_DIRS = ('fixtures',)

    MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

    SECRET_KEY = os_env('SECRET_KEY')

    @property
    def INSTALLED_APPS(self):
        installed = super(UipaOrgThemeBase, self).INSTALLED_APPS
        installed += [
            'celery_haystack',
            'djcelery_email',
            'django.contrib.redirects',
            'uipa_org.uipa_constants',
            'uipa_org.theme.templatetags.uipa_extras',
            'tinymce',
            'raven.contrib.django.raven_compat'
        ]
        return installed

    MIDDLEWARE_CLASSES = [
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
        'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
        'froide.account.middleware.AcceptNewTermsMiddleware',
    ]

    TINYMCE_DEFAULT_CONFIG = {
        'plugins': "table,spellchecker,paste,searchreplace",
        'theme': "advanced",
        'cleanup_on_startup': False
    }

    SECRET_URLS = values.DictValue({
        "admin": "uipa-admin",
        "postmark_inbound": "uipa_postmark_inbound",
        "postmark_bounce": "uipa_postmark_bounce"
    })

    HAYSTACK_CONNECTIONS = {
        'default': {
            'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
            'URL': 'http://127.0.0.1:9200/',
            'INDEX_NAME': 'haystack',
        }
    }

    TIME_ZONE = values.Value('Pacific/Honolulu')

    CELERY_IMPORTS = ('uipa_org.tasks', )
    CELERY_TIMEZONE = values.Value('Pacific/Honolulu')

    CELERYBEAT_SCHEDULE = {
        'fetch-mail': {
            'task': 'froide.foirequest.tasks.fetch_mail',
            'schedule': crontab(),
        },
        'detect-asleep': {
            'task': 'froide.foirequest.tasks.detect_asleep',
            'schedule': crontab(hour=0, minute=0),
        },
        'detect-overdue': {
            'task': 'froide.foirequest.tasks.detect_overdue',
            'schedule': crontab(hour=0, minute=0),
        },
        'update-foirequestfollowers': {
            'task': 'froide.foirequestfollower.tasks.batch_update',
            'schedule': crontab(hour=0, minute=0),
        },
        'classification-reminder': {
            'task': 'froide.foirequest.tasks.classification_reminder',
            'schedule': crontab(hour=7, minute=0, day_of_week=6),
        },
        'uipa-private_public_reminder': {
            'task': 'uipa_org.tasks.private_public_reminder',
            'schedule': crontab(hour=0, minute=0),
        },
        'uipa-make_public_private': {
            'task': 'uipa_org.tasks.make_public_private',
            'schedule': crontab(hour=0, minute=0),
        },
    }

    CELERY_RESULT_BACKEND = 'rpc'
    CELERY_RESULT_PERSISTENT = True

    @property
    def FROIDE_CONFIG(self):
        config = super(UipaOrgThemeBase, self).FROIDE_CONFIG
        config.update(dict(
            currency="Dollars",
            create_new_publicbody=False,
            publicbody_empty=False,
            user_can_hide_web=True,
            public_body_officials_public=True,
            public_body_officials_email_public=False,
            request_public_after_due_days=14,
            payment_possible=False,
            default_law=1,
            greetings=[rec(u"Dear (?:Mr\.?|Ms\.? .*?)")],
            closings=[rec(u"")],
            public_body_boosts={},
            dryrun=True,
            dryrun_domain="beta.uipa.org",
            allow_pseudonym=False,
            doc_conversion_binary=None,  # replace with libreoffice instance
            doc_conversion_call_func=None,  # see settings_test for use
            api_activated=True,
            search_engine_query='http://www.google.com/search?as_q=%(query)s&as_epq=&as_oq=&as_eq=&hl=en&lr=&cr=&as_ft=i&as_filetype=&as_qdr=all&as_occt=any&as_dt=i&as_sitesearch=%(domain)s&as_rights=&safe=images',
            show_public_body_employee_name=False,
            ga_tracking_id=os_env('GA_TRACKING_ID')
        ))
        return config


class SslEnabled(object):
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTOCOL', 'https')
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True


class Dev(UipaOrgThemeBase, Base):

    CACHES = {
        'default': {
            'LOCATION': 'dev-uipa',
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'
        }
    }

    HAYSTACK_SIGNAL_PROCESSOR = 'celery_haystack.signals.CelerySignalProcessor'


class Beta(UipaOrgThemeBase, Base):
    SITE_URL = values.Value('http://beta.uipa.org')
    SITE_EMAIL = 'info@beta.uipa.org'
    DEFAULT_FROM_EMAIL = 'info@beta.uipa.org'

    CACHES = {
        'default': {
            'LOCATION': 'beta-uipa',
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'
        }
    }

    HAYSTACK_SIGNAL_PROCESSOR = 'celery_haystack.signals.CelerySignalProcessor'

    HAYSTACK_CONNECTIONS = {
        'default': {
            'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
            'URL': 'http://127.0.0.1:9200/',
            'INDEX_NAME': 'haystack',
        }
    }

    ALLOWED_HOSTS = values.TupleValue(('beta.uipa.org',))

    FOI_EMAIL_TEMPLATE = values.Value('request+{secret}@{domain}')
    FOI_EMAIL_DOMAIN = values.Value('beta-foi.uipa.org')

    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    SERVER_EMAIL = values.Value(os_env('POSTMARK_INBOUND_ADDRESS'))
    DEFAULT_FROM_EMAIL = values.Value(os_env('POSTMARK_INBOUND_ADDRESS'))

    DATABASES = values.DatabaseURLValue(os_env('DATABASES'))
    BROKER_URL = os_env('BROKER_URL')
    CELERY_RESULT_BACKEND = os_env('CELERY_RESULT_BACKEND')

    # Official Notification Mail goes through
    # the normal Django SMTP Backend
    EMAIL_HOST = os_env('POSTMARK_SMTP_SERVER')
    EMAIL_PORT = values.IntegerValue(2525)
    EMAIL_HOST_USER = os_env('POSTMARK_API_KEY')
    EMAIL_HOST_PASSWORD = os_env('POSTMARK_API_KEY')
    EMAIL_USE_TLS = values.BooleanValue(True)

    # SMTP settings for sending FoI mail
    FOI_EMAIL_FIXED_FROM_ADDRESS = values.BooleanValue(False)
    FOI_EMAIL_HOST_FROM = os_env('POSTMARK_INBOUND_ADDRESS')
    FOI_EMAIL_HOST_USER = os_env('POSTMARK_API_KEY')
    FOI_EMAIL_HOST_PASSWORD = os_env('POSTMARK_API_KEY')
    FOI_EMAIL_HOST = os_env('POSTMARK_SMTP_SERVER')
    FOI_EMAIL_PORT = values.IntegerValue(2525)
    FOI_EMAIL_USE_TLS = values.BooleanValue(True)

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': True,
        'root': {
            'level': 'WARNING',
            'handlers': [],
        },
        'filters': {
            'require_debug_false': {
                '()': 'django.utils.log.RequireDebugFalse'
            }
        },
        'formatters': {
            'verbose': {
                'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
            },
        },
        'handlers': {
            'mail_admins': {
                'level': 'ERROR',
                'filters': ['require_debug_false'],
                'class': 'django.utils.log.AdminEmailHandler'
            },
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
            },
            'uipa_org_logfile': {
                'level':'DEBUG',
                'class':'logging.handlers.RotatingFileHandler',
                'filename': os.path.join('/var/log/uipa_org_beta/', 'uipa_org_beta_app.log'),
                'maxBytes': 1024*1024*5, # 5MB
                'backupCount': 10,
                'formatter': 'verbose',
            },
        },
        'loggers': {
            'froide': {
                'handlers': ['uipa_org_logfile'],
                'propagate': True,
                'level': 'DEBUG',
            },
            'django.request': {
                'handlers': ['mail_admins'],
                'level': 'ERROR',
                'propagate': True,
            },
            'django.db.backends': {
                'level': 'ERROR',
                'handlers': ['uipa_org_logfile'],
                'propagate': False,
            },
            'uipa_org': {
                'handlers': ['uipa_org_logfile',],
                'propagate': True,
                'level': 'DEBUG',
            },
        }
    }

    AWS_ACCESS_KEY_ID = os_env('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os_env('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os_env('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_SECURE_URLS = values.Value(True)
    AWS_QUERYSTRING_AUTH = values.Value(False)
    AWS_S3_HOST = 's3-us-west-1.amazonaws.com'
    AWS_S3_CALLING_FORMAT = 'boto.s3.connection.OrdinaryCallingFormat'
    AWS_S3_CUSTOM_DOMAIN = '%s.%s' % (AWS_STORAGE_BUCKET_NAME, AWS_S3_HOST)
    AWS_S3_FILE_OVERWRITE = False

    STATICFILES_STORAGE = values.Value('uipa_org.custom_storages.CachedS3BotoStorage')
    STATICFILES_LOCATION = 'static'
    STATIC_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, STATICFILES_LOCATION)

    COMPRESS_STORAGE = values.Value('uipa_org.custom_storages.CachedS3BotoStorage')

    DEFAULT_FILE_STORAGE = values.Value('uipa_org.custom_storages.MediaStorage')
    MEDIAFILES_LOCATION = 'media'
    MEDIA_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, MEDIAFILES_LOCATION)

    AWS_HEADERS = {
        'Expires': 'Thu, 31 Dec 2099 20:00:00 GMT',
        'Cache-Control': 'max-age=94608000',
    }
    AWS_IS_GZIPPED = True
    GZIP_CONTENT_TYPES = (
        'text/css',
        'application/javascript',
        'application/x-javascript',
        'text/javascript'
    )

    RAVEN_CONFIG = {
        'dsn': os_env('SENTRY_DSN')
    }

    @property
    def FROIDE_CONFIG(self):
        config = super(Beta, self).FROIDE_CONFIG
        config.update(dict(
            payment_possible=True,
            doc_conversion_binary="/usr/bin/libreoffice"))
        return config


class Production(SslEnabled, UipaOrgThemeBase, Base):
    DEBUG = False
    TEMPLATE_DEBUG = False

    # COMPRESS_ENABLED = values.BooleanValue(True)
    # COMPRESS_OFFLINE = values.BooleanValue(True)

    SITE_URL = values.Value('https://uipa.org')
    SITE_EMAIL = 'info@uipa.org'
    DEFAULT_FROM_EMAIL = 'info@uipa.org'

    CACHES = {
        'default': {
            'LOCATION': 'production-uipa',
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'
        }
    }

    HAYSTACK_SIGNAL_PROCESSOR = 'celery_haystack.signals.CelerySignalProcessor'

    HAYSTACK_CONNECTIONS = {
        'default': {
            'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
            'URL': 'http://127.0.0.1:9200/',
            'INDEX_NAME': 'haystack',
        }
    }

    ALLOWED_HOSTS = values.TupleValue(('uipa.org',))

    FOI_EMAIL_TEMPLATE = values.Value('request+{secret}@{domain}')
    FOI_EMAIL_DOMAIN = values.Value('uipa.org')

    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    SERVER_EMAIL = values.Value(os_env('POSTMARK_INBOUND_ADDRESS'))
    DEFAULT_FROM_EMAIL = values.Value(os_env('POSTMARK_INBOUND_ADDRESS'))

    DATABASES = values.DatabaseURLValue(os_env('DATABASES'))
    BROKER_URL = os_env('BROKER_URL')
    CELERY_RESULT_BACKEND = os_env('CELERY_RESULT_BACKEND')

    # Official Notification Mail goes through
    # the normal Django SMTP Backend
    EMAIL_HOST = os_env('POSTMARK_SMTP_SERVER')
    EMAIL_PORT = values.IntegerValue(2525)
    EMAIL_HOST_USER = os_env('POSTMARK_API_KEY')
    EMAIL_HOST_PASSWORD = os_env('POSTMARK_API_KEY')
    EMAIL_USE_TLS = values.BooleanValue(True)

    # SMTP settings for sending FoI mail
    FOI_EMAIL_FIXED_FROM_ADDRESS = values.BooleanValue(False)
    FOI_EMAIL_HOST_FROM = os_env('POSTMARK_INBOUND_ADDRESS')
    FOI_EMAIL_HOST_USER = os_env('POSTMARK_API_KEY')
    FOI_EMAIL_HOST_PASSWORD = os_env('POSTMARK_API_KEY')
    FOI_EMAIL_HOST = os_env('POSTMARK_SMTP_SERVER')
    FOI_EMAIL_PORT = values.IntegerValue(2525)
    FOI_EMAIL_USE_TLS = values.BooleanValue(True)

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': True,
        'root': {
            'level': 'WARNING',
            'handlers': [],
        },
        'filters': {
            'require_debug_false': {
                '()': 'django.utils.log.RequireDebugFalse'
            }
        },
        'formatters': {
            'verbose': {
                'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
            },
        },
        'handlers': {
            'mail_admins': {
                'level': 'ERROR',
                'filters': ['require_debug_false'],
                'class': 'django.utils.log.AdminEmailHandler'
            },
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
            },
            'uipa_org_logfile': {
                'level':'DEBUG',
                'class':'logging.handlers.RotatingFileHandler',
                'filename': os.path.join('/var/log/uipa_org/', 'uipa_org_app.log'),
                'maxBytes': 1024*1024*5, # 5MB
                'backupCount': 10,
                'formatter': 'verbose',
            },
        },
        'loggers': {
            'froide': {
                'handlers': ['uipa_org_logfile'],
                'propagate': True,
                'level': 'DEBUG',
            },
            'django.request': {
                'handlers': ['mail_admins'],
                'level': 'ERROR',
                'propagate': True,
            },
            'django.db.backends': {
                'level': 'ERROR',
                'handlers': ['uipa_org_logfile'],
                'propagate': False,
            },
            'uipa_org': {
                'handlers': ['uipa_org_logfile',],
                'propagate': True,
                'level': 'DEBUG',
            },
        }
    }

    AWS_ACCESS_KEY_ID = os_env('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os_env('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os_env('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_SECURE_URLS = values.Value(True)
    AWS_QUERYSTRING_AUTH = values.Value(False)
    AWS_S3_HOST = 's3-us-west-1.amazonaws.com'
    AWS_S3_CALLING_FORMAT = 'boto.s3.connection.OrdinaryCallingFormat'
    AWS_S3_CUSTOM_DOMAIN = '%s.%s' % (AWS_STORAGE_BUCKET_NAME, AWS_S3_HOST)
    AWS_S3_FILE_OVERWRITE = False

    STATICFILES_STORAGE = values.Value('uipa_org.custom_storages.CachedS3BotoStorage')
    STATICFILES_LOCATION = 'static'
    STATIC_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, STATICFILES_LOCATION)

    COMPRESS_STORAGE = values.Value('uipa_org.custom_storages.CachedS3BotoStorage')

    DEFAULT_FILE_STORAGE = values.Value('uipa_org.custom_storages.MediaStorage')
    MEDIAFILES_LOCATION = 'media'
    MEDIA_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, MEDIAFILES_LOCATION)

    AWS_HEADERS = {
        'Expires': 'Thu, 31 Dec 2099 20:00:00 GMT',
        'Cache-Control': 'max-age=94608000',
    }
    AWS_IS_GZIPPED = True
    GZIP_CONTENT_TYPES = (
        'text/css',
        'application/javascript',
        'application/x-javascript',
        'text/javascript'
    )

    RAVEN_CONFIG = {
        'dsn': os_env('SENTRY_DSN')
    }

    @property
    def FROIDE_CONFIG(self):
        config = super(Production, self).FROIDE_CONFIG
        config.update(dict(
            payment_possible=True,
            dryrun=True,
            dryrun_domain="uipa.org",
            doc_conversion_binary="/usr/bin/libreoffice"))
        return config

try:
    from .local_settings import *  # noqa
except ImportError:
    pass
