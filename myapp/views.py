from .models import UserImage, Post, Category, UserProfile
from .serializers import (UserImageSerializer, PostSerializer, CategorySerializer, UserProfileSerializer, UserRegistrationSerializer)
from rest_framework import permissions, viewsets, generics, status
from rest_framework.parsers import MultiPartParser, FormParser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.permissions import BasePermission


    # ------------------

    # custom permision владелец или админ


class IsAdminOrOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):

        # если запрос от юзера безопасный (GET, HEAD, OPTIONS) то возвращает True
        if request.method in permissions.SAFE_METHODS:
            return True

        # проверка на админа
        if request.user.is_staff or request.user.is_superuser:
            return True

        # проверка является ли юзер владельцем поста
        return obj.author == request.user


# ------------------


class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserImageViewSet(viewsets.ModelViewSet):
    queryset = UserImage.objects.order_by('-id')
    serializer_class = UserImageSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class PostListView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'author', 'created_date', 'categories']  # фильтрация по заданным параметрам


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAdminOrOwnerOrReadOnly]

    def get_object(self):
        # Получаем пост по id
        try:
            return Post.objects.get(id=self.kwargs['pk'])
        except Post.DoesNotExist:
            return None

    def delete(self, request, *args, **kwargs):
        post = self.get_object()

        if post is not None:
            # Проверяем, является ли пользователь владельцем поста
            if not IsAdminOrOwnerOrReadOnly().has_object_permission(request, self, post):
                return Response({"error": "You don't have permission to delete this post."},
                                status=status.HTTP_403_FORBIDDEN)

            # Удаляем пост
            post.delete()
            return Response({"message": "Post deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, *args, **kwargs):
        post = self.get_object()

        if post is not None:
            # Проверяем, является ли пользователь владельцем поста
            if not IsAdminOrOwnerOrReadOnly().has_object_permission(request, self, post):
                return Response({"error": "You don't have permission to update this post."},
                                status=status.HTTP_403_FORBIDDEN)

            serializer = self.get_serializer(post, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def post(self, request, *args, **kwargs):  # создаем категорию
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class ProfileListAPIView(generics.ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer