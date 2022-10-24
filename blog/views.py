from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import Blog, Category, Comment, Like, PostView
from .serializers import BlogSerializer, CategorySerializer, CommentSerializer, LikeSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view

from django.contrib.auth.models import User
# Create your views here.
class BlogView(ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    # permission_classes = (IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if(request.user != instance.author):
            message="You are not authorized to update this blog"
            return Response(message,status=status.HTTP_401_UNAUTHORIZED)
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
    def perform_update(self, serializer):
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if(request.user != instance.author):
            message="You are not authorized to delete this blog"
            return Response(message,status=status.HTTP_401_UNAUTHORIZED)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        PostView.objects.create(post=instance,user=request.user)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class CategoryView(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
@api_view(['GET',"POST"])
def comment_list(request,pk):
    queryset = Comment.objects.filter(post=pk) 
    serializer = CommentSerializer(queryset, many=True)
    if request.method == 'GET':
        comments = Comment.objects.filter(post=pk)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        post = get_object_or_404(Blog, pk=pk)
        if serializer.is_valid():
            serializer.save(post=post,user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    

@api_view(['GET','POST'])
def like(request, pk):
    queryset = Like.objects.all()
    LikeSerializers = LikeSerializer(queryset, many=True)   
    
    if request.method == 'POST':
        post = get_object_or_404(Blog, pk=pk)
        like_qs = Like.objects.filter(user=request.user, post=post)
        if like_qs.exists():
                like_qs[0].delete()
        else:
            Like.objects.create(user=request.user, post=post)
        return Response(LikeSerializers.data)
    return Response(LikeSerializers.data)



