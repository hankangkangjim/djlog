
import traceback
from importlib import import_module

from django.conf import settings
from django.utils.log import AdminEmailHandler as _AdminEmailHandler
from django.views.debug import ExceptionReporter


def _handler(request, reporter, exc_type, exc_val, exc_tb):
    print('=' * 40 + 'DJ-LOG' + '=' * 40)
    print('PATH: {}'.format(request.path))
    traceback.print_exception(exc_type, exc_val, exc_tb)


def handler(request, reporter, *args, **kwargs):
    log_hander_string = getattr(settings, 'DJ_LOG_HANDLER', '')
    if log_hander_string and ':' in log_hander_string:
        module, func = log_hander_string.split(':')
        _h = getattr(import_module(module), func)
    else:
        _h = _handler

    return _h(request, reporter, *args, **kwargs)


class CatchExceptionHandler(_AdminEmailHandler):
    def emit(self, record):
        try:
            request = record.request
        except Exception:
            return

        try:
            if record.exc_info:
                exc_info = record.exc_info
            else:
                exc_info = (None, record.getMessage(), None)
            reporter = ExceptionReporter(request, is_email=True, *exc_info)
            handler(request, reporter, *exc_info)
        except Exception as e:
            print e.message
