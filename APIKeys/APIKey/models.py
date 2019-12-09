# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

import binascii
import os

import datetime

from django.db import models
from django.contrib.auth.hashers import make_password
import logging
# Create your models here.
logger = logging.getLogger('django')

class APIKey (models.Model):
    """
    API key with a prefix to identify the owner of the api key
    the key will be stored hashed for security
    """
    name = models.CharField(max_length=100, null=False, blank=False)
    prefix = models.CharField(max_length=16, unique=True, null=True, blank=True)
    key = models.CharField(max_length=100, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta: 
        abstract = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.key = make_password(self.key)
        return super(APIKey, self).save(*args, **kwargs)

    def generateKeys(self):
        logger.info("OK")
        key = binascii.hexlify(os.urandom(16)).decode()
        prefix = binascii.hexlify(os.urandom(8)).decode()
        return (prefix, key)

    def __str__(self):
        return self.prefix
    
class Test(models.Model):
    test1 = models.CharField(max_length=11, default='123')


class APIKey2 (APIKey):
    """
    API key with a prefix to identify the owner of the api key
    the key will be stored hashed for security
    """
    user = models.ForeignKey(Test, on_delete=models.CASCADE, null=True)

    
