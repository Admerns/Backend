from rest_framework import generics, status
from rest_framework.fields import empty
from rest_framework.decorators import api_view
from tasks.models import task
from .serializers import Task_CreateSerializer, Task_GetSerializer, Task_EditSerializer, Task_Get_DaySerializer, Task_FinishSerializer, Task_DeleteSerializer
from rest_framework.response import Response
from .models import task
from rest_framework.permissions import IsAuthenticated 
from django.db import connection
from django.http.response import JsonResponse

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
        elif ('time' in serializer.data):
            time = serializer.data['time'].split('-')
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
            if(serializer.data.get("push_alarm") != None ):
                editingTask.push_alarm = (serializer.data.get("push_alarm"))

            editingTask.save()

            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Task updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FinishTaskAPI(generics.UpdateAPIView):
    serializer_class = Task_FinishSerializer
    permission_classes = (IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)

        if serializer.is_valid():
            if ('task_token' in serializer.data):
                finishedTask = task.objects.filter(userid = request.user.id , task_token = serializer.data['task_token']).first()
            else:
                response = {
                    'message': 'task_token is required.',
                }
                return Response(response)

            if (finishedTask == None):
                response = {
                    'message': 'Task not found.',
                }
                return Response(response)
            
            if (serializer.data['status'] == "done"):
                finishedTask.status = 'done'
            elif (serializer.data['status'] == "pending"):
                finishedTask.status = 'pending'
            else :
                response = {
                    'message': 'Status not defined.',
                }
                return Response(response)
            finishedTask.save()

            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Task finished successfully',
                'data': []
            }
            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetTasksDayAPI(generics.GenericAPIView):
    serializer_class = Task_Get_DaySerializer
    permission_classes = (IsAuthenticated,)
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception=True)

        with connection.cursor() as cursor:
            cursor.execute("SELECT id FROM `tasks` WHERE TRIM(SUBSTRING_INDEX(alarm_check,'_',1)) LIKE %s AND userid LIKE %s",
             [serializer.data['alarm_check'][:10], request.user.id])
            templist = cursor.fetchall()

        templist = list(templist)
        task_ids = []
        for i in templist:
            task_ids.append(i[0])

        tasks = task.objects.filter(userid = request.user.id, id__in = task_ids)
        serializer = (self.get_serializer(tasks, many=True))

        return Response(serializer.data)


class DeleteTaskAPI(generics.GenericAPIView):
    serializer_class = Task_DeleteSerializer
    permission_classes = (IsAuthenticated,)
    def delete(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)

        if serializer.is_valid():
            if ('task_token' in serializer.data):
                finishedTask = task.objects.filter(userid = request.user.id , task_token = serializer.data['task_token']).first()
                try:
                    task.delete(finishedTask)
                except Exception as e:
                    response = {
                        'message': 'Task not found.',
                    }
                    return Response(response)
            else:
                response = {
                    'message': 'task_token is required.',
                }
                return Response(response)
                
        

            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Task deleted successfully',
                'data': []
            }
            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
