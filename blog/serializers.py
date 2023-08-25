from rest_framework import serializers
from .models import Category, Comment, Post
from django.contrib.auth.models import User

class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User  # Kullanıcı modelinizi uygun şekilde belirtin
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

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
        parent_category_name = validated_data.get('parent_category_name')
        
        parent_category = None
        if parent_category_name:
            parent_category = Category.objects.filter(name=parent_category_name).first()
            if not parent_category:
                raise serializers.ValidationError("Üst kategori bulunamadı.")
            
        existing_category = Category.objects.filter(name=name, parent_category=parent_category).first()
            
        if existing_category:
            raise serializers.ValidationError("Bu kategori zaten mevcut.")
        
        return super().create({
            'name': name,
            'parent_category': parent_category
        })


