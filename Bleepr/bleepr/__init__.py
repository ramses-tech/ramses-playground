from pyramid.config import Configurator
from ramses import registry

@registry.add
def send_tha_bill(event):
    # send bill here
    return

def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.include('ramses')
    return config.make_wsgi_app()
