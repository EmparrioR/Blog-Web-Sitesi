from django.shortcuts import render, get_object_or_404, redirect
from .forms import PostForm,CommentForm, CustomUserCreationForm, PostCreateForm
from .models import Post, Comment, Category
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .serializers import CommentSerializer, PostSerializer, CategorySerializer
from .forms import CategoryForm, PostForm
from rest_framework import generics
from django.contrib.auth import authenticate, login
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import permission_classes
from django.http import JsonResponse

# Create your views here.


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('post_list')  # Başka bir sayfaya yönlendirme
    else:
        form = CustomUserCreationForm()
    return render(request, 'blog/register.html', {'form': form})


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)

    
    if request.method == 'POST':
        form = PostCreateForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save()
            return redirect('post_list')
    else:
        form = PostCreateForm(instance=post)

    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostCreateForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostCreateForm()

    return render(request, 'blog/post_create.html', {'form': form})

def post_list(request):
    posts = Post.objects.all()

    query = request.GET.get('q')
    if query:
        posts = posts.filter( 
            Q(title__icontains=query) | 
            Q(author__first_name__icontains=query) |
            Q(pub_date__icontains=query)  ).distinct()
           

    return render(request, 'blog/post_list.html', {'posts': posts})

def hesabim(request):

    

    return render(request, 'blog/hesabim.html')

@login_required
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

    if comment.author == request.user or comment.replies.filter(author=request.user).exists() or request.user.is_superuser:
        comment.delete()
        messages.success(request, 'Yorum başarıyla silindi.')
    else:
        messages.error(request, 'Yorumu silme yetkiniz yok.')

    return redirect('post_detail', pk=comment.post.pk) 




def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = Comment.objects.filter(post=post, parent=None)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            parent_comment_id = request.POST.get('parent_comment_id')
            parent_comment = Comment.objects.get(pk=parent_comment_id) if parent_comment_id else None
            comment = Comment(
                post=post,
                author=request.user,
                text=form.cleaned_data['text'],
                parent=parent_comment
            )
            comment.save()
            # Yorum gönderme işlemi tamamlandıktan sonra formu temizleyerek sayfayı yeniden yüklüyoruz
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()

    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form,
    })

@login_required
def reply_to_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.post = comment.post
            reply.author = request.user
            reply.parent = comment
            reply.save()
            
            return redirect('post_detail', pk=comment.post.pk)
    
    return redirect('post_detail', pk=comment.post.pk)


def category_list(request):
    categories = Category.objects.all()

    
    return render(request, 'blog/category_list.html', {'categories': categories})

    

def kategoriye_gore_listele(request, category_name):
    category = get_object_or_404(Category, name=category_name)
    posts = Post.objects.filter(category=category)
    return render(request, 'blog/kategoriye_gore_listele.html', {'posts': posts, 'category': category})



@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        post.delete()
        return redirect('post_list')

    return render(request, 'blog/post_delete.html', {'post': post})

@login_required
def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            return redirect('post_list') 
    else:
        form = CategoryForm()
    return render(request, 'blog/create_category.html', {'form': form})


class CategoryListCreateView(ListCreateAPIView):
    queryset = Category.objects.all()  
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]
    
    def perform_create(self, serializer):
        parent_category_id = self.request.data.get('parent', None)
        
        if parent_category_id:
            parent_category = Category.objects.get(id=parent_category_id)
            serializer.save(parent_category=parent_category)
        else:
            serializer.save()
            
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    


class CommentListCreateView(ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        parent_comment_id = self.request.data.get('parent', None)
        
        if parent_comment_id:
            parent_comment = Comment.objects.get(id=parent_comment_id)
            serializer.save(author=self.request.user, parent=parent_comment)
        else:
            serializer.save(author=self.request.user)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class PostListCreateView(ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
def get_subcategories(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    subcategories = category.subcategories.all()
    data = [{"id": subcategory.id, "name": subcategory.name} for subcategory in subcategories]
    return JsonResponse(data, safe=False)    