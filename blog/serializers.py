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
    class Meta:
        model = Category
        fields = ['id', 'name', 'parent_category']
        
    def create(self, validated_data):
        name = validated_data.get('name')
        parent_category = validated_data.get('parent_category')
        
        if parent_category:
            existing_category = Category.objects.filter(name=name, parent_category=parent_category).first()
        else:
            existing_category = Category.objects.filter(name=name, parent_category__isnull=True).first()
            
        if existing_category:
            raise serializers.ValidationError("Bu kategori zaten mevcut.")
        
        return super().create(validated_data)

class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = '__all__'
