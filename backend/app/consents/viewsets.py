from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin

from . import models, serializers

class ConsentsPetitionsViewset(GenericViewSet, CreateModelMixin, RetrieveModelMixin, ListModelMixin):
    queryset = models.ConsentsPetitions.objects.all()
    serializer_class = serializers.ConsentsPetitionsSerializer

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)