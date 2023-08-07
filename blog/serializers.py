from rest_framework import serializers
from .models import Category, Comment, Post
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)  
    class Meta:
        model = Comment
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField()

    def get_subcategories(self, obj):
        serializer = CategorySerializer(obj.subcategories.all(), many=True)
        return serializer.data

    class Meta:
        model = Category
        fields = ['id', 'name', 'parent_category', 'subcategories']

class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = '__all__'
