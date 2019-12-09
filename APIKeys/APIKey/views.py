from django.shortcuts import render

# Create your views here.
from .models import APIKey2, Test
from rest_framework import serializers, viewsets
from rest_framework.response import Response
from .authentication import BasicHTTPApiKeyAuthentication, ApiKeyAuthentication

import logging

logger = logging.getLogger('django')


from django.conf.urls import url, include
from rest_framework import routers, serializers, viewsets

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Test
        fields = ['test1']

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    authentication_classes = [ApiKeyAuthentication, BasicHTTPApiKeyAuthentication]
    queryset = Test.objects.all()
    serializer_class = UserSerializer

    def list (self, request):
        logger.info(request.user)
        return super(viewsets.ModelViewSet, self).list(self, request)


    
