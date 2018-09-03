import logging

from django.apps import AppConfig

logger = logging.getLogger(__name__)

class HydraDatastoreConfig(AppConfig):
    name = 'hydra_datastore'
    icon = '<i class="material-icons">settings_applications</i>'
    verbose_name = 'Datastore'
    order = 2

    def ready(self):
        logger.info('%s started: OK', (self.name))