# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin, messages
from .models import APIKey
import logging
# Register your models here.
logger = logging.getLogger(__name__)


class APIKeyAdmin (admin.ModelAdmin):
    fields=['name', 'is_active', 'user']
    readonly_fields=['prefix']
    list_display= ['name', 'prefix', 'is_active']

    def save_model(self, request, obj, form, change):
        logger.info(obj.prefix)
        if not obj.pk:
            prefix, key = obj.generateKeys()
            obj.prefix = prefix
            obj.key = key
            messages.add_message(
                request,
                messages.INFO,
                f'The API key is {prefix}.{key}\n'
                f'This won\'t be shown again, store '
                f'it somewhere safe'
            )
        super(APIKeyAdmin, self).save_model(request, obj, form, change)

    def get_fields(self, request, obj=None):
        if obj:
            return ['name', 'prefix', 'is_active']
        return self.fields

admin.site.register(APIKey, APIKeyAdmin)


