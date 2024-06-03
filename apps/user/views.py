from rest_framework import status, views, viewsets, generics
from django.contrib.auth import authenticate

from apps.user.models import User, Invitation
from apps.user.serializers import UserSerializer, UserLoginSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from apps.abiturient.models import Department
from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


class UserLoginAPI(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get("email")
        password = serializer.data.get("password")
        user = authenticate(email=email, password=password)
        print(user)
        if user is not None:
            token = get_tokens_for_user(user)
            return Response({
                "token": token,
                "user": UserSerializer(User.objects.get(id=user.id)).data,
            }, status=status.HTTP_200_OK)
        else:
            return Response(
                {"errors": {"non_field_errors": ["Email or Password is not Valid"]}}, status=status.HTTP_404_NOT_FOUND
            )


class UserRegisterAPI(generics.GenericAPIView):

    def post(self, request):
        print(request.data)
        token = request.data['token']
        invitation = Invitation.objects.get(invitation_token=token)
        if invitation:
            data = {
                'role': invitation.role,
                'department': Department.objects.get(name=invitation.department).id,
                'first_name': request.data['first_name'],
                'last_name': request.data['last_name'],
                'email': request.data['email'],
                'phone_number': request.data['phone_number'],
                'password': request.data['password'],
            }
            serializer = UserSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(["get"], detail=False)
    def me(self, request, *args, **kwargs):
        queryset = User.objects.filter(id=request.user.id)
        user = get_object_or_404(queryset)
        serializer = self.get_serializer(user, context={"request": request})
        return Response(serializer.data)
