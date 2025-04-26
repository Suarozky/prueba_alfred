from django.urls import path
from .views import RegisterView, LoginView, UserList, UpdateUser, DeleteUser,UserById

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('users/', UserList.as_view(), name='user-list'),
    path('userById/', UserById.as_view(), name='user-by-id'),  # Cambié a UserList.as_view()
    path('users/<int:pk>/', UpdateUser.as_view(), name='user-update'),
    path('users/<int:pk>/delete/', DeleteUser.as_view(), name='user-delete'),
]
