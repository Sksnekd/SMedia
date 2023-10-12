from rest_framework import serializers
from .models import UserImage, Post, Comment, Category, UserProfile


class UserImageSerializer(serializers.ModelSerializer):

    creator = serializers.ReadOnlyField(source='creator.username')
    creator_id = serializers.ReadOnlyField(source='creator.id')
    image_url = serializers.ImageField(required=False)

    class Meta:
        model = UserImage
        fields = ['id', 'creator', 'creator_id', 'title', 'description', 'image_url']

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')

class PostDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class CommentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('user', 'body', 'article', 'created_date', 'updated_date')


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('body', 'article')

    def create(self, validated_data):
        user = self.context['user']
        article = validated_data['article']
        body = validated_data['body']
        comment = Comment(user=user, article=article, body=body)
        comment.save()
        return comment
