import logging

from django.apps import AppConfig

logger = logging.getLogger(__name__)

class DatastoreConfig(AppConfig):
    name = 'datastore'
    icon = '<i class="material-icons">settings_applications</i>'
    verbose_name = 'Datastore'
    order = 2

    def ready(self):
        logger.info('%s started: OK', (self.name))