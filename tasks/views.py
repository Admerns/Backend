from rest_framework import generics

from tasks.models import task
from .serializers import Task_CreateSerializer, Task_GetSerializer
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated 

# Create your views here.
class TasksAPI(generics.GenericAPIView):
    serializer_class = Task_CreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        task = serializer.save()
        return Response({
        "task": Task_CreateSerializer(task, context=self.get_serializer_context()).data,
        })

class GetTasksAPI(generics.GenericAPIView):
    serializer_class = Task_GetSerializer
    permission_classes = (IsAuthenticated,)
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception=True)

        if ('task_token' in serializer.data):
            tasks = task.objects.filter(userid = request.user.id , task_token = serializer.data['task_token'])
        else:
            tasks = task.objects.filter(userid = request.user.id)
        serializer = (self.get_serializer(tasks, many=True))
        
        return Response(serializer.data)




