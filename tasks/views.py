from rest_framework import generics, status

from tasks.models import task
from .serializers import Task_CreateSerializer, Task_GetSerializer, Task_EditSerializer
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated 

# Create your views here.
class TasksAPI(generics.GenericAPIView):
    serializer_class = Task_CreateSerializer
    permission_classes = (IsAuthenticated,)

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

class EditTasksAPI(generics.UpdateAPIView):
    serializer_class = Task_EditSerializer
    permission_classes = (IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)


        if serializer.is_valid():
            if ('task_token' in serializer.data):
                editingTask = task.objects.filter(userid = request.user.id , task_token = serializer.data['task_token']).first()
            else:
                response = {
                    'message': 'task_token is required.',
                }
                return Response(response)

            if (editingTask == None):
                response = {
                    'message': 'Task not found.',
                }
                return Response(response)

            if(serializer.data.get("title") != None):
                editingTask.title = (serializer.data.get("title"))
            if(serializer.data.get("description") != None):
                editingTask.description = (serializer.data.get("description"))
            if(serializer.data.get("time") != None ):
                editingTask.time = (serializer.data.get("time"))
            if(serializer.data.get("category") != None ):
                editingTask.category = (serializer.data.get("category"))
            if(serializer.data.get("alarm_check") != None ):
                editingTask.alarm_check = (serializer.data.get("alarm_check"))
            if(serializer.data.get("push_notification") != None ):
                editingTask.push_notification = (serializer.data.get("push_notification"))

                
            editingTask.save()


            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Task updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




