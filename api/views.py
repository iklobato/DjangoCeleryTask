from rest_framework.response import Response

from api.models import User, CeleryTask
from api.api.serializers import UserSerializer, CeleryTaskSerializer
from rest_framework import viewsets, status
from tasks.task_test import add_task_to_queue


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_created')
    serializer_class = UserSerializer


class CeleryTaskViewSet(viewsets.ViewSet):
    queryset = CeleryTask.objects.all()
    serializer_class = CeleryTaskSerializer

    def create(self, request):
        serializer = CeleryTaskSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        obj_id = serializer.data.get('id')
        data = request.data
        payload = data.get('payload')
        task_name = data.get('task_name')
        if data:
            task_id = add_task_to_queue(
                data=payload,
                task_name=task_name,
                obj_id=obj_id
            )
            return Response(
                status=status.HTTP_201_CREATED,
                data={
                    'message': 'Task added to queue',
                    'task_id': task_id
                }
            )
        return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': 'No payload found'})

    def list(self, request):
        queryset = self.queryset.all()
        serializer = CeleryTaskSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        return Response(CeleryTaskSerializer(self.queryset.get(pk=pk)).data)

    def update(self, request, pk=None):
        return Response(CeleryTaskSerializer(self.queryset.get(pk=pk), data=request.data).data)

    def partial_update(self, request, pk=None):
        return Response(CeleryTaskSerializer(self.queryset.get(pk=pk), data=request.data, partial=True).data)

    def destroy(self, request, pk=None):
        query = self.queryset.get(pk=pk)
        query.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


