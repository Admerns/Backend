from rest_framework import generics
from .serializers import Task_CreateSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import task
from .serializers import Task_CreateSerializer, Task_ReadSerializer
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

class TaskReadView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = task.objects.all()
    serializer_class = Task_ReadSerializer