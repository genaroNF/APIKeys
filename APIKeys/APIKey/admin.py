# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin, messages
from .models import APIKey, APIKey2, Test
import logging
# Register your models here.
logger = logging.getLogger('django')


class APIKeyAdmin (admin.ModelAdmin):
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
        fields=['name', 'is_active']
        if obj:
            fields.insert(1, 'prefix')
        if hasattr(self.model, 'user'):
            fields.insert(1, 'user')
        return fields

class APIKeyAdmin2 (APIKeyAdmin):
    pass

class TestAdmin (admin.ModelAdmin):
    pass

admin.site.register(Test, TestAdmin)
admin.site.register(APIKey2, APIKeyAdmin2)
admin.site.register(APIKey, APIKeyAdmin)