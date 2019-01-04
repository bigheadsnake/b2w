# encoding: utf-8
from bottle import PluginError

from login_auth import User


class AuthPlugin(object):
    name = 'auth'

    def __init__(self, keyword='user'):
        self.keyword = keyword

    def setup(self, app):
        """ Make sure that other installed plugins don't affect the same
            keyword argument."""
        for other in app.plugins:
            if not isinstance(other, AuthPlugin):
                continue
            if other.keyword == self.keyword:
                raise PluginError("Found another auth plugin with "
                                  "conflicting settings (non-unique keyword).")

    def apply(self, callback, context):
        # Override global configuration with route-specific values.
        conf = context['config'].get('auth') or {}
        keyword = conf.get('keyword', self.keyword)

        def wrapper(*args, **kwargs):
            db = kwargs['db']
            user = User(db)
            # Add the connection handle as a keyword argument.
            kwargs[keyword] = user
            # 这里，rv 将会渲染输出整个页面，而不是某个 route 返回的结果
            rv = callback(*args, **kwargs)
            return rv

        # Replace the route callback with the wrapped one.
        return wrapper


Plugin = AuthPlugin
