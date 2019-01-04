import dbutils
from bottle import PluginError


class MysqlPlugin(object):
    name = 'mysql'

    def __init__(self, keyword='db'):
        self.keyword = keyword

    def setup(self, app):
        """ Make sure that other installed plugins don't affect the same
            keyword argument."""
        for other in app.plugins:
            if not isinstance(other, MysqlPlugin):
                continue
            if other.keyword == self.keyword:
                raise PluginError("Found another mysql plugin with "
                                  "conflicting settings (non-unique keyword).")

    def apply(self, callback, context):
        # Override global configuration with route-specific values.
        conf = context['config'].get('mysql') or {}
        keyword = conf.get('keyword', self.keyword)

        # Test if the original callback accepts a 'db' keyword.
        # Ignore it if it does not need a database handle.
        # @XXX disable this for decorator compatible
        # args = inspect.getargspec(context['callback'])[0]
        # if keyword not in args:
        #    return callback

        def wrapper(*args, **kwargs):
            db = dbutils.get_db()
            kwargs[keyword] = db

            rv = callback(*args, **kwargs)
            dbutils.close(db)
            return rv

        # Replace the route callback with the wrapped one.
        return wrapper


Plugin = MysqlPlugin
