from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins


class ModelWithoutListViewSet(mixins.CreateModelMixin,
                              mixins.RetrieveModelMixin,
                              mixins.UpdateModelMixin,
                              mixins.DestroyModelMixin,
                              GenericViewSet):
    pass
