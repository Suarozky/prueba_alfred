from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# ¡Te faltaba importar authenticate!
from django.contrib.auth import authenticate
from .models import User
from .serializers import UserSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import check_password
from rest_framework.permissions import IsAuthenticated


class UserList(APIView):
    def get(self, request):  # Faltaba el parámetro 'request'
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class UserById(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user  # Esto SÍ es el objeto User completo
        serializer = UserSerializer(user)
        return Response(serializer.data)


class UpdateUser(APIView):
    permission_classes = [IsAuthenticated]  
    def put(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            serializer = UserSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class DeleteUser(APIView):
    permission_classes = [IsAuthenticated]  
    def delete(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

      
            token = Token.objects.create(user=user)

            return Response(
                {"message": "Usuario creado exitosamente", "user": serializer.data, "token": token.key},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    
class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if email is None or password is None:
            return Response(
                {"error": "Se requieren 'email' y 'password'."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"error": "Credenciales inválidas."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if not check_password(password, user.password):
            return Response(
                {"error": "Credenciales inválidas."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        Token.objects.filter(user=user).delete()  
        token = Token.objects.create(user=user)

        return Response(
            {"message": "Login exitoso", "user_id": user.id, "token": token.key},
            status=status.HTTP_200_OK
        )
