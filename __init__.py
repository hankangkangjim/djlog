# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf import settings


def _defaultdict(_dict, key):
    if key not in _dict:
        _dict[key] = {}
    return _dict[key]


def update_logging(log_config):
    if not isinstance(log_config, dict):
        raise TypeError('settings.LOGGING must be adict')
    loggers = _defaultdict(log_config, 'loggers')
    handlers = _defaultdict(log_config, 'handlers')
    filters = _defaultdict(log_config, 'filters')

    default_logger = loggers.get('django.request', {})
    loggers['django.request'] = {
        'handlers': ['catch_except'] + default_logger.get('handlers', []),
        'level': default_logger.get('level', 'ERROR'),
        'propagate': default_logger.get('propagate', False),
    }

    handlers['catch_except'] = {
        'level': 'ERROR',
        'filters': ['require_debug_false'],
        'class': getattr(settings, '', 'djlog.handler.CatchExceptionHandler')
    }

    if 'require_debug_false' not in filters:
        filters['require_debug_false'] = {
            '()': 'django.utils.log.RequireDebugFalse'
        }

    return log_config
