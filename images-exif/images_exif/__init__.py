import logging

from pyramid.config import Configurator

log = logging.getLogger(__name__)


def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.include('ramses')
    return config.make_wsgi_app()
