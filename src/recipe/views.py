from rest_framework import viewsets, permissions, mixins
from rest_framework.authentication import TokenAuthentication

from . import models
from . import serializers
from .permissions import IsOwner


class TagViewSet(viewsets.GenericViewSet,
                 mixins.ListModelMixin, mixins.CreateModelMixin):
    """Manage Recipe Tags in the database"""
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsOwner, permissions.IsAuthenticated,)
    queryset = models.Tag.objects.all()
    serializer_class = serializers.TagSerializer

    def get_queryset(self):
        """Return objects for the current autheticated user only"""
        if self.request.user.is_superuser:
            return self.queryset.order_by('name')
        else:
            return self.queryset.filter(owner=self.request.user)\
                .order_by('name')

    def perform_create(self, serializer):
        """Override method to include user name before saving"""
        serializer.save(owner=self.request.user)
