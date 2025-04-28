from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from .models import User
from .serializers import UserSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import check_password
from rest_framework.permissions import IsAuthenticated


class UserList(APIView):
    """
    View para listar todos los usuarios
    """

    def get(self, request):
        """
        Método GET para obtener todos los usuarios
        """
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class UserById(APIView):
    """
    View para obtener el perfil del usuario autenticado
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Método GET para obtener los datos del usuario actual
        """
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)


class UpdateUser(APIView):
    """
    View para actualizar un usuario específico
    """
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        """
        Método PUT para actualizar los datos de un usuario por pk
        """
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
    """
    View para eliminar un usuario específico
    """
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        """
        Método DELETE para eliminar un usuario por pk
        """
        try:
            user = User.objects.get(pk=pk)
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class RegisterView(APIView):
    """
    View para registrar un nuevo usuario
    """

    def post(self, request):
        """
        Método POST para crear un nuevo usuario y asignarle un token
        """
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
    """
    View para iniciar sesión de un usuario
    """

    def post(self, request):
        """
        Método POST para autenticar un usuario y generar un nuevo token
        """
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

        Token.objects.filter(user=user).delete()  # Elimina token viejo para regenerar uno nuevo
        token = Token.objects.create(user=user)

        return Response(
            {"message": "Login exitoso", "user_id": user.id, "token": token.key},
            status=status.HTTP_200_OK
        )
