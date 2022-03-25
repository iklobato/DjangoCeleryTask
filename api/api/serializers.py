from abc import ABC

from rest_framework import serializers
from api.models import User, CeleryTask


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'date_created')


class CeleryTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = CeleryTask
        fields = (
            'id',
            'task_name',
            'task_status',
            'payload',
            'date_created'
        )
