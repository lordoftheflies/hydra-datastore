from rest_framework import serializers

from hydra_datastore.models import EntryModel, DatasetModel


class EntryDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = EntryModel
        fields = [
            'id',
            'output',
        ]


class EntryInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntryModel
        fields = [
            'id',
            'coordinates_json'
        ]


class DatasetInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatasetModel
        fields = [
            'id',
            'schema',
            'timestamp'
        ]


class DatasetDetailSerializer(serializers.ModelSerializer):
    values = EntryDetailSerializer(many=True, read_only=True)

    class Meta:
        model = DatasetModel
        fields = [
            'id',
            'schema',
            'values',
            'timestamp'
        ]
