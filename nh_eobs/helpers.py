# Part of Open eObs. See LICENSE file for full copyright and licensing details.
import logging
from functools import wraps

_logger = logging.getLogger(__name__)


def refresh_views(cr, views):
    """
    Execute the update of the views via SQL in the cursor

    :param cr: Odoo cursor
    :param views: list of views
    """
    sql = ''
    for view in views:
        sql += 'refresh materialized view ' + view + ';\n'
    cr.execute(sql)
    _logger.debug('Materialized view(s) refreshed')


def refresh_materialized_views(*views):
    """
    Decorator method to refresh materialized views passed
    as arguments.
    :param views: name(s) of materialized view(s) to refresh
    :return: True if activity is completed
    """
    def _refresh_materialized_views(f):
        @wraps(f)
        def _complete(*args, **kwargs):
            self, cr = args[:2]
            result = f(*args, **kwargs)
            refresh_views(cr, views)
            return result
        return _complete
    return _refresh_materialized_views


def v8_refresh_materialized_views(*views):
    """
    Decorator method to refresh materialized views passed
    as arguments.
    :param views: name(s) of materialized view(s) to refresh
    :return: True if activity is completed
    """
    def _refresh_materialized_views(f):
        @wraps(f)
        def _complete(*args, **kwargs):
            self = args[0]
            result = f(*args, **kwargs)
            refresh_views(self._cr, views)
            return result
        return _complete
    return _refresh_materialized_views
