from django.shortcuts import render

# Create your views here.
from .models import APIKey2, Test
from rest_framework import serializers, viewsets
from .authentication import ApiKeyAuthentication2
from rest_framework.response import Response

import logging

logger = logging.getLogger('django')


# Serializers define the API representation.

    
