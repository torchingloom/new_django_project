
from debug_toolbar.middleware import DebugToolbarMiddleware as DebugToolbarMiddleware_Base
from django.conf import LazySettings


class DebugToolbarMiddleware(DebugToolbarMiddleware_Base):
    def _show_toolbar(self, request):
        return bool(LazySettings().DEBUG)
