from django.http import Http404
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

from user_management.serializers import UserSerializer




# Create your views here.

class SignUpAPIView(CreateAPIView):
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()

            # Create JWT token
            refresh = RefreshToken.for_user(user)
            token_data = {
                'access': str(refresh.access_token),
            }

            return Response({'token': token_data}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserManagementAPIView(APIView):

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404
    
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            serialized_data = UserSerializer(user).data

            return Response(serialized_data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def get(self, request, *args, **kwargs):
        """
        Handle GET requests to retrieve user data.

        - If a 'pk' is provided, return details of the user with that ID.
        - If found, return user details with a 200 OK status.
        - If not found, return a 404 Not Found status with an error message.

        - If no 'pk' is provided, return a paginated list of all users.
        - Uses `PageNumberPagination` with 10 items per page.


        Returns:
        - A `Response` with user details or paginated user list.
        """

        if 'pk' in kwargs:
            user = User.objects.filter(id=kwargs['pk']).first()

            if user:
                response = {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                }
                
                return Response(response, status=status.HTTP_200_OK)

            else:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        user_list = User.objects.all()

        # Apply pagination
        paginator = PageNumberPagination()
        paginator.page_size = 10  # You can adjust the page size here
        paginated_user_list = paginator.paginate_queryset(user_list, request)

        serialized_data = UserSerializer(paginated_user_list, many=True).data

        return paginator.get_paginated_response(serialized_data)
    
    def delete(self, request, pk, format=None):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

    def patch(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)