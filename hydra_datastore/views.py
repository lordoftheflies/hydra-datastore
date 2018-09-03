import logging

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from hydra_datastore.models import DatasetModel, EntryModel
from hydra_datastore.serializers import DatasetInfoSerializer, DatasetDetailSerializer, EntryDetailSerializer, EntryInfoSerializer

logger = logging.getLogger(__name__)


# Create your views here.


class DatasetViewSet(viewsets.ModelViewSet):
    serializer_class = DatasetInfoSerializer
    queryset = DatasetModel.objects.all()

    @action(methods=['get'], detail=True, url_name='info', url_path='info')
    def details(self, request, pk):
        dataset = DatasetModel.objects.get(id=pk)
        serializer = DatasetDetailSerializer(dataset)
        return Response(serializer.data)

    @action(methods=['get'], detail=True, url_name='entries', url_path='entries')
    def entries(self, request, pk):
        dataset = DatasetModel.objects.get(id=pk) # type: DatasetModel
        entries = dataset.values
        logger.info('Dataset %s fetch %s entries.' % (
            pk,
            entries.count()
        ))
        serializer = EntryDetailSerializer(entries, many=True)
        return Response(serializer.data)


class EntryViewSet(viewsets.ModelViewSet):
    serializer_class = EntryInfoSerializer
    queryset = DatasetModel.objects.all()

    @action(methods=['get'], detail=True, url_name='execution', url_path='execution')
    def details_by_execution(self, request, pk):
        entries = EntryModel.objects.filter(coordinates__execution_id=int(pk))
        logger.info('Execution %s fetch %s entries.' % (
            pk,
            entries.count()
        ))
        serializer = EntryDetailSerializer(entries, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=False, url_name='data', url_path='data')
    def data(self, request):
        entries = EntryModel.objects.all()
        logger.info('Fetched entries (%s pcs).' % (
            entries.count()
        ))
        serializer = EntryDetailSerializer(entries, many=True)
        return Response(serializer.data)