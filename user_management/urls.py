

from django.urls import path

from user_management.views import SignUpAPIView, UserManagementAPIView



urlpatterns = [
    path('sign_up/', SignUpAPIView.as_view(), name='sign_up'),
    path('user/', UserManagementAPIView.as_view(), name='user_management'),
    path('user/<int:pk>/', UserManagementAPIView.as_view(), name='user_management_get_delete_update'),
]