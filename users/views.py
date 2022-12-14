from requests import request
from rest_framework import generics, status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .serializers import RegistrationSerializer, ProfileUpdateForm
from rest_framework.generics import RetrieveUpdateDestroyAPIView, RetrieveAPIView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Profile

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = serializer.data
        if Token.objects.filter(user=user).exists():
            token = Token.objects.get(user=user)
            data['token'] = token.key
        else:
            data['error'] = 'User dont have token. Please login'
        headers = self.get_success_headers(serializer.data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)


class ProfileView(LoginRequiredMixin, RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileUpdateForm

    def get_queryset(self):
        return self.queryset.all()

class OnlyRet(RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileUpdateForm

    def get(self, request, *args, **kwargs):
        print(self.request)
        print(self.get_object())
        return self.retrieve(request, *args, **kwargs)