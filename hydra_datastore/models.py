import json
import random

import datetime
from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import JSONField
from django.utils.translation import gettext as _
from django_pandas.managers import DataFrameManager


class SchemaModel(models.Model):
    value = JSONField()


class DatasetModel(models.Model):

    objects = DataFrameManager()

    schema = models.ForeignKey(
        to=SchemaModel,
        related_name='datasets',
        on_delete=models.CASCADE,
        default=None,
        blank=False,
        null=False
    )
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = _('Dataset')
        verbose_name_plural = _('Datasets')

    @property
    def definition(self):
        return self.schema.value

    @definition.setter
    def definition(self, schema):
        self.schema.value = schema

    def merge(self, items):
        return [{key: value for key, value in item.items()} for item in items]

    def frame(self, **kwargs):
        entry = EntryModel.objects.create(
            coordinates=kwargs,
            dataset=self
        )
        return entry

    @property
    def values(self):
        return EntryModel.objects.filter(dataset=self).all()

    def accept(self, visitor: 'IngestionVisitor'):
        visitor.visit_entry(self)


class EntryModel(models.Model):

    objects = DataFrameManager()

    coordinates = JSONField()
    data = JSONField(default=None, null=True, blank=True)
    dataset = models.ForeignKey(
        to=DatasetModel,
        related_name='entries',
        on_delete=models.CASCADE,
        default=None,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = _('Entry')
        verbose_name_plural = _('Entries')

    @property
    def coordinates_json(self):
        return self.coordinates

    @property
    def output(self):
        return {
            **(self.data if self.data is not None else {}),
            **(self.coordinates if self.coordinates is not None else {})
        }

    @property
    def data_json(self):
        return self.data

    def accept(self, visitor: 'IngestionVisitor'):
        visitor.visit_entry(self)


class Visitor:
    def visit_dataset(self, dataset: DatasetModel):
        pass

    def visit_entry(self, entry: EntryModel):
        pass


class SequenceVisitor(Visitor):

    def __init__(self, *args):
        self.items = args  # type: List[Visitor]

    def visit_dataset(self, dataset: DatasetModel):
        [item.visit_dataset(dataset) for item in self.items]

    def visit_entry(self, entry: EntryModel):
        [item.visit_entry(entry) for item in self.items]


class DataVisitor():

    def __init__(self, key, value):
        self.key = key
        self.value = value

    def visit_dataset(self, dataset: DatasetModel):
        [self.visit_entry(entry) for entry in dataset.values]

    def visit_entry(self, entry: EntryModel):
        if entry.data is None:
            entry.data = dict()
        entry.data[self.key] = self.value


class EnumerationGenerator():

    def __init__(self, *args):
        self.values = args

    def random(self):
        r = random.randint(0, len(self.values) - 1 if len(self.values) > 1 else 0)
        return self.values[r]


class DateTimeGenerator():

    def __init__(self, from_timestamp, to_timestamp):
        self.from_timestamp = from_timestamp
        self.to_timestamp = to_timestamp

    def random(self):
        return self.from_timestamp + datetime.timedelta(
            # Get a random amount of seconds between `start` and `end`
            seconds=random.randint(0, int((self.to_timestamp - self.from_timestamp).total_seconds())),
        )
