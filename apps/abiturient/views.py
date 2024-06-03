from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from .serializers.abitur_serializers import RequestSerializer, DepartmentSerializer, RequestReadSerializer
from apps.user.models import User
from apps.abiturient.models import Request, Department, Exam


class DepartmentList(generics.ListAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class RequestListAPI(generics.ListAPIView):
    queryset = Request.objects.all()
    serializer_class = RequestReadSerializer


class RequestDetailAPI(generics.RetrieveAPIView):
    queryset = Request.objects.all()
    serializer_class = RequestReadSerializer


class RequestCreateAPI(generics.CreateAPIView):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer

    def post(self, request, *args, **kwargs):
        # return self.create(request, *args, **kwargs)
        department_id = request.data.get('department')

        assistant = User.objects.filter(role='ASSISTANT', department=department_id).first()
        if assistant:
            data = request.data.copy()
            data['user'] = assistant.id

            request_serializer = self.get_serializer(data=data)

            if request_serializer.is_valid():
                request_serializer.save()
                return Response(request_serializer.data, status=status.HTTP_201_CREATED)
            return Response(request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data={'error': 'Assistant does not exist in the specified department'},
                            status=status.HTTP_400_BAD_REQUEST)


