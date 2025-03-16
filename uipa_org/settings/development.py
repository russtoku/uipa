# -*- coding: utf-8 -*-
from __future__ import absolute_import

from configurations import values

from .base import UipaOrgThemeBase, env, required_env

class Dev(UipaOrgThemeBase):
    DEBUG = True

    # Don't use the Vite server for frontend assets.
    # Prerequisite: Run `yarn build` to create the assets in the build directory.
    FRONTEND_DEBUG = False

    CACHES = {"default": {"BACKEND": "django.core.cache.backends.dummy.DummyCache"}}

    ELASTICSEARCH_HOST = values.Value("localhost", environ_prefix=None, environ_name="ELASTICSEARCH_HOST")
    ELASTICSEARCH_USER = values.Value("elastic", environ_prefix=None, environ_name="ELASTICSEARCH_USER")
    ELASTICSEARCH_PASSWORD = values.Value("froide", environ_prefix=None, environ_name="ELASTICSEARCH_PASSWORD")

    ELASTICSEARCH_DSL = {
        "default": {
            "hosts": "http://%s:9200" % ELASTICSEARCH_HOST,
            'http_auth': (ELASTICSEARCH_USER, ELASTICSEARCH_PASSWORD)
        }
    }

    @property
    def TEMPLATES(self):
        TEMP = super().TEMPLATES
        TEMP[0]["OPTIONS"]["debug"] = True
        return TEMP

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': True,
        'root': {
            'level': 'DEBUG',
            'handlers': ['uipa_org_logfile',],
        },
        'filters': {
            'require_debug_false': {
                '()': 'django.utils.log.RequireDebugFalse'
            },
            'require_debug_true': {
                '()': 'django.utils.log.RequireDebugTrue',
            },
        },
        'formatters': {
            'verbose': {
                'format': '[%(asctime)s] %(levelname)s (pid: %(process)d) [%(name)s.%(module)s: %(funcName)s:%(lineno)d] %(message)s',
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
                'filters': ['require_debug_true'],
                'class': 'logging.StreamHandler',
            },
            'uipa_org_logfile': {
                'level': 'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': 'uipa_org_dev_app.log', # put in the working directory
                'maxBytes': 1024*1024*5,  # 5MB
                'backupCount': 10,
                'formatter': 'verbose',
            },
        },
        'loggers': {
            'froide': {
                'handlers': ['uipa_org_logfile'],
                'level': 'DEBUG',
                'propagate': False,
            },
            'django': {
                'handlers': ['uipa_org_logfile'],
                'level': 'DEBUG',
                'propagate': False,
            },
            # Use instead of 'django.request' to log all requests; added in Django 1.11.
            'django.server': {
                'handlers': ['uipa_org_logfile'],
                'level': 'DEBUG',
                'propagate': False,
            },
            'django.security': {
                'handlers': ['uipa_org_logfile'],
                'level': 'DEBUG',
                'propagate': False,
            },
            'django.db.backends': {
                'level': 'DEBUG',
                'handlers': ['uipa_org_logfile'],
                'propagate': False,
            },
            'django.template': {
                'level': 'INFO',
                'handlers': ['uipa_org_logfile'],
                'propagate': False,
            },
            'uipa_org': {
                'handlers': ['uipa_org_logfile'],
                'level': 'DEBUG',
                'propagate': False,
            },
        }
    }

    # Start of email settings
    # Read the docs about these settings here: https://github.com/okfde/froide/blob/2dc1899cfe732c3f1d658f07ca86626dd5baa1a3/docs/configuration.rst#settings-for-sending-e-mail
    # The exact settings can be seen https://github.com/okfde/froide/blob/2dc1899cfe732c3f1d658f07ca86626dd5baa1a3/froide/settings.py#L618

    # General email settings
    # This is the feature flag for enabling email sending & receiving
    # This should be done with caution as it can lead to sending out emails to real public bodies
    # It is recommended to create a test public body for testing purposes, so that real public bodies are not contacted
    ENABLE_EMAIL = env("ENABLE_EMAIL", False)

    if ENABLE_EMAIL:
        SERVER_EMAIL = required_env("SERVER_EMAIL") # This is the inbound address for the SMTP server (i.e. ...@inbound.postmarkapp.com)
        DEFAULT_FROM_EMAIL = env(
            "DEFAULT_FROM_EMAIL", "TEST UIPA.org <test@beta.uipa.org>"
        )
        EMAIL_SUBJECT_PREFIX = env("EMAIL_SUBJECT_PREFIX", "[TEST UIPA.org] ")
        EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend' # This will be different for production

        # These settings are for sending regular email notifications (not FOI requests to public bodies)
        EMAIL_HOST = required_env("EMAIL_HOST") # This is the SMTP server for sending mail (i.e. smtp.postmarkapp.com)
        EMAIL_PORT = env("EMAIL_PORT", 2525)
        EMAIL_HOST_USER = required_env("EMAIL_HOST_USER") # This is the username for the SMTP server (i.e. 12345678-1234-1234-1234-123456789012) - this is the same as the password
        EMAIL_HOST_PASSWORD = required_env("EMAIL_HOST_PASSWORD") # This is the password for the SMTP server (i.e. 12345678-1234-1234-1234-123456789012)
        EMAIL_USE_TLS = env("EMAIL_USE_TLS", True)

        # These settings are for sending FOI requests to public bodies
        FOI_EMAIL_FIXED_FROM_ADDRESS = env("FOI_EMAIL_FIXED_FROM_ADDRESS", True)
        FOI_EMAIL_HOST_USER = required_env("FOI_EMAIL_HOST_USER") # This is the username for the SMTP server (i.e. 12345678-1234-1234-1234-123456789012) - this is the same as the password
        FOI_EMAIL_HOST_PASSWORD = required_env("FOI_EMAIL_HOST_PASSWORD") # This is the password for the SMTP server (i.e. 12345678-1234-1234-1234-123456789012)
        FOI_EMAIL_HOST = required_env("FOI_EMAIL_HOST") # This is the SMTP server for sending mail (i.e. smtp.postmarkapp.com)
        FOI_EMAIL_PORT = env("FOI_EMAIL_PORT", 2525)
        FOI_EMAIL_USE_TLS = env("FOI_EMAIL_USE_TLS", True)

        # These settings are for receiving FOI responses from public bodies
        FOI_EMAIL_HOST_FROM = required_env("FOI_EMAIL_HOST_FROM") # This is the inbound address for the SMTP server (i.e. ...@inbound.postmarkapp.com)
        # When defining the "FOI_EMAIL_DOMAIN" setting for testing, Postmark enforces that all recipient addresses must share the same domain as the inbound address.
        # Basically, if your email address ends in @example.com, then the "FOI_EMAIL_DOMAIN" setting must be set to "example.com".
        FOI_EMAIL_DOMAIN = required_env("FOI_EMAIL_DOMAIN") # This defines the "From" address for the inbound email (i.e. beta-foi.uipa.org)
        FOI_MAIL_SERVER_HOST = required_env("FOI_MAIL_SERVER_HOST") # This defines the "Message-Id" header for the inbound email (i.e. beta-foi.uipa.org)

        # End of email settings

